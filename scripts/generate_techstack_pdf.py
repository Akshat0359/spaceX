import os
#!/usr/bin/env python3
"""Generate Technology Stack PDF reusing ProjectPDF style."""

from generate_pdf import ProjectPDF


def generate():
    pdf = ProjectPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    # ── TITLE PAGE ──
    pdf.add_page()
    pdf.ln(50)
    pdf.set_font('Helvetica', 'B', 28)
    pdf.set_text_color(80, 60, 180)
    pdf.cell(0, 15, 'SpaceX', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.set_font('Helvetica', '', 18)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 12, 'Technology Stack', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    pdf.set_draw_color(80, 60, 180)
    pdf.set_line_width(1)
    pdf.line(60, pdf.get_y(), 150, pdf.get_y())
    pdf.ln(10)
    pdf.set_font('Helvetica', '', 12)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, 'Detailed Explanation of Technologies Used', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(20)

    # Overview table
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(0, 8, 'Stack Overview:', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.code_block(
        'Frontend:  HTML5 + CSS3 + JavaScript (Vanilla)\n'
        'Backend:   Python 3.9 + FastAPI + Uvicorn\n'
        'ML:        PyTorch + torchvision\n'
        'Vision:    OpenCV + Pillow (PIL)\n'
        'Data:      NumPy'
    )

    # ════════════════════════════════════
    # 1. PYTHON
    # ════════════════════════════════════
    pdf.add_page()
    pdf.section_title('1. Python 3.9')

    pdf.body_text(
        'Python is a high-level, interpreted programming language known for its readability and '
        'extensive ecosystem. It is the dominant language in machine learning and data science '
        'due to its rich library support.'
    )

    pdf.sub_title('Why Python?')
    w = [40, 100]
    pdf.table_row(['Reason', 'Detail'], w, header=True)
    pdf.table_row(['ML ecosystem', 'PyTorch, TensorFlow, scikit-learn - all Python-first'], w)
    pdf.table_row(['Rapid prototyping', 'Write and test code quickly without compilation'], w)
    pdf.table_row(['Community', 'Largest ML community, extensive documentation'], w)
    pdf.table_row(['Library support', '400,000+ packages on PyPI for any task'], w)
    pdf.ln(3)

    pdf.sub_title('How We Use It')
    pdf.bullet('All backend code: model definitions, training, API, visualization')
    pdf.bullet('Entry points: train.py (training), app.py (server), gradcam.py (visualization)')
    pdf.bullet('Manages entire ML pipeline: data loading, preprocessing, inference, encoding')

    # ════════════════════════════════════
    # 2. PYTORCH
    # ════════════════════════════════════
    pdf.add_page()
    pdf.section_title('2. PyTorch')

    pdf.body_text(
        'PyTorch is an open-source deep learning framework developed by Meta AI Research. It provides '
        'tensor computation with GPU acceleration, automatic differentiation (autograd) for training '
        'neural networks, and dynamic computational graphs for flexible model design.'
    )

    pdf.sub_title('Why PyTorch over TensorFlow?')
    w2 = [35, 50, 50]
    pdf.table_row(['Feature', 'PyTorch', 'TensorFlow'], w2, header=True)
    pdf.table_row(['Graph type', 'Dynamic (eager)', 'Static (graph mode)'], w2)
    pdf.table_row(['Debugging', 'Easy - standard Python', 'Harder - graph execution'], w2)
    pdf.table_row(['Research use', '80%+ of papers', 'Declining in research'], w2)
    pdf.table_row(['Learning curve', 'Pythonic, intuitive', 'Steeper, more boilerplate'], w2)
    pdf.table_row(['Apple Silicon', 'Native MPS support', 'Limited'], w2)
    pdf.ln(3)

    pdf.sub_title('How We Use It')
    pdf.sub_sub_title('Model Definition (nn.Module)')
    pdf.code_block(
        'class BabyDragonHatchling(nn.Module):\n'
        '    def __init__(self):\n'
        '        self.stage1 = BDHStage(64, 64)\n'
        '        self.stage2 = BDHStage(64, 128)\n'
        '    def forward(self, x):\n'
        '        x = self.stage1(x)\n'
        '        return x'
    )
    pdf.body_text(
        'Every model component (MultiScaleBlock, LateralInhibition, ContextualAttention) is '
        'a nn.Module subclass with learnable parameters.'
    )

    pdf.sub_sub_title('Key PyTorch Components Used')
    w3 = [40, 100]
    pdf.table_row(['Component', 'Purpose in SpaceX'], w3, header=True)
    pdf.table_row(['nn.Conv2d', 'Convolutional layers in all model stages'], w3)
    pdf.table_row(['nn.BatchNorm2d', 'Normalizes activations for stable training'], w3)
    pdf.table_row(['nn.Linear', 'Fully connected classifier layers'], w3)
    pdf.table_row(['nn.MaxPool2d', 'Downsamples spatial dimensions between stages'], w3)
    pdf.table_row(['nn.AdaptiveAvgPool2d', 'Global average pooling before classifier'], w3)
    pdf.table_row(['nn.Dropout', 'Regularization to prevent overfitting'], w3)
    pdf.table_row(['nn.Parameter', 'Learnable alpha in lateral inhibition'], w3)
    pdf.table_row(['F.relu / F.softmax', 'Non-linear activation / probability conversion'], w3)
    pdf.table_row(['optim.Adam', 'Optimizer for training both models'], w3)
    pdf.table_row(['CrossEntropyLoss', 'Classification loss function'], w3)

    # ════════════════════════════════════
    # 3. TORCHVISION
    # ════════════════════════════════════
    pdf.add_page()
    pdf.section_title('3. torchvision')

    pdf.body_text(
        'A PyTorch companion library providing pre-trained models (ResNet, VGG, Inception), '
        'image transformations (resize, normalize, augment), and dataset utilities (ImageFolder '
        'for loading labeled images).'
    )

    pdf.sub_title('How We Use It')
    pdf.sub_sub_title('Pre-trained ResNet-18')
    pdf.code_block(
        'from torchvision.models import resnet18, ResNet18_Weights\n'
        'model = resnet18(weights=ResNet18_Weights.IMAGENET1K_V1)\n'
        'model.fc = nn.Linear(512, 10)  # Replace for 10 classes'
    )
    pdf.body_text(
        'This gives us a model pre-trained on 1.3 million ImageNet images - it already knows '
        'edges, textures, and shapes. We only fine-tune it on satellite imagery.'
    )

    pdf.sub_sub_title('Image Transforms')
    pdf.code_block(
        'transforms.Compose([\n'
        '    transforms.Resize((64, 64)),\n'
        '    transforms.RandomHorizontalFlip(),\n'
        '    transforms.RandomRotation(15),\n'
        '    transforms.ColorJitter(brightness=0.2),\n'
        '    transforms.ToTensor(),\n'
        '    transforms.Normalize(mean=[0.485, 0.456, 0.406],\n'
        '                         std=[0.229, 0.224, 0.225])\n'
        '])'
    )

    pdf.sub_sub_title('Dataset Loading')
    pdf.code_block(
        'dataset = ImageFolder("data/eurosat/2750/", transform=transform)\n'
        'loader = DataLoader(dataset, batch_size=64, shuffle=True)'
    )
    pdf.body_text('ImageFolder automatically maps folder names to class labels.')

    # ════════════════════════════════════
    # 4. FASTAPI
    # ════════════════════════════════════
    pdf.add_page()
    pdf.section_title('4. FastAPI')

    pdf.body_text(
        'FastAPI is a modern, high-performance Python web framework for building APIs. Built on '
        'Starlette (async) and Pydantic (validation). It is one of the fastest Python web '
        'frameworks available.'
    )

    pdf.sub_title('Why FastAPI over Flask/Django?')
    w4 = [30, 35, 35, 35]
    pdf.table_row(['Feature', 'FastAPI', 'Flask', 'Django'], w4, header=True)
    pdf.table_row(['Speed', 'Very fast (async)', 'Medium', 'Slower'], w4)
    pdf.table_row(['Auto docs', 'Swagger auto-gen', 'Manual', 'Manual'], w4)
    pdf.table_row(['Type safety', 'Pydantic', 'None', 'Forms-based'], w4)
    pdf.table_row(['Async', 'Native', 'Plugin', 'Limited'], w4)
    pdf.table_row(['Simplicity', 'Minimal code', 'Minimal', 'Heavy'], w4)
    pdf.ln(3)

    pdf.sub_title('API Endpoints')
    w5 = [35, 20, 85]
    pdf.table_row(['Endpoint', 'Method', 'Returns'], w5, header=True)
    pdf.table_row(['/api/predict', 'POST', 'Both model predictions + spectral overlay'], w5)
    pdf.table_row(['/api/sample', 'GET', 'Random EuroSAT sample image'], w5)
    pdf.table_row(['/api/metrics', 'GET', 'Training benchmark data (accuracy, F1, etc.)'], w5)
    pdf.table_row(['/api/colors', 'GET', 'Color palette for all 10 land cover classes'], w5)
    pdf.ln(3)

    pdf.sub_title('Code Example')
    pdf.code_block(
        '@app.post("/api/predict")\n'
        'async def predict(file: UploadFile):\n'
        '    image = Image.open(io.BytesIO(await file.read()))\n'
        '    resnet_result = classify(resnet_model, image)\n'
        '    bdh_result = classify(bdh_model, image)\n'
        '    return {"resnet": resnet_result, "baby_dragon": bdh_result}'
    )

    # ════════════════════════════════════
    # 5. UVICORN
    # ════════════════════════════════════
    pdf.section_title('5. Uvicorn')
    pdf.body_text(
        'Uvicorn is an ASGI (Asynchronous Server Gateway Interface) web server for Python. '
        'It runs FastAPI applications and handles HTTP requests efficiently using async I/O.'
    )
    pdf.bullet('Recommended by FastAPI as the default server')
    pdf.bullet('Async I/O - handles concurrent requests efficiently')
    pdf.bullet('Hot reload - auto-restarts on code changes during development')
    pdf.bullet('Production-ready - can be paired with Gunicorn for multi-worker deployment')
    pdf.ln(2)
    pdf.code_block('uvicorn app:app --host 0.0.0.0 --port 8000')

    # ════════════════════════════════════
    # 6. OPENCV
    # ════════════════════════════════════
    pdf.add_page()
    pdf.section_title('6. OpenCV (cv2)')

    pdf.body_text(
        'OpenCV (Open Source Computer Vision Library) is the world\'s most used computer vision '
        'library with 2,500+ algorithms for image processing, object detection, and video analysis.'
    )

    pdf.sub_title('How We Use It')
    pdf.sub_sub_title('Spectral Segmentation')
    pdf.code_block(
        'hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)  # Color space\n'
        'lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)   # For urban detection'
    )

    pdf.sub_sub_title('Contour Detection')
    pdf.code_block(
        'contours, _ = cv2.findContours(mask,\n'
        '    cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)\n'
        'cv2.drawContours(overlay, contours, -1, color, 2)'
    )

    pdf.sub_sub_title('Morphological Operations')
    pdf.code_block(
        'kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))\n'
        'mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)  # Fill\n'
        'mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)   # Clean'
    )

    pdf.sub_sub_title('Key Functions Used')
    w6 = [45, 95]
    pdf.table_row(['Function', 'Purpose'], w6, header=True)
    pdf.table_row(['cvtColor', 'Convert RGB to HSV/LAB for spectral analysis'], w6)
    pdf.table_row(['findContours', 'Detect land cover region boundaries'], w6)
    pdf.table_row(['drawContours', 'Draw colored borders on overlay'], w6)
    pdf.table_row(['morphologyEx', 'Clean masks (close gaps, remove noise)'], w6)
    pdf.table_row(['countNonZero', 'Count pixels in a mask for area %'], w6)
    pdf.table_row(['moments', 'Calculate centroid for label placement'], w6)

    # ════════════════════════════════════
    # 7. PILLOW
    # ════════════════════════════════════
    pdf.add_page()
    pdf.section_title('7. Pillow (PIL)')

    pdf.body_text(
        'Pillow is the Python Imaging Library - the standard for opening, manipulating, and '
        'saving image files in Python.'
    )

    pdf.sub_title('How We Use It')
    pdf.code_block(
        '# Open uploaded image\n'
        'image = Image.open(io.BytesIO(file_bytes))\n\n'
        '# Draw text labels on overlay\n'
        'draw = ImageDraw.Draw(result)\n'
        'draw.text((x, y), "Forest 95.8%", fill=(34,220,77))\n\n'
        '# Encode to base64 for API response\n'
        'buffer = io.BytesIO()\n'
        'image.save(buffer, format="JPEG", quality=92)\n'
        'b64 = base64.b64encode(buffer.read()).decode("utf-8")'
    )

    w7 = [40, 100]
    pdf.table_row(['Function', 'Purpose'], w7, header=True)
    pdf.table_row(['Image.open()', 'Load uploaded satellite image'], w7)
    pdf.table_row(['image.resize()', 'Scale to display size (400x400)'], w7)
    pdf.table_row(['ImageDraw', 'Draw class labels and badges on overlay'], w7)
    pdf.table_row(['ImageFont', 'Load system fonts for text rendering'], w7)
    pdf.table_row(['image.save()', 'Encode result as JPEG for API response'], w7)

    # ════════════════════════════════════
    # 8. NUMPY
    # ════════════════════════════════════
    pdf.section_title('8. NumPy')

    pdf.body_text(
        'NumPy is the fundamental package for numerical computing in Python. It provides '
        'N-dimensional arrays and mathematical operations that are 50-100x faster than '
        'pure Python loops.'
    )

    pdf.sub_title('How We Use It')
    pdf.code_block(
        '# Convert PIL image to array\n'
        'img = np.array(image, dtype=np.uint8)\n\n'
        '# Compute Green Leaf Index (vegetation)\n'
        'r, g, b = img[:,:,0], img[:,:,1], img[:,:,2]\n'
        'gli = (2*g - r - b) / (2*g + r + b + 1)\n\n'
        '# Boolean mask for vegetation pixels\n'
        'veg_mask = (gli > 0.05) & (s > 40) & (h >= 25) & (h <= 90)'
    )
    pdf.body_text(
        'NumPy enables vectorized pixel operations - processing all 160,000 pixels (400x400) '
        'simultaneously instead of looping through each one.'
    )

    # ════════════════════════════════════
    # 9. FRONTEND
    # ════════════════════════════════════
    pdf.add_page()
    pdf.section_title('9. HTML5 + CSS3 + JavaScript')

    pdf.sub_title('Why Vanilla (No React/Vue)?')
    w8 = [40, 100]
    pdf.table_row(['Reason', 'Detail'], w8, header=True)
    pdf.table_row(['Simplicity', 'No build tools, no npm, no bundling. Just 3 files.'], w8)
    pdf.table_row(['Speed', 'Zero framework overhead. Instant page load.'], w8)
    pdf.table_row(['Portability', 'Works in any browser. No Node.js dependency.'], w8)
    pdf.table_row(['Integration', 'Served directly by FastAPI as static files.'], w8)
    pdf.ln(3)

    pdf.sub_title('HTML5 (index.html)')
    pdf.bullet('Semantic structure: <header>, <main>, <section>')
    pdf.bullet('Tab-based navigation: ResNet / BDH / Comparison')
    pdf.bullet('Image upload via <input type="file"> with drag-and-drop')
    pdf.bullet('SEO-optimized with meta tags and proper heading hierarchy')

    pdf.sub_title('CSS3 (style.css)')
    w9 = [45, 95]
    pdf.table_row(['Feature', 'Purpose'], w9, header=True)
    pdf.table_row(['Custom Properties', 'Design tokens (colors, spacing, fonts)'], w9)
    pdf.table_row(['Flexbox & Grid', 'Responsive layout for cards and tabs'], w9)
    pdf.table_row(['Glassmorphism', 'backdrop-filter: blur() for premium look'], w9)
    pdf.table_row(['CSS Animations', 'Background orbs, hover effects, loading states'], w9)
    pdf.table_row(['Dark mode', 'Full dark-mode palette with high-contrast colors'], w9)
    pdf.table_row(['Media queries', 'Responsive on mobile, tablet, desktop'], w9)
    pdf.ln(3)

    pdf.sub_title('JavaScript (app.js)')
    w10 = [45, 95]
    pdf.table_row(['Feature', 'What it does'], w10, header=True)
    pdf.table_row(['fetch() API', 'Calls FastAPI endpoints (/predict, /sample)'], w10)
    pdf.table_row(['FormData', 'Uploads image file to server'], w10)
    pdf.table_row(['Dynamic DOM', 'Creates result cards and charts programmatically'], w10)
    pdf.table_row(['Tab switching', 'Shows/hides ResNet, BDH, Comparison panels'], w10)
    pdf.table_row(['Color-coded bars', 'Probability distribution charts'], w10)
    pdf.table_row(['Base64 rendering', 'Displays spectral overlay images'], w10)

    # ════════════════════════════════════
    # SUMMARY TABLE
    # ════════════════════════════════════
    pdf.add_page()
    pdf.section_title('10. Summary')

    w11 = [30, 20, 45, 45]
    pdf.table_row(['Technology', 'Version', 'Role', 'Why Chosen'], w11, header=True)
    pdf.table_row(['Python', '3.9', 'Core language', 'ML ecosystem, readability'], w11)
    pdf.table_row(['PyTorch', '2.x', 'Deep learning', 'Dynamic graphs, MPS support'], w11)
    pdf.table_row(['torchvision', '0.x', 'Models + transforms', 'Pretrained ResNet, data load'], w11)
    pdf.table_row(['FastAPI', '0.100+', 'Web backend', 'Fast, async, auto-docs'], w11)
    pdf.table_row(['Uvicorn', '0.x', 'ASGI server', 'Async I/O, hot reload'], w11)
    pdf.table_row(['OpenCV', '4.x', 'Computer vision', 'Spectral segmentation'], w11)
    pdf.table_row(['Pillow', '10.x', 'Image I/O', 'Load, draw, encode images'], w11)
    pdf.table_row(['NumPy', '1.x', 'Numerical compute', 'Vectorized pixel ops'], w11)
    pdf.table_row(['HTML/CSS/JS', '5/3/ES6', 'Frontend', 'No deps, instant load'], w11)
    pdf.table_row(['fpdf2', '2.x', 'PDF generation', 'Report and docs'], w11)

    # Save
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'docs'/SpaceX_TechStack.pdf'
    pdf.output(path)
    print(f'PDF saved to: {path}')


if __name__ == '__main__':
    generate()
