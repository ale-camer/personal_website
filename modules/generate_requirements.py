import ast
import os
from tqdm import tqdm  # pip install tqdm
import sys
import sysconfig

project_path = "../"
output_file = "requirements.txt"  # como pediste
ignore_dirs = {"__pycache__", "venv"}  # carpetas a ignorar

imports = set()

# Obtener lista de librerías estándar de Python
std_libs = set(sys.builtin_module_names)
# También agregar carpetas del lib de Python
lib_paths = [sysconfig.get_paths()["stdlib"]]
for lib in lib_paths:
    for root, dirs, files in os.walk(lib):
        for file in files:
            if file.endswith(".py"):
                std_libs.add(os.path.splitext(file)[0])

def normalize_import(module_name):
    return module_name.split('.')[0]

# Generador que recorre los archivos .py ignorando carpetas específicas
def iter_py_files(path, ignore=set()):
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in ignore]
        for file in files:
            if file.endswith(".py"):
                yield os.path.join(root, file)

# Contar archivos para tqdm
def count_py_files(path, ignore=set()):
    return sum(1 for _ in iter_py_files(path, ignore))

total_files = count_py_files(project_path, ignore_dirs)

# Procesar archivos con generador y barra de progreso
for file_path in tqdm(iter_py_files(project_path, ignore_dirs), total=total_files, desc="Procesando archivos .py"):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        try:
            with open(file_path, "r", encoding="latin-1") as f:
                content = f.read()
        except UnicodeDecodeError:
            tqdm.write(f"⚠️  No se pudo leer el archivo: {file_path}, se ignora.")
            continue

    try:
        tree = ast.parse(content, filename=file_path)
    except SyntaxError:
        tqdm.write(f"⚠️  Error de sintaxis en {file_path}, se ignora.")
        continue

    # Detectar imports
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                pkg = normalize_import(n.name)
                # Filtrar estándar y privados
                if pkg not in std_libs and not pkg.startswith("_"):
                    imports.add(pkg)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                pkg = normalize_import(node.module)
                if pkg not in std_libs and not pkg.startswith("_"):
                    imports.add(pkg)

# Guardar requirements.txt
with open(output_file, "w") as f:
    for pkg in sorted(imports):
        f.write(pkg + "\n")

print(f"✅ requirements.txt generado ({output_file})")
