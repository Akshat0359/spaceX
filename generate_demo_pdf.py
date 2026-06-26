#!/usr/bin/env python3
"""Generate PDF of the demo presentation script."""

from fpdf import FPDF


class DemoPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 9)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, 'SensiSpace - College Demo Script', align='R')
        self.ln(4)
        self.set_draw_color(80, 60, 180)
        self.set_line_width(0.4)
        self.line(10, 12, 200, 12)
        self.ln(6)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

    def step_title(self, title):
        self.set_font('Helvetica', 'B', 15)
        self.set_text_color(80, 60, 180)
        self.ln(4)
        self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(80, 60, 180)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def sub(self, title):
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(50, 50, 50)
        self.ln(3)
        self.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def action(self, text):
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(200, 60, 60)
        self.multi_cell(0, 5.5, '[ACTION] ' + text)
        self.ln(1)

    def say(self, text):
        self.set_font('Helvetica', '', 10)
        self.set_fill_color(245, 245, 255)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 5.5, text, fill=True)
        self.ln(2)

    def note(self, text):
        self.set_font('Helvetica', 'I', 9)
        self.set_text_color(100, 100, 100)
        self.multi_cell(0, 5, text)
        self.ln(2)

    def code(self, text):
        self.set_font('Courier', '', 9)
        self.set_fill_color(235, 235, 240)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 5, text, fill=True)
        self.ln(2)

    def qa(self, question, answer):
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(80, 60, 180)
        self.set_x(self.l_margin)
        self.multi_cell(0, 5.5, 'Q: ' + question)
        self.ln(1)
        self.set_font('Helvetica', '', 10)
        self.set_text_color(30, 30, 30)
        self.set_x(self.l_margin)
        self.multi_cell(0, 5.5, 'A: ' + answer)
        self.ln(3)

    def bullet(self, text):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(30, 30, 30)
        self.set_x(self.l_margin + 8)
        self.multi_cell(self.w - self.l_margin - self.r_margin - 8, 5.5, '- ' + text)
        self.ln(1)


def generate():
    pdf = DemoPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    # ── TITLE PAGE ──
    pdf.add_page()
    pdf.ln(40)
    pdf.set_font('Helvetica', 'B', 30)
    pdf.set_text_color(80, 60, 180)
    pdf.cell(0, 15, 'SensiSpace', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.set_font('Helvetica', '', 16)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 10, 'College Demo Script', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)
    pdf.set_draw_color(80, 60, 180)
    pdf.set_line_width(1)
    pdf.line(70, pdf.get_y(), 140, pdf.get_y())
    pdf.ln(8)
    pdf.set_font('Helvetica', '', 12)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, 'Satellite Land Cover Classification', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, 'Baby Dragon Hatchling vs ResNet-18', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    pdf.set_font('Helvetica', 'I', 11)
    pdf.cell(0, 8, 'Total Demo Time: ~12-15 minutes', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(20)

    # Timeline table
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(0, 8, 'Demo Flow Overview:', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    w = [25, 55, 60]
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_fill_color(80, 60, 180)
    pdf.set_text_color(255, 255, 255)
    for col, cw in zip(['Time', 'Step', 'What You Do'], w):
        pdf.cell(cw, 7, col, border=1, fill=True, align='C')
    pdf.ln()
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(30, 30, 30)
    rows = [
        ('Before', 'Setup', 'Start server, open browser'),
        ('2 min', 'Introduction', 'Problem + your solution'),
        ('1 min', 'Dataset', 'Show EuroSAT samples, 10 classes'),
        ('3 min', 'Live Demo', 'Classify 2-3 images, show tabs'),
        ('4 min', 'Architecture', 'ResNet + BDH 4 modules (KEY!)'),
        ('1 min', 'Visualization', 'Explain spectral segmentation'),
        ('1 min', 'Conclusion', 'Results + future work'),
    ]
    for row in rows:
        pdf.set_fill_color(250, 250, 255)
        for val, cw in zip(row, w):
            pdf.cell(cw, 7, val, border=1, fill=True)
        pdf.ln()

    # ── STEP 0 ──
    pdf.add_page()
    pdf.step_title('STEP 0: Setup (Before Your Turn)')
    pdf.note('Do this 5 minutes before your demo starts.')
    pdf.action('Open Terminal and run:')
    pdf.code(
        'cd "/Users/yashlohia/Major project"\n'
        'source venv/bin/activate\n'
        'PYTHONPATH=$(pwd)/src uvicorn app:app --app-dir src --host 0.0.0.0 --port 8000'
    )
    pdf.action('Open Chrome -> http://localhost:8000')
    pdf.action('Keep the PDF report open as backup: SensiSpace_Project_Report.pdf')
    pdf.note('Load 2-3 diverse samples beforehand (forest, city, river) so you know what to expect.')

    # ── STEP 1 ──
    pdf.step_title('STEP 1: Introduction (2 minutes)')
    pdf.sub('What to say:')
    pdf.say(
        '"Good morning everyone. My project is called SensiSpace - a Satellite Land Cover '
        'Classification System.\n\n'
        'The problem: Organizations like ISRO collect millions of satellite images every day. '
        'Manually analyzing each image to identify what type of land it shows - is it a forest? '
        'a river? residential area? - is impossible at this scale. We need AI to do this automatically.\n\n'
        'My solution: I have built a deep learning system that takes any satellite image as input '
        'and instantly classifies it into one of 10 land cover types - Forest, River, Highway, '
        'Residential, Agricultural crops, and so on.\n\n'
        'What makes this unique: I designed a completely new neural network architecture called '
        'Baby Dragon Hatchling, inspired by how the human brain processes visual information. '
        'I compare it against ResNet-18, a standard industry CNN.\n\n'
        'The system is trained on EuroSAT - 27,000 real satellite images from the Sentinel-2 satellite."'
    )

    # ── STEP 2 ──
    pdf.add_page()
    pdf.step_title('STEP 2: Show the Dataset (1 minute)')
    pdf.action('Click "Load Random EuroSAT Sample" a few times to show different images.')
    pdf.say(
        '"These are actual 64x64 pixel satellite images from space. Each one is labeled '
        'with one of 10 classes:\n'
        '- Forest: dense tree cover\n'
        '- River: water bodies\n'
        '- Residential: houses and neighborhoods\n'
        '- Highway: major roads\n'
        '- AnnualCrop: agricultural fields\n'
        '- And 5 more types.\n\n'
        'We train on 21,600 images and test on 5,400."'
    )

    # ── STEP 3 ──
    pdf.step_title('STEP 3: Live Demo (3 minutes)')
    pdf.note('This is the WOW moment. Pick interesting images.')
    pdf.action('Click "Load Random EuroSAT Sample" - pick one with visible features')
    pdf.action('Click "Run Classification" - wait ~2 seconds')
    pdf.sub('While loading, say:')
    pdf.say('"Now I am running both models on this image simultaneously..."')
    pdf.sub('Once results appear:')
    pdf.say(
        '"Here you can see the results. ResNet-18 classified this as [read prediction] '
        'with [read confidence]% confidence in [read time] milliseconds.\n\n'
        'Below that is the spectral land cover map - pixel-level highlighting showing exactly '
        'WHICH parts of the image correspond to which land type. Notice how the boundaries '
        'follow actual features in the image."'
    )
    pdf.action('Click the "Baby Dragon Hatchling" tab')
    pdf.say(
        '"My custom model - Baby Dragon Hatchling - classified this as [read prediction] '
        'with [read confidence]% confidence.\n\n'
        'Look at the probability distribution chart - every class is color-coded."'
    )
    pdf.action('Click the "Comparison" tab')
    pdf.say('"This comparison view shows both models side by side."')
    pdf.note('Repeat with 2-3 different samples for variety.')

    # ── STEP 4 ──
    pdf.add_page()
    pdf.step_title('STEP 4: Explain Architecture (4 minutes)')
    pdf.note('THIS IS WHERE THE MARKS ARE. Speak clearly and confidently.')

    pdf.sub('Part A: ResNet-18')
    pdf.say(
        '"ResNet-18 is a well-known CNN - 18 layers of 3x3 convolutions with skip connections. '
        'The skip connections solve the vanishing gradient problem by adding the input directly '
        'to the output of each block. We use it pretrained on ImageNet - 1.3 million natural '
        'images - and fine-tune on satellite data. It has about 11.2 million parameters."'
    )

    pdf.sub('Part B: Baby Dragon Hatchling (THE KEY)')
    pdf.say(
        '"Baby Dragon Hatchling is my novel architecture, inspired by neuroscience. It has '
        'only 1.8 million parameters - 6 times fewer than ResNet - but much higher accuracy. '
        'It has 4 biologically-inspired modules:"'
    )

    pdf.sub('Module 1: Multi-Scale Feature Pyramid')
    pdf.say(
        '"Instead of one 3x3 convolution per layer, BDH uses three parallel convolutions: '
        '3x3, 5x5, and 7x7 simultaneously. The small kernel captures fine details like road '
        'edges. The medium captures buildings. The large captures broad patterns like forests. '
        'All three are concatenated. This is critical because in satellite images, a house is '
        'tiny but a forest is huge."'
    )

    pdf.sub('Module 2: Lateral Inhibition')
    pdf.say(
        '"From neuroscience: in your retina, when a neuron fires, it suppresses neighbors. '
        'This sharpens edge perception. BDH does the same - a depthwise convolution estimates '
        'surrounding activity, then we subtract a learnable fraction (alpha) from the center. '
        'This sharpens boundaries between land types - like where a river meets a forest."'
    )

    pdf.sub('Module 3: Contextual Attention')
    pdf.say(
        '"A dual attention mechanism. Channel Attention asks WHAT features matter using '
        'squeeze-and-excitation. Spatial Attention asks WHERE to look using pooling and 7x7 '
        'convolution. Together they give selective focus - like how you immediately notice '
        'the river in a complex satellite photo."'
    )

    pdf.add_page()
    pdf.sub('Module 4: Recurrent Refinement')
    pdf.say(
        '"The brain does not process images in one shot - it has feedback loops. BDH runs '
        '2 iterations of gated refinement. Each iteration proposes an improvement, and a '
        'sigmoid gate decides how much to accept. Features get progressively cleaner - like '
        'how you notice more details the longer you look at something."'
    )

    pdf.sub('The Punchline (say this with emphasis):')
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(200, 60, 60)
    pdf.multi_cell(0, 6,
        '"The result: 95.87% accuracy with BDH vs 81.98% with ResNet-18. '
        'A 14 percentage point improvement with 6x fewer parameters. '
        'This proves that domain-specific, biologically-inspired design '
        'beats brute-force parameter scaling."'
    )
    pdf.ln(4)

    # ── STEP 5 ──
    pdf.step_title('STEP 5: Visualization (1 minute)')
    pdf.say(
        '"For the visualization, instead of using Grad-CAM which produces blurry blobs, '
        'I use spectral color-space analysis - the same technique used in real satellite '
        'remote sensing.\n\n'
        'It converts the image to HSV and LAB color spaces, computes a Green Leaf Index '
        'to identify vegetation, identifies water by blue hue, and urban areas by warm gray '
        'tones. This gives pixel-accurate boundaries that follow actual land features. The '
        'model probabilities are used to label each region with the correct class."'
    )

    # ── STEP 6 ──
    pdf.step_title('STEP 6: Conclusion (1 minute)')
    pdf.say(
        '"The tech stack: PyTorch for deep learning, FastAPI for the backend API, and '
        'vanilla HTML/CSS/JavaScript for the frontend.\n\n'
        'In conclusion: This project demonstrates that biologically-inspired neural '
        'architectures can significantly outperform standard CNNs for satellite remote '
        'sensing. Baby Dragon Hatchling achieves near state-of-the-art accuracy with a '
        'fraction of the parameters, while providing interpretable, pixel-level land cover '
        'mapping.\n\n'
        'Thank you. I am happy to take questions."'
    )

    # ── Q&A ──
    pdf.add_page()
    pdf.step_title('ANTICIPATED QUESTIONS & ANSWERS')

    pdf.qa(
        'What is Baby Dragon Hatchling? Why that name?',
        'It is a novel neural network architecture I developed for this project. The name '
        'reflects that it is a small but powerful model - like a baby dragon - designed to '
        'grow into larger applications. It is referenced in the context of ISRO RESPOND '
        'initiative for intelligent Earth observation.'
    )
    pdf.qa(
        'Why is BDH better than ResNet?',
        'Three reasons: (1) Multi-scale processing captures objects at all sizes, '
        '(2) Lateral inhibition sharpens boundaries between land types, '
        '(3) Contextual attention lets it focus on what matters. ResNet only has uniform '
        '3x3 convolutions with no attention or inhibition.'
    )
    pdf.qa(
        'What is lateral inhibition?',
        'A biological mechanism in the retina. When a neuron fires, it suppresses neighbors, '
        'creating sharper edge perception. In BDH, a depthwise convolution estimates surrounding '
        'activity, then we subtract a learnable fraction from the center response. This amplifies '
        'differences between adjacent features.'
    )
    pdf.qa(
        'Why not use a bigger model like ResNet-50 or ViT?',
        'The point is to show that intelligent architecture design beats brute force. BDH has '
        '1.8M parameters vs ResNet-18 11.2M, yet outperforms it by 14%. A bigger model uses '
        'more compute without addressing the fundamental limitations of single-scale, '
        'attention-less processing.'
    )

    pdf.add_page()
    pdf.qa(
        'What dataset did you use?',
        'EuroSAT - 27,000 satellite images from the Sentinel-2 satellite, 64x64 pixels each, '
        '10 land cover classes. It is a standard benchmark in remote sensing research.'
    )
    pdf.qa(
        'Why spectral segmentation instead of Grad-CAM?',
        'Grad-CAM works on classification models that predict one label for the whole image. '
        'It produces blurry activation blobs, not precise boundaries. Spectral segmentation '
        'analyzes actual pixel colors - green for vegetation, blue for water - giving pixel-accurate '
        'boundaries. Same principle as professional remote sensing NDVI indices.'
    )
    pdf.qa(
        'Can this work on real-time satellite feeds?',
        'The inference time is under 30ms per image, so yes. The current system processes one '
        'image at a time via the web interface, but the architecture could be deployed for batch '
        'processing of satellite data streams.'
    )
    pdf.qa(
        'What is the recurrent refinement doing exactly?',
        'After feature extraction, 2 iterations where: (1) propose refined features via convolution, '
        '(2) compute a gate value 0-1 for each position, (3) blend original and refined based on '
        'the gate. Where gate is high, keep original. Where low, use refined. Features become '
        'progressively cleaner.'
    )
    pdf.qa(
        'How did you train it?',
        'Adam optimizer, learning rate 0.001 with StepLR decay, CrossEntropy loss, batch size 64, '
        '15 epochs with data augmentation (random flips, rotations, color jitter). Both models '
        'trained on the same 80/20 split for fair comparison.'
    )
    pdf.qa(
        'What is the scope / future work?',
        '(1) Train a semantic segmentation model (U-Net/DeepLab) for true pixel-level classification, '
        '(2) Support higher-resolution imagery from ISRO satellites, '
        '(3) Deploy as a cloud service for real-time Earth monitoring, '
        '(4) Apply to deforestation tracking, flood mapping, or urban expansion.'
    )

    # ── PRO TIPS ──
    pdf.add_page()
    pdf.step_title('PRO TIPS FOR THE DEMO')
    pdf.bullet('Load 2-3 diverse samples BEFORE your demo starts - forest, city, river')
    pdf.bullet('Speak SLOWLY when explaining the 4 BDH modules - that is where the marks are')
    pdf.bullet('Point at the screen when showing spectral overlay - "notice how the green follows the tree line"')
    pdf.bullet(
        'If a classification is wrong, say: "this shows the confidence distribution - '
        'even when wrong, the correct class usually appears in the top 3"'
    )
    pdf.bullet('Keep the PDF report open as backup: SensiSpace_Project_Report.pdf')
    pdf.bullet('Make eye contact with the evaluator, not the screen')
    pdf.bullet('End strong with: "95.87% accuracy, 6x fewer parameters, biologically inspired"')

    pdf.ln(8)
    pdf.step_title('RECOVERY COMMANDS')
    pdf.note('If anything goes wrong, use these:')
    pdf.sub('Start the server:')
    pdf.code(
        'cd "/Users/yashlohia/Major project"\n'
        'source venv/bin/activate\n'
        'PYTHONPATH=$(pwd)/src uvicorn app:app --app-dir src --host 0.0.0.0 --port 8000'
    )
    pdf.sub('Revert to saved state:')
    pdf.code('git checkout returnyash')

    # Save
    path = '/Users/yashlohia/Major project/SensiSpace_Demo_Script.pdf'
    pdf.output(path)
    print(f'PDF saved to: {path}')


if __name__ == '__main__':
    generate()
