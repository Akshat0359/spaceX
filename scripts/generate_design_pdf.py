import os
#!/usr/bin/env python3
"""Generate Design Document PDF for SpaceX project."""
from fpdf import FPDF

class DesignPDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(100,100,100)
        self.cell(0, 6, 'SpaceX - Design Document', align='R')
        self.ln(3)
        self.set_draw_color(80,60,180)
        self.set_line_width(0.4)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(150,150,150)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

    def section_title(self, title):
        self.set_font('Helvetica', 'B', 15)
        self.set_text_color(80,60,180)
        self.ln(5)
        self.cell(0, 9, title, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(80,60,180)
        self.set_line_width(0.3)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def sub_title(self, title):
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(50,50,50)
        self.ln(3)
        self.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def sub_sub(self, title):
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(80,80,80)
        self.ln(2)
        self.cell(0, 6, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def body(self, text):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(30,30,30)
        self.multi_cell(0, 5.5, text)
        self.ln(2)

    def bullet(self, text, indent=8):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(30,30,30)
        self.set_x(self.l_margin + indent)
        self.multi_cell(self.w - self.l_margin - self.r_margin - indent, 5.5, '- ' + text)
        self.ln(0.5)

    def bold_bullet(self, bold, normal, indent=8):
        self.set_x(self.l_margin + indent)
        self.set_font('Helvetica', '', 10)
        self.set_text_color(30,30,30)
        self.write(5.5, '- ')
        self.set_font('Helvetica', 'B', 10)
        self.write(5.5, bold)
        self.set_font('Helvetica', '', 10)
        self.write(5.5, normal)
        self.ln(7)

    def code(self, text):
        self.set_font('Courier', '', 8)
        self.set_fill_color(235,235,240)
        self.set_text_color(30,30,30)
        self.multi_cell(0, 4.5, text, fill=True)
        self.ln(2)

    def trow(self, cols, widths, header=False):
        h = 6
        if header:
            self.set_font('Helvetica', 'B', 8)
            self.set_fill_color(80,60,180)
            self.set_text_color(255,255,255)
        else:
            self.set_font('Helvetica', '', 8)
            self.set_fill_color(248,248,252)
            self.set_text_color(30,30,30)
        for i, (c, w) in enumerate(zip(cols, widths)):
            self.cell(w, h, str(c), border=1, fill=True, align='C' if i > 0 else 'L')
        self.ln()

    def trow_wrap(self, cols, widths, header=False):
        """Table row with text wrapping for longer content."""
        if header:
            self.set_font('Helvetica', 'B', 8)
            self.set_fill_color(80,60,180)
            self.set_text_color(255,255,255)
        else:
            self.set_font('Helvetica', '', 8)
            self.set_fill_color(248,248,252)
            self.set_text_color(30,30,30)

        # Calculate max height needed
        x_start = self.get_x()
        y_start = self.get_y()
        max_h = 6
        for c, w in zip(cols, widths):
            nb = self.multi_cell(w, 5, str(c), border=0, fill=False, split_only=True)
            cell_h = len(nb) * 5
            if cell_h > max_h:
                max_h = cell_h

        # Draw cells with uniform height
        self.set_xy(x_start, y_start)
        for i, (c, w) in enumerate(zip(cols, widths)):
            x = self.get_x()
            y = self.get_y()
            self.rect(x, y, w, max_h)
            if header:
                self.set_fill_color(80,60,180)
            else:
                self.set_fill_color(248,248,252)
            self.rect(x, y, w, max_h, 'F')
            self.rect(x, y, w, max_h, 'D')
            self.set_xy(x + 1, y + 1)
            self.multi_cell(w - 2, 5, str(c), border=0, fill=False)
            self.set_xy(x + w, y)
        self.set_xy(x_start, y_start + max_h)


def generate():
    pdf = DesignPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=18)

    # ═══ TITLE PAGE ═══
    pdf.add_page()
    pdf.ln(40)
    pdf.set_font('Helvetica', 'B', 28)
    pdf.set_text_color(80,60,180)
    pdf.cell(0, 15, 'SpaceX', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.set_font('Helvetica', '', 16)
    pdf.set_text_color(60,60,60)
    pdf.cell(0, 10, 'Design Document', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)
    pdf.set_draw_color(80,60,180)
    pdf.set_line_width(1)
    pdf.line(60, pdf.get_y(), 150, pdf.get_y())
    pdf.ln(8)
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(100,100,100)
    pdf.cell(0, 7, 'Satellite Land Cover Classification System', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, 'Baby Dragon Hatchling vs ResNet-18 on EuroSAT', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(12)
    pdf.set_font('Helvetica', 'I', 11)
    pdf.cell(0, 7, 'ISRO RESPOND Initiative - Major Project', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(30)
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(120,120,120)
    pdf.cell(0, 7, 'Interface Design | Design Decisions | Non-Functional Aspects | SRS Traceability', align='C', new_x="LMARGIN", new_y="NEXT")

    # ═══════════════════════════════════════════════
    # 1. INTERFACE OR INTERACTION DESIGN
    # ═══════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title('1. Interface or Interaction Design')

    # --- 1A. Frontend UI ---
    pdf.sub_title('1.1 Frontend UI Design')
    pdf.body(
        'The SpaceX web application uses a premium dark-mode single-page interface '
        'built with HTML5, CSS3 (glassmorphism design), and vanilla JavaScript. The interface '
        'is designed for intuitive satellite image analysis with real-time feedback.'
    )

    pdf.sub_sub('Layout Structure')
    w = [40, 90]
    pdf.trow(['Section', 'Purpose'], w, header=True)
    pdf.trow(['Header', 'Sticky navbar with SpaceX logo + ISRO RESPOND badge'], w)
    pdf.trow(['Hero', 'Title + subtitle explaining the project at a glance'], w)
    pdf.trow(['Upload Section', 'Drag-and-drop zone + file picker + sample loader'], w)
    pdf.trow(['Results (3 tabs)', 'ResNet-18 / Baby Dragon Hatchling / Comparison'], w)
    pdf.trow(['Footer', 'Project attribution and tech stack'], w)
    pdf.ln(3)

    pdf.sub_sub('User Interaction Flow')
    pdf.code(
        'User lands on page\n'
        '  -> Uploads satellite image (drag-drop or file picker)\n'
        '     OR clicks "Load Random EuroSAT Sample"\n'
        '  -> Clicks "Run Classification"\n'
        '  -> System shows loading spinner\n'
        '  -> Results appear in 3 tabs:\n'
        '      Tab 1: ResNet-18 prediction + confidence + overlay + chart\n'
        '      Tab 2: BDH prediction + confidence + overlay + chart\n'
        '      Tab 3: Side-by-side comparison + benchmark table + legend'
    )

    pdf.sub_sub('UI Design Elements')
    pdf.bold_bullet('Glassmorphism: ', 'Semi-transparent cards with backdrop-filter blur(24px) for depth')
    pdf.bold_bullet('Animated Background: ', '3 colored gradient orbs (purple, blue, green) for visual richness')
    pdf.bold_bullet('Color-Coded Results: ', 'Each land cover class has unique bright RGB color across strips, bars, overlays')
    pdf.bold_bullet('Micro-Animations: ', 'Fade-up on load, hover effects, animated probability bars, loading spinner')
    pdf.bold_bullet('Responsive Design: ', 'CSS media queries at 640px for mobile adaptation')
    pdf.bold_bullet('Typography: ', 'Inter (body) + Outfit (headings) from Google Fonts')

    # --- 1B. API Design ---
    pdf.add_page()
    pdf.sub_title('1.2 API Design (RESTful)')
    pdf.body(
        'The backend is built with FastAPI (Python ASGI framework), serving both the ML models '
        'and the static frontend files. CORS middleware is enabled for cross-origin requests.'
    )

    w2 = [28, 12, 50, 40]
    pdf.trow(['Endpoint', 'Method', 'Output', 'Purpose'], w2, header=True)
    pdf.trow(['/api/predict', 'POST', 'JSON: both models results + overlay', 'Core classification'], w2)
    pdf.trow(['/api/sample', 'GET', 'JPEG image file', 'Random EuroSAT sample'], w2)
    pdf.trow(['/api/metrics', 'GET', 'JSON: accuracy, F1, params etc.', 'Training benchmarks'], w2)
    pdf.trow(['/api/colors', 'GET', 'JSON: {class: [R,G,B]}', 'Color palette'], w2)
    pdf.trow(['/api/health', 'GET', 'JSON: {status, loaded}', 'Health check'], w2)
    pdf.ln(3)

    pdf.sub_sub('API Response Structure (/api/predict)')
    pdf.code(
        '{\n'
        '  "resnet": {\n'
        '    "prediction": "Forest",\n'
        '    "confidence": 0.8734,\n'
        '    "inference_ms": 0.18,\n'
        '    "all_probs": {"Forest": 0.87, "River": 0.05, ...},\n'
        '    "color": [34, 220, 77],\n'
        '    "description": "Dense tree cover...",\n'
        '    "cam_image": "data:image/jpeg;base64,..."\n'
        '  },\n'
        '  "baby_dragon": { /* same structure */ }\n'
        '}'
    )

    # --- 1C. Integrations ---
    pdf.sub_title('1.3 Integrations')
    w3 = [40, 90]
    pdf.trow(['Integration', 'Purpose'], w3, header=True)
    pdf.trow(['PyTorch', 'Model loading, inference, tensor operations'], w3)
    pdf.trow(['torchvision', 'EuroSAT dataset, transforms, ResNet-18 weights'], w3)
    pdf.trow(['OpenCV', 'HSV/LAB conversion, morphology, contour detection'], w3)
    pdf.trow(['Pillow (PIL)', 'Image I/O, overlay rendering, label drawing'], w3)
    pdf.trow(['scikit-learn', 'Accuracy, precision, recall, F1 computation'], w3)
    pdf.trow(['Uvicorn', 'ASGI server for FastAPI deployment'], w3)

    # ═══════════════════════════════════════════════
    # 2. KEY DESIGN DECISIONS
    # ═══════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title('2. Key Design Decisions, Assumptions, and Constraints')

    pdf.sub_title('2.1 Design Decisions')
    w4 = [48, 82]
    pdf.trow(['Decision', 'Rationale'], w4, header=True)
    pdf.trow(['Custom BDH architecture', 'Standard CNNs are not purpose-built for satellite imagery; BDH modules target multi-scale objects and spectral boundaries'], w4)
    pdf.trow(['Spectral segmentation over Grad-CAM', 'Grad-CAM produces blurry 8x8 blobs; HSV/LAB spectral analysis provides pixel-accurate boundaries'], w4)
    pdf.trow(['ResNet-18 frozen base', 'Represents common industry transfer learning approach for fair, realistic baseline comparison'], w4)
    pdf.trow(['64x64 input resolution', 'Matches EuroSAT native resolution; avoids upscaling artifacts; keeps inference fast'], w4)
    pdf.trow(['FastAPI over Flask/Django', 'Async support, auto OpenAPI docs, type validation, better ML model serving performance'], w4)
    pdf.trow(['Vanilla JS (no React/Vue)', 'Simple SPA with limited interactivity; framework adds unnecessary complexity and bundle size'], w4)
    pdf.trow(['Adam + CosineAnnealingLR', 'Adaptive LR for stable convergence; cosine annealing for better final accuracy'], w4)
    pdf.trow(['Dual dropout (0.3 + 0.2)', 'Prevents overfitting on 27K images without excessive regularization'], w4)
    pdf.ln(4)

    pdf.sub_title('2.2 Assumptions')
    w5 = [48, 82]
    pdf.trow(['Assumption', 'Justification'], w5, header=True)
    pdf.trow(['Input images are RGB satellite', 'EuroSAT provides RGB; spectral segmentation relies on color analysis'], w5)
    pdf.trow(['64x64 resolution sufficient', 'EuroSAT benchmark standard; 10m/pixel Sentinel-2 captures land cover'], w5)
    pdf.trow(['10 classes cover primary uses', 'EuroSAT classes represent major land types for ISRO monitoring'], w5)
    pdf.trow(['Single-label classification', 'Each EuroSAT image shows one dominant land type; multi-label is out of scope'], w5)
    pdf.trow(['CPU deployment sufficient', 'Ensures portability; inference is <1ms per image regardless'], w5)
    pdf.ln(4)

    pdf.sub_title('2.3 Constraints')
    w6 = [48, 82]
    pdf.trow(['Constraint', 'Impact and Mitigation'], w6, header=True)
    pdf.trow(['Dataset: 27,000 images', 'Sufficient for proof-of-concept; data augmentation mitigates limited size'], w6)
    pdf.trow(['RGB only (3 channels)', 'Sentinel-2 has 13 bands; future: extend to full multi-spectral'], w6)
    pdf.trow(['Image-level classification', 'Not pixel-level; spectral overlay provides approximate pixel mapping'], w6)
    pdf.trow(['No real-time satellite feed', 'Processes uploaded images only; future: integrate live data streams'], w6)
    pdf.trow(['CPU inference only', 'Limits batch throughput; sufficient for interactive single-image use'], w6)

    # ═══════════════════════════════════════════════
    # 3. NON-FUNCTIONAL ASPECTS
    # ═══════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title('3. Non-Functional Aspects')

    # --- Performance ---
    pdf.sub_title('3.1 Performance')
    w7 = [50, 40, 40]
    pdf.trow(['Metric', 'ResNet-18', 'BDH'], w7, header=True)
    pdf.trow(['Inference latency', '0.18 ms/image', '0.60 ms/image'], w7)
    pdf.trow(['Throughput (theoretical)', '~5,500 img/sec', '~1,666 img/sec'], w7)
    pdf.trow(['Model load time', '< 2 sec', '< 1 sec'], w7)
    pdf.trow(['Frontend load time', '< 1 sec', '< 1 sec'], w7)
    pdf.ln(3)
    pdf.bullet('Both models achieve sub-millisecond inference on CPU -- real-time interactive performance')
    pdf.bullet('FastAPI async architecture prevents blocking during image processing')
    pdf.bullet('Frontend uses lazy rendering -- results section hidden until classification completes')
    pdf.bullet('Probability bar animations use CSS transitions (GPU-accelerated), not JavaScript')
    pdf.ln(3)

    # --- Scalability ---
    pdf.sub_title('3.2 Scalability')
    w8 = [35, 42, 53]
    pdf.trow(['Aspect', 'Current', 'Scalability Path'], w8, header=True)
    pdf.trow(['Concurrent users', 'Single Uvicorn worker', 'Add --workers N or Gunicorn'], w8)
    pdf.trow(['Model serving', 'In-process PyTorch', 'TorchServe / Triton Inference Server'], w8)
    pdf.trow(['Dataset', '27K (EuroSAT)', 'Swap for BigEarthNet (590K images)'], w8)
    pdf.trow(['Classes', '10 (configurable)', 'Change num_classes parameter'], w8)
    pdf.trow(['Image size', '64x64', 'Fully convolutional; works with any size'], w8)
    pdf.trow(['Horizontal scaling', 'Single server', 'Containerize (Docker) + load balance'], w8)
    pdf.ln(3)

    # --- Security ---
    pdf.sub_title('3.3 Security')
    w9 = [42, 88]
    pdf.trow(['Concern', 'Mitigation'], w9, header=True)
    pdf.trow(['CORS policy', 'Currently allow_origins=["*"] for dev; restrict in production'], w9)
    pdf.trow(['File upload validation', 'FastAPI UploadFile + PIL format validation; no raw file writes'], w9)
    pdf.trow(['Authentication', 'None (academic demo); production would add API keys or OAuth'], w9)
    pdf.trow(['Injection attacks', 'No SQL/database; all data in-memory or JSON files -- no injection surface'], w9)
    pdf.trow(['Model weights', 'Stored as .pth files loaded at startup; not exposed via API'], w9)
    pdf.trow(['Input sanitization', 'Fixed transform pipeline (resize, normalize) prevents adversarial inputs'], w9)
    pdf.ln(3)

    # --- Reliability ---
    pdf.sub_title('3.4 Reliability')
    pdf.bullet('Graceful error handling: /api/predict returns HTTP 503 if models not loaded, with descriptive error')
    pdf.bullet('Fallback fonts: Spectral overlay tries Helvetica -> DejaVuSans -> default font')
    pdf.bullet('Auto device detection: Automatically selects CUDA -> MPS -> CPU based on availability')
    pdf.bullet('Startup verification: Logs confirm each model loaded successfully with device info')

    # ═══════════════════════════════════════════════
    # 4. SRS TRACEABILITY
    # ═══════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title('4. Design with Traceability from SRS')

    pdf.sub_title('4.1 Functional Requirements Traceability')
    w10 = [15, 45, 70]
    pdf.trow(['Req ID', 'Requirement', 'Implementation'], w10, header=True)
    pdf.trow(['FR-1', 'Classify satellite images into land cover', 'baby_dragon.py, resnet.py'], w10)
    pdf.trow(['FR-2', 'Support 10 EuroSAT classes', 'CLASS_LABELS in train.py, num_classes=10'], w10)
    pdf.trow(['FR-3', 'Accept user-uploaded images', '#fileInput in index.html, /api/predict POST'], w10)
    pdf.trow(['FR-4', 'Provide sample images for demo', '/api/sample GET in app.py, #sampleBtn'], w10)
    pdf.trow(['FR-5', 'Compare two model architectures', 'Dual run_model() calls in /api/predict'], w10)
    pdf.trow(['FR-6', 'Visualize classification results', 'gradcam.py (spectral), app.js (charts)'], w10)
    pdf.trow(['FR-7', 'Display confidence scores', 'softmax() in app.py, stat-pill in HTML'], w10)
    pdf.trow(['FR-8', 'Show training benchmarks', 'metrics.json, renderMetrics() in app.js'], w10)
    pdf.ln(4)

    pdf.sub_title('4.2 Non-Functional Requirements Traceability')
    w11 = [15, 45, 70]
    pdf.trow(['Req ID', 'Requirement', 'Implementation'], w11, header=True)
    pdf.trow(['NFR-1', 'Real-time inference (<1 sec)', 'BDH: 0.60ms, ResNet: 0.18ms per image'], w11)
    pdf.trow(['NFR-2', 'Responsive UI across devices', '@media (max-width: 640px) in style.css'], w11)
    pdf.trow(['NFR-3', 'Handle missing models gracefully', 'HTTP 503 check in /api/predict'], w11)
    pdf.trow(['NFR-4', 'No external service dependency', 'All inference local; no cloud API calls'], w11)
    pdf.trow(['NFR-5', 'Fast page load', '<1s load; 3 static files, no JS framework'], w11)
    pdf.ln(4)

    pdf.sub_title('4.3 Design Consistency Principles')
    w12 = [45, 85]
    pdf.trow(['Principle', 'How Enforced'], w12, header=True)
    pdf.trow(['Separation of Concerns', 'Models (src/models/), API (app.py), Frontend (static/), Training (train.py) fully separated'], w12)
    pdf.trow(['Single Responsibility', 'Each file has one job: architecture, baseline, visualization, or routing'], w12)
    pdf.trow(['Consistent API responses', 'Both models return identical JSON structure for frontend compatibility'], w12)
    pdf.trow(['Fair training pipeline', 'Both models use same optimizer, LR, loss, augmentation, eval metrics'], w12)
    pdf.trow(['Consistent color scheme', 'LAND_COVER_COLORS shared across backend overlays and frontend charts'], w12)
    pdf.trow(['Modular architecture', 'BDH stages are composable: MultiScale + LateralInhibition + Attention'], w12)

    # Save
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'docs'/SpaceX_Design_Document.pdf'
    pdf.output(out)
    print(f'Design Document PDF saved to: {out}')

if __name__ == '__main__':
    generate()
