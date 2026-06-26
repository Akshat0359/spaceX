#!/usr/bin/env python3
"""Generate Data Flow Diagram PDF for SensiSpace project."""
from fpdf import FPDF

class DFDPDF(FPDF):
    def header(self):
        if self.page_no()==1: return
        self.set_font('Helvetica','I',8); self.set_text_color(100,100,100)
        self.cell(0,6,'SensiSpace - Data Flow Diagrams',align='R'); self.ln(3)
        self.set_draw_color(80,60,180); self.set_line_width(0.4)
        self.line(10,self.get_y(),200,self.get_y()); self.ln(4)
    def footer(self):
        self.set_y(-15); self.set_font('Helvetica','I',8); self.set_text_color(150,150,150)
        self.cell(0,10,f'Page {self.page_no()}/{{nb}}',align='C')
    def stitle(self,t):
        self.set_font('Helvetica','B',15); self.set_text_color(80,60,180); self.ln(5)
        self.cell(0,9,t,new_x="LMARGIN",new_y="NEXT")
        self.set_draw_color(80,60,180); self.set_line_width(0.3)
        self.line(10,self.get_y(),200,self.get_y()); self.ln(4)
    def sub(self,t):
        self.set_font('Helvetica','B',12); self.set_text_color(50,50,50); self.ln(3)
        self.cell(0,7,t,new_x="LMARGIN",new_y="NEXT"); self.ln(2)
    def sub2(self,t):
        self.set_font('Helvetica','B',10); self.set_text_color(80,80,80); self.ln(2)
        self.cell(0,6,t,new_x="LMARGIN",new_y="NEXT"); self.ln(1)
    def body(self,t):
        self.set_font('Helvetica','',10); self.set_text_color(30,30,30)
        self.multi_cell(0,5.5,t); self.ln(2)
    def bul(self,t,ind=8):
        self.set_font('Helvetica','',10); self.set_text_color(30,30,30)
        self.set_x(self.l_margin+ind); self.multi_cell(self.w-self.l_margin-self.r_margin-ind,5.5,'- '+t); self.ln(0.5)
    def bbul(self,b,n,ind=8):
        self.set_x(self.l_margin+ind); self.set_font('Helvetica','',10); self.set_text_color(30,30,30)
        self.write(5.5,'- '); self.set_font('Helvetica','B',10); self.write(5.5,b)
        self.set_font('Helvetica','',10); self.write(5.5,n); self.ln(7)
    def code(self,t):
        self.set_font('Courier','',8); self.set_fill_color(235,235,240); self.set_text_color(30,30,30)
        self.multi_cell(0,4.5,t,fill=True); self.ln(2)
    def trow(self,cols,widths,hdr=False):
        h=6
        if hdr:
            self.set_font('Helvetica','B',8); self.set_fill_color(80,60,180); self.set_text_color(255,255,255)
        else:
            self.set_font('Helvetica','',8); self.set_fill_color(248,248,252); self.set_text_color(30,30,30)
        for i,(c,w) in enumerate(zip(cols,widths)):
            self.cell(w,h,str(c),border=1,fill=True,align='C' if i>0 else 'L')
        self.ln()
    def flow_box(self,x,y,w,h,text,fill_r=80,fill_g=60,fill_b=180,text_color=(255,255,255)):
        self.set_fill_color(fill_r,fill_g,fill_b); self.set_draw_color(60,40,140)
        self.rect(x,y,w,h,'DF'); self.set_text_color(*text_color)
        self.set_font('Helvetica','B',7); self.set_xy(x+1,y+h/2-2)
        self.cell(w-2,4,text,align='C')
    def flow_arrow(self,x1,y1,x2,y2):
        self.set_draw_color(80,60,180); self.set_line_width(0.5)
        self.line(x1,y1,x2,y2)
        # arrowhead
        import math
        a=math.atan2(y2-y1,x2-x1); sz=2
        self.line(x2,y2,x2-sz*math.cos(a-0.4),y2-sz*math.sin(a-0.4))
        self.line(x2,y2,x2-sz*math.cos(a+0.4),y2-sz*math.sin(a+0.4))

def generate():
    pdf=DFDPDF(); pdf.alias_nb_pages(); pdf.set_auto_page_break(auto=True,margin=18)

    # TITLE PAGE
    pdf.add_page(); pdf.ln(40)
    pdf.set_font('Helvetica','B',28); pdf.set_text_color(80,60,180)
    pdf.cell(0,15,'SensiSpace',align='C',new_x="LMARGIN",new_y="NEXT")
    pdf.set_font('Helvetica','',16); pdf.set_text_color(60,60,60)
    pdf.cell(0,10,'Data Flow Diagrams',align='C',new_x="LMARGIN",new_y="NEXT")
    pdf.ln(8); pdf.set_draw_color(80,60,180); pdf.set_line_width(1)
    pdf.line(60,pdf.get_y(),150,pdf.get_y()); pdf.ln(8)
    pdf.set_font('Helvetica','',11); pdf.set_text_color(100,100,100)
    pdf.cell(0,7,'Satellite Land Cover Classification System',align='C',new_x="LMARGIN",new_y="NEXT")
    pdf.cell(0,7,'Baby Dragon Hatchling (BDH) vs ResNet-18',align='C',new_x="LMARGIN",new_y="NEXT")
    pdf.ln(12); pdf.set_font('Helvetica','I',11)
    pdf.cell(0,7,'BDH Architecture | ResNet-18 Pipeline | Training & Inference Flows',align='C',new_x="LMARGIN",new_y="NEXT")

    # ══ LEVEL 0 ══
    pdf.add_page(); pdf.stitle('1. Level 0 - Context Diagram')
    pdf.body('The highest-level view showing SensiSpace as a single process boundary interacting with external entities - the User and the EuroSAT satellite dataset.')
    # Draw context diagram
    pdf.flow_box(15,65,40,15,'User',50,120,50)
    pdf.flow_box(80,55,50,15,'SensiSpace\nSystem',80,60,180)
    pdf.flow_box(80,80,50,15,'EuroSAT Dataset',40,40,120)
    pdf.flow_box(155,65,40,15,'Results',50,120,50)
    pdf.flow_arrow(55,72,80,62); pdf.flow_arrow(130,62,155,72)
    pdf.flow_arrow(105,80,105,70)
    pdf.ln(50)
    pdf.sub2('External Entities')
    pdf.bbul('User: ','Uploads satellite images via web UI for land cover classification.')
    pdf.bbul('EuroSAT Dataset: ','27,000 Sentinel-2 satellite images across 10 land cover classes.')
    pdf.sub2('System Outputs')
    pdf.bbul('Classification Results: ','BDH + ResNet predictions, confidence scores, spectral overlays, comparison metrics.')

    # ══ LEVEL 1 ══
    pdf.add_page(); pdf.stitle('2. Level 1 - System Data Flow Diagram')
    pdf.body('Decomposition of the SensiSpace system into four major subsystems: Training Pipeline, Inference Engine, Spectral Segmentation, and Frontend Visualization.')
    pdf.sub2('Subsystems')
    w=[10,40,80]
    pdf.trow(['#','Subsystem','Description'],w,hdr=True)
    pdf.trow(['1.0','Training Pipeline','Loads EuroSAT, augments data, trains BDH & ResNet, saves weights + metrics'],w)
    pdf.trow(['2.0','Inference & Prediction','Accepts uploaded image, runs dual-model forward pass, assembles results'],w)
    pdf.trow(['3.0','Spectral Segmentation','HSV/LAB pixel analysis to generate land cover overlay visualization'],w)
    pdf.trow(['4.0','Frontend Visualization','Renders results in tabbed UI with charts, comparison, and overlays'],w)
    pdf.ln(3)
    pdf.sub2('Data Stores')
    w2=[10,45,75]
    pdf.trow(['ID','Store','Contents'],w2,hdr=True)
    pdf.trow(['D1','saved_models/','resnet.pth, baby_dragon.pth (trained model weights)'],w2)
    pdf.trow(['D2','classes.json','List of 10 EuroSAT class names'],w2)
    pdf.trow(['D3','metrics.json','Accuracy, precision, recall, F1, inference time, params per model'],w2)
    pdf.trow(['D4','colors.json','RGB color map for each land cover class'],w2)
    pdf.ln(3)
    pdf.sub2('Data Flows Between Subsystems')
    pdf.bul('EuroSAT Dataset --> [1.0 Training] --> D1 (weights), D2 (classes), D3 (metrics), D4 (colors)')
    pdf.bul('User Image --> [2.0 Inference] --> loads from D1, D2, D4')
    pdf.bul('[2.0 Inference] --> predicted class + probabilities --> [3.0 Spectral Segmentation]')
    pdf.bul('[3.0 Spectral] --> base64 overlay image --> [2.0 Inference] --> JSON response')
    pdf.bul('JSON response --> [4.0 Frontend] --> rendered UI to User')
    pdf.bul('D3 (metrics) --> [4.0 Frontend] --> benchmark comparison table')

    # ══ BDH DFD ══
    pdf.add_page(); pdf.stitle('3. BDH Architecture - Data Flow Diagram')
    pdf.body('The Baby Dragon Hatchling (BDH) is a novel biologically-inspired architecture with four key innovations: Multi-Scale Feature Pyramids, Lateral Inhibition, Contextual Attention, and Recurrent Refinement.')
    pdf.sub2('3.1 End-to-End Pipeline')
    pdf.code(
        'Input Image (3x64x64)\n'
        '    |\n'
        '    v\n'
        '[STEM] Conv2d 3->32 + BN + ReLU -> Conv2d 32->64 + BN + ReLU\n'
        '    |\n'
        '    v\n'
        '[BDH STAGE 1] MultiScale(64) -> LateralInhibition(64) -> ContextualAttention(64) + Residual\n'
        '    | MaxPool2d (64ch, 32x32)\n'
        '    v\n'
        '[BDH STAGE 2] MultiScale(128) -> LateralInhibition(128) -> ContextualAttention(128) + Residual\n'
        '    | MaxPool2d (128ch, 16x16)         <-- Grad-CAM target layer\n'
        '    v\n'
        '[BDH STAGE 3] MultiScale(256) -> LateralInhibition(256) -> ContextualAttention(256) + Residual\n'
        '    | MaxPool2d (256ch, 8x8)\n'
        '    v\n'
        '[RECURRENT REFINEMENT] x2 iterations: Conv->BN->ReLU -> Gate(sigmoid) -> Gated Mix\n'
        '    |\n'
        '    v\n'
        '[CLASSIFIER] GlobalAvgPool -> Dropout(0.3) -> FC(256->128) -> ReLU -> Dropout(0.2) -> FC(128->10)\n'
        '    |\n'
        '    v\n'
        'Output: 10 Class Logits -> Softmax -> Predicted Land Cover'
    )

    pdf.sub2('3.2 Multi-Scale Feature Pyramid Block')
    pdf.body('Processes input through three parallel convolution branches with different kernel sizes to capture features at multiple spatial scales - essential for satellite imagery where objects vary dramatically in size.')
    pdf.code(
        'Input Feature Map\n'
        '    |------------|------------|  (parallel branches)\n'
        '    v            v            v\n'
        ' [3x3 Conv]  [5x5 Conv]  [7x7 Conv]\n'
        ' [BatchNorm] [BatchNorm] [BatchNorm]\n'
        ' [ReLU]      [ReLU]      [ReLU]\n'
        '    |            |            |\n'
        '    v            v            v\n'
        '    |--- Concatenate (channel dim) ---|\n'
        '                 |\n'
        '                 v\n'
        '         Multi-Scale Output'
    )

    pdf.sub2('3.3 Lateral Inhibition Block')
    pdf.body('Biologically inspired by neural circuits where neighboring neurons suppress each other. Uses depthwise convolution as surround suppression with a learnable inhibition strength alpha.')
    pdf.code(
        'Input x\n'
        '    |-----------|  (two paths)\n'
        '    |           v\n'
        '    |    [Depthwise Conv 3x3] (surround estimation)\n'
        '    |    [BatchNorm]\n'
        '    |           |\n'
        '    v           v\n'
        '  x    -   alpha * surround(x)   =   inhibited\n'
        '                                        |\n'
        '                                     [ReLU]\n'
        '                                        |\n'
        '                                        v\n'
        '                                 Sharpened Features'
    )

    pdf.add_page()
    pdf.sub2('3.4 Contextual Attention Module')
    pdf.body('Dual attention mechanism combining channel attention (Squeeze-and-Excitation style) and spatial attention to model long-range contextual relationships in geospatial imagery.')
    pdf.code(
        'Input Features\n'
        '    |\n'
        '    v\n'
        '[CHANNEL ATTENTION]\n'
        '  GlobalAvgPool -> FC(C -> C/8) -> ReLU -> FC(C/8 -> C) -> Sigmoid\n'
        '    --> Multiply channel weights with features\n'
        '    |\n'
        '    v\n'
        '[SPATIAL ATTENTION]\n'
        '  AvgPool(channel) + MaxPool(channel) -> Concat -> Conv2d(7x7) -> Sigmoid\n'
        '    --> Multiply spatial weights with features\n'
        '    |\n'
        '    v\n'
        'Attention-Weighted Features'
    )

    pdf.sub2('3.5 Recurrent Refinement Module')
    pdf.body('A lightweight recurrent loop (2 iterations) that mimics the brain\'s top-down feedback pathways. Uses gated residual mixing to iteratively refine feature representations.')
    pdf.code(
        'Input x (from Stage 3)\n'
        '    |  FOR i = 1 to 2:\n'
        '    |      refined = Conv2d(256->256) + BN + ReLU\n'
        '    |      gate    = Sigmoid(Conv2d 1x1)\n'
        '    |      x       = x * gate + refined * (1 - gate)\n'
        '    |  END FOR\n'
        '    v\n'
        'Refined Features (256ch, 8x8)'
    )

    # ══ RESNET DFD ══
    pdf.add_page(); pdf.stitle('4. ResNet-18 Architecture - Data Flow Diagram')
    pdf.body('Standard ResNet-18 with ImageNet pre-trained weights. The convolutional backbone is frozen (transfer learning); only the final fully connected layer is fine-tuned for 10 EuroSAT classes.')
    pdf.sub2('4.1 End-to-End Pipeline')
    pdf.code(
        'Input Image (3x64x64)\n'
        '    |\n'
        '    v\n'
        '[FROZEN BACKBONE - ImageNet Pre-trained]\n'
        '  Conv2d(3->64, 7x7, stride=2) + BN + ReLU + MaxPool\n'
        '    |\n'
        '    v\n'
        '  Layer 1: 2x BasicBlock (64 channels)\n'
        '    |\n'
        '    v\n'
        '  Layer 2: 2x BasicBlock (128 channels)\n'
        '    |\n'
        '    v\n'
        '  Layer 3: 2x BasicBlock (256 channels)    <-- Grad-CAM target layer\n'
        '    |\n'
        '    v\n'
        '  Layer 4: 2x BasicBlock (512 channels)\n'
        '    |\n'
        '    v\n'
        '  AdaptiveAvgPool2d -> Flatten (512)\n'
        '    |\n'
        '    v\n'
        '[TRAINABLE] Linear(512 -> 10)\n'
        '    |\n'
        '    v\n'
        'Output: 10 Class Logits -> Softmax -> Predicted Land Cover'
    )
    pdf.sub2('4.2 BasicBlock Internal Flow')
    pdf.code(
        'Input x\n'
        '    |-----------|  (residual skip)\n'
        '    v            |\n'
        ' [3x3 Conv+BN]  |\n'
        ' [ReLU]         |\n'
        ' [3x3 Conv+BN]  |\n'
        '    |            |\n'
        '    v            v\n'
        '    +--- ADD ----+\n'
        '         |\n'
        '      [ReLU]\n'
        '         |\n'
        '         v\n'
        '      Output'
    )
    pdf.sub2('4.3 Transfer Learning Strategy')
    pdf.bul('All convolutional parameters are FROZEN (requires_grad=False)')
    pdf.bul('Only the final FC layer (512 -> 10) is trainable')
    pdf.bul('Leverages ImageNet features for general visual recognition')
    pdf.bul('Represents industry-standard baseline approach')

    # ══ TRAINING DFD ══
    pdf.add_page(); pdf.stitle('5. Training Pipeline - Data Flow Diagram')
    pdf.body('End-to-end training data flow from raw EuroSAT dataset to saved model weights and evaluation metrics.')
    pdf.sub2('5.1 Data Preparation Flow')
    pdf.code(
        'EuroSAT Dataset (27,000 images, 10 classes)\n'
        '    |\n'
        '    v\n'
        '[torchvision.datasets.EuroSAT] download=True\n'
        '    |\n'
        '    v\n'
        '[random_split] 80% Train (21,600) / 20% Test (5,400)\n'
        '    |                          |\n'
        '    v                          v\n'
        '[Train Augmentation]     [Test Transform]\n'
        '  Resize 64x64            Resize 64x64\n'
        '  RandomHFlip             ToTensor\n'
        '  RandomVFlip             Normalize\n'
        '  RandomRotation(15)\n'
        '  ColorJitter\n'
        '  ToTensor\n'
        '  Normalize\n'
        '    |                          |\n'
        '    v                          v\n'
        '[DataLoader batch=32]    [DataLoader batch=32]'
    )
    pdf.sub2('5.2 Training Loop Flow')
    pdf.code(
        'FOR model IN [ResNet-18, BDH]:\n'
        '  Initialize model (pretrained or from scratch)\n'
        '  optimizer = Adam(lr=1e-3)\n'
        '  scheduler = CosineAnnealingLR(T_max=10)\n'
        '  criterion = CrossEntropyLoss\n'
        '    |\n'
        '  FOR epoch = 1 to 10:\n'
        '    FOR batch IN train_loader:\n'
        '      images, labels --> model --> outputs\n'
        '      loss = criterion(outputs, labels)\n'
        '      loss.backward() --> optimizer.step()\n'
        '    END\n'
        '    scheduler.step()\n'
        '  END\n'
        '    |\n'
        '    v\n'
        '  [Evaluate on test_loader]\n'
        '    accuracy, precision, recall, F1, inference_time\n'
        '    |\n'
        '    v\n'
        '  [Save] model.pth, classes.json, metrics.json, colors.json'
    )

    # ══ INFERENCE DFD ══
    pdf.add_page(); pdf.stitle('6. Inference & Prediction - Data Flow Diagram')
    pdf.body('Real-time prediction data flow when a user uploads a satellite image through the web interface.')
    pdf.sub2('6.1 Request Flow')
    pdf.code(
        'User uploads image via browser\n'
        '    |\n'
        '    v\n'
        '[Frontend] FileReader -> preview -> POST /api/predict (FormData)\n'
        '    |\n'
        '    v\n'
        '[FastAPI] Read UploadFile bytes\n'
        '    |\n'
        '    v\n'
        '[PIL] Image.open().convert("RGB")\n'
        '    |\n'
        '    v\n'
        '[Transform] Resize(64x64) -> ToTensor -> Normalize -> unsqueeze(0)\n'
        '    |\n'
        '    |--- Tensor cloned for each model ---|\n'
        '    v                                     v\n'
        '[ResNet-18 Forward Pass]          [BDH Forward Pass]\n'
        '  torch.no_grad()                   torch.no_grad()\n'
        '  output -> softmax -> probs        output -> softmax -> probs\n'
        '  argmax -> predicted class         argmax -> predicted class\n'
        '  measure inference time            measure inference time\n'
        '    |                                     |\n'
        '    v                                     v\n'
        '[Spectral Segmentation]          [Spectral Segmentation]\n'
        '  generate_cam_image()              generate_cam_image()\n'
        '  -> base64 overlay                 -> base64 overlay\n'
        '    |                                     |\n'
        '    v                                     v\n'
        '    |-------- Assemble JSON Response -----|\n'
        '    |\n'
        '    v\n'
        '{ "resnet": {prediction, confidence, all_probs, cam_image, ...},\n'
        '  "baby_dragon": {prediction, confidence, all_probs, cam_image, ...} }\n'
        '    |\n'
        '    v\n'
        '[Frontend] renderResults() -> Tabs + Charts + Comparison'
    )

    # ══ SPECTRAL DFD ══
    pdf.add_page(); pdf.stitle('7. Spectral Segmentation - Data Flow Diagram')
    pdf.body('Pixel-accurate land cover visualization using HSV/LAB color-space analysis instead of Grad-CAM. Produces precise boundaries by analyzing actual pixel colors.')
    pdf.sub2('7.1 Segmentation Pipeline')
    pdf.code(
        'Original PIL Image + Model Class Probabilities\n'
        '    |\n'
        '    v\n'
        '[Resize to 400x400] -> RGB numpy array\n'
        '    |\n'
        '    |--- cv2.cvtColor ---|--- cv2.cvtColor ---|\n'
        '    v                    v                     v\n'
        '  [RGB Channels]    [HSV: H,S,V]         [LAB: L,A,B]\n'
        '    R, G, B\n'
        '    |\n'
        '    v\n'
        '[Vegetation Indices]\n'
        '  GLI = (2G - R - B) / (2G + R + B + 1)\n'
        '  ExG = 2G - R - B\n'
        '    |\n'
        '    v\n'
        '[Generate 6 Spectral Masks]\n'
        '  Dense Vegetation:  GLI>0.05, S>40, green hue\n'
        '  Light Vegetation:  near-zero GLI, moderate sat\n'
        '  Water:             blue hue OR dark+blue tint\n'
        '  Urban:             low sat, warm tones\n'
        '  Road:              very low sat, neutral LAB\n'
        '  Bare Soil:         brownish, warm hue\n'
        '    |\n'
        '    v\n'
        '[Morphological Cleanup]\n'
        '  Close (5x5 ellipse) + Open (3x3 ellipse)\n'
        '    |\n'
        '    v\n'
        '[Overlap Resolution] Priority: Water > Vegetation > Urban > Road > Soil\n'
        '    |\n'
        '    v\n'
        '[Map Spectral -> EuroSAT Classes]\n'
        '  dense_veg -> Forest, HerbaceousVegetation, Pasture\n'
        '  water     -> River, SeaLake\n'
        '  urban     -> Residential, Industrial\n'
        '  Pick candidate with highest model probability\n'
        '    |\n'
        '    v\n'
        '[Overlay Rendering]\n'
        '  Color fill per region (alpha = prob * 0.4)\n'
        '  Draw contours (cv2.findContours)\n'
        '  Add text labels: class_name + confidence%\n'
        '    |\n'
        '    v\n'
        'Base64 JPEG encoded overlay image'
    )

    # ══ COMPARISON TABLE ══
    pdf.add_page(); pdf.stitle('8. BDH vs ResNet-18 - Data Flow Comparison')
    w3=[45,47,47]
    pdf.trow(['Aspect','BDH (Baby Dragon Hatchling)','ResNet-18'],w3,hdr=True)
    pdf.trow(['Input Shape','3 x 64 x 64','3 x 64 x 64'],w3)
    pdf.trow(['Feature Extraction','Multi-Scale Pyramid (3x3+5x5+7x7)','Sequential BasicBlocks (3x3+3x3)'],w3)
    pdf.trow(['Contrast Enhancement','Lateral Inhibition (surround suppression)','None'],w3)
    pdf.trow(['Attention','Dual Channel + Spatial Attention','None'],w3)
    pdf.trow(['Feedback Processing','Recurrent Refinement (2 gated iters)','None (pure feedforward)'],w3)
    pdf.trow(['Pretrained Weights','Trained from scratch','ImageNet pretrained (frozen)'],w3)
    pdf.trow(['Trainable Layers','All layers','Only final FC layer'],w3)
    pdf.trow(['Classifier','256->128->10 (with dropout)','512->10 (single linear)'],w3)
    pdf.trow(['Grad-CAM Target','stage2 (16x16 activations)','layer3 (8x8 activations)'],w3)
    pdf.trow(['Output','10-class logits -> Softmax','10-class logits -> Softmax'],w3)
    pdf.ln(5)

    pdf.sub2('Key Architectural Differences')
    pdf.bbul('Multi-Scale vs Sequential: ','BDH captures features at 3 scales simultaneously; ResNet processes sequentially with fixed 3x3 kernels.')
    pdf.bbul('Biological Inspiration: ','BDH uses lateral inhibition (neural suppression) and recurrent refinement (feedback loops) not found in ResNet.')
    pdf.bbul('Attention Mechanisms: ','BDH applies dual channel+spatial attention at every stage; ResNet has no attention.')
    pdf.bbul('Transfer vs Novel: ','ResNet leverages ImageNet knowledge; BDH learns satellite-specific features from scratch.')
    pdf.bbul('Parameter Efficiency: ','BDH has fewer parameters but compensates with architectural innovations.')

    out='/Users/yashlohia/Major project/SensiSpace_DFD.pdf'
    pdf.output(out)
    print(f'DFD PDF saved to: {out}')

if __name__=='__main__':
    generate()
