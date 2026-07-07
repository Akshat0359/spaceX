"""
SpaceX Backend API
======================
FastAPI server for satellite image land cover classification.
Serves both models (BDH + ResNet-18) and the frontend UI.
"""

import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'src'))

import json
import time
import random
from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import torch
from torchvision import transforms
from PIL import Image
import io

from models.baby_dragon import BabyDragonHatchling
from models.resnet import get_resnet

app = FastAPI(title="SpaceX API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)

MODELS_DIR = os.path.join(PROJECT_ROOT, 'saved_models')
STATIC_DIR = os.path.join(PROJECT_ROOT, 'static')
DATA_DIR = os.path.join(PROJECT_ROOT, 'data', 'eurosat', '2750')

device = torch.device('cpu')
if torch.cuda.is_available():
    device = torch.device('cuda')
elif torch.backends.mps.is_available():
    device = torch.device('mps')

resnet_model = None
bdh_model = None
class_names = []
historical_metrics = {}
land_cover_colors = {}

transform_pipeline = transforms.Compose([
    transforms.Resize((64, 64)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# Bright color map — every color visible on dark backgrounds
DEFAULT_COLORS = {
    "AnnualCrop":           [255, 220, 50],
    "Forest":               [34, 220, 77],
    "HerbaceousVegetation": [100, 255, 130],
    "Highway":              [190, 190, 220],
    "Industrial":           [255, 100, 50],
    "Pasture":              [150, 255, 80],
    "PermanentCrop":        [255, 180, 50],
    "Residential":          [255, 70, 100],
    "River":                [80, 160, 255],
    "SeaLake":              [50, 120, 255]
}

# Land cover descriptions for the frontend
LAND_COVER_INFO = {
    "AnnualCrop":           "Agricultural land with annually harvested crops like wheat, corn, or rice.",
    "Forest":               "Dense tree cover including deciduous and coniferous forests.",
    "HerbaceousVegetation": "Grasslands and non-woody vegetation such as meadows and scrubland.",
    "Highway":              "Major road infrastructure including highways and expressways.",
    "Industrial":           "Industrial zones, factories, warehouses, and manufacturing areas.",
    "Pasture":              "Grazing land used for livestock farming and animal husbandry.",
    "PermanentCrop":        "Orchards, vineyards, and other permanent agricultural plantations.",
    "Residential":          "Urban residential areas with houses, apartments, and neighborhoods.",
    "River":                "Inland water bodies — rivers, streams, and canals.",
    "SeaLake":              "Large water bodies including seas, lakes, and reservoirs."
}


@app.on_event("startup")
async def load_models():
    global resnet_model, bdh_model, class_names, historical_metrics, land_cover_colors

    # Classes
    p = os.path.join(MODELS_DIR, 'classes.json')
    class_names = json.load(open(p)) if os.path.exists(p) else list(DEFAULT_COLORS.keys())

    # Always use bright color palette (overrides any old saved colors)
    land_cover_colors = DEFAULT_COLORS

    # Metrics
    p = os.path.join(MODELS_DIR, 'metrics.json')
    if os.path.exists(p):
        historical_metrics = json.load(open(p))

    # ResNet-18
    p = os.path.join(MODELS_DIR, 'resnet.pth')
    if os.path.exists(p):
        resnet_model = get_resnet().to(device)
        resnet_model.load_state_dict(torch.load(p, map_location=device))
        resnet_model.eval()
        print(f"[✓] ResNet-18 loaded on {device}")

    # Baby Dragon Hatchling
    p = os.path.join(MODELS_DIR, 'baby_dragon.pth')
    if os.path.exists(p):
        bdh_model = BabyDragonHatchling(num_classes=10).to(device)
        bdh_model.load_state_dict(torch.load(p, map_location=device))
        bdh_model.eval()
        print(f"[✓] Baby Dragon Hatchling loaded on {device}")


# ─── API Routes ───────────────────────────────────────

@app.get("/api/health")
async def health():
    return {"status": "ok", "models_loaded": resnet_model is not None and bdh_model is not None}


@app.get("/api/metrics")
async def get_metrics():
    return historical_metrics


@app.get("/api/colors")
async def get_colors():
    return land_cover_colors


@app.get("/api/sample")
async def get_sample():
    if not os.path.exists(DATA_DIR):
        return JSONResponse(status_code=404, content={"error": "Dataset not found."})

    classes = [d for d in os.listdir(DATA_DIR) if os.path.isdir(os.path.join(DATA_DIR, d))]
    if not classes:
        return JSONResponse(status_code=404, content={"error": "No classes found."})

    cls = random.choice(classes)
    folder = os.path.join(DATA_DIR, cls)
    imgs = [f for f in os.listdir(folder) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.tif'))]
    if not imgs:
        return JSONResponse(status_code=404, content={"error": "No images found."})

    return FileResponse(os.path.join(folder, random.choice(imgs)), media_type="image/jpeg")


@app.post("/api/predict")
async def predict(file: UploadFile = File(...)):
    if not resnet_model or not bdh_model:
        return JSONResponse(status_code=503,
                            content={"error": "Models not loaded. Please run train.py first."})

    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert('RGB')
    tensor = transform_pipeline(image).unsqueeze(0).to(device)

    from models.gradcam import generate_cam_image

    def run_model(model, target_layer):
        # Standard forward pass for prediction (no grad)
        t0 = time.time()
        with torch.no_grad():
            out = model(tensor.clone())
            probs = torch.nn.functional.softmax(out, dim=1)[0]
        ms = (time.time() - t0) * 1000
        pred_idx = torch.argmax(probs).item()
        all_probs = {class_names[i]: round(float(probs[i]), 4) for i in range(len(class_names))}
        color = land_cover_colors.get(class_names[pred_idx], [128, 128, 128])

        # Generate multi-class Grad-CAM overlay
        cam_b64 = ""
        pred_name = class_names[pred_idx]
        pred_conf = float(probs[pred_idx])
        try:
            cam_tensor = transform_pipeline(image).unsqueeze(0).to(device)
            cam_b64 = generate_cam_image(
                model, target_layer, cam_tensor, image, color,
                class_name=pred_name, confidence=pred_conf,
                all_probs=all_probs, class_names=class_names
            )
        except Exception as e:
            print(f"Grad-CAM error: {e}")
            import traceback; traceback.print_exc()

        return {
            "prediction":   pred_name,
            "confidence":   round(pred_conf, 4),
            "inference_ms": round(ms, 2),
            "all_probs":    all_probs,
            "color":        color,
            "description":  LAND_COVER_INFO.get(pred_name, ""),
            "cam_image":    cam_b64,
        }

    # ResNet target layer: layer3 gives higher-res activations (8x8) than layer4 (4x4)
    resnet_target = resnet_model.layer3[-1]
    # BDH target layer: stage2 gives 16x16 activations (sharper than stage3's 8x8)
    bdh_target = bdh_model.stage2

    return {
        "resnet":      run_model(resnet_model, resnet_target),
        "baby_dragon": run_model(bdh_model, bdh_target),
    }


# ─── Static Files (must be last) ─────────────────────
os.makedirs(STATIC_DIR, exist_ok=True)
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")
