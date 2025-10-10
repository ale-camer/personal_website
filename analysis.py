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
# Scoring y seniority
# ===============================
def score_backend(metrics):
    clases_pts = metrics['py_classes'] * 2
    funcs_pts = metrics['py_functions'] * 1
    methods_pts = metrics['py_methods'] * 2
    imports_pts = metrics['py_imports'] * 0.5
    raw_score = (clases_pts + funcs_pts + methods_pts + imports_pts) / (metrics['lines'] or 1) * 100
    if raw_score > 5:
        level = "Senior"
    elif raw_score > 2:
        level = "Mid"
    else:
        level = "Junior"
    note = min(max(int(raw_score / 1.5),1),10)
    breakdown = {
        'Clases': clases_pts,
        'Funciones': funcs_pts,
        'Métodos': methods_pts,
        'Imports': imports_pts,
        'JSON→HTML': metrics['py_json_html'],
        'Raw Score': round(raw_score,2),
        'Nivel': level,
        'Nota': note
    }
    return breakdown

def score_frontend(metrics):
    html_tags_pts = metrics['html_tags'] * 0.3
    html_classes_pts = metrics['html_classes'] * 0.5
    css_classes_pts = metrics['css_classes'] * 0.5
    css_props_pts = metrics['css_properties'] * 0.3
    js_funcs_pts = metrics['js_functions'] * 0.5
    js_events_pts = metrics['js_event_handlers'] * 0.7
    total_lines = metrics.get('lines',1)
    raw_score = (html_tags_pts + html_classes_pts + css_classes_pts + css_props_pts +
                 js_funcs_pts + js_events_pts) / total_lines * 100
    if raw_score > 5:
        level = "Senior"
    elif raw_score > 2:
        level = "Mid"
    else:
        level = "Junior"
    note = min(max(int(raw_score / 1.5),1),10)
    breakdown = {
        'HTML tags': html_tags_pts,
        'HTML clases': html_classes_pts,
        'CSS clases': css_classes_pts,
        'CSS propiedades': css_props_pts,
        'JS funciones': js_funcs_pts,
        'JS eventos': js_events_pts,
        'Raw Score': round(raw_score,2),
        'Nivel': level,
        'Nota': note
    }
    return breakdown

def score_automation(metrics):
    raw_score = metrics['py_json_html'] * 10
    if raw_score > 20:
        level = "Senior"
    elif raw_score > 0:
        level = "Mid"
    else:
        level = "Junior"
    note = min(max(int(raw_score/2),1),10)
    breakdown = {
        'Funciones JSON→HTML': metrics['py_json_html'],
        'Raw Score': raw_score,
        'Nivel': level,
        'Nota': note
    }
    return breakdown

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

    # Seniority desglosado
    backend_breakdown = score_backend(metrics)
    frontend_breakdown = score_frontend(metrics)
    automation_breakdown = score_automation(metrics)

    print("\n===========================")
    print("Estimación de seniority por dominio (desglosado):")
    print("===========================")
    print("Backend Python:")
    for k,v in backend_breakdown.items():
        print(f"  {k}: {v}")
    print("\nFrontend HTML/CSS/JS:")
    for k,v in frontend_breakdown.items():
        print(f"  {k}: {v}")
    print("\nAutomatización / JSON→HTML:")
    for k,v in automation_breakdown.items():
        print(f"  {k}: {v}")
    print("===========================\n")
