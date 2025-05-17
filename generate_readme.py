"""
Generate README.md file.
"""

import os
from time import time
from modules.utils import reading_json

NO_COMMENT_STRING = "No comment available"

def _read_file_content(file_path: str) -> str:
    """
    Read the entire content of a file as a string.
    
    Args:
        file_path (str): Path to the file.
        
    Returns:
        str: File content as a string.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def _write_readme_file(content: str, file_name: str = "README.md") -> None:
    """
    Write the given content to a file.
  
    Args:
        content (str): Text content to be written to the file.
        filename (str, optional): Name of the file to write to. Defaults to "README.md".
  
    Returns:
        None
    """
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(content)
        
def get_first_python_docstring(file_path: str) -> str:
    """
    Extract the first Python docstring from a file.
    
    Handles both single-line and multi-line docstrings.
    
    Args:
        file_path (str): Path to the Python file.
        
    Returns:
        str: Extracted docstring or a default no-comment message.
    """
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
    """
    Extract the first CSS block comment from a file.
    
    Args:
        file_path (str): Path to the CSS file.
        
    Returns:
        str: First CSS comment or a default no-comment message.
    """
    content = _read_file_content(file_path)
    if "/*" in content and "*/" in content:
        return content.split("/*")[1].split("*/")[0].strip().replace("\n", " ")
    return NO_COMMENT_STRING

def get_first_js_comment(file_path: str) -> str:
    """
    Extract the first JavaScript comment from a file.
    
    Supports both single-line (//) and multi-line (/* */) comments.
    
    Args:
        file_path (str): Path to the JavaScript file.
        
    Returns:
        str: First JS comment or a default no-comment message.
    """
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
    """
    Extract the first HTML comment from a file.
    
    Args:
        file_path (str): Path to the HTML file.
        
    Returns:
        str: First HTML comment or a default no-comment message.
    """
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
    """
    Get the first comment or docstring from a file based on its extension.
    
    Args:
        file_path (str): Path to the file.
        
    Returns:
        str: Extracted comment or an empty string if not supported.
    """
    if file_path.endswith(".py"): return get_first_python_docstring(file_path)
    elif file_path.endswith(".css"): return get_first_css_comment(file_path)
    elif file_path.endswith(".js"): return get_first_js_comment(file_path)
    elif file_path.endswith(".html"): return get_first_html_comment(file_path)
    return ""

def generate_tree(
    directory: str, 
    dir_comments: dict,
    indent: int = 0, 
    tree_str: str = "", 
    last_item: bool = False
  ) -> str:
    """
    Recursively generate a directory tree string with comments for directories and files.
    
    Args:
        directory (str): Root directory to start generating the tree.
        dir_comments (dict): Dictionary with directory comments keyed by directory name.
        indent (int, optional): Current indentation level. Defaults to 0.
        tree_str (str, optional): Accumulated tree string. Defaults to "".
        last_item (bool, optional): Indicates if current item is the last in the directory. Defaults to False.
        
    Returns:
        str: Formatted directory tree as a string.
    """
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
    """
    Generate a README.md file with the directory tree and file comments.
    
    Reads directory comments from a JSON config file and writes
    a formatted tree to README.md.
    
    Args:
        path (str): Root directory path to generate the tree from.
        
    Returns:
        str: The generated tree string in markdown format.
    """
    start_time = time()
    tree_comments = reading_json(os.path.join('static', 'json', 'config.json'))["tree_comments"]
    tree = generate_tree(path, tree_comments)
    markdown_tree = "```bash\n" + tree + "```"
    _write_readme_file(markdown_tree)
    print(f"README.md file generated in {round(time() - start_time, 4)} seconds.")

if __name__ == "__main__":
    generate_readme_file(".")