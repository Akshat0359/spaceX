#!/usr/bin/env python3
"""Generate an attractive, clean Gantt chart PDF with real dates and milestones."""

from fpdf import FPDF
from datetime import date, timedelta


# ── DATE CONFIGURATION ──
START = date(2026, 3, 12)
PHASE1_END = date(2026, 3, 27)
PHASE2_END = date(2026, 4, 23)
PHASE3_END = date(2026, 5, 9)
TOTAL_DAYS = (PHASE3_END - START).days

# Colors
P1_CLR = (67, 133, 244)    # Google Blue
P2_CLR = (251, 166, 36)    # Amber
P3_CLR = (52, 199, 136)    # Teal Green
ACCENT = (94, 53, 177)     # Deep Purple
MILE_CLR = (234, 67, 53)   # Red milestone diamond
BG_LIGHT = (250, 250, 254)
BG_ALT = (244, 244, 250)


class GanttPDF(FPDF):
    def footer(self):
        self.set_y(-12)
        self.set_font('Helvetica', '', 7)
        self.set_text_color(170, 170, 170)
        self.cell(0, 8, f'SensiSpace Project Timeline  |  Page {self.page_no()}/{{nb}}', align='C')


def day_num(d):
    return (d - START).days


def draw_bar(pdf, x, y, w, h, r, g, b, rounded=True):
    """Draw a colored bar with slight gradient effect."""
    pdf.set_fill_color(r, g, b)
    pdf.set_draw_color(max(0, r-30), max(0, g-30), max(0, b-30))
    pdf.set_line_width(0.15)
    pdf.rect(x, y, w, h, 'FD')
    # Highlight strip on top
    pdf.set_fill_color(min(255, r+40), min(255, g+40), min(255, b+40))
    pdf.rect(x, y, w, h * 0.3, 'F')


def draw_milestone(pdf, x, y, size=3):
    """Draw a red diamond milestone marker."""
    r, g, b = MILE_CLR
    pdf.set_fill_color(r, g, b)
    # Diamond shape using polygon
    points = [
        (x, y - size),
        (x + size, y),
        (x, y + size),
        (x - size, y),
    ]
    # Use lines to draw diamond
    pdf.set_draw_color(r, g, b)
    pdf.set_line_width(0.3)
    for i in range(4):
        x1, y1 = points[i]
        x2, y2 = points[(i+1) % 4]
        pdf.line(x1, y1, x2, y2)


def generate():
    pdf = GanttPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=18)

    # ═══════════════════════════════════════
    # TITLE PAGE
    # ═══════════════════════════════════════
    pdf.add_page()
    pdf.ln(30)

    # Decorative top line
    pdf.set_draw_color(*ACCENT)
    pdf.set_line_width(2)
    pdf.line(30, 35, 180, 35)
    pdf.ln(12)

    pdf.set_font('Helvetica', 'B', 34)
    pdf.set_text_color(*ACCENT)
    pdf.cell(0, 16, 'SensiSpace', align='C', new_x="LMARGIN", new_y="NEXT")

    pdf.set_font('Helvetica', '', 14)
    pdf.set_text_color(100, 100, 110)
    pdf.cell(0, 9, 'Project Development Timeline', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(130, 130, 140)
    pdf.cell(0, 7, 'Satellite Land Cover Classification using Deep Learning', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(12)

    # Date range box
    pdf.set_draw_color(*ACCENT)
    pdf.set_line_width(0.4)
    bx, by, bw, bh = 35, pdf.get_y(), 140, 14
    pdf.rect(bx, by, bw, bh, 'D')
    pdf.set_xy(bx, by + 3)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(*ACCENT)
    pdf.cell(bw, 8, f'{START.strftime("%B %d, %Y")}  -  {PHASE3_END.strftime("%B %d, %Y")}  ({TOTAL_DAYS} days)', align='C')
    pdf.ln(22)

    # Phase cards
    phases_info = [
        ('Phase 1', 'Research & Design', START, PHASE1_END, P1_CLR),
        ('Phase 2', 'Development & Deployment', PHASE1_END + timedelta(1), PHASE2_END, P2_CLR),
        ('Phase 3', 'Testing & Documentation', PHASE2_END + timedelta(1), PHASE3_END, P3_CLR),
    ]

    for pname, pdesc, ps, pe, (r, g, b) in phases_info:
        days = (pe - ps).days + 1
        # Card background
        pdf.set_fill_color(r, g, b)
        cy = pdf.get_y()
        pdf.rect(25, cy, 5, 16, 'F')  # Color strip
        pdf.set_draw_color(220, 220, 225)
        pdf.rect(30, cy, 145, 16, 'D')

        pdf.set_xy(33, cy + 2)
        pdf.set_font('Helvetica', 'B', 11)
        pdf.set_text_color(r, g, b)
        pdf.cell(40, 6, pname)
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(70, 70, 70)
        pdf.cell(50, 6, pdesc)
        pdf.set_font('Helvetica', '', 9)
        pdf.set_text_color(120, 120, 120)
        pdf.cell(50, 6, f'{ps.strftime("%b %d")} - {pe.strftime("%b %d")}  ({days}d)', align='R')

        pdf.ln(20)

    # Key milestones summary
    pdf.ln(5)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(*ACCENT)
    pdf.cell(0, 8, 'Key Milestones', new_x="LMARGIN", new_y="NEXT")
    pdf.set_draw_color(*ACCENT)
    pdf.set_line_width(0.3)
    pdf.line(10, pdf.get_y(), 80, pdf.get_y())
    pdf.ln(4)

    milestones = [
        (PHASE1_END, 'M1: Architecture Design Complete'),
        (date(2026, 4, 8), 'M2: Models Trained & Validated'),
        (PHASE2_END, 'M3: Web Application Deployed'),
        (PHASE3_END, 'M4: Final Report & Demo Ready'),
    ]

    for md, mlabel in milestones:
        pdf.set_font('Helvetica', 'B', 9)
        pdf.set_text_color(*MILE_CLR)
        pdf.cell(25, 6, md.strftime('%b %d'))
        pdf.set_font('Helvetica', '', 9)
        pdf.set_text_color(60, 60, 60)
        pdf.cell(0, 6, mlabel, new_x="LMARGIN", new_y="NEXT")

    # ═══════════════════════════════════════
    # GANTT CHART
    # ═══════════════════════════════════════
    pdf.add_page()

    # Title
    pdf.set_font('Helvetica', 'B', 15)
    pdf.set_text_color(*ACCENT)
    pdf.cell(0, 10, 'Gantt Chart', new_x="LMARGIN", new_y="NEXT")
    pdf.set_draw_color(*ACCENT)
    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y(), 60, pdf.get_y())
    pdf.ln(5)

    # Legend
    pdf.set_font('Helvetica', '', 7)
    for label, (r, g, b) in [('Phase 1', P1_CLR), ('Phase 2', P2_CLR), ('Phase 3', P3_CLR)]:
        pdf.set_fill_color(r, g, b)
        pdf.rect(pdf.get_x(), pdf.get_y() + 1.5, 5, 3, 'F')
        pdf.cell(7, 5, '')
        pdf.set_text_color(80, 80, 80)
        pdf.cell(25, 5, label)
    # Milestone legend
    pdf.set_text_color(*MILE_CLR)
    pdf.set_font('Helvetica', 'B', 8)
    pdf.cell(5, 5, ' ')
    pdf.cell(25, 5, 'Milestone')
    pdf.ln(8)

    # Chart dimensions
    label_w = 50
    chart_x = label_w + 5
    chart_w = 200 - chart_x - 5
    day_w = chart_w / TOTAL_DAYS
    row_h = 7.5
    y_start = pdf.get_y()

    # Month headers
    pdf.set_font('Helvetica', 'B', 7)
    months = [
        (date(2026, 3, 12), date(2026, 3, 31), 'MARCH'),
        (date(2026, 4, 1), date(2026, 4, 30), 'APRIL'),
        (date(2026, 5, 1), date(2026, 5, 9), 'MAY'),
    ]
    for ms, me, mname in months:
        mx = chart_x + day_num(ms) * day_w
        mw = (min(day_num(me), TOTAL_DAYS) - day_num(ms) + 1) * day_w
        pdf.set_text_color(100, 100, 110)
        pdf.text(mx + mw/2 - 5, y_start - 5, mname)

    # Date ticks
    pdf.set_font('Helvetica', '', 5)
    pdf.set_text_color(150, 150, 155)
    d = START
    while d <= PHASE3_END:
        if d.day in [1, 5, 10, 15, 20, 25]:
            x = chart_x + day_num(d) * day_w
            pdf.text(x - 2.5, y_start - 1, d.strftime('%d'))
        d += timedelta(1)

    # Tasks definition
    tasks = [
        # Phase 1
        ('Literature survey', date(2026, 3, 12), date(2026, 3, 17), P1_CLR),
        ('Dataset analysis', date(2026, 3, 14), date(2026, 3, 18), P1_CLR),
        ('Architecture design', date(2026, 3, 17), date(2026, 3, 23), P1_CLR),
        ('Environment setup', date(2026, 3, 19), date(2026, 3, 21), P1_CLR),
        ('Data pipeline', date(2026, 3, 22), date(2026, 3, 26), P1_CLR),
        ('Design validation', date(2026, 3, 25), date(2026, 3, 27), P1_CLR),
        None,  # spacer
        # Phase 2
        ('ResNet-18 implementation', date(2026, 3, 28), date(2026, 4, 1), P2_CLR),
        ('BDH architecture coding', date(2026, 3, 30), date(2026, 4, 6), P2_CLR),
        ('Training pipeline', date(2026, 4, 2), date(2026, 4, 5), P2_CLR),
        ('Model training (15 epochs)', date(2026, 4, 5), date(2026, 4, 10), P2_CLR),
        ('Hyperparameter tuning', date(2026, 4, 9), date(2026, 4, 12), P2_CLR),
        ('Spectral segmentation', date(2026, 4, 11), date(2026, 4, 15), P2_CLR),
        ('Backend API (FastAPI)', date(2026, 4, 14), date(2026, 4, 17), P2_CLR),
        ('Frontend UI design', date(2026, 4, 16), date(2026, 4, 20), P2_CLR),
        ('Integration & testing', date(2026, 4, 20), date(2026, 4, 22), P2_CLR),
        ('Deployment', date(2026, 4, 22), date(2026, 4, 23), P2_CLR),
        None,  # spacer
        # Phase 3
        ('Performance optimization', date(2026, 4, 24), date(2026, 4, 28), P3_CLR),
        ('Extended testing', date(2026, 4, 27), date(2026, 5, 1), P3_CLR),
        ('Documentation & report', date(2026, 4, 30), date(2026, 5, 5), P3_CLR),
        ('Demo preparation', date(2026, 5, 4), date(2026, 5, 7), P3_CLR),
        ('Final review & submission', date(2026, 5, 7), date(2026, 5, 9), P3_CLR),
    ]

    total_rows = len(tasks)

    # Phase background bands
    phase_ranges = [
        (0, 6, P1_CLR),
        (7, 17, P2_CLR),
        (18, total_rows, P3_CLR),
    ]
    for rs, re, (r, g, b) in phase_ranges:
        pdf.set_fill_color(r, g, b)
        pdf.rect(chart_x + day_num(
            [START, PHASE1_END + timedelta(1), PHASE2_END + timedelta(1)][phase_ranges.index((rs, re, (r, g, b)))]
        ) * day_w, y_start, (
            [day_num(PHASE1_END)+1, day_num(PHASE2_END) - day_num(PHASE1_END),
             day_num(PHASE3_END) - day_num(PHASE2_END)][phase_ranges.index((rs, re, (r, g, b)))]
        ) * day_w, total_rows * row_h, 'F')

    # Make bands very subtle
    for i, (rs, re, (r, g, b)) in enumerate(phase_ranges):
        start_dates = [START, PHASE1_END + timedelta(1), PHASE2_END + timedelta(1)]
        end_dates = [PHASE1_END, PHASE2_END, PHASE3_END]
        sd = day_num(start_dates[i])
        ed = day_num(end_dates[i]) + 1
        pdf.set_fill_color(min(255, r+180), min(255, g+180), min(255, b+180))
        pdf.rect(chart_x + sd * day_w, y_start, (ed - sd) * day_w, total_rows * row_h, 'F')

    # Vertical grid
    pdf.set_draw_color(230, 230, 235)
    pdf.set_line_width(0.08)
    d = START
    while d <= PHASE3_END:
        if d.day in [1, 10, 20]:
            x = chart_x + day_num(d) * day_w
            pdf.line(x, y_start, x, y_start + total_rows * row_h)
        d += timedelta(1)

    # Phase divider lines
    pdf.set_draw_color(180, 180, 190)
    pdf.set_line_width(0.2)
    pdf.set_dash_pattern(dash=1.5, gap=1)
    for pd_date in [PHASE1_END + timedelta(1), PHASE2_END + timedelta(1)]:
        x = chart_x + day_num(pd_date) * day_w
        pdf.line(x, y_start - 2, x, y_start + total_rows * row_h)
    pdf.set_dash_pattern()

    # Horizontal row lines
    pdf.set_draw_color(240, 240, 242)
    pdf.set_line_width(0.06)
    for i in range(total_rows + 1):
        y = y_start + i * row_h
        pdf.line(10, y, 200, y)

    # Draw task bars
    for i, task in enumerate(tasks):
        y = y_start + i * row_h

        if task is None:
            continue

        label, ts, te, (r, g, b) = task
        dn_s = day_num(ts)
        dur = (te - ts).days + 1

        # Label
        pdf.set_font('Helvetica', '', 6.5)
        pdf.set_text_color(50, 50, 55)
        pdf.text(11, y + 5, label)

        # Bar
        bx = chart_x + dn_s * day_w
        bw = dur * day_w
        draw_bar(pdf, bx, y + 1.5, bw, row_h - 3, r, g, b)

        # Duration label in bar
        if bw > 12:
            pdf.set_font('Helvetica', 'B', 5)
            pdf.set_text_color(255, 255, 255)
            pdf.text(bx + bw/2 - 3, y + 5, f'{dur}d')

    # Milestone diamonds
    milestones_chart = [
        (PHASE1_END, 5),     # M1 at row 5
        (date(2026, 4, 10), 10),  # M2 at row 10
        (PHASE2_END, 16),    # M3 at row 16
        (PHASE3_END, 22),    # M4 at row 22
    ]
    for md, row in milestones_chart:
        if row < total_rows:
            mx = chart_x + day_num(md) * day_w
            my = y_start + row * row_h + row_h / 2
            draw_milestone(pdf, mx, my, 2.5)

    pdf.set_y(y_start + total_rows * row_h + 5)

    # Milestone key below chart
    pdf.ln(3)
    pdf.set_font('Helvetica', 'B', 8)
    pdf.set_text_color(*ACCENT)
    pdf.cell(0, 6, 'Milestones & Deliverables', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)

    for md, mlabel in [
        (PHASE1_END, 'M1: Architecture Design Complete - BDH architecture finalized, dataset ready'),
        (date(2026, 4, 10), 'M2: Models Trained - ResNet: 81.98%, BDH: 95.87% accuracy achieved'),
        (PHASE2_END, 'M3: Web App Deployed - Full-stack application with spectral visualization'),
        (PHASE3_END, 'M4: Project Complete - Final report, demo script, all documentation'),
    ]:
        pdf.set_font('Helvetica', 'B', 7)
        pdf.set_text_color(*MILE_CLR)
        pdf.cell(18, 5, md.strftime('%b %d'))
        pdf.set_font('Helvetica', '', 7)
        pdf.set_text_color(60, 60, 65)
        pdf.cell(0, 5, mlabel, new_x="LMARGIN", new_y="NEXT")

    # ═══════════════════════════════════════
    # PHASE 1 DETAIL
    # ═══════════════════════════════════════
    pdf.add_page()
    r, g, b = P1_CLR
    pdf.set_fill_color(r, g, b)
    pdf.rect(10, 18, 190, 2, 'F')
    pdf.ln(2)
    pdf.set_font('Helvetica', 'B', 16)
    pdf.set_text_color(r, g, b)
    pdf.cell(0, 10, 'Phase 1: Research & Design', new_x="LMARGIN", new_y="NEXT")
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(110, 110, 115)
    pdf.cell(0, 6,
        f'{START.strftime("%B %d")} - {PHASE1_END.strftime("%B %d, %Y")}  |  '
        f'{(PHASE1_END - START).days + 1} days', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)

    # Tasks table
    col_w = [28, 85, 50]
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_fill_color(r, g, b)
    pdf.set_text_color(255, 255, 255)
    for c, w in zip(['Duration', 'Task', 'Deliverable'], col_w):
        pdf.cell(w, 8, c, border=1, fill=True, align='C')
    pdf.ln()

    p1_tasks = [
        ('Mar 12 - 17', 'Literature & reference survey', 'Research notes'),
        ('', '  CNN architectures (ResNet, VGG, Inception)', ''),
        ('', '  Attention mechanisms (SE-Net, CBAM)', ''),
        ('', '  Lateral inhibition in neuroscience', ''),
        ('', '  Remote sensing classification papers', ''),
        ('Mar 14 - 18', 'EuroSAT dataset analysis', 'Dataset report'),
        ('', '  27,000 images, 10 classes, Sentinel-2', ''),
        ('Mar 17 - 23', 'BDH architecture design', 'Architecture diagram'),
        ('', '  Multi-Scale Feature Pyramid (3x3/5x5/7x7)', ''),
        ('', '  Lateral Inhibition Block', ''),
        ('', '  Contextual Attention (channel + spatial)', ''),
        ('', '  Recurrent Refinement (gated feedback)', ''),
        ('Mar 19 - 21', 'Environment & dependency setup', 'Dev environment'),
        ('Mar 22 - 26', 'Data pipeline & augmentation', 'Data loading code'),
        ('', '  80/20 split, flips, rotation, color jitter', ''),
        ('Mar 25 - 27', 'Architecture review & validation', 'Validated design'),
    ]

    for dur, task, deliv in p1_tasks:
        is_main = bool(dur)
        pdf.set_font('Helvetica', 'B' if is_main else '', 8)
        pdf.set_fill_color(240, 245, 255) if is_main else pdf.set_fill_color(250, 252, 255)
        pdf.set_text_color(r, g, b) if is_main else pdf.set_text_color(100, 100, 105)
        pdf.cell(col_w[0], 6, dur, border=1 if is_main else 0, fill=is_main)
        pdf.set_text_color(40, 40, 45) if is_main else pdf.set_text_color(100, 100, 105)
        pdf.cell(col_w[1], 6, task, border=1 if is_main else 0, fill=is_main)
        pdf.set_font('Helvetica', 'I', 8)
        pdf.set_text_color(110, 110, 115)
        pdf.cell(col_w[2], 6, deliv, border=1 if is_main else 0, fill=is_main)
        pdf.ln()

    # Milestone box
    pdf.ln(5)
    pdf.set_draw_color(r, g, b)
    pdf.set_fill_color(235, 243, 255)
    pdf.rect(10, pdf.get_y(), 190, 12, 'FD')
    pdf.set_xy(14, pdf.get_y() + 2)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_text_color(*MILE_CLR)
    pdf.cell(5, 4, '')
    pdf.set_text_color(r, g, b)
    pdf.cell(0, 8, f'Milestone M1 ({PHASE1_END.strftime("%b %d")}): Architecture finalized, dataset preprocessed, dev environment ready')

    # ═══════════════════════════════════════
    # PHASE 2 DETAIL
    # ═══════════════════════════════════════
    pdf.add_page()
    r, g, b = P2_CLR
    pdf.set_fill_color(r, g, b)
    pdf.rect(10, 18, 190, 2, 'F')
    pdf.ln(2)
    pdf.set_font('Helvetica', 'B', 16)
    pdf.set_text_color(r, g, b)
    pdf.cell(0, 10, 'Phase 2: Development & Deployment', new_x="LMARGIN", new_y="NEXT")
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(110, 110, 115)
    p2s = PHASE1_END + timedelta(1)
    pdf.cell(0, 6,
        f'{p2s.strftime("%B %d")} - {PHASE2_END.strftime("%B %d, %Y")}  |  '
        f'{(PHASE2_END - p2s).days + 1} days', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)

    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_fill_color(r, g, b)
    pdf.set_text_color(255, 255, 255)
    for c, w in zip(['Duration', 'Task', 'Deliverable'], col_w):
        pdf.cell(w, 8, c, border=1, fill=True, align='C')
    pdf.ln()

    p2_tasks = [
        ('Mar 28 - Apr 1', 'ResNet-18 baseline implementation', 'resnet.py'),
        ('', '  Pretrained ImageNet, FC: 512 -> 10', ''),
        ('Mar 30 - Apr 6', 'BDH architecture coding', 'baby_dragon.py'),
        ('', '  MultiScaleBlock, LateralInhibition', ''),
        ('', '  ContextualAttention, RecurrentRefinement', ''),
        ('Apr 2 - 5', 'Training pipeline development', 'train.py'),
        ('', '  Adam, LR=0.001, StepLR, CrossEntropy', ''),
        ('Apr 5 - 10', 'Model training (15 epochs each)', 'Trained weights'),
        ('', '  ResNet-18: 81.98% accuracy', ''),
        ('', '  BDH: 95.87% accuracy', ''),
        ('Apr 9 - 12', 'Hyperparameter tuning', 'Optimized config'),
        ('Apr 11 - 15', 'Spectral segmentation module', 'gradcam.py'),
        ('', '  HSV/LAB analysis, Green Leaf Index', ''),
        ('Apr 14 - 17', 'Backend API development', 'app.py'),
        ('', '  /predict, /sample, /metrics, /colors', ''),
        ('Apr 16 - 20', 'Frontend UI development', 'HTML/CSS/JS'),
        ('', '  3-tab dark-mode interface, charts', ''),
        ('Apr 20 - 22', 'Integration & end-to-end testing', 'Working app'),
        ('Apr 22 - 23', 'Deployment & verification', 'Deployed system'),
    ]

    for dur, task, deliv in p2_tasks:
        is_main = bool(dur)
        pdf.set_font('Helvetica', 'B' if is_main else '', 8)
        pdf.set_fill_color(255, 245, 225) if is_main else pdf.set_fill_color(255, 250, 240)
        pdf.set_text_color(r, g, b) if is_main else pdf.set_text_color(100, 100, 105)
        pdf.cell(col_w[0], 6, dur, border=1 if is_main else 0, fill=is_main)
        pdf.set_text_color(40, 40, 45) if is_main else pdf.set_text_color(100, 100, 105)
        pdf.cell(col_w[1], 6, task, border=1 if is_main else 0, fill=is_main)
        pdf.set_font('Helvetica', 'I', 8)
        pdf.set_text_color(110, 110, 115)
        pdf.cell(col_w[2], 6, deliv, border=1 if is_main else 0, fill=is_main)
        pdf.ln()

    pdf.ln(5)
    pdf.set_draw_color(r, g, b)
    pdf.set_fill_color(255, 245, 225)
    pdf.rect(10, pdf.get_y(), 190, 18, 'FD')
    pdf.set_xy(14, pdf.get_y() + 2)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_text_color(r, g, b)
    pdf.cell(0, 6, f'Milestone M2 (Apr 10): Both models trained - BDH: 95.87%, ResNet: 81.98%')
    pdf.ln(6)
    pdf.set_x(14)
    pdf.cell(0, 6, f'Milestone M3 ({PHASE2_END.strftime("%b %d")}): Full-stack web application deployed with spectral visualization')

    # ═══════════════════════════════════════
    # PHASE 3 DETAIL
    # ═══════════════════════════════════════
    pdf.add_page()
    r, g, b = P3_CLR
    pdf.set_fill_color(r, g, b)
    pdf.rect(10, 18, 190, 2, 'F')
    pdf.ln(2)
    pdf.set_font('Helvetica', 'B', 16)
    pdf.set_text_color(r, g, b)
    pdf.cell(0, 10, 'Phase 3: Testing, Optimization & Documentation', new_x="LMARGIN", new_y="NEXT")
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(110, 110, 115)
    p3s = PHASE2_END + timedelta(1)
    pdf.cell(0, 6,
        f'{p3s.strftime("%B %d")} - {PHASE3_END.strftime("%B %d, %Y")}  |  '
        f'{(PHASE3_END - p3s).days + 1} days', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)

    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_fill_color(r, g, b)
    pdf.set_text_color(255, 255, 255)
    for c, w in zip(['Duration', 'Task', 'Deliverable'], col_w):
        pdf.cell(w, 8, c, border=1, fill=True, align='C')
    pdf.ln()

    p3_tasks = [
        ('Apr 24 - 28', 'Performance optimization', 'Optimized models'),
        ('', '  Inference speed benchmarking', ''),
        ('', '  Memory usage optimization', ''),
        ('Apr 27 - May 1', 'Extended testing & validation', 'Test report'),
        ('', '  Edge case testing', ''),
        ('', '  Cross-browser compatibility', ''),
        ('', '  Error handling verification', ''),
        ('Apr 30 - May 5', 'Documentation & final report', 'Project report PDF'),
        ('', '  Architecture explanation document', ''),
        ('', '  Training results & analysis', ''),
        ('', '  System architecture documentation', ''),
        ('May 4 - 7', 'Demo preparation & rehearsal', 'Demo script PDF'),
        ('', '  Presentation flow & talking points', ''),
        ('', '  Q&A preparation', ''),
        ('May 7 - 9', 'Final review & submission', 'Final deliverables'),
        ('', '  Code review & cleanup', ''),
        ('', '  Final project submission', ''),
    ]

    for dur, task, deliv in p3_tasks:
        is_main = bool(dur)
        pdf.set_font('Helvetica', 'B' if is_main else '', 8)
        pdf.set_fill_color(230, 250, 240) if is_main else pdf.set_fill_color(242, 252, 247)
        pdf.set_text_color(r, g, b) if is_main else pdf.set_text_color(100, 100, 105)
        pdf.cell(col_w[0], 6, dur, border=1 if is_main else 0, fill=is_main)
        pdf.set_text_color(40, 40, 45) if is_main else pdf.set_text_color(100, 100, 105)
        pdf.cell(col_w[1], 6, task, border=1 if is_main else 0, fill=is_main)
        pdf.set_font('Helvetica', 'I', 8)
        pdf.set_text_color(110, 110, 115)
        pdf.cell(col_w[2], 6, deliv, border=1 if is_main else 0, fill=is_main)
        pdf.ln()

    pdf.ln(5)
    pdf.set_draw_color(r, g, b)
    pdf.set_fill_color(225, 248, 238)
    pdf.rect(10, pdf.get_y(), 190, 12, 'FD')
    pdf.set_xy(14, pdf.get_y() + 2)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_text_color(r, g, b)
    pdf.cell(0, 8, f'Milestone M4 ({PHASE3_END.strftime("%b %d")}): Final report submitted, demo presentation complete')

    # ═══════════════════════════════════════
    # MILESTONE SUMMARY
    # ═══════════════════════════════════════
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 15)
    pdf.set_text_color(*ACCENT)
    pdf.cell(0, 10, 'Milestones & Deliverables Summary', new_x="LMARGIN", new_y="NEXT")
    pdf.set_draw_color(*ACCENT)
    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y(), 100, pdf.get_y())
    pdf.ln(8)

    all_milestones = [
        ('M1', PHASE1_END, 'Architecture Design Complete', P1_CLR,
         ['BDH architecture (4 modules) designed and validated',
          'EuroSAT dataset analyzed and preprocessed',
          'Development environment fully configured',
          'Data augmentation pipeline implemented']),
        ('M2', date(2026, 4, 10), 'Models Trained & Validated', P2_CLR,
         ['ResNet-18 fine-tuned: 81.98% accuracy',
          'Baby Dragon Hatchling trained: 95.87% accuracy',
          'Training curves and metrics generated',
          'Spectral segmentation visualization working']),
        ('M3', PHASE2_END, 'Web Application Deployed', P2_CLR,
         ['FastAPI backend with 4 API endpoints',
          'Premium dark-mode frontend (3 tabs)',
          'Color-coded probability distribution charts',
          'End-to-end integration tested']),
        ('M4', PHASE3_END, 'Project Complete', P3_CLR,
         ['Performance optimized and benchmarked',
          'Comprehensive project report (PDF)',
          'Demo script with Q&A preparation',
          'All code documented and submitted']),
    ]

    for mid, mdate, mtitle, (r, g, b), deliverables in all_milestones:
        # Milestone header
        pdf.set_fill_color(r, g, b)
        pdf.rect(10, pdf.get_y(), 4, 22, 'F')

        pdf.set_draw_color(220, 220, 225)
        pdf.rect(14, pdf.get_y(), 186, 22, 'D')

        y0 = pdf.get_y()
        pdf.set_xy(17, y0 + 1)
        pdf.set_font('Helvetica', 'B', 10)
        pdf.set_text_color(r, g, b)
        pdf.cell(15, 6, mid)
        pdf.set_text_color(50, 50, 55)
        pdf.cell(80, 6, mtitle)
        pdf.set_font('Helvetica', '', 9)
        pdf.set_text_color(120, 120, 125)
        pdf.cell(0, 6, mdate.strftime('%B %d, %Y'), align='R')

        pdf.set_xy(17, y0 + 8)
        pdf.set_font('Helvetica', '', 7.5)
        pdf.set_text_color(80, 80, 85)
        for i, d in enumerate(deliverables):
            pdf.set_x(20)
            pdf.cell(85, 4, '- ' + d)
            if i < len(deliverables) - 1 and (i % 2 == 1):
                pdf.ln(3.5)
            elif i % 2 == 0 and i + 1 < len(deliverables):
                pass  # next item on same conceptual line
            else:
                pdf.ln(3.5)

        pdf.set_y(y0 + 26)

    # Save
    path = '/Users/yashlohia/Major project/SensiSpace_Timeline.pdf'
    pdf.output(path)
    print(f'PDF saved to: {path}')


if __name__ == '__main__':
    generate()
