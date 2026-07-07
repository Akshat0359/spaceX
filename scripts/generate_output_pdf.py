import os
#!/usr/bin/env python3
"""Generate Output & Results Comparison PDF reusing ProjectPDF style."""

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
    pdf.cell(0, 12, 'Output & Results', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    pdf.set_draw_color(80, 60, 180)
    pdf.set_line_width(1)
    pdf.line(60, pdf.get_y(), 150, pdf.get_y())
    pdf.ln(10)
    pdf.set_font('Helvetica', '', 12)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, 'Comparison Parameters: ResNet-18 vs Baby Dragon Hatchling', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(20)

    # Quick summary table on title page
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(0, 8, 'Results at a Glance:', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    w0 = [40, 30, 30, 20, 25]
    pdf.table_row(['Parameter', 'ResNet-18', 'BDH', 'Winner', 'Margin'], w0, header=True)
    pdf.table_row(['Accuracy', '81.98%', '95.87%', 'BDH', '+13.89%'], w0)
    pdf.table_row(['Precision', '81.64%', '95.78%', 'BDH', '+14.14%'], w0)
    pdf.table_row(['Recall', '81.51%', '96.01%', 'BDH', '+14.50%'], w0)
    pdf.table_row(['F1-Score', '81.51%', '95.85%', 'BDH', '+14.34%'], w0)
    pdf.table_row(['Parameters', '11.18M', '2.03M', 'BDH', '5.5x less'], w0)
    pdf.table_row(['Inference', '0.18 ms', '0.60 ms', 'ResNet', '3.3x fast'], w0)
    pdf.table_row(['Training', '245 s', '3,658 s', 'ResNet', '15x fast'], w0)
    pdf.ln(3)
    pdf.body_text('BDH wins on 5 out of 7 parameters (all quality metrics + model size).')

    # ════════════════════════════════════
    # 1. ACCURACY
    # ════════════════════════════════════
    pdf.add_page()
    pdf.section_title('1. Accuracy (Overall Correctness)')
    pdf.body_text('"Out of all images, how many did the model classify correctly?"')

    w = [50, 45]
    pdf.table_row(['Model', 'Accuracy'], w, header=True)
    pdf.table_row(['ResNet-18', '81.98%'], w)
    pdf.table_row(['Baby Dragon Hatchling', '95.87%'], w, bold=True)
    pdf.ln(3)

    pdf.sub_title('Formula')
    pdf.code_block('Accuracy = Correct Predictions / Total Predictions')

    pdf.sub_title('What This Means')
    pdf.body_text('Out of 5,400 test images:')
    pdf.bold_bullet('ResNet-18: ', 'Correctly classified 4,427 images, got 973 wrong')
    pdf.bold_bullet('BDH: ', 'Correctly classified 5,177 images, got only 223 wrong')

    pdf.sub_title('Why BDH is Higher')
    pdf.body_text(
        'BDH\'s multi-scale processing captures objects at all sizes (small buildings AND '
        'large forests), while ResNet\'s uniform 3x3 kernels struggle with scale variation '
        'in satellite imagery. The lateral inhibition module also sharpens land type '
        'boundaries, reducing misclassifications at borders.'
    )

    # ════════════════════════════════════
    # 2. PRECISION
    # ════════════════════════════════════
    pdf.section_title('2. Precision (Quality of Predictions)')
    pdf.body_text('"When the model says \'this is Forest\', how often is it actually Forest?"')

    pdf.table_row(['Model', 'Precision'], w, header=True)
    pdf.table_row(['ResNet-18', '81.64%'], w)
    pdf.table_row(['Baby Dragon Hatchling', '95.78%'], w, bold=True)
    pdf.ln(3)

    pdf.sub_title('Formula')
    pdf.code_block('Precision = True Positives / (True Positives + False Positives)')

    pdf.sub_title('What This Means')
    pdf.bold_bullet('ResNet: ', 'When it says "Forest", correct ~82% of the time - 18% are false alarms')
    pdf.bold_bullet('BDH: ', 'When it says "Forest", correct ~96% of the time - only 4% false alarms')

    pdf.sub_title('Why It Matters')
    pdf.body_text(
        'High precision means fewer false alarms. If you are monitoring deforestation, you '
        'don\'t want the system incorrectly flagging residential areas as forest. Every false '
        'alarm wastes investigation resources.'
    )

    # ════════════════════════════════════
    # 3. RECALL
    # ════════════════════════════════════
    pdf.add_page()
    pdf.section_title('3. Recall (Completeness of Detection)')
    pdf.body_text('"Out of all actual Forest images, how many did the model find?"')

    pdf.table_row(['Model', 'Recall'], w, header=True)
    pdf.table_row(['ResNet-18', '81.51%'], w)
    pdf.table_row(['Baby Dragon Hatchling', '96.01%'], w, bold=True)
    pdf.ln(3)

    pdf.sub_title('Formula')
    pdf.code_block('Recall = True Positives / (True Positives + False Negatives)')

    pdf.sub_title('What This Means')
    pdf.bold_bullet('ResNet: ', 'Misses about 18.5% of actual instances of each class')
    pdf.bold_bullet('BDH: ', 'Misses only about 4% - it finds almost everything')

    pdf.sub_title('Why It Matters')
    pdf.body_text(
        'High recall means fewer missed detections. If you are tracking rivers for flood '
        'monitoring, you need the system to find ALL rivers, not miss some. A missed river '
        'could mean an undetected flood risk.'
    )

    # ════════════════════════════════════
    # 4. F1-SCORE
    # ════════════════════════════════════
    pdf.section_title('4. F1-Score (Balanced Measure)')
    pdf.body_text('"A single number that balances precision and recall."')

    pdf.table_row(['Model', 'F1-Score'], w, header=True)
    pdf.table_row(['ResNet-18', '81.51%'], w)
    pdf.table_row(['Baby Dragon Hatchling', '95.85%'], w, bold=True)
    pdf.ln(3)

    pdf.sub_title('Formula')
    pdf.code_block('F1 = 2 x (Precision x Recall) / (Precision + Recall)')

    pdf.sub_title('What This Means')
    pdf.body_text(
        'F1-Score is the harmonic mean of precision and recall. It is the most reliable '
        'single metric because:'
    )
    pdf.bullet('An F1 of 95.85% means BDH has BOTH high precision AND high recall')
    pdf.bullet('You cannot get a high F1 by cheating (e.g., predicting everything as one class)')
    pdf.bullet('Accuracy alone can be misleading with imbalanced datasets; F1 catches this')

    # ════════════════════════════════════
    # 5. PARAMETERS
    # ════════════════════════════════════
    pdf.add_page()
    pdf.section_title('5. Model Parameters (Complexity)')
    pdf.body_text('"How many learnable numbers does the model contain?"')

    w2 = [50, 40, 30]
    pdf.table_row(['Model', 'Parameters', 'Size'], w2, header=True)
    pdf.table_row(['ResNet-18', '11,181,642', '11.18M'], w2)
    pdf.table_row(['Baby Dragon Hatchling', '2,032,275', '2.03M'], w2, bold=True)
    pdf.ln(3)

    pdf.body_text('ResNet has 5.5x more parameters than BDH.')

    pdf.sub_title('What This Means')
    pdf.bullet('More parameters = more memory, more computation, harder to train')
    pdf.bullet('BDH achieves higher accuracy with 5.5x fewer parameters')
    pdf.bullet('This proves that intelligent architecture design is more effective than simply having more parameters')

    pdf.sub_title('Why It Matters for Deployment')
    pdf.bold_bullet('Cheaper hardware: ', 'Smaller model runs on edge devices, drones, even satellites')
    pdf.bold_bullet('Less energy: ', 'Lower compute = lower power consumption')
    pdf.bold_bullet('Faster updates: ', 'Smaller model files transfer and load faster')
    pdf.bold_bullet('Less overfitting: ', 'Fewer parameters means the model generalizes better')

    # ════════════════════════════════════
    # 6. INFERENCE TIME
    # ════════════════════════════════════
    pdf.section_title('6. Inference Time (Speed)')
    pdf.body_text('"How fast can the model classify one image?"')

    pdf.table_row(['Model', 'Inference Time'], w, header=True)
    pdf.table_row(['ResNet-18', '0.18 ms'], w, bold=True)
    pdf.table_row(['Baby Dragon Hatchling', '0.60 ms'], w)
    pdf.ln(3)

    pdf.sub_title('What This Means')
    pdf.bullet('ResNet is ~3.3x faster per image (simpler architecture, optimized by PyTorch)')
    pdf.bullet('BDH at 0.6ms is still extremely fast - can process ~1,666 images/second')
    pdf.bullet('Both models are well within real-time requirements')

    pdf.sub_title('Why ResNet is Faster')
    pdf.body_text(
        'ResNet uses simple, uniform 3x3 convolutions that are highly optimized in hardware '
        '(GPU/MPS). BDH\'s parallel multi-scale convolutions (3x3 + 5x5 + 7x7), attention '
        'modules, and recurrent refinement (2 iterations) add computational overhead - but '
        'the 14% accuracy gain is worth the 0.42ms trade-off.'
    )

    pdf.sub_title('Trade-off Analysis')
    pdf.body_text(
        'BDH is 3.3x slower but 14% more accurate. For satellite imagery where accuracy '
        'matters more than milliseconds (images are analyzed in batches, not video streams), '
        'BDH is the clear winner.'
    )

    # ════════════════════════════════════
    # 7. TRAINING TIME
    # ════════════════════════════════════
    pdf.add_page()
    pdf.section_title('7. Training Time')
    pdf.body_text('"How long did it take to train the model?"')

    pdf.table_row(['Model', 'Training Time'], w, header=True)
    pdf.table_row(['ResNet-18', '245 seconds (~4 min)'], w, bold=True)
    pdf.table_row(['Baby Dragon Hatchling', '3,658 seconds (~61 min)'], w)
    pdf.ln(3)

    pdf.body_text('BDH takes ~15x longer to train.')

    pdf.sub_title('Why BDH Takes Longer')
    pdf.bullet('ResNet starts from pretrained ImageNet weights (transfer learning) - already knows basic features')
    pdf.bullet('BDH is trained from scratch - must learn everything from zero')
    pdf.bullet('BDH has recurrent refinement (2 iterations = 2x computation per forward pass)')
    pdf.bullet('BDH has multi-scale branches (3 parallel convolutions per stage)')

    pdf.sub_title('Why This is Acceptable')
    pdf.body_text(
        'Training is a one-time cost. You train once, then deploy. The 61 minutes '
        'for BDH is negligible compared to the permanent accuracy advantage. In production, '
        'only inference time matters - and both models are real-time capable.'
    )

    # ════════════════════════════════════
    # MODULE CONTRIBUTION
    # ════════════════════════════════════
    pdf.section_title('8. Why BDH Outperforms - Module Contribution')
    pdf.body_text(
        'Each of the 4 biologically-inspired modules in BDH contributes to a specific '
        'quality improvement:'
    )

    w3 = [40, 45, 55]
    pdf.table_row(['BDH Module', 'What It Improves', 'Impact'], w3, header=True)
    pdf.table_row(['Multi-Scale Pyramid', 'Accuracy', 'Captures small houses AND large forests'], w3)
    pdf.table_row(['Lateral Inhibition', 'Precision (fewer FP)', 'Sharpens boundaries between land types'], w3)
    pdf.table_row(['Contextual Attention', 'Recall (fewer FN)', 'Focuses on informative features'], w3)
    pdf.table_row(['Recurrent Refinement', 'F1-Score (overall)', 'Iteratively cleans up features'], w3)

    # ════════════════════════════════════
    # CONCLUSION
    # ════════════════════════════════════
    pdf.add_page()
    pdf.section_title('9. Conclusion')

    pdf.body_text(
        'We evaluated both models using 7 comparison parameters. Baby Dragon Hatchling '
        'wins on all 5 quality metrics - accuracy, precision, recall, F1-score, and model '
        'size. ResNet-18 wins only on speed metrics (inference time and training time), but '
        'both models are fast enough for real-time use.'
    )

    pdf.ln(3)
    w4 = [40, 30, 30, 20, 25]
    pdf.table_row(['Parameter', 'ResNet-18', 'BDH', 'Winner', 'Margin'], w4, header=True)
    pdf.table_row(['Accuracy', '81.98%', '95.87%', 'BDH', '+13.89%'], w4)
    pdf.table_row(['Precision', '81.64%', '95.78%', 'BDH', '+14.14%'], w4)
    pdf.table_row(['Recall', '81.51%', '96.01%', 'BDH', '+14.50%'], w4)
    pdf.table_row(['F1-Score', '81.51%', '95.85%', 'BDH', '+14.34%'], w4)
    pdf.table_row(['Parameters', '11.18M', '2.03M', 'BDH', '5.5x less'], w4)
    pdf.table_row(['Inference', '0.18 ms', '0.60 ms', 'ResNet', '3.3x fast'], w4)
    pdf.table_row(['Training', '245 s', '3,658 s', 'ResNet', '15x fast'], w4, bold=True)
    pdf.ln(5)

    pdf.body_text(
        'The key result: 95.87% accuracy with 2.03 million parameters vs 81.98% with '
        '11.18 million - a 14 percentage point improvement with 5.5x fewer parameters. '
        'This conclusively demonstrates that biologically-inspired, domain-specific '
        'architecture design outperforms generic deep networks for satellite remote sensing.'
    )

    pdf.ln(3)
    pdf.sub_title('How to Explain During Demo')
    pdf.set_font('Helvetica', 'I', 10)
    pdf.set_text_color(80, 60, 180)
    pdf.multi_cell(0, 5.5,
        '"We compare both models on 7 parameters. BDH wins on all 5 quality metrics - '
        'accuracy, precision, recall, F1-score, and model size. ResNet is faster, but '
        'both are real-time capable. The key result: 95.87% accuracy with 2 million '
        'parameters vs 81.98% with 11 million - proving that intelligent architecture '
        'design beats brute-force scaling."'
    )

    # Save
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'docs'/SpaceX_Output.pdf'
    pdf.output(path)
    print(f'PDF saved to: {path}')


if __name__ == '__main__':
    generate()
