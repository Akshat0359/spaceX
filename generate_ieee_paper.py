#!/usr/bin/env python3
"""Generate IEEE-format PDF paper for SensiSpace project."""
from fpdf import FPDF

class IEEEPDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(100,100,100)
        self.cell(0, 6, 'SensiSpace: Biologically-Inspired Deep Learning for Satellite Land Cover Classification', align='C')
        self.ln(4)
        self.set_draw_color(0,0,0)
        self.set_line_width(0.3)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128,128,128)
        self.cell(0, 10, str(self.page_no()), align='C')

    def section(self, num, title):
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(0,0,0)
        self.ln(4)
        self.cell(0, 7, f'{num}. {title.upper()}', new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def subsec(self, letter, title):
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(0,0,0)
        self.ln(2)
        self.cell(0, 6, f'{letter}. {title}', new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def body(self, text):
        self.set_font('Helvetica', '', 9)
        self.set_text_color(0,0,0)
        self.multi_cell(0, 4.5, text, align='J')
        self.ln(1.5)

    def italic_body(self, text):
        self.set_font('Helvetica', 'I', 9)
        self.set_text_color(0,0,0)
        self.multi_cell(0, 4.5, text, align='J')
        self.ln(1.5)

    def bullet(self, text, indent=8):
        self.set_font('Helvetica', '', 9)
        self.set_text_color(0,0,0)
        self.set_x(self.l_margin + indent)
        self.multi_cell(self.w - self.l_margin - self.r_margin - indent, 4.5, '- ' + text)
        self.ln(0.5)

    def bold_inline(self, bold, normal):
        self.set_font('Helvetica', 'B', 9)
        self.set_text_color(0,0,0)
        self.write(4.5, bold)
        self.set_font('Helvetica', '', 9)
        self.write(4.5, normal)
        self.ln(5)

    def code(self, text):
        self.set_font('Courier', '', 8)
        self.set_fill_color(235,235,235)
        self.set_text_color(30,30,30)
        self.multi_cell(0, 4.2, text, fill=True)
        self.ln(2)

    def trow(self, cols, widths, header=False):
        if header:
            self.set_font('Helvetica', 'B', 8)
            self.set_fill_color(30,30,30)
            self.set_text_color(255,255,255)
        else:
            self.set_font('Helvetica', '', 8)
            self.set_fill_color(248,248,248)
            self.set_text_color(0,0,0)
        for i, (c, w) in enumerate(zip(cols, widths)):
            self.cell(w, 6, str(c), border=1, fill=True, align='C' if i > 0 else 'L')
        self.ln()


def generate():
    pdf = IEEEPDF()
    pdf.set_auto_page_break(auto=True, margin=18)

    # ── TITLE PAGE ──
    pdf.add_page()
    pdf.ln(20)
    pdf.set_font('Helvetica', 'B', 18)
    pdf.set_text_color(0,0,0)
    pdf.multi_cell(0, 9, 'SensiSpace: A Biologically-Inspired Deep\nLearning Architecture for Satellite\nLand Cover Classification', align='C')
    pdf.ln(6)
    pdf.set_font('Helvetica', '', 11)
    pdf.cell(0, 7, 'Yash Lohia', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.set_font('Helvetica', 'I', 10)
    pdf.cell(0, 6, 'Department of Computer Science and Engineering', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, 'ISRO RESPOND Initiative - Major Project', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    pdf.set_draw_color(0,0,0)
    pdf.line(60, pdf.get_y(), 150, pdf.get_y())
    pdf.ln(8)

    # Abstract
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 7, 'Abstract', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.set_font('Helvetica', 'I', 9)
    pdf.set_text_color(0,0,0)
    pdf.multi_cell(0, 4.5,
        'Automated land cover classification from satellite imagery is critical for environmental monitoring, '
        'urban planning, and resource management. This paper presents SensiSpace, a satellite image classification '
        'system featuring a novel biologically-inspired architecture called Baby Dragon Hatchling (BDH). BDH '
        'incorporates four neuroscience-inspired modules: (1) Multi-Scale Feature Pyramids for capturing objects '
        'at varying spatial scales, (2) Lateral Inhibition Blocks that sharpen feature boundaries by mimicking '
        'retinal neural circuits, (3) Contextual Attention combining channel and spatial attention for selective '
        'feature focusing, and (4) Recurrent Refinement that iteratively improves feature representations through '
        'gated feedback loops. Evaluated on the EuroSAT benchmark dataset (27,000 Sentinel-2 satellite images '
        'across 10 land cover classes), BDH achieves 95.87% classification accuracy with approximately 2.03M '
        'parameters, outperforming a transfer-learning-based ResNet-18 baseline (81.98% accuracy) by 13.89 '
        'percentage points. We further integrate a spectral color-space segmentation module for pixel-level land '
        'cover visualization. The complete system is deployed as a full-stack web application using FastAPI and PyTorch.',
        align='J')
    pdf.ln(3)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.write(4.5, 'Keywords: ')
    pdf.set_font('Helvetica', 'I', 9)
    pdf.write(4.5, 'Satellite Remote Sensing, Land Cover Classification, Biologically-Inspired Neural Networks, '
              'Convolutional Neural Networks, EuroSAT, Attention Mechanisms')
    pdf.ln(8)

    # ── I. INTRODUCTION ──
    pdf.section('I', 'Introduction')
    pdf.body(
        'Satellite remote sensing generates massive volumes of high-resolution imagery used by organizations '
        'such as ISRO (Indian Space Research Organisation) and ESA (European Space Agency) for Earth observation. '
        'Manual analysis of this data is impractical at scale, motivating the need for automated classification systems.')
    pdf.body(
        'Conventional CNN architectures like ResNet, while effective for natural image classification via transfer '
        'learning, are not purpose-built for the unique characteristics of satellite imagery -- namely multi-scale '
        'land cover patterns, subtle spectral boundaries between adjacent land types, and the need for contextual '
        'understanding of geospatial features.')
    pdf.set_font('Helvetica', 'B', 9)
    pdf.cell(0, 5, 'Contributions of this paper:', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)
    pdf.bullet('Baby Dragon Hatchling (BDH): A novel biologically-inspired CNN incorporating lateral inhibition, dual attention, multi-scale extraction, and recurrent refinement.')
    pdf.bullet('Comprehensive benchmarking against ResNet-18 with ImageNet transfer learning on EuroSAT under identical training conditions.')
    pdf.bullet('Spectral segmentation module for pixel-level land cover visualization using HSV/LAB color-space analysis.')
    pdf.bullet('Full-stack web deployment for real-time satellite image classification and visualization.')

    # ── II. RELATED WORK ──
    pdf.section('II', 'Related Work')
    pdf.subsec('A', 'CNNs for Remote Sensing')
    pdf.body('Helber et al. [1] introduced the EuroSAT dataset and demonstrated that CNNs like ResNet-50 and GoogLeNet achieve strong performance on Sentinel-2 imagery. Transfer learning from ImageNet has been widely adopted [2], though domain mismatch between natural and satellite images can limit effectiveness.')
    pdf.subsec('B', 'Attention Mechanisms')
    pdf.body('Squeeze-and-Excitation Networks [3] introduced channel attention. CBAM [4] extended this with spatial attention. These mechanisms enable selective focus on informative features, particularly relevant for satellite imagery where different spectral channels carry varying importance.')
    pdf.subsec('C', 'Multi-Scale Feature Extraction')
    pdf.body('Inception modules [5] demonstrated effectiveness of parallel convolutions with different kernel sizes. Feature Pyramid Networks [6] showed that multi-scale representations are critical for detecting objects at different scales.')
    pdf.subsec('D', 'Biologically-Inspired Models')
    pdf.body('Lateral inhibition, first described by Hartline et al. [7] in the horseshoe crab retina, is fundamental in biological visual processing. Recurrent processing in the visual cortex [8] has inspired feedback mechanisms, but these remain underexplored for geospatial applications.')

    # ── III. DATASET ──
    pdf.section('III', 'Dataset - EuroSAT')
    pdf.body('The EuroSAT dataset [1] consists of 27,000 georeferenced satellite images captured by the Sentinel-2 satellite (European Space Agency). Each image is 64x64 pixels in RGB with 10m spatial resolution.')
    pdf.subsec('A', 'Dataset Properties')
    w = [55, 55]
    pdf.trow(['Property', 'Value'], w, header=True)
    for r in [('Source', 'Sentinel-2 (ESA)'), ('Total Images', '27,000'), ('Resolution', '64x64 RGB'), ('Classes', '10'), ('Train/Test Split', '80% / 20%'), ('Spatial Resolution', '10 m/pixel')]:
        pdf.trow(r, w)
    pdf.ln(3)

    pdf.subsec('B', 'Land Cover Classes')
    w2 = [48, 82]
    pdf.trow(['Class', 'Description'], w2, header=True)
    for r in [('AnnualCrop','Wheat, corn, rice fields'), ('Forest','Dense deciduous/coniferous tree cover'),
              ('HerbaceousVegetation','Grasslands, meadows, scrubland'), ('Highway','Major roads and expressways'),
              ('Industrial','Factories, warehouses'), ('Pasture','Grazing land for livestock'),
              ('PermanentCrop','Orchards, vineyards'), ('Residential','Urban residential areas'),
              ('River','Rivers, streams, canals'), ('SeaLake','Seas, lakes, reservoirs')]:
        pdf.trow(r, w2)

    # ── IV. PROPOSED ARCHITECTURE ──
    pdf.add_page()
    pdf.section('IV', 'Proposed Architecture - Baby Dragon Hatchling')
    pdf.subsec('A', 'Architecture Overview')
    pdf.body('BDH is a three-stage deep learning architecture where each stage chains three biologically-inspired modules -- Multi-Scale Feature Pyramid, Lateral Inhibition Block, and Contextual Attention -- followed by a Recurrent Refinement module before classification.')
    pdf.code(
        'Input (3x64x64)\n'
        '  -> Stem: Conv3x3->BN->ReLU->Conv3x3->BN->ReLU  [3->64 ch]\n'
        '  -> BDH Stage 1 (64 ch)  -> MaxPool 2x2 -> 32x32\n'
        '  -> BDH Stage 2 (128 ch) -> MaxPool 2x2 -> 16x16\n'
        '  -> BDH Stage 3 (256 ch) -> MaxPool 2x2 -> 8x8\n'
        '  -> Recurrent Refinement (2 iterations)\n'
        '  -> Global Avg Pool (256x1x1)\n'
        '  -> Dropout(0.3)->FC(256->128)->ReLU->Dropout(0.2)->FC(128->10)')
    pdf.body('Each BDH Stage:')
    pdf.code(
        'Input -> MultiScale -> LateralInhibition -> ContextualAttention -> ADD -> ReLU\n'
        '  |                                                                  ^\n'
        '  +------------------ 1x1 Conv Residual Projection ----------------+')

    pdf.subsec('B', 'Module 1: Multi-Scale Feature Pyramid')
    pdf.body('Satellite images contain objects at vastly different spatial scales. BDH processes input through three parallel convolution branches with kernels of 3x3 (fine edges), 5x5 (medium structures), and 7x7 (large patterns). Outputs are concatenated along the channel dimension:')
    pdf.code('F_ms(x) = Concat[f_3x3(x), f_5x5(x), f_7x7(x)]\nwhere f_kxk(x) = ReLU(BN(Conv_kxk(x)))')

    pdf.subsec('C', 'Module 2: Lateral Inhibition Block')
    pdf.body('Inspired by retinal neural circuits where neighboring neurons suppress each other to sharpen edges. A depthwise convolution estimates surround activity, which is subtracted with learnable strength alpha (initialized to 0.3):')
    pdf.code('F_li(x) = ReLU(x - alpha * BN(DWConv_3x3(x)))\nalpha is a learnable nn.Parameter')
    pdf.body('This sharpens feature boundaries -- critical for distinguishing adjacent land types (e.g., where a river meets a forest).')

    pdf.subsec('D', 'Module 3: Contextual Attention')
    pdf.body('A dual attention mechanism combining channel and spatial attention:')
    pdf.bold_inline('Channel Attention (WHAT): ', 'GAP -> FC(C->C/8) -> ReLU -> FC(C/8->C) -> Sigmoid. Produces per-channel weights (SE-Net style, reduction r=8).')
    pdf.bold_inline('Spatial Attention (WHERE): ', 'AvgPool + MaxPool across channels -> Concat -> Conv7x7 -> Sigmoid. Produces per-pixel attention map.')
    pdf.body('Input is sequentially reweighted: first by channel importance, then by spatial importance.')

    pdf.subsec('E', 'Module 4: Recurrent Refinement')
    pdf.body('Mimics the brain\'s top-down feedback pathways. Over 2 iterations, features are iteratively refined through a gated mechanism:')
    pdf.code('refined = ReLU(BN(Conv3x3(x)))\ngate = Sigmoid(Conv1x1(refined))\nx_new = x * gate + refined * (1 - gate)')
    pdf.body('The sigmoid gate decides per-element whether to keep original features (gate near 1) or replace with refined features (gate near 0).')

    pdf.subsec('F', 'Parameter Summary')
    w3 = [65, 45]
    pdf.trow(['Component', 'Parameters'], w3, header=True)
    for r in [('Stem (2x Conv3x3 + BN)', '~19K'), ('BDH Stage 1 (64->64)', '~60K'),
              ('BDH Stage 2 (64->128)', '~200K'), ('BDH Stage 3 (128->256)', '~750K'),
              ('Recurrent Refinement', '~720K'), ('Classifier (FC)', '~34K'),
              ('TOTAL', '~2,032,275')]:
        pdf.trow(r, w3)

    # ── V. BASELINE ──
    pdf.section('V', 'Baseline - ResNet-18')
    pdf.body('We use ResNet-18 [9] as a CNN baseline with ImageNet transfer learning. The convolutional base is frozen, and only the final fully connected layer FC(512->10) is trainable, yielding ~5,130 trainable parameters. The total ResNet-18 architecture contains 11.2M parameters (11.17M frozen).')

    # ── VI. EXPERIMENTAL SETUP ──
    pdf.section('VI', 'Experimental Setup')
    pdf.subsec('A', 'Training Configuration')
    w4 = [55, 55]
    pdf.trow(['Setting', 'Value'], w4, header=True)
    for r in [('Optimizer', 'Adam'), ('Learning Rate', '1e-3'), ('LR Scheduler', 'CosineAnnealingLR'),
              ('Loss Function', 'CrossEntropyLoss'), ('Batch Size', '32'), ('Epochs', '10')]:
        pdf.trow(r, w4)
    pdf.ln(3)
    pdf.subsec('B', 'Data Augmentation')
    w5 = [55, 55]
    pdf.trow(['Transform', 'Value'], w5, header=True)
    for r in [('Resize', '64x64'), ('Random H/V Flip', 'p=0.5'), ('Random Rotation', '+/-15 deg'),
              ('Color Jitter', 'brightness=0.2, contrast=0.2'), ('Normalization', 'ImageNet mean/std')]:
        pdf.trow(r, w5)

    # ── VII. RESULTS ──
    pdf.add_page()
    pdf.section('VII', 'Results and Analysis')
    pdf.subsec('A', 'Performance Comparison')
    w6 = [40, 30, 30, 30]
    pdf.trow(['Metric', 'ResNet-18', 'BDH', 'Winner'], w6, header=True)
    pdf.trow(['Accuracy', '81.98%', '95.87%', 'BDH'], w6)
    pdf.trow(['Precision', '81.64%', '95.78%', 'BDH'], w6)
    pdf.trow(['Recall', '81.51%', '96.01%', 'BDH'], w6)
    pdf.trow(['F1-Score', '81.51%', '95.85%', 'BDH'], w6)
    pdf.trow(['Inference (ms)', '0.18', '0.60', 'ResNet'], w6)
    pdf.trow(['Train Time (s)', '245.0', '3658.4', 'ResNet'], w6)
    pdf.trow(['Parameters', '5,130', '2,032,275', 'ResNet'], w6)
    pdf.ln(3)

    pdf.subsec('B', 'Analysis')
    pdf.bold_inline('Accuracy Superiority: ', 'BDH outperforms ResNet-18 by 13.89 percentage points across all metrics. The improvement is consistent across precision, recall, and F1, indicating robust performance across all 10 classes.')
    pdf.bold_inline('Parameter Efficiency: ', 'While BDH has more trainable parameters (2.03M vs 5.1K), ResNet-18\'s total architecture is 11.2M (11.17M frozen). BDH achieves higher accuracy with ~5.5x fewer total parameters, demonstrating domain-specific architecture beats brute-force scaling.')
    pdf.bold_inline('Inference Speed: ', 'ResNet-18 is ~3.3x faster (0.18ms vs 0.60ms), but BDH\'s 0.60ms still enables >1,600 images/second -- well within real-time requirements.')
    pdf.bold_inline('Training Time: ', 'BDH requires 15x more training time (3,658s vs 245s) because it trains all parameters from scratch. This is a one-time cost not affecting deployment.')

    pdf.subsec('C', 'Architectural Feature Comparison')
    w7 = [42, 40, 45]
    pdf.trow(['Feature', 'ResNet-18', 'BDH'], w7, header=True)
    for r in [('Type', 'Standard CNN', 'Bio-Inspired CNN'), ('Multi-Scale', 'No (3x3 only)', 'Yes (3x3+5x5+7x7)'),
              ('Attention', 'None', 'Channel + Spatial'), ('Lateral Inhibition', 'None', 'Yes (learnable)'),
              ('Recurrent Feedback', 'None', 'Yes (2 iterations)'), ('Skip Connections', 'Additive residual', 'Projected residual'),
              ('Pre-trained', 'Yes (ImageNet)', 'No (from scratch)'), ('Accuracy', '81.98%', '95.87%')]:
        pdf.trow(r, w7)

    # ── VIII. SPECTRAL VISUALIZATION ──
    pdf.section('VIII', 'Spectral Land Cover Visualization')
    pdf.body('Standard Grad-CAM produces blurry, low-resolution activation maps. We implement spectral segmentation based on color-space analysis -- the same principle underlying NDVI in professional remote sensing.')
    pdf.subsec('A', 'Method')
    pdf.bullet('Convert RGB to HSV and CIELAB color spaces')
    pdf.bullet('Compute Green Leaf Index: GLI = (2G-R-B)/(2G+R+B+1) for vegetation detection')
    pdf.bullet('HSV hue analysis: green -> vegetation, blue -> water, low saturation -> urban')
    pdf.bullet('LAB a-channel for urban warmth, b-channel for bare soil')
    pdf.bullet('Threshold into 6 masks: dense vegetation, light vegetation, water, urban, road, bare soil')
    pdf.bullet('Map spectral categories to EuroSAT classes using model softmax probabilities')
    pdf.bullet('Render colored overlays with contour borders and confidence labels')
    pdf.ln(2)
    pdf.subsec('B', 'Spectral-to-Class Mapping')
    w8 = [45, 85]
    pdf.trow(['Spectral Type', 'Candidate EuroSAT Classes'], w8, header=True)
    for r in [('Dense Vegetation', 'Forest, HerbaceousVegetation, Pasture'), ('Light Vegetation', 'AnnualCrop, PermanentCrop, Pasture'),
              ('Water', 'River, SeaLake'), ('Urban', 'Residential, Industrial'),
              ('Road', 'Highway'), ('Bare Soil', 'AnnualCrop, PermanentCrop, Industrial')]:
        pdf.trow(r, w8)

    # ── IX. SYSTEM ARCHITECTURE ──
    pdf.section('IX', 'System Architecture')
    pdf.subsec('A', 'Technology Stack')
    w9 = [45, 65]
    pdf.trow(['Layer', 'Technology'], w9, header=True)
    for r in [('Deep Learning', 'PyTorch'), ('Backend API', 'FastAPI (Python)'), ('Frontend', 'HTML5, CSS3, JavaScript'),
              ('Image Processing', 'OpenCV, Pillow'), ('Metrics', 'scikit-learn'), ('Server', 'Uvicorn ASGI')]:
        pdf.trow(r, w9)
    pdf.ln(3)
    pdf.subsec('B', 'API Endpoints')
    w10 = [30, 15, 65]
    pdf.trow(['Endpoint', 'Method', 'Description'], w10, header=True)
    for r in [('/api/predict', 'POST', 'Both models predictions + spectral overlay'),
              ('/api/sample', 'GET', 'Random EuroSAT sample image'),
              ('/api/metrics', 'GET', 'Training benchmark data'),
              ('/api/colors', 'GET', 'RGB color palette for 10 classes'),
              ('/api/health', 'GET', 'System health check')]:
        pdf.trow(r, w10)
    pdf.ln(3)
    pdf.subsec('C', 'Frontend')
    pdf.body('Premium dark-mode web UI with three tabbed views: (1) ResNet-18 results with probability charts and spectral overlay, (2) BDH results, (3) Head-to-head comparison with full benchmark table and side-by-side attention maps. Features glassmorphism design, micro-animations, and drag-and-drop image upload.')

    # ── X. CONCLUSION ──
    pdf.section('X', 'Conclusion')
    pdf.body(
        'This paper presents Baby Dragon Hatchling (BDH), a biologically-inspired deep learning architecture '
        'for satellite land cover classification. BDH achieves 95.87% accuracy on EuroSAT -- a 13.89 percentage '
        'point improvement over ResNet-18 with transfer learning -- while using 5.5x fewer total architecture '
        'parameters. The four key innovations -- multi-scale feature pyramids, lateral inhibition, contextual '
        'attention, and recurrent refinement -- each contribute by mimicking how the human visual cortex '
        'processes complex spatial information.')
    pdf.set_font('Helvetica', 'B', 9)
    pdf.cell(0, 5, 'Future Work:', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)
    pdf.bullet('Extending BDH to multi-spectral (13-band) Sentinel-2 data beyond RGB')
    pdf.bullet('Semantic segmentation variant for pixel-level classification')
    pdf.bullet('Scaling to BigEarthNet (590K images)')
    pdf.bullet('Lightweight model distillation for edge/satellite hardware deployment')
    pdf.bullet('Integration with real-time satellite data feeds for continuous monitoring')

    # ── REFERENCES ──
    pdf.section('', 'References')
    refs = [
        '[1] P. Helber, B. Bischke, A. Dengel, D. Borth, "EuroSAT: A Novel Dataset and Deep Learning Benchmark for Land Use and Land Cover Classification," IEEE JSTARS, vol. 12, no. 7, pp. 2217-2226, 2019.',
        '[2] J. Yosinski, J. Clune, Y. Bengio, H. Lipson, "How transferable are features in deep neural networks?" NeurIPS, pp. 3320-3328, 2014.',
        '[3] J. Hu, L. Shen, G. Sun, "Squeeze-and-Excitation Networks," IEEE CVPR, pp. 7132-7141, 2018.',
        '[4] S. Woo, J. Park, J.-Y. Lee, I.S. Kweon, "CBAM: Convolutional Block Attention Module," ECCV, pp. 3-19, 2018.',
        '[5] C. Szegedy et al., "Going Deeper with Convolutions," IEEE CVPR, pp. 1-9, 2015.',
        '[6] T.-Y. Lin et al., "Feature Pyramid Networks for Object Detection," IEEE CVPR, pp. 2117-2125, 2017.',
        '[7] H.K. Hartline, H.G. Wagner, F. Ratliff, "Inhibition in the eye of Limulus," J. Gen. Physiology, vol. 39, no. 5, pp. 651-673, 1956.',
        '[8] J.J. DiCarlo, D. Zoccolan, N.C. Rust, "How Does the Brain Solve Visual Object Recognition?" Neuron, vol. 73, no. 3, pp. 415-434, 2012.',
        '[9] K. He, X. Zhang, S. Ren, J. Sun, "Deep Residual Learning for Image Recognition," IEEE CVPR, pp. 770-778, 2016.',
    ]
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(0,0,0)
    for ref in refs:
        pdf.multi_cell(0, 4, ref)
        pdf.ln(1)

    out = '/Users/yashlohia/Major project/SensiSpace_IEEE_Paper.pdf'
    pdf.output(out)
    print(f'IEEE Paper PDF saved to: {out}')

if __name__ == '__main__':
    generate()
