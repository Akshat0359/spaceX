#!/usr/bin/env python3
"""Generate DFD PDF with proper visual flowchart diagrams using matplotlib."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import os
from fpdf import FPDF

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'docs''
IMG_DIR = os.path.join(OUT_DIR, '_dfd_imgs')
os.makedirs(IMG_DIR, exist_ok=True)

# ── Drawing helpers ──
def styled_box(ax, x, y, w, h, text, color='#503CB4', text_color='white', fontsize=9, style='round'):
    if style == 'round':
        box = FancyBboxPatch((x-w/2, y-h/2), w, h, boxstyle="round,pad=0.15", 
                             facecolor=color, edgecolor='#2a1a6e', linewidth=1.5, zorder=3)
    elif style == 'circle':
        circle = plt.Circle((x, y), w/2, facecolor=color, edgecolor='#2a1a6e', linewidth=2, zorder=3)
        ax.add_patch(circle)
        ax.text(x, y, text, ha='center', va='center', fontsize=fontsize, color=text_color, fontweight='bold', zorder=4, wrap=True)
        return
    else:
        box = FancyBboxPatch((x-w/2, y-h/2), w, h, boxstyle="square,pad=0.1",
                             facecolor=color, edgecolor='#2a1a6e', linewidth=1.5, zorder=3)
    ax.add_patch(box)
    lines = text.split('\n')
    for i, line in enumerate(lines):
        offset = (i - (len(lines)-1)/2) * (fontsize*1.3/72)
        fw = 'bold' if i == 0 else 'normal'
        ax.text(x, y - offset, line, ha='center', va='center', fontsize=fontsize if i==0 else fontsize-1,
                color=text_color, fontweight=fw, zorder=4)

def arrow(ax, x1, y1, x2, y2, label='', color='#503CB4'):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=1.8, connectionstyle='arc3,rad=0'),
                zorder=2)
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx+0.15, my, label, fontsize=7, color='#333', ha='left', va='center',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='#ffffcc', edgecolor='#ccc', alpha=0.9), zorder=5)

def save_fig(fig, name):
    path = os.path.join(IMG_DIR, name)
    fig.savefig(path, dpi=180, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    return path

# ═══════════════════════════════════════════
# DIAGRAM 1: Level 0 Context Diagram
# ═══════════════════════════════════════════
def draw_context():
    fig, ax = plt.subplots(1, 1, figsize=(10, 5))
    ax.set_xlim(0, 10); ax.set_ylim(0, 5); ax.axis('off')
    ax.set_title('Level 0 — Context Diagram', fontsize=16, fontweight='bold', color='#503CB4', pad=15)
    styled_box(ax, 1.5, 2.5, 2, 1, 'User', '#2d8a4e', 'white', 11)
    styled_box(ax, 5, 2.5, 2.5, 1.5, 'SpaceX\nClassification\nSystem', '#503CB4', 'white', 11, 'circle')
    styled_box(ax, 8.5, 2.5, 2, 1, 'EuroSAT\nDataset', '#1a5276', 'white', 10)
    arrow(ax, 2.5, 2.8, 3.75, 2.8, 'Satellite Image')
    arrow(ax, 6.25, 2.8, 7.5, 2.8, '27K Images')
    arrow(ax, 5, 1.5, 1.5, 1.7, 'Classification Results')
    return save_fig(fig, '01_context.png')

# ═══════════════════════════════════════════
# DIAGRAM 2: Level 1 System DFD
# ═══════════════════════════════════════════
def draw_level1():
    fig, ax = plt.subplots(1, 1, figsize=(11, 7))
    ax.set_xlim(0, 11); ax.set_ylim(0, 7); ax.axis('off')
    ax.set_title('Level 1 — System Data Flow Diagram', fontsize=16, fontweight='bold', color='#503CB4', pad=15)
    # External
    styled_box(ax, 1.2, 6, 1.8, 0.8, 'User', '#2d8a4e')
    styled_box(ax, 1.2, 1, 1.8, 0.8, 'EuroSAT\nDataset', '#1a5276')
    # Processes
    styled_box(ax, 4.5, 1, 2.2, 0.9, '1.0\nTraining Pipeline', '#503CB4')
    styled_box(ax, 4.5, 3.5, 2.2, 0.9, '2.0\nInference Engine', '#503CB4')
    styled_box(ax, 8.5, 3.5, 2.2, 0.9, '3.0\nSpectral Segmentation', '#8e44ad')
    styled_box(ax, 4.5, 6, 2.2, 0.9, '4.0\nFrontend UI', '#2980b9')
    # Data stores
    styled_box(ax, 8.5, 1, 2, 0.7, 'D1: Model Weights', '#c0392b', 'white', 8, 'square')
    styled_box(ax, 8.5, 5.5, 2, 0.7, 'D2: Metrics/Config', '#c0392b', 'white', 8, 'square')
    # Arrows
    arrow(ax, 2.1, 1, 3.4, 1, 'Raw Images')
    arrow(ax, 5.6, 1.45, 7.5, 1, 'Weights')
    arrow(ax, 8.5, 1.35, 5.5, 3.1, 'Load Models')
    arrow(ax, 2.1, 6, 3.4, 6, 'Upload Image')
    arrow(ax, 4.5, 5.55, 4.5, 3.95, 'Image')
    arrow(ax, 5.6, 3.5, 7.4, 3.5, 'Probs + Image')
    arrow(ax, 7.4, 3.9, 5.6, 3.9, 'Overlay')
    arrow(ax, 4.5, 3.05, 4.5, 5.55, 'JSON Response')
    arrow(ax, 8.5, 5.15, 5.6, 5.7, 'Metrics')
    return save_fig(fig, '02_level1.png')

# ═══════════════════════════════════════════
# DIAGRAM 3: BDH Architecture DFD
# ═══════════════════════════════════════════
def draw_bdh():
    fig, ax = plt.subplots(1, 1, figsize=(10, 14))
    ax.set_xlim(0, 10); ax.set_ylim(0, 14); ax.axis('off')
    ax.set_title('BDH Architecture — Data Flow Diagram', fontsize=16, fontweight='bold', color='#503CB4', pad=15)
    y = 13
    styled_box(ax, 5, y, 3, 0.7, 'Input Image (3×64×64)', '#1a5276'); y -= 1
    arrow(ax, 5, y+0.65, 5, y+0.35)
    styled_box(ax, 5, y, 3.5, 0.7, 'STEM: Conv 3→32→64 + BN + ReLU', '#2c3e50'); y -= 1.2

    for stage, ch, res in [('Stage 1', '64', '64×64→32×32'), ('Stage 2', '128', '32×32→16×16'), ('Stage 3', '256', '16×16→8×8')]:
        arrow(ax, 5, y+0.85, 5, y+0.55)
        # Stage box
        ax.add_patch(FancyBboxPatch((1.5, y-1.2), 7, 1.7, boxstyle="round,pad=0.15",
                                     facecolor='#f0ecff', edgecolor='#503CB4', linewidth=2, zorder=1))
        ax.text(5, y+0.35, f'BDH {stage} ({ch} channels)', fontsize=10, ha='center', fontweight='bold', color='#503CB4', zorder=4)
        # 3 sub-boxes
        styled_box(ax, 2.8, y-0.4, 2, 0.6, 'Multi-Scale\n3×3 | 5×5 | 7×7', '#6c3483', 'white', 7)
        styled_box(ax, 5.3, y-0.4, 1.8, 0.6, 'Lateral\nInhibition', '#1a5276', 'white', 7)
        styled_box(ax, 7.7, y-0.4, 1.8, 0.6, 'Contextual\nAttention', '#8e44ad', 'white', 7)
        arrow(ax, 3.8, y-0.4, 4.4, y-0.4, color='#666')
        arrow(ax, 6.2, y-0.4, 6.8, y-0.4, color='#666')
        # Residual
        ax.annotate('', xy=(8.6, y-0.7), xytext=(1.8, y-0.7),
                    arrowprops=dict(arrowstyle='->', color='#e74c3c', lw=1.2, linestyle='--', connectionstyle='arc3,rad=-0.3'), zorder=2)
        ax.text(5, y-0.9, f'+ Residual → MaxPool ({res})', fontsize=7, ha='center', color='#e74c3c', zorder=4)
        y -= 2.2

    arrow(ax, 5, y+0.85, 5, y+0.55)
    styled_box(ax, 5, y, 4, 0.8, 'Recurrent Refinement (×2)\nConv→Gate(σ)→ x·g + ref·(1-g)', '#d35400', 'white', 9); y -= 1.2
    arrow(ax, 5, y+0.75, 5, y+0.45)
    styled_box(ax, 5, y, 4.5, 0.8, 'Classifier\nGAP → Drop(0.3) → FC(256→128) → FC(128→10)', '#2c3e50', 'white', 8); y -= 1
    arrow(ax, 5, y+0.55, 5, y+0.35)
    styled_box(ax, 5, y, 3, 0.6, '10 Class Logits → Softmax', '#27ae60', 'white', 9)
    return save_fig(fig, '03_bdh.png')

# ═══════════════════════════════════════════
# DIAGRAM 4: ResNet-18 Architecture DFD
# ═══════════════════════════════════════════
def draw_resnet():
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis('off')
    ax.set_title('ResNet-18 Architecture — Data Flow Diagram', fontsize=16, fontweight='bold', color='#2980b9', pad=15)
    y = 9
    styled_box(ax, 5, y, 3, 0.7, 'Input Image (3×64×64)', '#1a5276'); y -= 1.1
    # Frozen backbone box
    ax.add_patch(FancyBboxPatch((1.5, 1.8), 7, 6.3, boxstyle="round,pad=0.2",
                                 facecolor='#eaf2f8', edgecolor='#2980b9', linewidth=2, linestyle='--', zorder=0))
    ax.text(8, 7.9, 'FROZEN', fontsize=10, color='#2980b9', fontweight='bold', fontstyle='italic', zorder=4)
    
    layers = [
        ('Conv 7×7 stride=2 + BN + ReLU + MaxPool', '64ch'),
        ('Layer 1: 2× BasicBlock', '64ch'),
        ('Layer 2: 2× BasicBlock', '128ch'),
        ('Layer 3: 2× BasicBlock ★ Grad-CAM', '256ch'),
        ('Layer 4: 2× BasicBlock', '512ch'),
        ('AdaptiveAvgPool → Flatten', '512'),
    ]
    for text, ch in layers:
        arrow(ax, 5, y+0.45, 5, y+0.15)
        c = '#e74c3c' if 'Grad-CAM' in text else '#2c3e50'
        styled_box(ax, 5, y-0.3, 5, 0.6, f'{text} ({ch})', c, 'white', 8)
        y -= 1
    
    arrow(ax, 5, y+0.45, 5, y+0.15)
    styled_box(ax, 5, y-0.3, 3.5, 0.7, 'TRAINABLE\nLinear(512 → 10)', '#8e44ad', 'white', 10); y -= 1.2
    arrow(ax, 5, y+0.55, 5, y+0.35)
    styled_box(ax, 5, y-0.1, 3, 0.6, '10 Class Logits → Softmax', '#27ae60', 'white', 9)
    return save_fig(fig, '04_resnet.png')

# ═══════════════════════════════════════════
# DIAGRAM 5: Training Pipeline DFD
# ═══════════════════════════════════════════
def draw_training():
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_xlim(0, 12); ax.set_ylim(0, 8); ax.axis('off')
    ax.set_title('Training Pipeline — Data Flow Diagram', fontsize=16, fontweight='bold', color='#503CB4', pad=15)
    # Data source
    styled_box(ax, 1.5, 7, 2.2, 0.8, 'EuroSAT Dataset\n27K images, 10 classes', '#1a5276')
    arrow(ax, 2.6, 6.6, 4, 6.3)
    styled_box(ax, 5.5, 6, 2.5, 0.8, 'Data Preparation\nResize, Augment, Normalize', '#2c3e50')
    # Split
    arrow(ax, 4.5, 5.6, 3.5, 5)
    arrow(ax, 6.5, 5.6, 7.5, 5)
    styled_box(ax, 3, 4.7, 2, 0.6, 'Train Set\n21,600 images', '#27ae60', 'white', 8)
    styled_box(ax, 8, 4.7, 2, 0.6, 'Test Set\n5,400 images', '#e67e22', 'white', 8)
    # Two model paths
    arrow(ax, 3, 4.4, 3, 3.6)
    arrow(ax, 3, 4.4, 7, 3.6)
    styled_box(ax, 3, 3.2, 2.5, 0.8, 'Train ResNet-18\nAdam, lr=1e-3\n10 epochs', '#2980b9', 'white', 8)
    styled_box(ax, 7, 3.2, 2.5, 0.8, 'Train BDH\nAdam, lr=1e-3\n10 epochs', '#503CB4', 'white', 8)
    # Evaluate
    arrow(ax, 3, 2.8, 3, 2.2)
    arrow(ax, 7, 2.8, 7, 2.2)
    arrow(ax, 8, 4.4, 3, 2)
    arrow(ax, 8, 4.4, 7, 2)
    styled_box(ax, 3, 1.8, 2.2, 0.7, 'Evaluate\nAcc, P, R, F1', '#e74c3c', 'white', 8)
    styled_box(ax, 7, 1.8, 2.2, 0.7, 'Evaluate\nAcc, P, R, F1', '#e74c3c', 'white', 8)
    # Save
    arrow(ax, 3, 1.45, 5, 0.9)
    arrow(ax, 7, 1.45, 5, 0.9)
    styled_box(ax, 5, 0.6, 4, 0.7, 'Save: resnet.pth, baby_dragon.pth\nmetrics.json, classes.json', '#c0392b', 'white', 8)
    return save_fig(fig, '05_training.png')

# ═══════════════════════════════════════════
# DIAGRAM 6: Inference DFD
# ═══════════════════════════════════════════
def draw_inference():
    fig, ax = plt.subplots(1, 1, figsize=(12, 10))
    ax.set_xlim(0, 12); ax.set_ylim(0, 10); ax.axis('off')
    ax.set_title('Inference & Prediction — Data Flow Diagram', fontsize=16, fontweight='bold', color='#503CB4', pad=15)
    styled_box(ax, 2, 9, 2, 0.7, 'User Upload\nSatellite Image', '#2d8a4e')
    arrow(ax, 3, 8.65, 5.5, 8.15)
    styled_box(ax, 5.5, 7.8, 3, 0.7, 'Preprocessing\nResize 64×64 → Normalize', '#2c3e50')
    # Split to two models
    arrow(ax, 4.5, 7.45, 3, 6.8)
    arrow(ax, 6.5, 7.45, 8, 6.8)
    styled_box(ax, 3, 6.4, 2.5, 0.8, 'ResNet-18\nForward Pass\n(no_grad)', '#2980b9', 'white', 9)
    styled_box(ax, 8, 6.4, 2.5, 0.8, 'BDH\nForward Pass\n(no_grad)', '#503CB4', 'white', 9)
    # Softmax
    arrow(ax, 3, 6, 3, 5.4)
    arrow(ax, 8, 6, 8, 5.4)
    styled_box(ax, 3, 5.1, 2, 0.6, 'Softmax\n→ Probabilities', '#8e44ad', 'white', 8)
    styled_box(ax, 8, 5.1, 2, 0.6, 'Softmax\n→ Probabilities', '#8e44ad', 'white', 8)
    # Spectral
    arrow(ax, 3, 4.8, 3, 4.1)
    arrow(ax, 8, 4.8, 8, 4.1)
    styled_box(ax, 3, 3.7, 2.5, 0.7, 'Spectral\nSegmentation', '#d35400', 'white', 9)
    styled_box(ax, 8, 3.7, 2.5, 0.7, 'Spectral\nSegmentation', '#d35400', 'white', 9)
    # Assemble
    arrow(ax, 3, 3.35, 5.5, 2.6)
    arrow(ax, 8, 3.35, 5.5, 2.6)
    styled_box(ax, 5.5, 2.2, 4, 0.8, 'Assemble JSON Response\n{resnet: {...}, baby_dragon: {...}}', '#c0392b', 'white', 9)
    arrow(ax, 5.5, 1.8, 5.5, 1.2)
    styled_box(ax, 5.5, 0.8, 3.5, 0.7, 'Frontend Render\nTabs, Charts, Comparison', '#2d8a4e', 'white', 9)
    # Data stores
    styled_box(ax, 10.5, 7, 1.5, 0.6, 'D1: Weights', '#c0392b', 'white', 7, 'square')
    arrow(ax, 9.75, 7, 9.25, 6.6, color='#c0392b')
    arrow(ax, 9.75, 6.8, 4.25, 6.6, color='#c0392b')
    return save_fig(fig, '06_inference.png')

# ═══════════════════════════════════════════
# DIAGRAM 7: Spectral Segmentation DFD
# ═══════════════════════════════════════════
def draw_spectral():
    fig, ax = plt.subplots(1, 1, figsize=(11, 9))
    ax.set_xlim(0, 11); ax.set_ylim(0, 9); ax.axis('off')
    ax.set_title('Spectral Segmentation — Data Flow Diagram', fontsize=16, fontweight='bold', color='#d35400', pad=15)
    styled_box(ax, 3, 8.2, 2.5, 0.7, 'Original Image\n(PIL)', '#1a5276')
    styled_box(ax, 8, 8.2, 2.5, 0.7, 'Model Probabilities\n{class: prob}', '#503CB4')
    arrow(ax, 3, 7.85, 3, 7.3)
    styled_box(ax, 3, 7, 2.5, 0.6, 'Resize 400×400\n→ RGB Array', '#2c3e50')
    # Color space split
    arrow(ax, 2, 6.7, 1.5, 6.2)
    arrow(ax, 3, 6.7, 3, 6.2)
    arrow(ax, 4, 6.7, 5, 6.2)
    styled_box(ax, 1.5, 5.9, 1.5, 0.5, 'HSV\nH, S, V', '#2980b9', 'white', 7)
    styled_box(ax, 3.2, 5.9, 1.5, 0.5, 'LAB\nL, A, B', '#8e44ad', 'white', 7)
    styled_box(ax, 5, 5.9, 1.8, 0.5, 'Veg Indices\nGLI, ExG', '#27ae60', 'white', 7)
    # Masks
    arrow(ax, 3, 5.65, 3, 5.1)
    masks = ['Dense Veg', 'Light Veg', 'Water', 'Urban', 'Road', 'Bare Soil']
    for i, m in enumerate(masks):
        x = 1 + i * 1.65
        styled_box(ax, x, 4.8, 1.4, 0.5, m, '#e67e22', 'white', 6)
        arrow(ax, x, 4.55, x, 4.1, color='#e67e22')
    # Cleanup
    styled_box(ax, 5, 3.8, 6, 0.6, 'Morphological Cleanup + Overlap Resolution (priority-based)', '#c0392b')
    arrow(ax, 5, 3.5, 5, 3)
    # Map to classes
    styled_box(ax, 5, 2.7, 5, 0.6, 'Map Spectral → EuroSAT Classes\n(pick highest-probability candidate)', '#503CB4')
    arrow(ax, 8, 7.85, 8, 3)
    arrow(ax, 5, 2.4, 5, 1.8)
    styled_box(ax, 5, 1.5, 5, 0.6, 'Overlay Rendering\nColor Fill + Contours + Labels', '#d35400')
    arrow(ax, 5, 1.2, 5, 0.7)
    styled_box(ax, 5, 0.4, 3, 0.5, 'Base64 JPEG Output', '#27ae60', 'white', 9)
    return save_fig(fig, '07_spectral.png')

# ═══════════════════════════════════════════
# Build PDF
# ═══════════════════════════════════════════
def build_pdf():
    print("Generating diagram images...")
    images = [
        (draw_context(), 'Level 0 — Context Diagram'),
        (draw_level1(), 'Level 1 — System Data Flow Diagram'),
        (draw_bdh(), 'BDH Architecture — Data Flow Diagram'),
        (draw_resnet(), 'ResNet-18 Architecture — Data Flow Diagram'),
        (draw_training(), 'Training Pipeline — Data Flow Diagram'),
        (draw_inference(), 'Inference & Prediction — Data Flow Diagram'),
        (draw_spectral(), 'Spectral Segmentation — Data Flow Diagram'),
    ]
    
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Title page
    pdf.add_page()
    pdf.ln(50)
    pdf.set_font('Helvetica', 'B', 32)
    pdf.set_text_color(80, 60, 180)
    pdf.cell(0, 15, 'SpaceX', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.set_font('Helvetica', '', 18)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 10, 'Data Flow Diagrams', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)
    pdf.set_draw_color(80, 60, 180)
    pdf.set_line_width(1.2)
    pdf.line(60, pdf.get_y(), 150, pdf.get_y())
    pdf.ln(10)
    pdf.set_font('Helvetica', '', 12)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, 'Satellite Land Cover Classification', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, 'Baby Dragon Hatchling (BDH) vs ResNet-18', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(15)
    pdf.set_font('Helvetica', 'I', 11)
    pdf.cell(0, 8, 'Visual Flowchart Diagrams', align='C', new_x="LMARGIN", new_y="NEXT")
    
    # Diagram pages
    for img_path, title in images:
        pdf.add_page()
        # Header
        pdf.set_font('Helvetica', 'I', 8)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 6, 'SpaceX - Data Flow Diagrams', align='R')
        pdf.ln(2)
        pdf.set_draw_color(80, 60, 180)
        pdf.set_line_width(0.4)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)
        # Image - fit to page width
        pdf.image(img_path, x=10, w=190)
    
    out = os.path.join(OUT_DIR, 'SpaceX_DFD_Visual.pdf')
    pdf.output(out)
    print(f'Visual DFD PDF saved to: {out}')
    
    # Cleanup temp images
    import shutil
    shutil.rmtree(IMG_DIR, ignore_errors=True)
    return out

if __name__ == '__main__':
    build_pdf()
