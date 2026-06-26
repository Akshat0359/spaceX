"""
Baby Dragon Hatchling (BDH) Architecture
=========================================
A novel biologically-inspired deep learning architecture designed for satellite
remote sensing image analysis. Unlike conventional CNNs, BDH introduces:

1. Lateral Inhibition Blocks — Inspired by biological neural circuits where
   neighboring neurons suppress each other to sharpen spatial features.
2. Contextual Attention Module — A dual spatial + channel attention mechanism
   that models long-range contextual relationships in geospatial imagery.  
3. Multi-Scale Feature Pyramid — Extracts features at multiple receptive field
   sizes simultaneously, critical for satellite images where objects vary in scale.
4. Recurrent Refinement — A lightweight recurrent loop that iteratively refines
   feature maps, mimicking the brain's feedback processing pathways.

Reference: ISRO RESPOND initiative for intelligent Earth observation systems.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class LateralInhibitionBlock(nn.Module):
    """
    Biologically-inspired lateral inhibition: enhances contrast between
    neighboring feature map activations. Simulates how biological neurons
    suppress surrounding activity to sharpen feature detection.
    """
    def __init__(self, channels):
        super().__init__()
        # Learned inhibition kernel (depthwise conv simulating surround suppression)
        self.inhibition = nn.Conv2d(channels, channels, kernel_size=3, padding=1,
                                     groups=channels, bias=False)
        self.bn = nn.BatchNorm2d(channels)
        self.alpha = nn.Parameter(torch.tensor(0.3))  # Learnable inhibition strength

    def forward(self, x):
        surround = self.inhibition(x)
        surround = self.bn(surround)
        # Subtract scaled surround response (lateral inhibition)
        inhibited = x - self.alpha * surround
        return F.relu(inhibited)


class ContextualAttention(nn.Module):
    """
    Dual attention module combining:
    - Channel Attention: learns which feature channels are most informative
    - Spatial Attention: learns which spatial locations to focus on
    This models long-range contextual relationships critical for satellite imagery
    where land cover patterns span large areas.
    """
    def __init__(self, channels, reduction=8):
        super().__init__()
        # Channel attention (Squeeze-and-Excitation style)
        self.channel_pool = nn.AdaptiveAvgPool2d(1)
        self.channel_fc = nn.Sequential(
            nn.Linear(channels, channels // reduction, bias=False),
            nn.ReLU(inplace=True),
            nn.Linear(channels // reduction, channels, bias=False),
            nn.Sigmoid()
        )
        # Spatial attention
        self.spatial_conv = nn.Sequential(
            nn.Conv2d(2, 1, kernel_size=7, padding=3, bias=False),
            nn.Sigmoid()
        )

    def forward(self, x):
        b, c, h, w = x.size()
        
        # Channel attention
        ca = self.channel_pool(x).view(b, c)
        ca = self.channel_fc(ca).view(b, c, 1, 1)
        x = x * ca
        
        # Spatial attention
        avg_out = torch.mean(x, dim=1, keepdim=True)
        max_out, _ = torch.max(x, dim=1, keepdim=True)
        sa = self.spatial_conv(torch.cat([avg_out, max_out], dim=1))
        x = x * sa
        
        return x


class MultiScaleBlock(nn.Module):
    """
    Multi-Scale Feature Pyramid block. Processes input through parallel
    convolutions with different kernel sizes to capture features at multiple
    spatial scales — essential for EuroSAT where land cover varies in size
    (e.g., small buildings vs. large forests).
    """
    def __init__(self, in_channels, out_channels):
        super().__init__()
        mid = out_channels // 3
        remainder = out_channels - 2 * mid
        
        self.branch_3x3 = nn.Sequential(
            nn.Conv2d(in_channels, mid, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(mid),
            nn.ReLU(inplace=True)
        )
        self.branch_5x5 = nn.Sequential(
            nn.Conv2d(in_channels, mid, kernel_size=5, padding=2, bias=False),
            nn.BatchNorm2d(mid),
            nn.ReLU(inplace=True)
        )
        self.branch_7x7 = nn.Sequential(
            nn.Conv2d(in_channels, remainder, kernel_size=7, padding=3, bias=False),
            nn.BatchNorm2d(remainder),
            nn.ReLU(inplace=True)
        )

    def forward(self, x):
        b3 = self.branch_3x3(x)
        b5 = self.branch_5x5(x)
        b7 = self.branch_7x7(x)
        return torch.cat([b3, b5, b7], dim=1)


class BDHStage(nn.Module):
    """
    One processing stage of the Baby Dragon Hatchling architecture.
    Combines: Multi-Scale Feature Extraction → Lateral Inhibition → Contextual Attention
    with a residual connection for gradient flow.
    """
    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.multi_scale = MultiScaleBlock(in_channels, out_channels)
        self.lateral_inhibition = LateralInhibitionBlock(out_channels)
        self.contextual_attention = ContextualAttention(out_channels)
        
        # Residual projection if channel dimensions change
        self.residual = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=1, bias=False),
            nn.BatchNorm2d(out_channels)
        ) if in_channels != out_channels else nn.Identity()

    def forward(self, x):
        identity = self.residual(x)
        
        out = self.multi_scale(x)
        out = self.lateral_inhibition(out)
        out = self.contextual_attention(out)
        
        out = out + identity  # Residual connection
        return F.relu(out)


class BabyDragonHatchling(nn.Module):
    """
    Baby Dragon Hatchling (BDH) Architecture
    ==========================================
    A biologically-inspired deep learning model for satellite remote sensing.
    
    Architecture pipeline:
        Input (3×64×64)
        → Stem Convolution
        → BDH Stage 1 (64 channels) + Pool
        → BDH Stage 2 (128 channels) + Pool
        → BDH Stage 3 (256 channels) + Pool
        → Recurrent Refinement (2 iterations of feedback processing)
        → Global Average Pool → Classifier
    
    The recurrent refinement loop mimics the brain's top-down feedback pathways,
    allowing the network to iteratively improve its feature representations.
    """
    def __init__(self, num_classes=10, refine_iterations=2):
        super().__init__()
        self.refine_iterations = refine_iterations
        
        # Stem: initial feature extraction
        self.stem = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, stride=1, padding=1, bias=False),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1, bias=False),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
        )
        
        # Main BDH stages with progressive feature expansion
        self.stage1 = BDHStage(64, 64)
        self.pool1 = nn.MaxPool2d(2)
        
        self.stage2 = BDHStage(64, 128)
        self.pool2 = nn.MaxPool2d(2)
        
        self.stage3 = BDHStage(128, 256)
        self.pool3 = nn.MaxPool2d(2)
        
        # Recurrent refinement module (lightweight feedback loop)
        self.refine_conv = nn.Sequential(
            nn.Conv2d(256, 256, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
        )
        self.refine_gate = nn.Sequential(
            nn.Conv2d(256, 256, kernel_size=1, bias=False),
            nn.Sigmoid()
        )
        
        # Classifier head
        self.global_pool = nn.AdaptiveAvgPool2d(1)
        self.classifier = nn.Sequential(
            nn.Dropout(0.3),
            nn.Linear(256, 128),
            nn.ReLU(inplace=True),
            nn.Dropout(0.2),
            nn.Linear(128, num_classes)
        )

    def forward(self, x):
        # Stem
        x = self.stem(x)
        
        # Progressive BDH stages
        x = self.stage1(x)
        x = self.pool1(x)
        
        x = self.stage2(x)
        x = self.pool2(x)
        
        x = self.stage3(x)
        x = self.pool3(x)
        
        # Recurrent refinement — iterative feedback processing
        for _ in range(self.refine_iterations):
            refined = self.refine_conv(x)
            gate = self.refine_gate(refined)
            x = x * gate + refined * (1 - gate)  # Gated residual refinement
        
        # Classification
        x = self.global_pool(x).flatten(1)
        x = self.classifier(x)
        return x
