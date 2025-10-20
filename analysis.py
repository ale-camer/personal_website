import os
from collections import defaultdict
import re

# ===============================
# Configuración
# ===============================
EXTENSIONS = ['.py', '.html', '.css', '.js']
EXCLUDE_DIRS = ['venv', '.git', '__pycache__']

# ===============================
# Funciones de análisis
# ===============================
def should_exclude(dirpath):
    return any(ex in dirpath for ex in EXCLUDE_DIRS)

def valid_html(filename):
    # Ignorar HTML con más de 2 palabras separadas por _
    name = os.path.splitext(filename)[0]
    return len(name.split('_')) <= 2

def analyze_file(path, ext):
    metrics = defaultdict(int)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return metrics

    lines = content.splitlines()
    metrics['lines'] = len(lines)

    if ext == '.py':
        metrics['py_classes'] = len(re.findall(r'^class\s+\w+', content, re.MULTILINE))
        metrics['py_functions'] = len(re.findall(r'^def\s+\w+', content, re.MULTILINE))
        metrics['py_methods'] = len(re.findall(r'^\s+def\s+\w+', content, re.MULTILINE))
        metrics['py_imports'] = len(re.findall(r'^(import|from)\s+\w+', content, re.MULTILINE))
        metrics['py_json_html'] = len(re.findall(r'json.*?html', content, re.IGNORECASE))
    elif ext == '.html':
        metrics['html_tags'] = len(re.findall(r'<\w+', content))
        metrics['html_classes'] = len(re.findall(r'class=".*?"', content))
    elif ext == '.css':
        metrics['css_classes'] = len(re.findall(r'\.\w+', content))
        metrics['css_properties'] = len(re.findall(r':', content))
    elif ext == '.js':
        metrics['js_functions'] = len(re.findall(r'function\s+\w+', content))
        metrics['js_event_handlers'] = len(re.findall(r'\.addEventListener', content))

    return metrics

def analyze_repo(root='.'):
    results = defaultdict(int)
    metrics_total = defaultdict(int)

    for dirpath, dirnames, filenames in os.walk(root):
        if should_exclude(dirpath):
            continue
        for file in filenames:
            ext = os.path.splitext(file)[1].lower()
            if ext not in EXTENSIONS:
                continue
            if ext == '.html' and not valid_html(file):
                continue
            path = os.path.join(dirpath, file)
            file_metrics = analyze_file(path, ext)
            metrics_total[ext] += file_metrics.get('lines',0)
            for k, v in file_metrics.items():
                metrics_total[k] += v

    return metrics_total

# ===============================
# Ejecutar análisis
# ===============================
if __name__ == '__main__':
    metrics = analyze_repo('.')

    total_lines = sum(metrics[ext] for ext in EXTENSIONS)

    print("\n===========================")
    print("Resumen por lenguaje:")
    print("===========================")
    for ext in EXTENSIONS:
        lines = metrics.get(ext,0)
        pct = (lines / total_lines *100) if total_lines else 0
        print(f"{ext} : {lines:,} líneas ({pct:.2f}%)")
    print("---------------------------")
    print(f"TOTAL : {total_lines:,} líneas")
    print("===========================")