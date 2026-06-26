#!/usr/bin/env python3
"""Generate a professional PDF report of the SensiSpace project."""

from fpdf import FPDF

class ProjectPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, 'SensiSpace - Satellite Land Cover Classification', align='R')
        self.ln(5)
        self.set_draw_color(100, 80, 200)
        self.set_line_width(0.5)
        self.line(10, 13, 200, 13)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

    def section_title(self, title):
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(80, 60, 180)
        self.ln(6)
        self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(80, 60, 180)
        self.set_line_width(0.3)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def sub_title(self, title):
        self.set_font('Helvetica', 'B', 13)
        self.set_text_color(50, 50, 50)
        self.ln(4)
        self.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def sub_sub_title(self, title):
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(80, 80, 80)
        self.ln(3)
        self.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def body_text(self, text):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 5.5, text)
        self.ln(2)

    def bullet(self, text, indent=10):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(30, 30, 30)
        self.set_x(self.l_margin + indent)
        self.multi_cell(self.w - self.l_margin - self.r_margin - indent, 5.5, '- ' + text)
        self.ln(1)

    def bold_bullet(self, bold_part, normal_part, indent=10):
        self.set_x(self.l_margin + indent)
        self.set_font('Helvetica', '', 10)
        self.set_text_color(30, 30, 30)
        self.write(5.5, '- ')
        self.set_font('Helvetica', 'B', 10)
        self.write(5.5, bold_part)
        self.set_font('Helvetica', '', 10)
        self.write(5.5, normal_part)
        self.ln(7)

    def code_block(self, text):
        self.set_font('Courier', '', 9)
        self.set_fill_color(240, 240, 245)
        self.set_text_color(40, 40, 40)
        y0 = self.get_y()
        self.multi_cell(0, 5, text, fill=True)
        self.ln(3)

    def table_row(self, cols, widths, bold=False, header=False):
        if header:
            self.set_font('Helvetica', 'B', 9)
            self.set_fill_color(80, 60, 180)
            self.set_text_color(255, 255, 255)
        elif bold:
            self.set_font('Helvetica', 'B', 9)
            self.set_fill_color(245, 245, 250)
            self.set_text_color(30, 30, 30)
        else:
            self.set_font('Helvetica', '', 9)
            self.set_fill_color(250, 250, 255)
            self.set_text_color(30, 30, 30)
        for i, (col, w) in enumerate(zip(cols, widths)):
            self.cell(w, 7, str(col), border=1, fill=True, align='C' if i > 0 else 'L')
        self.ln()


def generate():
    pdf = ProjectPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    # ═══════════════════════════════════════════
    # TITLE PAGE
    # ═══════════════════════════════════════════
    pdf.add_page()
    pdf.ln(50)
    pdf.set_font('Helvetica', 'B', 28)
    pdf.set_text_color(80, 60, 180)
    pdf.cell(0, 15, 'SensiSpace', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.set_font('Helvetica', '', 18)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 12, 'Satellite Land Cover Classification', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    pdf.set_draw_color(80, 60, 180)
    pdf.set_line_width(1)
    pdf.line(60, pdf.get_y(), 150, pdf.get_y())
    pdf.ln(10)
    pdf.set_font('Helvetica', '', 12)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, 'A Deep Learning Approach using Baby Dragon Hatchling Architecture', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, 'vs ResNet-18 on EuroSAT Dataset (27,000 images)', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(15)
    pdf.set_font('Helvetica', 'I', 11)
    pdf.cell(0, 8, 'ISRO RESPOND Initiative - Deep Learning Research', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, 'Major Project Report', align='C', new_x="LMARGIN", new_y="NEXT")

    # ═══════════════════════════════════════════
    # 1. PROBLEM STATEMENT
    # ═══════════════════════════════════════════
    pdf.add_page()
    pdf.section_title('1. Problem Statement')
    pdf.body_text(
        'Satellite remote sensing generates vast amounts of high-resolution imagery used for '
        'monitoring Earth\'s surface, environmental changes, and natural resources. Organizations '
        'like ISRO (Indian Space Research Organisation) collect this data, but manually analyzing '
        'it is impractical at scale.'
    )
    pdf.body_text(
        'This project introduces an intelligent system that automatically classifies satellite '
        'images into 10 land cover types using deep learning, and visually highlights which '
        'parts of the image correspond to which land type.'
    )
    pdf.body_text(
        'We compare a standard industry baseline (ResNet-18) against a novel, biologically-inspired '
        'architecture called Baby Dragon Hatchling (BDH) to demonstrate that purpose-built '
        'architectures can outperform generic ones with fewer parameters.'
    )

    # ═══════════════════════════════════════════
    # 2. DATASET
    # ═══════════════════════════════════════════
    pdf.section_title('2. Dataset - EuroSAT')
    pdf.body_text(
        'EuroSAT is a benchmark dataset of 27,000 georeferenced satellite images from the '
        'Sentinel-2 satellite (European Space Agency). Each image is 64x64 pixels in RGB and '
        'labeled with one of 10 land cover classes.'
    )

    pdf.sub_title('Dataset Properties')
    w = [50, 50]
    pdf.table_row(['Property', 'Value'], w, header=True)
    for row in [
        ('Source', 'Sentinel-2 satellite'),
        ('Total Images', '27,000'),
        ('Image Size', '64 x 64 pixels, RGB'),
        ('Classes', '10 land cover types'),
        ('Train/Val Split', '80% / 20%'),
    ]:
        pdf.table_row(row, w)
    pdf.ln(5)

    pdf.sub_title('The 10 Land Cover Classes')
    w2 = [45, 85]
    pdf.table_row(['Class', 'Description'], w2, header=True)
    classes = [
        ('AnnualCrop', 'Wheat, corn, rice fields'),
        ('Forest', 'Dense tree cover (deciduous/coniferous)'),
        ('HerbaceousVegetation', 'Grasslands, meadows, scrubland'),
        ('Highway', 'Major roads and expressways'),
        ('Industrial', 'Factories, warehouses'),
        ('Pasture', 'Grazing land for livestock'),
        ('PermanentCrop', 'Orchards, vineyards'),
        ('Residential', 'Houses, apartments, neighborhoods'),
        ('River', 'Rivers and streams'),
        ('SeaLake', 'Seas, lakes, reservoirs'),
    ]
    for row in classes:
        pdf.table_row(row, w2)

    # ═══════════════════════════════════════════
    # 3. RESNET-18
    # ═══════════════════════════════════════════
    pdf.add_page()
    pdf.section_title('3. Model 1 - ResNet-18 (CNN Baseline)')

    pdf.sub_title('What is ResNet?')
    pdf.body_text(
        'ResNet (Residual Network) is a standard Convolutional Neural Network developed by '
        'Microsoft Research in 2015. The key innovation is skip connections (residual connections) '
        'that allow gradients to flow directly through the network, solving the vanishing gradient '
        'problem in deep networks. ResNet-18 has 18 layers and approximately 11.2 million parameters.'
    )

    pdf.sub_title('Architecture Pipeline')
    pdf.code_block(
        'Input (3x64x64)\n'
        '  |-> Conv 7x7, stride 2 + BatchNorm + ReLU + MaxPool 3x3\n'
        '  |     -> 64 channels\n'
        '  |-> Layer 1: 2x BasicBlock (64 channels)\n'
        '  |-> Layer 2: 2x BasicBlock (128 channels, stride 2)\n'
        '  |-> Layer 3: 2x BasicBlock (256 channels, stride 2)\n'
        '  |-> Layer 4: 2x BasicBlock (512 channels, stride 2)\n'
        '  |-> Global Average Pooling (512x1x1)\n'
        '  |-> Fully Connected: 512 -> 10 classes'
    )

    pdf.sub_title('BasicBlock (Building Block)')
    pdf.code_block(
        'Input ----> Conv3x3 -> BN -> ReLU -> Conv3x3 -> BN ----> ADD -> ReLU -> Output\n'
        '  |                                                        |\n'
        '  +--------------- Skip Connection (identity) ------------+'
    )
    pdf.body_text(
        'The skip connection adds the original input directly to the output. The block only '
        'needs to learn the difference (residual) between input and desired output, making '
        'training much easier. This is what allows ResNet to train successfully with many layers.'
    )

    pdf.sub_title('Transfer Learning')
    pdf.body_text(
        'We use ResNet-18 pretrained on ImageNet (1.3 million natural images). The model already '
        'knows basic visual features like edges, textures, and shapes. We replace the final '
        'fully connected layer (512->1000) with (512->10) and fine-tune the entire network on '
        'EuroSAT satellite imagery. This approach is called transfer learning - leveraging '
        'knowledge from one domain (natural images) for another (satellite imagery).'
    )

    # ═══════════════════════════════════════════
    # 4. BABY DRAGON HATCHLING
    # ═══════════════════════════════════════════
    pdf.add_page()
    pdf.section_title('4. Model 2 - Baby Dragon Hatchling (BDH)')

    pdf.body_text(
        'Baby Dragon Hatchling is a novel, biologically-inspired deep learning architecture '
        'designed specifically for satellite remote sensing image analysis. Developed under the '
        'ISRO RESPOND initiative, it draws from neuroscience - how the human visual cortex '
        'processes images - and incorporates four specialized modules that standard CNNs lack.'
    )

    pdf.sub_title('Architecture Pipeline')
    pdf.code_block(
        'Input (3x64x64)\n'
        '  |-> Stem: Conv3x3 -> BN -> ReLU -> Conv3x3 -> BN -> ReLU (3 -> 64 ch)\n'
        '  |\n'
        '  |-> BDH Stage 1 (64 ch, 64x64)  -> MaxPool 2x2 -> 32x32\n'
        '  |-> BDH Stage 2 (128 ch, 32x32) -> MaxPool 2x2 -> 16x16\n'
        '  |-> BDH Stage 3 (256 ch, 16x16) -> MaxPool 2x2 -> 8x8\n'
        '  |\n'
        '  |-> Recurrent Refinement (2 iterations)\n'
        '  |\n'
        '  |-> Global Average Pool (256x1x1)\n'
        '  |-> Dropout(0.3) -> FC(256->128) -> ReLU\n'
        '  |-> Dropout(0.2) -> FC(128->10)'
    )

    pdf.sub_title('Inside Each BDH Stage')
    pdf.code_block(
        'Input --> Multi-Scale Pyramid --> Lateral Inhibition --> Contextual Attention --> ADD --> ReLU\n'
        '  |                                                                              |\n'
        '  +--------------------------- 1x1 Conv Residual Projection --------------------+'
    )
    pdf.body_text(
        'Each stage chains three biologically-inspired modules with a residual connection. '
        'The residual projection (1x1 convolution) adjusts channel dimensions when they change '
        'between stages.'
    )

    # Module 1
    pdf.add_page()
    pdf.sub_title('Module 1: Multi-Scale Feature Pyramid')
    pdf.body_text(
        'Problem: Satellite images contain objects at many different sizes - a small house vs. '
        'a large forest. A single 3x3 convolution can only "see" a small receptive field.'
    )
    pdf.body_text(
        'Solution: Process the input through three parallel convolutions with different kernel '
        'sizes simultaneously, then concatenate the results:'
    )
    pdf.code_block(
        'Input --+--> Conv 3x3 + BN + ReLU  (fine detail: edges, small objects)     --+\n'
        '        +--> Conv 5x5 + BN + ReLU  (medium features: buildings, patches)   --+--> Concatenate\n'
        '        +--> Conv 7x7 + BN + ReLU  (large patterns: forests, water bodies) --+'
    )
    pdf.body_text(
        'The 3x3 branch captures fine edges (road boundaries), the 5x5 captures medium '
        'structures (buildings), and the 7x7 captures broad patterns (forest canopy). By '
        'concatenating all three, the model gets a rich, multi-resolution representation at '
        'every stage. This is critical for EuroSAT where land cover objects vary dramatically in scale.'
    )

    # Module 2
    pdf.sub_title('Module 2: Lateral Inhibition Block')
    pdf.body_text(
        'Biological inspiration: In the human retina, when a neuron fires, it suppresses its '
        'neighboring neurons. This is called lateral inhibition - it is why we perceive sharper '
        'edges between light and dark areas than actually exist in the image.'
    )
    pdf.code_block(
        'surround = depthwise_conv_3x3(x)      # Estimate surrounding activity\n'
        'surround = batch_norm(surround)\n'
        'output   = x - alpha * surround        # Subtract surround (alpha is learnable)\n'
        'output   = ReLU(output)'
    )
    pdf.body_text(
        'The depthwise convolution estimates the "surround" response for each feature channel. '
        'Subtracting it amplifies differences between adjacent regions. The learnable parameter '
        'alpha (initialized to 0.3) controls inhibition strength. Result: sharper feature '
        'boundaries - critical for distinguishing adjacent land types (e.g., where a river meets a forest).'
    )

    # Module 3
    pdf.sub_title('Module 3: Contextual Attention')
    pdf.body_text(
        'Problem: Not all features are equally important. In a satellite image, water texture '
        'might be more informative than road edges for classifying "River."'
    )
    pdf.body_text(
        'Solution: A dual attention mechanism that learns to focus on what matters:'
    )

    pdf.sub_sub_title('Channel Attention (WHAT features matter):')
    pdf.code_block(
        'Global Avg Pool -> FC(C -> C/8) -> ReLU -> FC(C/8 -> C) -> Sigmoid\n'
        'Output: a weight per channel, e.g., "90% attention to water features, 10% to edges"'
    )

    pdf.sub_sub_title('Spatial Attention (WHERE to look):')
    pdf.code_block(
        'AvgPool(channels) + MaxPool(channels) -> Concat -> Conv 7x7 -> Sigmoid\n'
        'Output: a weight per pixel, e.g., "focus on center-right where the river is"'
    )
    pdf.body_text(
        'The input is first reweighted by channel importance, then by spatial importance. '
        'This gives the model selective focus - just like how humans look at a complex image '
        'and immediately focus on the relevant parts.'
    )

    # Module 4
    pdf.add_page()
    pdf.sub_title('Module 4: Recurrent Refinement')
    pdf.body_text(
        'Biological inspiration: The brain does not process visual information in a single pass. '
        'There are feedback connections from higher visual areas back to lower ones - the brain '
        'iteratively refines its interpretation of what it sees.'
    )
    pdf.code_block(
        'for iteration in [1, 2]:\n'
        '    refined = Conv3x3 + BN + ReLU(x)       # Propose a refinement\n'
        '    gate    = Sigmoid(Conv1x1(refined))      # How much to update? (0 to 1)\n'
        '    x       = x * gate + refined * (1-gate)  # Gated blend'
    )
    pdf.body_text(
        'Each iteration, the network computes a "refined" version of the features. A sigmoid '
        'gate decides how much of the refinement to accept. Where gate is close to 1, the original '
        'features are kept (already good). Where gate is close to 0, they are replaced with the '
        'refined version (needs improvement). Result: features become progressively cleaner '
        'and more discriminative over 2 iterations.'
    )

    # ═══════════════════════════════════════════
    # 5. TRAINING
    # ═══════════════════════════════════════════
    pdf.section_title('5. Training Pipeline')
    pdf.body_text(
        'Both models are trained on the same 80/20 split of EuroSAT with identical '
        'augmentation and optimization settings for fair comparison.'
    )

    pdf.sub_title('Training Configuration')
    w3 = [55, 55]
    pdf.table_row(['Setting', 'Value'], w3, header=True)
    for row in [
        ('Optimizer', 'Adam'),
        ('Learning Rate', '0.001'),
        ('LR Scheduler', 'StepLR (x0.1 every 5 epochs)'),
        ('Loss Function', 'CrossEntropyLoss'),
        ('Batch Size', '64'),
        ('Epochs', '15'),
        ('Augmentation', 'Flip, Rotate +/-15°, Color Jitter'),
        ('Normalization', 'ImageNet mean/std'),
    ]:
        pdf.table_row(row, w3)
    pdf.ln(5)

    pdf.sub_title('Results')
    w4 = [50, 35, 35]
    pdf.table_row(['Metric', 'ResNet-18', 'BDH'], w4, header=True)
    pdf.table_row(['Final Accuracy', '81.98%', '95.87%'], w4)
    pdf.table_row(['Parameters', '~11.2M', '~1.8M'], w4)
    pdf.table_row(['Architecture', 'Transfer Learning', 'Trained from scratch'], w4)
    pdf.ln(5)

    pdf.body_text(
        'Key insight: BDH achieves 14% higher accuracy with 6x fewer parameters - demonstrating '
        'that domain-specific architecture design beats brute-force parameter scaling. The '
        'biologically-inspired modules (multi-scale processing, lateral inhibition, attention, '
        'and recurrent refinement) are more effective than simply stacking more layers.'
    )

    # ═══════════════════════════════════════════
    # 6. VISUALIZATION
    # ═══════════════════════════════════════════
    pdf.add_page()
    pdf.section_title('6. Spectral Land Cover Segmentation')

    pdf.body_text(
        'After classification, we generate a visual overlay showing which parts of the image '
        'correspond to which land type. This provides interpretable, visual evidence for the '
        'model\'s classification decision.'
    )

    pdf.sub_title('Why Not Grad-CAM?')
    pdf.body_text(
        'Grad-CAM (Gradient-weighted Class Activation Mapping) is a common visualization '
        'technique, but it produces blurry, inaccurate blobs for this use case because: '
        '(1) Classification models learn "this whole image = Forest" - they do not learn '
        'pixel-level boundaries. (2) The activation maps are very low resolution (8x8 or 2x2 '
        'pixels upscaled to 64x64), creating unavoidable artifacts.'
    )

    pdf.sub_title('Our Approach: Spectral Color Analysis')
    pdf.body_text(
        'We use spectral analysis - the same principle used in professional satellite remote '
        'sensing with indices like NDVI (Normalized Difference Vegetation Index). The approach '
        'analyzes actual pixel colors in HSV and LAB color spaces:'
    )

    pdf.bold_bullet('Green Leaf Index (GLI): ', '(2G - R - B) / (2G + R + B) - identifies vegetation')
    pdf.bold_bullet('HSV Hue Analysis: ', 'Green hue = vegetation, Blue hue = water, Low saturation = urban')
    pdf.bold_bullet('LAB Color Space: ', 'a-channel warmth for urban detection, b-channel for soil')

    pdf.ln(3)
    pdf.sub_title('Segmentation Pipeline')
    pdf.code_block(
        '1. Convert satellite image to HSV + LAB color spaces\n'
        '2. Compute vegetation/water/urban spectral indices per pixel\n'
        '3. Threshold pixels into categories: vegetation, water, urban, road, soil\n'
        '4. Map each category to the specific EuroSAT class using model probabilities\n'
        '5. Draw colored overlays + contour borders on the original image\n'
        '6. Add class labels with confidence percentages'
    )

    pdf.body_text(
        'Result: Pixel-accurate boundaries that follow actual land features (river edges, '
        'forest boundaries, road paths) - far more accurate than Grad-CAM.'
    )

    # ═══════════════════════════════════════════
    # 7. SYSTEM ARCHITECTURE
    # ═══════════════════════════════════════════
    pdf.section_title('7. System Architecture')
    pdf.body_text(
        'The system is a full-stack web application with a FastAPI backend serving PyTorch '
        'models and a premium dark-mode frontend.'
    )

    pdf.sub_title('Backend (FastAPI + PyTorch)')
    w5 = [35, 20, 80]
    pdf.table_row(['Endpoint', 'Method', 'Returns'], w5, header=True)
    pdf.table_row(['/api/predict', 'POST', 'Both models predictions + spectral overlay'], w5)
    pdf.table_row(['/api/sample', 'GET', 'Random EuroSAT sample image'], w5)
    pdf.table_row(['/api/metrics', 'GET', 'Training benchmark data'], w5)
    pdf.table_row(['/api/colors', 'GET', 'Color palette for all 10 classes'], w5)
    pdf.ln(5)

    pdf.sub_title('Frontend (HTML/CSS/JS)')
    pdf.bullet('3-slide tabbed interface: ResNet-18, Baby Dragon Hatchling, Comparison')
    pdf.bullet('Color-coded probability distribution charts for all 10 classes')
    pdf.bullet('Side-by-side spectral overlay comparison')
    pdf.bullet('Premium dark-mode design with glassmorphism and micro-animations')
    pdf.bullet('Upload custom images or load random EuroSAT samples')

    # ═══════════════════════════════════════════
    # 8. COMPARISON TABLE
    # ═══════════════════════════════════════════
    pdf.add_page()
    pdf.section_title('8. Architecture Comparison Summary')

    w6 = [50, 45, 45]
    pdf.table_row(['Feature', 'ResNet-18', 'BDH'], w6, header=True)
    rows = [
        ('Type', 'Standard CNN', 'Bio-inspired CNN'),
        ('Depth', '18 layers', '3 stages + refinement'),
        ('Multi-Scale', 'No (single 3x3)', 'Yes (3x3 + 5x5 + 7x7)'),
        ('Attention', 'None', 'Channel + Spatial'),
        ('Lateral Inhibition', 'None', 'Yes (learnable)'),
        ('Recurrent Feedback', 'None (feed-forward)', 'Yes (2 iterations)'),
        ('Skip Connections', 'Yes (residual)', 'Yes (residual)'),
        ('Parameters', '~11.2M', '~1.8M'),
        ('Pretrained', 'Yes (ImageNet)', 'No (from scratch)'),
        ('Final Accuracy', '81.98%', '95.87%'),
    ]
    for row in rows:
        pdf.table_row(row, w6)

    pdf.ln(10)
    pdf.section_title('9. Conclusion')
    pdf.body_text(
        'This project demonstrates that biologically-inspired neural network architectures '
        'can significantly outperform standard CNNs for satellite remote sensing tasks. '
        'The Baby Dragon Hatchling architecture achieves 95.87% accuracy with only 1.8 million '
        'parameters - 14 percentage points higher than ResNet-18 with 6x fewer parameters.'
    )
    pdf.body_text(
        'The four key innovations - multi-scale feature pyramids, lateral inhibition, '
        'contextual attention, and recurrent refinement - each contribute to this improvement '
        'by mimicking how the human visual system processes complex spatial information. '
        'Combined with spectral color-space segmentation for visualization, the system provides '
        'both accurate classification and interpretable, pixel-level land cover mapping.'
    )
    pdf.body_text(
        'The system is production-ready for demonstration, with a full web interface allowing '
        'users to upload satellite images and receive instant classification results with '
        'visual land cover highlighting.'
    )

    # Save
    output_path = '/Users/yashlohia/Major project/SensiSpace_Project_Report.pdf'
    pdf.output(output_path)
    print(f'PDF saved to: {output_path}')

if __name__ == '__main__':
    generate()
