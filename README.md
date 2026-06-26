# 🛰️ SensiSpace — Satellite Land Cover Classification

A deep-learning web application that classifies satellite images into **10 land cover categories** using two competing models:

- **Baby Dragon Hatchling (BDH)** — a custom lightweight CNN architecture
- **ResNet-18** — a standard pretrained baseline

Upload a satellite image (or use a random sample) and get side-by-side predictions with Grad-CAM visualizations showing *what* each model focuses on.

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.128-green)
![PyTorch](https://img.shields.io/badge/PyTorch-2.8-red)

---

## 📸 Features

- Side-by-side BDH vs. ResNet-18 comparison
- Grad-CAM heatmap overlays for model interpretability
- Spectral land cover segmentation visualization
- Real-time inference speed benchmarking
- 10-class EuroSAT land cover classification

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd Major\ project
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate         # Windows
```

### 3. Install dependencies

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

### 4. Download the EuroSAT dataset

Download [EuroSAT RGB](https://zenodo.org/records/7711810#.ZAm3k-zMKEA) and extract so the folder structure looks like:

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

### 5. Train the models

```bash
source venv/bin/activate
PYTHONPATH=$PYTHONPATH:$(pwd)/src python src/train.py
```

This will train both BDH and ResNet-18 and save weights to `saved_models/`.

### 6. Run the app

```bash
source venv/bin/activate
PYTHONPATH=$PYTHONPATH:$(pwd)/src uvicorn app:app --app-dir src --host 0.0.0.0 --port 8000 --reload
```

Or simply:

```bash
./run_app.sh
```

Then open **http://localhost:8000** in your browser.

---

## 📁 Project Structure

```
.
├── src/
│   ├── app.py                 # FastAPI backend
│   ├── train.py               # Model training script
│   └── models/
│       ├── baby_dragon.py     # BDH architecture
│       ├── resnet.py          # ResNet-18 wrapper
│       └── gradcam.py         # Grad-CAM visualization
├── static/
│   ├── index.html             # Frontend UI
│   ├── app.js                 # Frontend logic
│   └── style.css              # Styles
├── saved_models/              # Trained weights (generated after training)
│   ├── baby_dragon.pth
│   ├── resnet.pth
│   ├── classes.json
│   ├── colors.json
│   └── metrics.json
├── data/eurosat/2750/         # EuroSAT dataset (download separately)
├── requirements.txt
├── run_app.sh
└── README.md
```

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: No module named 'models'` | Make sure you set `PYTHONPATH` as shown above, or use `run_app.sh` |
| `Models not loaded` error in browser | Run `train.py` first to generate the `.pth` weight files |
| `torch` won't install | See the platform-specific instructions in Step 3 above |
| Port 8000 already in use | Use `--port 8001` or kill the existing process |

---

## 📄 License

This project was developed as a Major Project for academic purposes.
