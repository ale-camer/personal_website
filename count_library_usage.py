import ast
import os
from collections import Counter

folders_to_scan = ["modules", "app"]
ignore_dirs = {"modules/refactoring"}

# Cargar librerías externas
with open("requirements.txt", "r") as f:
    external_libs = set(line.strip().split("==")[0] for line in f if line.strip())

usage_counter = Counter()

def normalize_import(name):
    return name.split('.')[0]

# Generador que recorre archivos .py ignorando carpetas específicas
def iter_py_files(folders, ignore=set()):
    for folder in folders:
        for root, dirs, files in os.walk(folder):
            dirs[:] = [d for d in dirs if os.path.join(root, d) not in ignore and d not in ignore]
            for file in files:
                if file.endswith(".py"):
                    yield os.path.join(root, file)

# Función para construir mapa de nombres importados -> paquete
def build_import_map(tree):
    import_map = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                pkg = normalize_import(n.name)
                if pkg in external_libs:
                    import_map[n.asname or n.name] = pkg
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                pkg = normalize_import(node.module)
                if pkg in external_libs:
                    for n in node.names:
                        import_map[n.asname or n.name] = pkg
    return import_map

# Analizar archivos
for file_path in iter_py_files(folders_to_scan, ignore_dirs):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        try:
            with open(file_path, "r", encoding="latin-1") as f:
                content = f.read()
        except UnicodeDecodeError:
            print(f"⚠️ No se pudo leer: {file_path}")
            continue

    try:
        tree = ast.parse(content, filename=file_path)
    except SyntaxError:
        print(f"⚠️ Error de sintaxis: {file_path}")
        continue

    # Mapa alias -> paquete
    import_map = build_import_map(tree)

    # Contar usos
    class LibUsageVisitor(ast.NodeVisitor):
        def visit_Name(self, node):
            if node.id in import_map:
                usage_counter[import_map[node.id]] += 1
            self.generic_visit(node)

        def visit_Attribute(self, node):
            # para cosas tipo np.array, dash.html, etc.
            value = node
            while isinstance(value, ast.Attribute):
                value = value.value
            if isinstance(value, ast.Name) and value.id in import_map:
                usage_counter[import_map[value.id]] += 1
            self.generic_visit(node)

    LibUsageVisitor().visit(tree)

# Mostrar resultados
print("📊 Uso real de librerías externas en modules y app:")
for pkg, count in usage_counter.most_common():
    print(f"{pkg}: {count} veces")
