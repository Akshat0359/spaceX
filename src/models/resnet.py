import torch
import torch.nn as nn
from torchvision import models

def get_resnet() -> nn.Module:
    """
    Returns a standard ResNet18 model configured for 10 classes (EuroSAT).
    Pretrained on ImageNet to leverage transfer learning.
    """
    # Load pretrained resnet18
    # NOTE: In recent torchvision, using weights parameter is preferred over pretrained=True
    model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
    
    # Freeze the convolutional base to speed up training
    # For a fairer comparison, we can optionally just fine-tune the final layer
    for param in model.parameters():
        param.requires_grad = False
        
    num_ftrs = model.fc.in_features
    # Replace the final fully connected layer for 10 classes
    model.fc = nn.Linear(num_ftrs, 10)
    
    return model
