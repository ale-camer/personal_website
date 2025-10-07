#!/usr/bin/env python3
"""
Automatic requirements.txt generator
Analyzes all .py files in the project and extracts necessary dependencies.
Can run in two modes:
1. Discovery Mode (--discover): Prints a 'pip install' command to the console.
2. Generation Mode (default): Creates a complete requirements.txt file with versions.
"""

import os
import ast
import sys
import subprocess
from pathlib import Path
import re
from tqdm import tqdm
import argparse

class RequirementsGenerator:
    def __init__(self, project_path="."):
        self.project_path = Path(project_path)
        self.imports = set()
        self.stdlib_modules = self._get_stdlib_modules()
        self.builtin_modules = self._get_builtin_modules()
        # Lista para ignorar paquetes que no son dependencias directas del proyecto
        self.exclude_list = {'importlib_metadata', 'pip', 'setuptools', 'wheel'}
        self.debug_mode = False
        self.file_contents = {}  # Store file contents for implicit dependency detection

    def enable_debug(self):
        """Enable debug mode for troubleshooting"""
        self.debug_mode = True

    def _debug_print(self, message):
        """Print debug messages if debug mode is enabled"""
        if self.debug_mode:
            print(f"DEBUG: {message}")

    def _get_builtin_modules(self):
        """Gets list of built-in modules that shouldn't be in requirements"""
        builtin = {
            'dataclasses', 'typing', 'typing_extensions', '__future__',
            '__main__', 'builtins', 'pkg_resources'
        }
        return builtin

    def _get_stdlib_modules(self):
        """Gets list of Python standard library modules"""
        stdlib = {
            'os', 'sys', 'json', 'csv', 'xml', 'html', 'http', 'urllib',
            'datetime', 'time', 'calendar', 'collections', 'itertools',
            'functools', 'operator', 'pathlib', 'glob', 'tempfile',
            'shutil', 'subprocess', 'threading', 'multiprocessing',
            'asyncio', 'socket', 'ssl', 'hashlib', 'hmac', 'secrets',
            'random', 'statistics', 'math', 'decimal', 'fractions',
            're', 'string', 'textwrap', 'unicodedata', 'stringprep',
            'struct', 'codecs', 'pickle', 'copyreg', 'shelve',
            'marshal', 'dbm', 'sqlite3', 'zlib', 'gzip', 'bz2',
            'lzma', 'zipfile', 'tarfile', 'configparser', 'netrc',
            'xdrlib', 'plistlib', 'argparse', 'logging', 'getopt',
            'curses', 'platform', 'errno', 'ctypes', 'io', 'email',
            'mailcap', 'mailbox', 'mimetypes', 'base64', 'binhex',
            'binascii', 'quopri', 'uu', 'warnings', 'contextlib',
            'abc', 'atexit', 'traceback', 'gc', 'inspect', 'site',
            'builtins', '__future__', '__main__', 'importlib',
            'types', 'copy', 'pprint', 'reprlib', 'enum', 'numbers',
            'cmath', 'array', 'weakref', 'bisect', 'heapq', 'keyword',
            'ast', 'dis', 'pickletools', 'formatter', 'getpass',
            'locale', 'fpectl', 'turtle', 'cmd', 'shlex'
        }
        return stdlib

    # Dentro de la clase RequirementsGenerator, reemplaza la función entera:

    def _is_local_module(self, module_name):
        """
        Checks if an import corresponds to a local .py file or directory
        within the project, to avoid adding project's own modules to requirements.
        """
        # 1. Check for a direct .py file match in the root
        if (self.project_path / f"{module_name}.py").exists():
            return True
            
        # 2. Check for a directory (package) match in the root
        if (self.project_path / module_name).is_dir():
            # Make sure it's a Python package (contains __init__.py)
            if (self.project_path / module_name / "__init__.py").exists():
                return True
                
        # 3. Check within common source directories like 'src' or 'modules'
        for src_dir in ['src', 'modules']:
            base = self.project_path / src_dir
            if not base.is_dir():
                continue
                
            if (base / f"{module_name}.py").exists():
                return True
                
            if (base / module_name).is_dir() and (base / module_name / "__init__.py").exists():
                return True

        # If none of the above, it's not a local module
        return False
    
    def _extract_imports_from_file(self, file_path):
        """Extracts imports from a Python file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.file_contents[str(file_path)] = content
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        self.imports.add(alias.name.split('.')[0])
                elif isinstance(node, ast.ImportFrom) and node.module:
                    self.imports.add(node.module.split('.')[0])
        except (SyntaxError, UnicodeDecodeError) as e:
            print(f"Error processing {file_path}: {e}")

    def _is_valid_package_name(self, package_name):
        """Validates if a package name is a real installable package"""
        invalid_names = {
            'modules', 'src', 'lib', 'utils', 'config', 'main', 'app',
            'test', 'tests', 'scripts', 'helpers', 'core', 'common',
            'tools', 'data', 'models', 'views', 'controllers'
        }
        if package_name in invalid_names or len(package_name) <= 1:
            return False
        return True

    def scan_project(self):
        """Scans the project looking for .py files"""
        print(f"Scanning project at: {self.project_path.resolve()}")
        python_files = [
            py_file for py_file in self.project_path.rglob("*.py")
            if not any(d in py_file.parts for d in {'__pycache__', '.git', 'venv', 'env', '.venv'})
        ]
        if not python_files:
            print("No Python files found.")
            return
        print(f"Found {len(python_files)} Python files to analyze.")
        for py_file in tqdm(python_files, desc="Analyzing files", unit="file"):
            self._extract_imports_from_file(py_file)

    def _get_package_version_importlib(self, package_name):
        """Gets the installed version using importlib.metadata (Python 3.8+)"""
        try:
            from importlib import metadata
        except ImportError:
            try:
                import importlib_metadata as metadata
            except ImportError:
                return None
        try:
            return metadata.version(package_name)
        except metadata.PackageNotFoundError:
            return None

    def _get_package_version(self, import_name):
        """Gets the installed version of a package"""
        correct_name = self._get_correct_package_name(import_name)
        version = self._get_package_version_importlib(correct_name)
        if version:
            return correct_name, version
        
        # Fallback if mapped name fails, try original import name
        if correct_name != import_name:
            version = self._get_package_version_importlib(import_name)
            if version:
                return import_name, version
        
        return correct_name, None

    def _get_implicit_dependencies(self):
        """Detect implicit dependencies based on code patterns"""
        implicit_deps = set()
        patterns = {
            'openpyxl': [r'\.to_excel\(', r'pd\.read_excel\(', r'ExcelWriter\(', r'\.xlsx["\']'],
            'python-dotenv': [r'load_dotenv\(', r'find_dotenv\('],
        }
        for content in self.file_contents.values():
            for dep, pattern_list in patterns.items():
                if any(re.search(p, content) for p in pattern_list):
                    implicit_deps.add(dep)
                    break
        return implicit_deps

    def _get_correct_package_name(self, import_name):
        """Gets the correct package name for installation from a map."""
        name_mapping = {
            'bs4': 'beautifulsoup4', 'cv2': 'opencv-python',
            'dotenv': 'python-dotenv', 'flask': 'Flask', 'PIL': 'Pillow',
            'sklearn': 'scikit-learn', 'yaml': 'PyYAML',
        }
        return name_mapping.get(import_name, import_name)

    def get_package_list(self, include_implicit=True):
        """Returns a clean list of package names for installation."""
        all_deps = set()
        for imp in sorted(self.imports):
            if imp in self.stdlib_modules or imp in self.builtin_modules or self._is_local_module(imp) or not self._is_valid_package_name(imp):
                continue
            all_deps.add(imp)

        if include_implicit:
            all_deps.update(self._get_implicit_dependencies())
        
        installable_names = {self._get_correct_package_name(dep) for dep in all_deps}
        return sorted(list(installable_names - self.exclude_list))

    def generate_requirements(self, output_file="requirements.txt", include_versions=True, include_implicit=True):
        """Generates the requirements.txt file"""
        package_list = self.get_package_list(include_implicit)
        if not package_list:
            print("No external dependencies found.")
            return

        print(f"\nFound {len(package_list)} external dependencies to process.")
        
        requirements = {}
        version_not_found = []

        for dep_name in tqdm(package_list, desc="Processing packages", unit="pkg"):
            correct_name, version = self._get_package_version(dep_name)
            if correct_name in requirements: continue

            if include_versions and version:
                requirements[correct_name] = f"{correct_name}=={version}"
            else:
                requirements[correct_name] = correct_name
                if include_versions:
                    version_not_found.append(correct_name)
        
        output_path = self.project_path / output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('# Generated by RequirementsGenerator\n')
            if version_not_found:
                f.write('# WARNING: Could not determine version for some packages\n')
            f.write('\n' + '\n'.join(sorted(requirements.values())) + '\n')

        print(f"\n✅ File '{output_file}' generated successfully at {output_path.resolve()}!")
        print(f"📦 Total dependencies written: {len(requirements)}")
        if version_not_found:
            print(f"\n⚠️ Warning: Could not find versions for: {', '.join(sorted(version_not_found))}")
            print("   Tip: Run this script inside your project's activated virtual environment.")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Generate requirements.txt from project imports.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("--path", "-p", default=".", help="Path to the project root (default: current directory)")
    parser.add_argument("--output", "-o", default="requirements.txt", help="Output file name (default: requirements.txt)")
    parser.add_argument("--no-versions", action="store_true", help="Do not include package versions")
    parser.add_argument("--no-implicit", action="store_true", help="Do not scan for implicit dependencies")
    parser.add_argument("--debug", action="store_true", help="Enable detailed debug output")
    parser.add_argument("--discover", action="store_true",
                        help="""Run in Discovery Mode.
Prints a 'pip install' command to the console with all
discovered dependencies and then exits. Does not create a file.""")

    args = parser.parse_args()
    
    generator = RequirementsGenerator(args.path)
    if args.debug:
        generator.enable_debug()

    generator.scan_project()
        
    if args.discover:
        print("\n[INFO] Running in Discovery Mode...")
        packages_to_install = generator.get_package_list(include_implicit=not args.no_implicit)
        if packages_to_install:
            print(f"[OK] Found {len(packages_to_install)} dependencies.")
            # MODIFICACIÓN: Guarda la lista en un archivo temporal
            with open("temp_deps.txt", "w") as f:
                f.write(" ".join(packages_to_install))
        else:
            print("[INFO] No external dependencies found.")
        sys.exit(0) # Salimos para que el .bat continúe

    generator.generate_requirements(
        output_file=args.output,
        include_versions=not args.no_versions,
        include_implicit=not args.no_implicit
    )

if __name__ == "__main__":
    main()