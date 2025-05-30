"""Generate README.md file."""

from time import time
from pathlib import Path
from dataclasses import dataclass
from abc import ABC, abstractmethod
from modules.utils import read_json, read_file, write_file

# =============================================================================
# CONFIG
# =============================================================================
@dataclass
class TreeConfig:
    comments: dict[str, str]
    ignore_items: set = None
    ignore_files: set = None

    def __post_init__(self):
        if self.ignore_items is None:
            self.ignore_items = {
                '.git', '.vscode', '__pycache__', 'venv', '.DS_Store',
                'node_modules', '.pytest_cache', '.idea', '*.pyc',
                '*.swp', '*.log', 'dist', 'build', '*.egg-info', 'migrations'
            }
        if self.ignore_files is None:
            self.ignore_files = {'generate_readme.py', 'roadmap_app_deployment.txt'}

# =============================================================================
# EXTRACTORS
# =============================================================================
class CommentExtractor(ABC):

    NO_COMMENT = ""

    @abstractmethod
    def extract(self, content: str) -> str:
        pass

    def extract_from_file(self, file_path: Path) -> str:
        content = read_file(str(file_path))
        if not content:
            return self.NO_COMMENT

        result = self.extract(content)
        return result.strip() if result and result.strip() else self.NO_COMMENT

class PythonCommentExtractor(CommentExtractor):

    def extract(self, content: str) -> str:
        lines = content.splitlines()
        docstring_lines = []
        in_docstring = False
        quote_type = None

        for line in lines:
            stripped = line.strip()

            if stripped.startswith('"""') or stripped.startswith("'''"):
                current_quote = stripped[:3]

                if stripped.endswith(current_quote) and len(stripped) > 6:
                    return stripped[3:-3].strip()

                if not in_docstring:
                    in_docstring = True
                    quote_type = current_quote
                    if len(stripped) > 3:
                        docstring_lines.append(stripped[3:].strip())
                elif stripped.endswith(quote_type):
                    if len(stripped) > 3:
                        docstring_lines.append(stripped[:-3].strip())
                    break
            elif in_docstring:
                docstring_lines.append(stripped)

        return " ".join(filter(None, docstring_lines)).strip()

class CSSCommentExtractor(CommentExtractor):

    def extract(self, content: str) -> str:
        start = content.index("/*") + 2
        end = content.index("*/", start)
        return ' '.join(content[start:end].strip().split())

class JavaScriptCommentExtractor(CommentExtractor):

    def extract(self, content: str) -> str:
        try:
            start = content.index("/*") + 2
            end = content.index("*/", start)
            return ' '.join(content[start:end].strip().split())
        except ValueError:
            pass

        for line in content.splitlines():
            stripped = line.strip()
            if stripped.startswith('//'):
                return stripped[2:].strip()

        return self.NO_COMMENT

class HTMLCommentExtractor(CommentExtractor):

    def extract(self, content: str) -> str:
        try:
            start = content.index("<!--") + 4
            end = content.index("-->", start)
            return ' '.join(content[start:end].strip().split())
        except ValueError:
            return self.NO_COMMENT

class CommentExtractorFactory:

    _extractors = {
        '.py': PythonCommentExtractor(),
        '.css': CSSCommentExtractor(),
        '.js': JavaScriptCommentExtractor(),
        '.html': HTMLCommentExtractor(),
        '.htm': HTMLCommentExtractor(),
    }

    @classmethod
    def get_comment(cls, file_path: Path) -> str:
        extractor = cls._extractors.get(file_path.suffix.lower())
        return extractor.extract_from_file(file_path) if extractor else CommentExtractor.NO_COMMENT

# =============================================================================
# TREE
# =============================================================================
class DirectoryTreeGenerator:

    def __init__(self, config: TreeConfig):
        self.config = config
        self.comment_factory = CommentExtractorFactory()

    def generate(self, directory: Path, indent_level: int = 0, parent_prefix: str = "") -> str:
        if indent_level == 0:
            return self._generate_root_tree(directory)

        return self._generate_subtree(directory, indent_level, parent_prefix)

    def _generate_root_tree(self, directory: Path) -> str:
        root_name = directory.name
        root_comment = self._get_comment_for_item(root_name, directory)
        comment_str = f"  # {root_comment}" if root_comment else ""

        tree_parts = [f"{root_name}/{comment_str}\n"]
        tree_parts.append(self._generate_subtree(directory, 1, ""))

        return "".join(tree_parts)

    def _generate_subtree(self, directory: Path, indent_level: int, parent_prefix: str) -> str:
        items = self._get_filtered_items(directory)

        tree_parts = []
        for i, item_path in enumerate(items):
            is_last = (i == len(items) - 1)
            connector = "└── " if is_last else "├── "
            line_prefix = parent_prefix + connector

            comment = self._get_comment_for_item(item_path.name, item_path)
            comment_str = f"  # {comment}" if comment else ""

            if item_path.is_dir():
                tree_parts.append(f"{line_prefix}{item_path.name}/{comment_str}\n")
                child_prefix = parent_prefix + ("    " if is_last else "│   ")
                tree_parts.append(self._generate_subtree(item_path, indent_level + 1, child_prefix))
            else:
                tree_parts.append(f"{line_prefix}{item_path.name}{comment_str}\n")

        return "".join(tree_parts)

    def _get_filtered_items(self, directory: Path) -> list[Path]:
        items = []
        for item in directory.iterdir():
            if not self._should_ignore_item(item):
                items.append(item)
        return sorted(items)

    def _should_ignore_item(self, item: Path) -> bool:
        if item.name in self.config.ignore_items or item.name in self.config.ignore_files:
            return True

        for pattern in self.config.ignore_items:
            if '*' in pattern and pattern.replace('*', '') in item.name:
                return True

        return False

    def _get_comment_for_item(self, item_name: str, item_path: Path) -> str:
        script_path = Path(__file__).resolve()
        project_root = script_path.parent.parent if script_path.parent.name == "modules" else script_path.parent

        relative_path = item_path.relative_to(project_root).as_posix()

        comment = self.config.comments.get(relative_path,
                 self.config.comments.get(item_name, ""))

        if item_path.is_dir() and not comment:
            comment = self.config.comments.get(f"{item_name}/", "")

        if not comment and item_path.is_file():
            comment = self.comment_factory.get_comment(item_path)

        return comment

# =============================================================================
# README
# =============================================================================
class ReadmeGenerator:

    def __init__(self, output_file: str = "README.md"):
        self.output_file = output_file

        script_path = Path(__file__).resolve()
        self.project_root = script_path.parent.parent if script_path.parent.name == "modules" else script_path.parent

        self.read_json = read_json
        self.read_file = read_file
        self.write_file = write_file

    def generate_readme_file(self) -> None:
        start_time = time()

        readme_data = self._load_readme_data()
        markdown_content = self._build_markdown(readme_data)
        output_path = self.project_root / self.output_file
        self.write_file(markdown_content, str(output_path))

        elapsed_time = round(time() - start_time, 4)
        print(f"{self.output_file} generated in {elapsed_time} seconds.")

    def _load_readme_data(self) -> dict:
        json_path = self.project_root / 'static' / 'json' / 'readme.json'
        return self.read_json(str(json_path))

    def _build_markdown(self, data: dict) -> str:
        parts = []
        parts.append(data.get("title", "# Project Title"))
        if "introduction" in data:
            parts.append(data["introduction"])
        if "live_demo" in data:
            parts.extend(self._build_live_demo_section(data["live_demo"]))
        parts.extend(self._build_main_sections(data.get("sections", {})))
        return "\n\n".join(parts).strip()

    def _build_live_demo_section(self, demo_data: dict) -> list[str]:
        parts = [demo_data.get("title", "## Live Demo")]
        if "content" in demo_data:
            parts.append("\n".join(demo_data["content"]))
        return parts

    def _build_main_sections(self, sections: dict) -> list[str]:
        section_order = [
            "features", "installation", "usage", "technologies",
            "key_files", "project_structure", "author", "license"
        ]
        parts = []
        for section_key in section_order:
            if section_key not in sections:
                continue

            section_data = sections[section_key]
            parts.append(section_data.get("title", f"## {section_key.replace('_', ' ').title()}"))

            if "content" in section_data:
                parts.append("\n".join(section_data["content"]))

            if section_key == "project_structure":
                tree_config = TreeConfig(
                    comments=sections.get("tree_comments", {})
                )
                tree_generator = DirectoryTreeGenerator(tree_config)
                tree = tree_generator.generate(self.project_root)
                parts.append(f"```bash\n{tree.strip()}\n```")
        return parts
