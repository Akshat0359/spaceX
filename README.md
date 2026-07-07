<div align="center">
  <h1>🚀 SpaceX: Satellite Land Cover Intelligence</h1>
  <p><strong>Advanced Deep-Learning Powered Web Application for Planetary Classification</strong></p>
  
  <p>
    <img src="https://img.shields.io/badge/Python-3.9+-blue.svg?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/FastAPI-0.128-00a67d.svg?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
    <img src="https://img.shields.io/badge/PyTorch-2.8-EE4C2C.svg?style=for-the-badge&logo=pytorch&logoColor=white" alt="PyTorch" />
  </p>
</div>

<hr/>

## 🌌 Overview

**SpaceX** is an AI-driven inference engine that classifies satellite telemetry and imagery into **10 distinct planetary land cover categories**. The system evaluates a highly-experimental, lightweight neural architecture against a proven industry standard:

- 🐉 **Baby Dragon Hatchling (BDH):** An experimental, lightweight CNN architecture featuring lateral inhibition and contextual attention.
- 🏗️ **ResNet-18:** A standard ImageNet-pretrained baseline specifically tuned for Earth observation tasks.

Upload satellite telemetry to receive **real-time side-by-side predictions**, featuring interactive **Grad-CAM heatmaps** that reveal exactly *where* the neural networks focus their attention.

---

## ✨ Mission Features

| Feature | Description |
|:---:|---|
| ⚖️ **Architectural Comparison** | Side-by-side performance benchmarking of BDH vs. ResNet-18. |
| 🗺️ **Grad-CAM Heatmaps** | Deep-learning model interpretability through visual focus mapping. |
| 📊 **Spectral Segmentation** | Visualizing structural features of planetary land cover. |
| ⚡ **Real-Time Benchmarking** | Precise inference latency tracking for performance analysis. |
| 🌍 **10-Class Classification** | Comprehensive EuroSAT land cover categorization. |

---

## 🛰️ Command Center Quick Start

Follow these steps to deploy the inference engine locally.

### 1️⃣ Initialize & Configure Virtual Environment

```bash
git clone https://github.com/Akshat0359/spaceX.git
cd SpaceX
python -m venv venv

# macOS/Linux
source venv/bin/activate
# Windows
venv\Scripts\activate

pip install -r requirements.txt
```
> 💡 **Note:** If `torch` installation fails, please install PyTorch separately from [pytorch.org](https://pytorch.org/get-started/locally/) before installing the remaining dependencies.

### 2️⃣ Sync the EuroSAT Dataset

Download the [EuroSAT RGB Dataset](https://zenodo.org/records/7711810#.ZAm3k-zMKEA). Extract the contents so the directory matches this structure:

```text
data/eurosat/2750/<classes>/
```

### 3️⃣ Train Neural Models

```bash
# macOS/Linux
PYTHONPATH=$PYTHONPATH:$(pwd)/src python src/train.py

# Windows
set PYTHONPATH=%PYTHONPATH%;%cd%\src
python src\train.py
```
*(This process generates the required `.pth` weights for both models).*

### 4️⃣ Launch the Inference Engine

You can start the engine using the provided shell script:
```bash
./run_app.sh
```
Or run `uvicorn` directly:
```bash
uvicorn app:app --app-dir src --host 0.0.0.0 --port 8000 --reload
```

🌐 **Dashboard:** Open [**http://localhost:8000**](http://localhost:8000) in your browser.

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

## 🔧 Diagnostics & Troubleshooting

| Anomaly | Resolution |
|---|---|
| ❌ `ModuleNotFoundError: No module named 'models'` | Ensure `PYTHONPATH` is set correctly or launch via `run_app.sh`. |
| ❌ `Models not loaded` (Browser) | Run `train.py` first to generate the `.pth` weight files. |
| ❌ `Port 8000 already in use` | Use `--port 8001` or terminate the existing process. |
