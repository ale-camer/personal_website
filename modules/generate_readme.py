"""Generate README.md file."""

import os
from time import time
from modules.utils import read_json

NO_COMMENT_STRING = "No comment available"
OUTPUT_FILE = "README.md"

def _read_file_content(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def _write_readme_file(content: str, file_name: str = OUTPUT_FILE) -> None:
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(content)
        
def get_first_python_docstring(file_path: str) -> str:
    content = _read_file_content(file_path)
    lines = content.splitlines()

    docstring = ""
    in_docstring = False
    for line in lines:
        if line.strip().startswith('"""') and not in_docstring:
            in_docstring = True
            if line.strip().endswith('"""') and len(line.strip()) > 3 and line.strip() != '"""':  # single-line docstring
                docstring += line.strip()[3:-3].strip() + " "
                break
            if not (line.strip().endswith('"""') and len(line.strip()) == 3):  # multi-line docstring
                current_line_content = line.strip()[3:]
                if current_line_content:
                    docstring += current_line_content.strip() + " "
            continue

        if in_docstring:  # accumulate docstring content
            if line.strip().endswith('"""'):
                current_line_content = line.strip()[:-3]
                if current_line_content:
                    docstring += current_line_content.strip() + " "
                break
            docstring += line.strip() + " "

    return docstring.strip() if docstring.strip() else NO_COMMENT_STRING

def get_first_css_comment(file_path: str) -> str:
    content = _read_file_content(file_path)
    if "/*" in content and "*/" in content:
        return content.split("/*")[1].split("*/")[0].strip().replace("\n", " ")
    return NO_COMMENT_STRING

def get_first_js_comment(file_path: str) -> str:
    content = _read_file_content(file_path)
    lines = content.splitlines()

    comment = ""
    in_comment = False
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith('//') and not in_comment:  # single-line comment 
            comment += stripped_line.lstrip('/').strip() + " "
            return comment.strip() if comment.strip() else NO_COMMENT_STRING

        elif stripped_line.startswith('/*'):  # start multi-line comment
            in_comment = True
            if stripped_line.endswith('*/'):
                comment += stripped_line[2:-2].strip() + " "
                break
            comment += stripped_line[2:].strip() + " "
        elif in_comment and stripped_line.endswith('*/'): # end multi-line comment
            comment += stripped_line[:-2].strip() + " "
            break
        elif in_comment: # accumulate block content
            comment += stripped_line + " "

    return comment.strip() if comment.strip() else NO_COMMENT_STRING

def get_first_html_comment(file_path: str) -> str:
    content = _read_file_content(file_path)
    lines = content.splitlines()

    for line in lines:
        if line.strip().startswith("<!--"): # start html comment
            stripped_line = line.strip()
            if stripped_line.endswith("-->"): # one-line comment
                comment_content = stripped_line[4:-3].strip()
            else: # unclosed comment (partial)
                comment_content = stripped_line[4:].strip()
            return comment_content if comment_content else NO_COMMENT_STRING
    return NO_COMMENT_STRING

def get_file_comment(file_path: str) -> str:
    if file_path.endswith(".py"): return get_first_python_docstring(file_path)
    elif file_path.endswith(".css"): return get_first_css_comment(file_path)
    elif file_path.endswith(".js"): return get_first_js_comment(file_path)
    elif file_path.endswith(".html"): return get_first_html_comment(file_path)
    return ""

def generate_tree(directory: str, dir_comments: dict, indent: int = 0, tree_str: str = "", last_item: bool = False) -> str:
    items = sorted([
        item for item in os.listdir(directory)
        if not item.startswith('.') and not item.startswith('_')
    ])

    for i, item in enumerate(items):
        item_path = os.path.join(directory, item)
        is_last = (i == len(items) - 1)
        prefix = "  " * indent + ("└── " if is_last else "├── ")

        if os.path.isdir(item_path):
            comment = dir_comments.get(item, "")
            comment_str = f"  # {comment}" if comment else ""
            tree_str += f"{prefix}{item}/{comment_str}\n"
            if item == 'images' and directory.endswith('static'): continue # skip images
            tree_str = generate_tree(item_path, dir_comments, indent + 1, tree_str, is_last)
        else:
            comment = get_file_comment(item_path)
            comment_str = f"  # {comment}" if comment else ""
            tree_str += f"{prefix}{item}{comment_str}\n"

    return tree_str

def generate_readme_file(path: str) -> str:
    start_time = time()
    config_file_path = os.path.join('static', 'json', 'config.json')
    tree_comments = read_json(config_file_path)["tree_comments"]
    tree = generate_tree(path, tree_comments)
    markdown_tree = "```bash\n" + tree + "```"
    _write_readme_file(markdown_tree)
    print(f"{OUTPUT_FILE} file generated in {round(time() - start_time, 4)} seconds.")

if __name__ == "__main__":
    generate_readme_file(".")