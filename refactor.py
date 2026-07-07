import os
import shutil

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.join(ROOT_DIR, 'scripts')
DOCS_DIR = os.path.join(ROOT_DIR, 'docs')

os.makedirs(SCRIPTS_DIR, exist_ok=True)
os.makedirs(DOCS_DIR, exist_ok=True)

# 1. Delete SensiSpace-main duplicate directory
duplicate_dir = os.path.join(ROOT_DIR, 'SensiSpace-main')
if os.path.exists(duplicate_dir):
    shutil.rmtree(duplicate_dir)
    print(f"Deleted {duplicate_dir}")

# 2. Delete unrelated Log Analysis files
unrelated_files = [
    'zadara.py', 'zadaraerrorfree.py', 'log.app',
    'AI_Log_Analysis_Explanation.md', 'AI_Log_Analysis_Problem_Statement.md',
    'AI_Log_Analysis_Presentation.pdf', 'generate_log_analysis_pdf.py',
    'img_anomaly.png', 'img_architecture.png', 'img_correlation.png',
    'img_ingestion.png', 'img_storage.png', 'img_title.png', 'GANTT CHART.pdf'
]
for f in unrelated_files:
    path = os.path.join(ROOT_DIR, f)
    if os.path.exists(path):
        os.remove(path)
        print(f"Deleted {f}")

# 3. Move and rename generated PDFs
for f in os.listdir(ROOT_DIR):
    if f.endswith('.pdf') and f.startswith('SensiSpace_'):
        new_name = f.replace('SensiSpace_', 'SpaceX_')
        shutil.move(os.path.join(ROOT_DIR, f), os.path.join(DOCS_DIR, new_name))
        print(f"Moved {f} to docs/{new_name}")

# 4. Process PDF generation scripts
generate_scripts = [
    'generate_demo_pdf.py', 'generate_design_pdf.py', 'generate_dfd_pdf.py',
    'generate_dfd_visual.py', 'generate_feasibility_pdf.py', 'generate_ieee_paper.py',
    'generate_output_pdf.py', 'generate_pdf.py', 'generate_techstack_pdf.py', 'generate_timeline_pdf.py'
]

for script in generate_scripts:
    old_path = os.path.join(ROOT_DIR, script)
    if os.path.exists(old_path):
        with open(old_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Replace SensiSpace with SpaceX
        content = content.replace('SensiSpace', 'SpaceX')
        
        # Replace hardcoded output directory with dynamic docs directory
        content = content.replace("'/Users/yashlohia/Major project", "os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'docs'")
        content = content.replace('"/Users/yashlohia/Major project', 'os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs"')
        
        # Just incase the above breaks any strings that didn't have closing quotes, we fix common known strings
        content = content.replace("out='/Users/yashlohia/Major project/", "out=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'docs', '")
        content = content.replace("path = '/Users/yashlohia/Major project/", "path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'docs', '")
        content = content.replace("output_path = '/Users/yashlohia/Major project/", "output_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'docs', '")
        content = content.replace("out = '/Users/yashlohia/Major project/", "out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'docs', '")
        
        # Ensure os is imported
        if 'import os' not in content:
            content = 'import os\n' + content
            
        new_path = os.path.join(SCRIPTS_DIR, script)
        with open(new_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        os.remove(old_path)
        print(f"Moved {script} to scripts/ and updated paths.")

print("\nRefactoring complete! The repository is now clean and branded as SpaceX.")
