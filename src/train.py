"""
Training Pipeline for Satellite Image Land Cover Classification
===============================================================
Trains both Baby Dragon Hatchling (BDH) and ResNet-18 on the full
EuroSAT dataset (27,000 images, 10 land cover classes).
"""

import os
import json
import time
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, transforms
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

from models.baby_dragon import BabyDragonHatchling
from models.resnet import get_resnet

# ─── Configuration ────────────────────────────────────────────
BATCH_SIZE = 32
EPOCHS = 10
LR_BDH = 1e-3
LR_RESNET = 1e-3
DATA_DIR = './data'
MODELS_DIR = './saved_models'

CLASS_LABELS = [
    "AnnualCrop", "Forest", "HerbaceousVegetation", "Highway",
    "Industrial", "Pasture", "PermanentCrop", "Residential",
    "River", "SeaLake"
]

# Land cover color map (RGB) for frontend visualization
LAND_COVER_COLORS = {
    "AnnualCrop":             [255, 255, 100],
    "Forest":                 [0, 128, 0],
    "HerbaceousVegetation":   [144, 238, 144],
    "Highway":                [128, 128, 128],
    "Industrial":             [255, 69, 0],
    "Pasture":                [124, 252, 0],
    "PermanentCrop":          [218, 165, 32],
    "Residential":            [220, 20, 60],
    "River":                  [65, 105, 225],
    "SeaLake":                [0, 0, 205]
}


def prepare_data():
    """Load EuroSAT dataset with augmentation for training."""
    train_transform = transforms.Compose([
        transforms.Resize((64, 64)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomVerticalFlip(),
        transforms.RandomRotation(15),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.1),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    test_transform = transforms.Compose([
        transforms.Resize((64, 64)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    full_dataset = datasets.EuroSAT(root=DATA_DIR, download=True, transform=train_transform)
    print(f"📊 Dataset: {len(full_dataset)} images, {len(full_dataset.classes)} classes")

    train_size = int(0.8 * len(full_dataset))
    test_size = len(full_dataset) - train_size
    train_set, test_set = random_split(full_dataset, [train_size, test_size])

    train_loader = DataLoader(train_set, batch_size=BATCH_SIZE, shuffle=True, num_workers=2)
    test_loader = DataLoader(test_set, batch_size=BATCH_SIZE, shuffle=False, num_workers=2)

    return train_loader, test_loader, full_dataset.classes


def train_model(model, train_loader, device, epochs, lr, name="Model"):
    """Standard training loop for any PyTorch model."""
    print(f"\n🚀 Training {name}...")
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)

    start = time.time()
    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0

        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()

        acc = 100. * correct / total
        avg_loss = running_loss / len(train_loader)
        print(f"  Epoch [{epoch+1}/{epochs}]  Loss: {avg_loss:.4f}  Train Acc: {acc:.2f}%")
        scheduler.step()

    elapsed = time.time() - start
    print(f"  ✓ {name} trained in {elapsed:.1f}s")
    return model, elapsed


def evaluate_model(model, test_loader, device):
    """Compute accuracy, precision, recall, F1, and inference time."""
    model.eval()
    all_preds, all_targets = [], []
    inference_times = []

    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)

            t0 = time.time()
            outputs = model(images)
            _, predicted = outputs.max(1)
            t1 = time.time()

            inference_times.append((t1 - t0) / images.size(0))
            all_preds.extend(predicted.cpu().numpy())
            all_targets.extend(labels.cpu().numpy())

    accuracy = accuracy_score(all_targets, all_preds)
    precision, recall, f1, _ = precision_recall_fscore_support(
        all_targets, all_preds, average='macro', zero_division=0)
    avg_inf = (sum(inference_times) / len(inference_times)) * 1000

    return {
        "accuracy":          round(accuracy, 4),
        "precision":         round(precision, 4),
        "recall":            round(recall, 4),
        "f1":                round(f1, 4),
        "inference_time_ms": round(avg_inf, 4)
    }


def count_params(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


def main():
    os.makedirs(MODELS_DIR, exist_ok=True)

    device = torch.device('cpu')
    if torch.cuda.is_available():
        device = torch.device('cuda')
    elif torch.backends.mps.is_available():
        device = torch.device('mps')
    print(f"🖥  Device: {device}")

    train_loader, test_loader, classes = prepare_data()

    # ── 1. Train ResNet-18 ──────────────────────────────
    resnet = get_resnet().to(device)
    resnet, resnet_time = train_model(resnet, train_loader, device, EPOCHS, LR_RESNET, "ResNet-18")
    resnet_metrics = evaluate_model(resnet, test_loader, device)
    resnet_metrics["train_time_s"] = round(resnet_time, 2)
    resnet_metrics["parameters"] = count_params(resnet)
    torch.save(resnet.state_dict(), os.path.join(MODELS_DIR, 'resnet.pth'))
    print(f"  📈 ResNet Accuracy: {resnet_metrics['accuracy']*100:.2f}%")

    # ── 2. Train Baby Dragon Hatchling ──────────────────
    bdh = BabyDragonHatchling(num_classes=10).to(device)
    bdh, bdh_time = train_model(bdh, train_loader, device, EPOCHS, LR_BDH, "Baby Dragon Hatchling")
    bdh_metrics = evaluate_model(bdh, test_loader, device)
    bdh_metrics["train_time_s"] = round(bdh_time, 2)
    bdh_metrics["parameters"] = count_params(bdh)
    torch.save(bdh.state_dict(), os.path.join(MODELS_DIR, 'baby_dragon.pth'))
    print(f"  📈 BDH Accuracy: {bdh_metrics['accuracy']*100:.2f}%")

    # ── Save metadata ──────────────────────────────────
    with open(os.path.join(MODELS_DIR, 'classes.json'), 'w') as f:
        json.dump(list(classes), f)

    with open(os.path.join(MODELS_DIR, 'colors.json'), 'w') as f:
        json.dump(LAND_COVER_COLORS, f)

    comparison = {"resnet": resnet_metrics, "baby_dragon": bdh_metrics}
    with open(os.path.join(MODELS_DIR, 'metrics.json'), 'w') as f:
        json.dump(comparison, f, indent=4)

    print("\n═══════════════════════════════════════")
    print("  TRAINING COMPLETE — Results Summary")
    print("═══════════════════════════════════════")
    print(json.dumps(comparison, indent=4))


if __name__ == "__main__":
    main()
