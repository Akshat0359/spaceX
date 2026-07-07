# 🚀 SpaceX: Satellite Land Cover Intelligence

An advanced, deep-learning powered web application that classifies satellite telemetry and imagery into **10 distinct planetary land cover categories**. This system evaluates an experimental, biologically-inspired neural architecture against a standard baseline:

- **Baby Dragon Hatchling (BDH)** — an experimental, lightweight CNN architecture featuring lateral inhibition and contextual attention.
- **ResNet-18** — a standard ImageNet-pretrained baseline for Earth observation tasks.

Upload satellite telemetry (or run a calibration sample) and receive side-by-side inference predictions with Grad-CAM heatmaps showing *where* each model focuses its attention.

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.128-green)
![PyTorch](https://img.shields.io/badge/PyTorch-2.8-red)

---

## 📡 Features

- Side-by-side BDH vs. ResNet-18 architectural comparison
- Grad-CAM heatmap overlays for model interpretability and telemetry focus mapping
- Spectral land cover segmentation visualization
- Real-time inference latency benchmarking
- 10-class EuroSAT planetary land cover classification

---

## 🛰️ Mission Quick Start

### 1. Initialize the Repository

```bash
git clone <your-repo-url>
cd SpaceX
```

### 2. Configure Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate         # Windows
```

### 3. Install Mission Dependencies

```bash
pip install -r requirements.txt
```

> **Note (Apple Silicon / Windows):** If `torch` installation fails, install PyTorch separately first:
> ```bash
> # macOS Apple Silicon
> pip install torch torchvision torchaudio
>
> # Windows (CPU only)
> pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
>
> # Windows (CUDA)
> pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
> ```
> Then run `pip install -r requirements.txt` again to get the rest.

### 4. Sync EuroSAT Dataset

Download [EuroSAT RGB](https://zenodo.org/records/7711810#.ZAm3k-zMKEA) and extract so the directory structure looks like:

```
data/
└── eurosat/
    └── 2750/
        ├── AnnualCrop/
        ├── Forest/
        ├── HerbaceousVegetation/
        ├── Highway/
        ├── Industrial/
        ├── Pasture/
        ├── PermanentCrop/
        ├── Residential/
        ├── River/
        └── SeaLake/
```

### 5. Train Neural Models

```bash
source venv/bin/activate
PYTHONPATH=$PYTHONPATH:$(pwd)/src python src/train.py
```

This will train both the BDH and ResNet-18 models, saving their serialized weights to `saved_models/`.

### 6. Launch Inference Engine

```bash
source venv/bin/activate
PYTHONPATH=$PYTHONPATH:$(pwd)/src uvicorn app:app --app-dir src --host 0.0.0.0 --port 8000 --reload
```

Or simply:

```bash
./run_app.sh
```

Then open **http://localhost:8000** in your command center browser.

---

## 📁 System Architecture

```
SpaceX/
├── src/
│   ├── app.py                 # FastAPI inference engine backend
│   ├── train.py               # Model training script
│   └── models/
│       ├── baby_dragon.py     # Experimental BDH architecture
│       ├── resnet.py          # ResNet-18 wrapper
│       └── gradcam.py         # Grad-CAM visualization module
├── static/
│   ├── index.html             # Frontend telemetry UI
│   ├── app.js                 # Frontend application logic
│   └── style.css              # Aerospace dark theme styling
├── saved_models/              # Neural network weights (generated post-training)
│   ├── baby_dragon.pth
│   ├── resnet.pth
│   ├── classes.json
│   ├── colors.json
│   └── metrics.json
├── data/eurosat/2750/         # EuroSAT dataset (download separately)
├── scripts/                   # PDF generation scripts
├── docs/                      # Generated architecture PDFs
├── requirements.txt
├── run_app.sh
└── README.md
```

---

## 🔧 Troubleshooting

| Anomaly | Resolution |
|---------|----------|
| `ModuleNotFoundError: No module named 'models'` | Ensure `PYTHONPATH` is set as shown above, or use `run_app.sh` |
| `Models not loaded` error in browser | Run `train.py` first to generate the `.pth` weight files |
| `torch` won't install | Reference the platform-specific instructions in Step 3 |
| Port 8000 already in use | Use `--port 8001` or terminate the existing process binding the port |

---

## 📄 License

This project was developed for Earth Observation AI research and demonstration purposes.
