# 🚀 SpaceX: Satellite Land Cover Intelligence

An advanced, deep-learning powered web application that classifies satellite telemetry and imagery into **10 distinct planetary land cover categories**. The system evaluates a lightweight neural architecture against a standard baseline:

- **Baby Dragon Hatchling (BDH)** — an experimental, lightweight CNN architecture featuring lateral inhibition and contextual attention.
- **ResNet-18** — a standard ImageNet-pretrained baseline for Earth observation tasks.

Upload satellite telemetry to receive side-by-side predictions with Grad-CAM heatmaps showing *where* each model focuses its attention.

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.128-green)
![PyTorch](https://img.shields.io/badge/PyTorch-2.8-red)

---

## 📡 Features

- Side-by-side BDH vs. ResNet-18 architectural comparison.
- Grad-CAM heatmap overlays for model interpretability.
- Spectral land cover segmentation visualization.
- Real-time inference latency benchmarking.
- 10-class EuroSAT planetary land cover classification.

---

## 🛰️ Mission Quick Start

### 1. Initialize & Configure Virtual Environment

```bash
git clone https://github.com/Akshat0359/spaceX.git
cd SpaceX
python -m venv venv
# macOS/Linux: source venv/bin/activate
# Windows: venv\Scripts\activate
pip install -r requirements.txt
```

> **Note:** If `torch` installation fails, install PyTorch separately from [pytorch.org](https://pytorch.org/get-started/locally/) before installing the remaining dependencies.

### 2. Sync EuroSAT Dataset

Download [EuroSAT RGB](https://zenodo.org/records/7711810#.ZAm3k-zMKEA) and extract it so the directory looks like:
`data/eurosat/2750/<classes>/`

### 3. Train Neural Models

```bash
# macOS/Linux
PYTHONPATH=$PYTHONPATH:$(pwd)/src python src/train.py
# Windows
set PYTHONPATH=%PYTHONPATH%;%cd%\src
python src\train.py
```

### 4. Launch Inference Engine

```bash
./run_app.sh
```
*Or via uvicorn directly:*
```bash
uvicorn app:app --app-dir src --host 0.0.0.0 --port 8000 --reload
```

Open **http://localhost:8000** in your browser.

---

## 📁 System Architecture

```text
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
├── data/eurosat/2750/         # EuroSAT dataset (download separately)
├── scripts/                   # Utility scripts
├── requirements.txt
└── run_app.sh
```

---

## 🔧 Troubleshooting

| Anomaly | Resolution |
|---------|----------|
| `ModuleNotFoundError: No module named 'models'` | Ensure `PYTHONPATH` is set correctly or use `run_app.sh`. |
| `Models not loaded` error in browser | Run `train.py` first to generate the `.pth` weight files. |
| Port 8000 already in use | Use `--port 8001` or terminate the existing process. |
