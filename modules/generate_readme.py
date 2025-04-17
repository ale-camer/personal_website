"""
Generate README.md file.
"""

import os

def get_python_docstring(file_path):
    """Extracts the first docstring from a Python file, excluding the final triple quotes."""
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    docstring = ""
    in_docstring = False
    for line in lines:
        if line.strip().startswith('"""') and not in_docstring:
            in_docstring = True
            continue
        if in_docstring:
            docstring += line.strip() + " "
        if line.strip().endswith('"""') and in_docstring:
            break

    return docstring.strip().replace('"','') if docstring else "No docstring available"

def get_css_comment(file_path):
    """Extracts the first CSS comment block."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    if "/*" in content and "*/" in content:
        return content.split("/*")[1].split("*/")[0].strip().replace("\n", " ")
    return "No comment available"

def get_js_comment(file_path):
    """Extracts the first comment from a JavaScript file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    comment = ""
    in_comment = False
    for line in lines:
        if line.strip().startswith('//') and not in_comment:
            in_comment = True
            comment += line.strip() + " "
        elif line.strip().startswith('/*'):
            in_comment = True
            comment += line.strip() + " "
        elif line.strip().endswith('*/') and in_comment:
            break

    return comment.strip().replace("/","") if comment else "No comment available"
  
def get_html_comment(file_path):
    """Extracts the first comment from an HTML file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        if line.strip().startswith("<!--"):
            comment = line.strip().strip("<!--").strip("-->").strip()
            return comment
    return "No comment available"
  
def generate_tree(directory, indent=0, tree_str="", last_item=False):
    """Generates a directory tree as a string, with inline comments for each item."""
    if not os.path.exists(directory):  # check if exists
        return f"Error: Directory {directory} does not exist."

    items = sorted(os.listdir(directory))

    for i, item in enumerate(items):
        item_path = os.path.join(directory, item)

        if item.startswith('.') or item.startswith('_'): continue

        is_last_item = (i == len(items) - 1)
        prefix = "  " * indent + ("└── " if is_last_item else "├── ")

        if os.path.isdir(item_path):
            if item == "modules": tree_str += f"{prefix}{item}/  # Contain Python modules.\n"
            elif item == "static": tree_str += f"{prefix}{item}/  # Contain static files (CSS, JS and images).\n"
            elif item == "templates": tree_str += f"{prefix}{item}/  # Contain HTML templates.\n"
            elif item == "css": tree_str += f"{prefix}{item}/  # Contain CSS main script.\n"
            elif item == "js": tree_str += f"{prefix}{item}/  # Contain JavaScript scripts.\n"
            elif item == "seasonality_prediction": tree_str += f"{prefix}{item}/  # Contain Seasonality Prediction functionality temporary files.\n"
            elif item == "world_bank": tree_str += f"{prefix}{item}/  # Contain World Bank functionality temporary files.\n"
            elif item == 'images': 
              tree_str += f"{prefix}{item}/  # Contain images for the UI.\n"
              continue
            else: tree_str += f"{prefix}{item}/\n"
            tree_str = generate_tree(item_path, indent + 1, tree_str, last_item=is_last_item)
        else:
            if item.endswith(".py"): tree_str += f"{prefix}{item}  # {get_python_docstring(item_path)}\n"
            elif item.endswith(".css"): tree_str += f"{prefix}{item}  # {get_css_comment(item_path)}\n"
            elif item.endswith(".js"): tree_str += f"{prefix}{item}  # {get_js_comment(item_path)}\n"
            elif item.endswith(".html"): tree_str += f"{prefix}{item}  # {get_html_comment(item_path)}\n"
            else: tree_str += f"{prefix}{item}\n"


    return tree_str

def generate_readme(path):
    # tree_output = generate_tree(os.path.dirname(os.path.realpath(__file__)))
    tree_output = generate_tree(path)
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(tree_output)
    print("README.md file generated.")

# lala = generate_readme()
# print(lala)



# Ejecutar directamente la función al importar el módulo
# generate_readme()
# if __name__ == "__main__":
#     tree_output = generate_tree(os.path.dirname(os.path.realpath(__file__)))
#     with open("README.md", "w", encoding="utf-8") as f: f.write(tree_output)
#     print("Directory tree saved to README.md")
