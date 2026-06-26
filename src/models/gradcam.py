"""
Spectral Land Cover Segmentation
===================================
Uses HSV/LAB color-space analysis to identify land cover types at PIXEL
level — the same principle used in real satellite remote sensing (NDVI,
spectral indices). This produces vastly more accurate boundaries than
Grad-CAM because it analyzes actual pixel colors:

  Green pixels   → Vegetation (Forest, Pasture, Crop)
  Blue pixels    → Water (River, SeaLake)
  Gray/brown     → Urban (Residential, Industrial, Highway)
  Yellow/bright  → Agriculture (AnnualCrop, PermanentCrop)

The model's classification probabilities are used to LABEL each region
with the correct class name and confidence.
"""

import torch
import torch.nn.functional as F
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cv2
import io
import base64
import copy


BRIGHT_COLORS = {
    "AnnualCrop":           (255, 220, 50),
    "Forest":               (34, 220, 77),
    "HerbaceousVegetation": (100, 255, 130),
    "Highway":              (190, 190, 220),
    "Industrial":           (255, 100, 50),
    "Pasture":              (150, 255, 80),
    "PermanentCrop":        (255, 180, 50),
    "Residential":          (255, 70, 100),
    "River":                (80, 160, 255),
    "SeaLake":              (50, 120, 255),
}

# Map spectral land types to EuroSAT classes
SPECTRAL_CLASS_MAP = {
    "dense_vegetation":  ["Forest", "HerbaceousVegetation", "Pasture"],
    "light_vegetation":  ["AnnualCrop", "PermanentCrop", "Pasture", "HerbaceousVegetation"],
    "water":             ["River", "SeaLake"],
    "urban":             ["Residential", "Industrial"],
    "road":              ["Highway"],
    "bare_soil":         ["AnnualCrop", "PermanentCrop", "Industrial"],
}


def get_color(class_name):
    return BRIGHT_COLORS.get(class_name, (180, 180, 255))


def spectral_segmentation(img_rgb):
    """
    Segment satellite image into land cover types using spectral analysis.
    Uses HSV and LAB color spaces for robust color-based classification.
    
    Returns: dict of {spectral_type: binary_mask}
    """
    hsv = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV)
    lab = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2LAB)
    
    h, s, v = hsv[:,:,0], hsv[:,:,1], hsv[:,:,2]
    l_ch, a_ch, b_ch = lab[:,:,0], lab[:,:,1], lab[:,:,2]
    
    # RGB channels
    r, g, b = img_rgb[:,:,0].astype(float), img_rgb[:,:,1].astype(float), img_rgb[:,:,2].astype(float)
    
    # ── Vegetation Index (like NDVI but for RGB) ──
    # Green Leaf Index: (2*G - R - B) / (2*G + R + B + 1)
    gli = (2*g - r - b) / (2*g + r + b + 1)
    
    # Excess Green Index: 2*G - R - B
    exg = 2*g - r - b
    
    masks = {}
    
    # Dense vegetation: high green, low red, high saturation
    masks["dense_vegetation"] = (
        (gli > 0.05) & (s > 40) & (h >= 25) & (h <= 90) & (g > r * 0.9)
    ).astype(np.uint8) * 255
    
    # Light vegetation / agriculture: yellowish-green, moderate saturation
    masks["light_vegetation"] = (
        (gli > -0.05) & (gli <= 0.05) & (s > 20) & 
        ((h >= 20) & (h <= 100)) & (v > 80)
    ).astype(np.uint8) * 255
    
    # Water: dark blue/dark areas with low saturation OR blue hue
    masks["water"] = (
        ((h >= 90) & (h <= 140) & (s > 25)) |  # Blue hue
        ((v < 70) & (s < 40) & (b_ch > 128)) |  # Dark with blue tint
        ((r < 80) & (g < 80) & (b > 50) & (b > r))  # Dark blue
    ).astype(np.uint8) * 255
    
    # Urban / residential: low saturation, medium-high brightness, red-ish
    masks["urban"] = (
        (s < 60) & (v > 80) & (gli < -0.02) & 
        ((a_ch > 128) | ((r > g) & (r > b)))  # Warm tones
    ).astype(np.uint8) * 255
    
    # Road / highway: very low saturation, medium brightness, linear
    masks["road"] = (
        (s < 30) & (v > 60) & (v < 200) & 
        (abs(a_ch.astype(int) - 128) < 15) & (abs(b_ch.astype(int) - 128) < 15)
    ).astype(np.uint8) * 255
    
    # Bare soil: brownish, warm, low-medium saturation
    masks["bare_soil"] = (
        (h >= 5) & (h <= 30) & (s > 30) & (s < 120) & 
        (v > 80) & (r > g) & (r > b)
    ).astype(np.uint8) * 255
    
    # Clean up each mask
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    for key in masks:
        masks[key] = cv2.morphologyEx(masks[key], cv2.MORPH_CLOSE, kernel)
        masks[key] = cv2.morphologyEx(masks[key], cv2.MORPH_OPEN, 
                                       cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
    
    # Resolve overlaps: priority order
    priority = ["water", "dense_vegetation", "urban", "road", "bare_soil", "light_vegetation"]
    assigned = np.zeros(img_rgb.shape[:2], dtype=np.uint8)
    
    for ptype in priority:
        if ptype in masks:
            # Only assign pixels not yet assigned
            unassigned = (assigned == 0)
            masks[ptype] = cv2.bitwise_and(masks[ptype], masks[ptype], 
                                            mask=unassigned.astype(np.uint8) * 255)
            assigned = cv2.bitwise_or(assigned, (masks[ptype] > 0).astype(np.uint8))
    
    return masks


def map_spectral_to_classes(spectral_masks, class_probs):
    """
    Map spectral segmentation regions to EuroSAT class names using
    the model's classification probabilities to pick the right label.
    
    Returns: dict {class_name: binary_mask}
    """
    class_masks = {}
    
    for spectral_type, mask in spectral_masks.items():
        if cv2.countNonZero(mask) < 20:
            continue
        
        # Get candidate EuroSAT classes for this spectral type
        candidates = SPECTRAL_CLASS_MAP.get(spectral_type, [])
        if not candidates:
            continue
        
        # Pick the candidate with highest model probability
        best_class = None
        best_prob = -1
        for c in candidates:
            prob = class_probs.get(c, 0.0)
            if prob > best_prob:
                best_prob = prob
                best_class = c
        
        if best_class and best_prob > 0.001:
            if best_class not in class_masks:
                class_masks[best_class] = mask.copy()
            else:
                class_masks[best_class] = cv2.bitwise_or(class_masks[best_class], mask)
    
    return class_masks


def create_spectral_overlay(original_image, class_probs):
    """
    Create pixel-accurate land cover overlay using spectral segmentation.
    No Grad-CAM needed — uses actual pixel colors for precision.
    """
    SIZE = 400
    img = original_image.resize((SIZE, SIZE), Image.LANCZOS)
    img_rgb = np.array(img, dtype=np.uint8).copy()
    overlay = img_rgb.copy()
    
    # Step 1: Spectral segmentation
    spectral_masks = spectral_segmentation(img_rgb)
    
    # Step 2: Map to EuroSAT classes using model predictions
    class_masks = map_spectral_to_classes(spectral_masks, class_probs)
    
    # Step 3: Color each class region
    labels_to_draw = []
    
    for cname, mask in class_masks.items():
        if cv2.countNonZero(mask) < 50:
            continue
        
        color = get_color(cname)
        r, g, b = color
        prob = class_probs.get(cname, 0.0)
        
        # Fill with class color
        fill_alpha = min(0.35, max(0.15, prob * 0.4))
        fill = np.zeros_like(overlay)
        fill[:, :] = [r, g, b]
        mask_f = (mask.astype(np.float32) / 255.0)[:, :, np.newaxis]
        overlay = (overlay.astype(np.float32) * (1 - fill_alpha * mask_f) +
                   fill.astype(np.float32) * fill_alpha * mask_f)
        overlay = np.clip(overlay, 0, 255).astype(np.uint8)
        
        # Draw contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        thickness = 2 if prob > 0.1 else 1
        cv2.drawContours(overlay, contours, -1, (r, g, b), thickness, cv2.LINE_AA)
        
        # Find label position
        if contours:
            largest = max(contours, key=cv2.contourArea)
            M = cv2.moments(largest)
            if M["m00"] > 0:
                labels_to_draw.append((cname, prob,
                                       int(M["m10"]/M["m00"]),
                                       int(M["m01"]/M["m00"]), color))
    
    # Step 4: Draw labels
    result = Image.fromarray(overlay)
    draw = ImageDraw.Draw(result)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)
    except Exception:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
        except Exception:
            font = ImageFont.load_default()
    
    for cname, prob, cx, cy, color in labels_to_draw:
        label = f"{cname} {prob*100:.1f}%"
        bbox = draw.textbbox((0, 0), label, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        pad = 4
        lx = max(2, min(cx - tw // 2, SIZE - tw - 2*pad - 2))
        ly = max(2, min(cy - th // 2, SIZE - th - 2*pad - 2))
        draw.rounded_rectangle([lx, ly, lx + tw + 2*pad, ly + th + 2*pad],
                               radius=4, fill=(0, 0, 0, 220))
        draw.text((lx + pad, ly + pad), label, fill=color, font=font)
    
    return result


def generate_cam_image(model, target_layer, input_tensor, original_image, land_color,
                       class_name="", confidence=0.0, all_probs=None, class_names=None):
    """
    Generate pixel-accurate land cover visualization using spectral analysis.
    No Grad-CAM — uses direct pixel color analysis for precise boundaries.
    """
    try:
        probs_dict = all_probs or {class_name: confidence}
        result_img = create_spectral_overlay(original_image, probs_dict)
        
        # Encode to base64
        buffer = io.BytesIO()
        result_img.save(buffer, format='JPEG', quality=92)
        buffer.seek(0)
        b64 = base64.b64encode(buffer.read()).decode('utf-8')
        
        return f"data:image/jpeg;base64,{b64}"
    
    except Exception as e:
        print(f"[Spectral] Error: {e}")
        import traceback
        traceback.print_exc()
        return ""
