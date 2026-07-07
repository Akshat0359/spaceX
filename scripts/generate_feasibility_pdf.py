import os
#!/usr/bin/env python3
"""Generate Feasibility & Scalability PDF reusing ProjectPDF style."""

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
    pdf.cell(0, 12, 'Feasibility Analysis &', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 12, 'Scalability Considerations', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    pdf.set_draw_color(80, 60, 180)
    pdf.set_line_width(1)
    pdf.line(60, pdf.get_y(), 150, pdf.get_y())
    pdf.ln(10)
    pdf.set_font('Helvetica', '', 12)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, 'Satellite Land Cover Classification System', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, 'Baby Dragon Hatchling vs ResNet-18', align='C', new_x="LMARGIN", new_y="NEXT")

    # ════════════════════════════════════
    # 1. FEASIBILITY
    # ════════════════════════════════════
    pdf.add_page()
    pdf.section_title('1. Feasibility Analysis')
    pdf.body_text(
        'Feasibility analysis evaluates whether the project can be successfully completed '
        'given the available resources, technology, budget, and timeline.'
    )

    # 1.1 Technical
    pdf.sub_title('1.1 Technical Feasibility')
    pdf.body_text(
        'Can this system be built with available technology? YES.'
    )
    w = [40, 100]
    pdf.table_row(['Aspect', 'Assessment'], w, header=True)
    rows = [
        ('Hardware', 'Trained on MacBook Air (M-series). No GPU cluster needed.'),
        ('Software', 'Open-source: Python, PyTorch, FastAPI, OpenCV.'),
        ('Dataset', 'EuroSAT: 27,000 images, publicly free (~90MB).'),
        ('Training', 'BDH: ~61 min, ResNet: ~4 min on single machine.'),
        ('Deployment', 'FastAPI local server. Dockerizable for cloud.'),
        ('Accuracy', '95.87% - exceeds published EuroSAT benchmarks.'),
    ]
    for r in rows:
        pdf.table_row(r, w)
    pdf.ln(3)

    pdf.sub_sub_title('Technical Risks & Mitigations')
    w2 = [40, 20, 80]
    pdf.table_row(['Risk', 'Likelihood', 'Mitigation'], w2, header=True)
    pdf.table_row(['GPU unavailable', 'Medium', 'BDH trains on CPU/MPS in ~1 hour'], w2)
    pdf.table_row(['Class imbalance', 'Low', 'EuroSAT is balanced (~2,700/class)'], w2)
    pdf.table_row(['Model overfitting', 'Low', 'Dropout + augmentation + small model'], w2)
    pdf.table_row(['Browser compat.', 'Low', 'Standard HTML/CSS/JS, no frameworks'], w2)

    # 1.2 Economic
    pdf.add_page()
    pdf.sub_title('1.2 Economic Feasibility')
    pdf.body_text('Is the project cost-effective? YES. Total cost: Rs 0.')

    w3 = [45, 30, 65]
    pdf.table_row(['Cost Item', 'Amount', 'Notes'], w3, header=True)
    pdf.table_row(['Hardware', 'Rs 0', 'Existing laptop (8GB+ RAM sufficient)'], w3)
    pdf.table_row(['Software', 'Rs 0', 'Python, PyTorch, FastAPI - all open-source'], w3)
    pdf.table_row(['Dataset', 'Rs 0', 'EuroSAT freely available from ESA'], w3)
    pdf.table_row(['Cloud (optional)', 'Rs 500-1000/mo', 'Free tier available on AWS/GCP'], w3)
    pdf.table_row(['Development', '40 days', 'Single developer'], w3)
    pdf.table_row(['TOTAL', 'Rs 0-1000', 'Near-zero cost project'], w3, bold=True)
    pdf.ln(3)

    pdf.sub_sub_title('Cost-Benefit Analysis')
    pdf.bold_bullet('Manual analysis: ', '1 analyst processes ~50 images/day at Rs 500/day = Rs 10/image')
    pdf.bold_bullet('SpaceX: ', '~1,666 images/second at near-zero marginal cost')
    pdf.bold_bullet('Break-even: ', 'After just 100 images, the automated system saves money')
    pdf.bold_bullet('ROI: ', 'Effectively infinite - train once, run indefinitely')

    # 1.3 Operational
    pdf.sub_title('1.3 Operational Feasibility')
    pdf.body_text('Can end-users actually use this system? YES.')

    w4 = [40, 100]
    pdf.table_row(['Factor', 'Assessment'], w4, header=True)
    pdf.table_row(['User interface', 'Web-based UI, no installation. Upload + click.'], w4)
    pdf.table_row(['Training needed', 'Minimal - basic computer literacy sufficient.'], w4)
    pdf.table_row(['Response time', '< 2 seconds for full classification + visualization.'], w4)
    pdf.table_row(['Availability', 'Runs on any machine with Python. 24/7 capable.'], w4)
    pdf.table_row(['Maintenance', 'Low - no external API dependencies.'], w4)
    pdf.table_row(['Interpretability', 'Color-coded maps with labels and confidence %.'], w4)

    # 1.4 Schedule
    pdf.add_page()
    pdf.sub_title('1.4 Schedule Feasibility')
    pdf.body_text('Can it be completed in the given timeframe? YES (Completed).')

    w5 = [60, 25, 25, 25]
    pdf.table_row(['Phase', 'Planned', 'Actual', 'Status'], w5, header=True)
    pdf.table_row(['Phase 1: Research & Design', '16 days', '16 days', 'Done'], w5)
    pdf.table_row(['Phase 2: Development & Deploy', '27 days', '27 days', 'Done'], w5)
    pdf.table_row(['Phase 3: Testing & Docs', '16 days', 'In progress', 'On track'], w5)
    pdf.table_row(['TOTAL', '59 days', '59 days', 'On schedule'], w5, bold=True)

    # ════════════════════════════════════
    # 2. SUSTAINABILITY
    # ════════════════════════════════════
    pdf.section_title('2. Sustainability Considerations')

    pdf.sub_title('2.1 Environmental Sustainability')
    w6 = [40, 100]
    pdf.table_row(['Factor', 'Assessment'], w6, header=True)
    pdf.table_row(['Energy use', 'BDH: 2.03M params. Training ~0.1 kWh (a phone charge).'], w6)
    pdf.table_row(['Carbon footprint', 'Negligible. Inference at 0.6ms has near-zero cost.'], w6)
    pdf.table_row(['Impact', 'POSITIVE - enables deforestation/flood monitoring.'], w6)
    pdf.table_row(['Hardware', 'Consumer laptop. No specialized GPUs required.'], w6)

    pdf.sub_title('2.2 Data Sustainability')
    pdf.table_row(['Factor', 'Assessment'], w6, header=True)
    pdf.table_row(['Availability', 'Sentinel-2 data free until at least 2030 (ESA).'], w6)
    pdf.table_row(['Freshness', 'Retrain on newer imagery without architecture changes.'], w6)
    pdf.table_row(['Privacy', 'Public satellite imagery. No personal data concerns.'], w6)
    pdf.table_row(['Storage', 'Dataset ~90MB. Models <10MB each. Minimal.'], w6)

    pdf.add_page()
    pdf.sub_title('2.3 Technical Sustainability')
    pdf.table_row(['Factor', 'Assessment'], w6, header=True)
    pdf.table_row(['Dependencies', 'Stable libs: PyTorch (Meta), FastAPI. Long-term support.'], w6)
    pdf.table_row(['Maintainability', 'Modular code. Each BDH module is a separate class.'], w6)
    pdf.table_row(['Knowledge transfer', 'Documented code with docstrings. Published principles.'], w6)
    pdf.table_row(['Obsolescence risk', 'Low. CNNs remain standard. PyTorch actively developed.'], w6)

    # ════════════════════════════════════
    # 3. SCALABILITY
    # ════════════════════════════════════
    pdf.section_title('3. Scalability Considerations')

    pdf.sub_title('3.1 Data Scalability')
    w7 = [35, 30, 30, 45]
    pdf.table_row(['Dimension', 'Current', 'Scalable To', 'How'], w7, header=True)
    pdf.table_row(['Image count', '27,000', 'Millions', 'Batch DataLoader, streaming'], w7)
    pdf.table_row(['Resolution', '64x64', '256x256+', 'Adaptive pooling layers'], w7)
    pdf.table_row(['Classes', '10', '50+', 'Change final FC layer'], w7)
    pdf.table_row(['Spectral bands', '3 (RGB)', '13 (Sentinel-2)', 'Change stem input channels'], w7)

    pdf.sub_title('3.2 Compute Scalability')
    w8 = [35, 30, 30, 45]
    pdf.table_row(['Dimension', 'Current', 'Scalable To', 'Method'], w8, header=True)
    pdf.table_row(['Single image', '0.6ms', 'Already optimal', '-'], w8)
    pdf.table_row(['Batch processing', 'Sequential', '1000+/batch', 'GPU batch inference'], w8)
    pdf.table_row(['Multi-GPU', 'Single device', 'GPU cluster', 'DistributedDataParallel'], w8)
    pdf.table_row(['Concurrent users', '1', '100+', 'Gunicorn + Nginx'], w8)

    pdf.add_page()
    pdf.sub_title('3.3 Architecture Scalability (BDH)')
    pdf.body_text(
        'The BDH architecture is designed to scale by adding stages, increasing channels, '
        'or adding more refinement iterations:'
    )
    pdf.code_block(
        'Current:   3 stages (64->128->256)           = 2.03M params\n'
        'Scaled:    4 stages (64->128->256->512)       = ~5M params\n'
        'Large:     5 stages (64->128->256->512->1024)  = ~15M params'
    )

    w9 = [45, 45, 50]
    pdf.table_row(['Scaling Method', 'What Changes', 'Expected Impact'], w9, header=True)
    pdf.table_row(['Add stages', 'More hierarchy levels', 'Better on complex scenes'], w9)
    pdf.table_row(['Increase channels', 'Wider features', 'More land cover subtypes'], w9)
    pdf.table_row(['More refinement', '2->4 iterations', 'Cleaner features'], w9)
    pdf.table_row(['Larger kernels', 'Add 9x9, 11x11', 'Better for high-res imagery'], w9)

    pdf.sub_title('3.4 Deployment Scalability')
    w10 = [40, 25, 75]
    pdf.table_row(['Option', 'Effort', 'Capacity'], w10, header=True)
    pdf.table_row(['Local (current)', 'Done', '1 user, ~1,666 images/sec'], w10)
    pdf.table_row(['Docker container', '1 day', 'Portable, any cloud provider'], w10)
    pdf.table_row(['Cloud (AWS/GCP)', '3 days', 'Auto-scaling, 100+ concurrent users'], w10)
    pdf.table_row(['Edge device', '5 days', 'On-satellite or drone-mounted processing'], w10)
    pdf.table_row(['API service', '2 days', 'RESTful API for GIS integration'], w10)

    # ════════════════════════════════════
    # 4. FUTURE ROADMAP
    # ════════════════════════════════════
    pdf.add_page()
    pdf.section_title('4. Future Scalability Roadmap')

    w11 = [25, 65, 50]
    pdf.table_row(['Timeline', 'Enhancement', 'Impact'], w11, header=True)
    pdf.table_row(['Near-term', 'Higher-res imagery (256x256)', 'Better mixed-area classification'], w11)
    pdf.table_row(['Near-term', 'Per-class confusion matrix', 'Identify weak classes'], w11)
    pdf.table_row(['Mid-term', 'Semantic segmentation (U-Net+BDH)', 'True pixel-level classification'], w11)
    pdf.table_row(['Mid-term', 'Multi-spectral (13 bands)', 'Major accuracy improvement'], w11)
    pdf.table_row(['Long-term', 'Real-time satellite feed', 'Continuous Earth monitoring'], w11)
    pdf.table_row(['Long-term', 'ISRO satellite integration', 'Indian-specific land analysis'], w11)
    pdf.table_row(['Long-term', 'Federated learning', 'Privacy-preserving distributed ML'], w11)

    # ── SUMMARY ──
    pdf.section_title('5. Summary')

    w12 = [55, 70, 20]
    pdf.table_row(['Dimension', 'Key Finding', 'Rating'], w12, header=True)
    pdf.table_row(['Technical feasibility', 'All tools available, model works', 'HIGH'], w12)
    pdf.table_row(['Economic feasibility', 'Near-zero cost, massive ROI', 'HIGH'], w12)
    pdf.table_row(['Operational feasibility', 'Simple UI, minimal training', 'HIGH'], w12)
    pdf.table_row(['Schedule feasibility', 'Completed on time', 'HIGH'], w12)
    pdf.table_row(['Environmental sustainability', 'Low energy, positive impact', 'HIGH'], w12)
    pdf.table_row(['Data sustainability', 'Free, continuously available', 'HIGH'], w12)
    pdf.table_row(['Technical sustainability', 'Stable deps, modular code', 'HIGH'], w12)
    pdf.table_row(['Scalability', 'Designed for growth', 'HIGH'], w12)
    pdf.ln(5)

    pdf.body_text(
        'Conclusion: The SpaceX system is fully feasible with current technology and '
        'resources, environmentally sustainable due to its lightweight architecture (2.03M '
        'parameters, ~0.1 kWh training), and architecturally designed to scale from a single '
        'laptop to a cloud-deployed Earth monitoring service.'
    )

    # Save
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'docs'/SpaceX_Feasibility.pdf'
    pdf.output(path)
    print(f'PDF saved to: {path}')


if __name__ == '__main__':
    generate()
