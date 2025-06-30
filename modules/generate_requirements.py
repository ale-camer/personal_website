#!/usr/bin/env python3
"""
Automatic requirements.txt generator
Analyzes all .py files in the project and extracts necessary dependencies
"""

import os
import ast
import sys
import subprocess
import pkg_resources
from pathlib import Path
import re
from tqdm import tqdm

class RequirementsGenerator:
    def __init__(self, project_path="."):
        self.project_path = Path(project_path)
        self.imports = set()
        self.stdlib_modules = self._get_stdlib_modules()
        self.builtin_modules = self._get_builtin_modules()
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
            'dataclasses',  # Built-in since Python 3.7
            'pkg_resources',  # Part of setuptools, not a standalone package
            'typing',  # Built-in since Python 3.5
            'typing_extensions',  # Usually installed by other packages
            '__future__',
            '__main__',
            'builtins'
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

    def _is_local_module(self, module_name):
        """Checks if it's a local project module"""
        # Lista de nombres comunes de directorios locales
        local_dirs = {
            'modules', 'src', 'lib', 'utils', 'config', 'main', 'app', 
            'test', 'tests', 'scripts', 'helpers', 'core', 'common',
            'tools', 'data', 'models', 'views', 'controllers'
        }
        
        # Si es exactamente el nombre de un directorio local conocido
        if module_name in local_dirs:
            return True

        # Verificar si existe como archivo o directorio en el proyecto
        module_path = self.project_path / f"{module_name}.py"
        package_path = self.project_path / module_name / "__init__.py"
        modules_package_path = self.project_path / "modules" / module_name / "__init__.py"
        modules_file_path = self.project_path / "modules" / f"{module_name}.py"
        src_package_path = self.project_path / "src" / module_name / "__init__.py"
        src_file_path = self.project_path / "src" / f"{module_name}.py"

        is_local = (module_path.exists() or
                   package_path.exists() or
                   modules_package_path.exists() or
                   modules_file_path.exists() or
                   src_package_path.exists() or
                   src_file_path.exists())

        if is_local:
            self._debug_print(f"Module '{module_name}' identified as local")

        return is_local

    def _extract_imports_from_file(self, file_path):
        """Extracts imports from a Python file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Store content for implicit dependency detection
            self.file_contents[str(file_path)] = content

            tree = ast.parse(content)
            file_imports = set()

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        import_name = alias.name.split('.')[0]
                        file_imports.add(import_name)
                        self.imports.add(import_name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        import_name = node.module.split('.')[0]
                        file_imports.add(import_name)
                        self.imports.add(import_name)

            if file_imports and self.debug_mode:
                self._debug_print(f"File {file_path.name}: {', '.join(sorted(file_imports))}")

        except (SyntaxError, UnicodeDecodeError) as e:
            print(f"Error processing {file_path}: {e}")

    def _is_valid_package_name(self, package_name):
        """Validates if a package name is a real installable package"""
        # Skip obvious non-packages
        invalid_names = {
            'modules',  # Local modules directory
            'src',      # Common source directory
            'lib',      # Common library directory
            'utils',    # Common utils directory/file
            'config',   # Common config file
            'main',     # Common main file
            'app',      # Common app file
            'test',     # Test files
            'tests',    # Test directory
            'scripts',  # Scripts directory
            'helpers',  # Helpers directory
            'core',     # Core directory
            'common',   # Common directory
            'tools',    # Tools directory
            'data',     # Data directory
            'models',   # Models directory
            'views',    # Views directory
            'controllers', # Controllers directory
        }

        if package_name in invalid_names:
            self._debug_print(f"Package '{package_name}' marked as invalid (common directory/file name)")
            return False

        # Skip single letter names (usually variables)
        if len(package_name) <= 1:
            self._debug_print(f"Package '{package_name}' marked as invalid (too short)")
            return False

        # Skip names that look like file extensions
        if package_name in ['py', 'txt', 'json', 'csv', 'xml']:
            self._debug_print(f"Package '{package_name}' marked as invalid (file extension)")
            return False

        return True

    def scan_project(self):
        """Scans the project looking for .py files in root directory and subdirectories"""
        print(f"Scanning project at: {self.project_path.absolute()}")

        python_files = []

        # Scan all Python files recursively, but exclude common non-relevant directories
        exclude_dirs = {'__pycache__', '.pytest_cache', '.git', 'venv', 'env', '.venv', 'node_modules', '.tox'}
        
        for py_file in self.project_path.rglob("*.py"):
            # Skip files in excluded directories
            if any(excluded_dir in py_file.parts for excluded_dir in exclude_dirs):
                continue
            python_files.append(py_file)

        if not python_files:
            print("No Python files found in the project")
            return

        print(f"Found {len(python_files)} Python files")
        self._debug_print(f"Processing {len(python_files)} files")

        # Process files with progress bar
        for py_file in tqdm(python_files, desc="Analyzing files", unit="file"):
            self._extract_imports_from_file(py_file)

        self._debug_print(f"Total unique imports found: {len(self.imports)}")
        if self.debug_mode:
            self._debug_print(f"All imports: {', '.join(sorted(self.imports))}")

    def _get_package_version(self, package_name):
        """Gets the installed version of a package"""
        try:
            return pkg_resources.get_distribution(package_name).version
        except pkg_resources.DistributionNotFound:
            # Try with common alternative names
            alternative_names = {
                'cv2': 'opencv-python',
                'PIL': 'Pillow',
                'sklearn': 'scikit-learn',
                'yaml': 'PyYAML',
                'bs4': 'beautifulsoup4',
                'serial': 'pyserial',
                'dotenv': 'python-dotenv'
            }

            if package_name in alternative_names:
                try:
                    alt_name = alternative_names[package_name]
                    version = pkg_resources.get_distribution(alt_name).version
                    self._debug_print(f"Found version for {package_name} via {alt_name}: {version}")
                    return version
                except pkg_resources.DistributionNotFound:
                    pass

            self._debug_print(f"No version found for package: {package_name}")
            return None

    def _get_implicit_dependencies(self):
        """Detect implicit dependencies based on code patterns"""
        implicit_deps = set()

        # Patrones mejorados para detectar dependencias implícitas
        patterns = {
            'openpyxl': [
                r'\.to_excel\s*\(',
                r'pd\.read_excel\s*\(',
                r'pandas\.read_excel\s*\(',
                r'ExcelWriter\s*\(',
                r'\.xlsx["\']',
                r'engine\s*=\s*["\']openpyxl["\']',
                r'pd\.ExcelWriter\s*\(',
                r'pandas\.ExcelWriter\s*\(',
            ],
            'xlrd': [
                r'engine\s*=\s*["\']xlrd["\']',
                r'\.xls["\']',
            ],
            'lxml': [
                r'\.read_xml\s*\(',
                r'pd\.read_xml\s*\(',
                r'pandas\.read_xml\s*\(',
                r'\.to_xml\s*\(',
                r'engine\s*=\s*["\']lxml["\']',
            ],
            'sqlalchemy': [
                r'\.read_sql\s*\(',
                r'pd\.read_sql\s*\(',
                r'pandas\.read_sql\s*\(',
                r'\.to_sql\s*\(',
                r'create_engine\s*\(',
            ],
            'beautifulsoup4': [
                r'\.read_html\s*\(',
                r'pd\.read_html\s*\(',
                r'pandas\.read_html\s*\(',
            ],
            'python-dotenv': [
                r'load_dotenv\s*\(',
                r'find_dotenv\s*\(',
                r'dotenv_values\s*\(',
                r'set_key\s*\(',
                r'get_key\s*\(',
                r'unset_key\s*\(',
                r'from\s+dotenv\s+import',
                r'import\s+dotenv',
            ]
        }

        # Verificar todos los contenidos de archivos almacenados
        for file_path, content in self.file_contents.items():
            for dep, pattern_list in patterns.items():
                for pattern in pattern_list:
                    if re.search(pattern, content, re.IGNORECASE):
                        implicit_deps.add(dep)
                        self._debug_print(f"Found implicit dependency '{dep}' in {Path(file_path).name} (pattern: {pattern})")
                        break  # Found one pattern for this dependency, move to next

        return implicit_deps

    def _get_correct_package_name(self, import_name):
        """Gets the correct package name for installation"""
        # Common alternative names mapping
        name_mapping = {
            'cv2': 'opencv-python',
            'PIL': 'Pillow',
            'sklearn': 'scikit-learn',
            'yaml': 'PyYAML',
            'bs4': 'beautifulsoup4',
            'serial': 'pyserial',
            'dotenv': 'python-dotenv'
        }

        correct_name = name_mapping.get(import_name, import_name)
        if correct_name != import_name:
            self._debug_print(f"Mapped {import_name} -> {correct_name}")

        return correct_name

    def generate_requirements(self, output_file="requirements.txt", include_versions=True, include_implicit=True):
        """Generates the requirements.txt file"""
        # Filter imports
        external_packages = []
        skipped_packages = []

        for imp in sorted(self.imports):
            skip_reason = None

            # Skip standard library modules
            if imp in self.stdlib_modules:
                skip_reason = "stdlib"
            # Skip built-in modules
            elif imp in self.builtin_modules:
                skip_reason = "builtin"
            # Skip local modules
            elif self._is_local_module(imp):
                skip_reason = "local"
            # Skip invalid package names
            elif not self._is_valid_package_name(imp):
                skip_reason = "invalid"
            # Skip relative imports and other special cases
            elif imp.startswith('.') or imp == '':
                skip_reason = "special"

            if skip_reason:
                skipped_packages.append((imp, skip_reason))
                self._debug_print(f"Skipped '{imp}' ({skip_reason})")
            else:
                external_packages.append(imp)
                self._debug_print(f"Added '{imp}' as external package")

        # Add implicit dependencies
        implicit_deps = set()
        if include_implicit:
            implicit_deps = self._get_implicit_dependencies()
            for dep in implicit_deps:
                # Get the correct package name for comparison
                correct_dep_name = self._get_correct_package_name(dep)
                
                # Check if this dependency is already covered by explicit imports
                already_covered = False
                for existing_pkg in external_packages:
                    existing_correct_name = self._get_correct_package_name(existing_pkg)
                    if correct_dep_name == existing_correct_name:
                        already_covered = True
                        self._debug_print(f"Implicit dependency '{dep}' already covered by explicit import '{existing_pkg}'")
                        break
                
                if not already_covered:
                    external_packages.append(dep)
                    self._debug_print(f"Added '{dep}' as implicit dependency")

        if self.debug_mode:
            print(f"\nDEBUG Summary:")
            print(f"Total imports found: {len(self.imports)}")
            print(f"Implicit dependencies found: {len(implicit_deps)}")
            print(f"External packages: {len(external_packages)}")
            print(f"Skipped packages: {len(skipped_packages)}")
            if implicit_deps:
                print(f"Implicit dependencies: {', '.join(sorted(implicit_deps))}")
            if skipped_packages:
                print("Skipped packages breakdown:")
                for reason in set(reason for _, reason in skipped_packages):
                    count = len([p for p, r in skipped_packages if r == reason])
                    examples = [p for p, r in skipped_packages if r == reason][:3]
                    print(f"  {reason}: {count} packages (e.g., {', '.join(examples)})")

        if not external_packages:
            print("No external dependencies found")
            if self.debug_mode:
                print("This might indicate:")
                print("1. No external imports in your code")
                print("2. All imports are being classified as local/stdlib")
                print("3. Issue with file scanning")
            return

        print(f"\nExternal dependencies found: {len(external_packages)}")
        if self.debug_mode:
            print(f"External packages: {', '.join(external_packages)}")

        # Generate requirements.txt (remove duplicates and sort)
        requirements = []
        seen_packages = set()

        for package in tqdm(external_packages, desc="Processing packages", unit="pkg"):
            # Get the correct package name for installation
            correct_name = self._get_correct_package_name(package)
            
            # Skip if we've already processed this package
            if correct_name in seen_packages:
                self._debug_print(f"Skipping duplicate package: {correct_name} (from {package})")
                continue
                
            seen_packages.add(correct_name)

            if include_versions:
                version = self._get_package_version(package)
                if version:
                    requirements.append(f"{correct_name}=={version}")
                else:
                    requirements.append(correct_name)
            else:
                requirements.append(correct_name)

        # Write file with header
        output_path = self.project_path / output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('# Generated by RequirementsGenerator\n')
            f.write('# This file lists all Python dependencies for this project\n\n')
            f.write('\n'.join(sorted(requirements)))
            f.write('\n')

        print(f"\n✅ File {output_file} generated successfully!")
        print(f"📍 Location: {output_path.absolute()}")
        print(f"📦 Total dependencies: {len(requirements)}")

        # Show summary of packages
        print("\nPackages included:")
        for req in sorted(requirements):
            if "==" in req:
                pkg_name, version = req.split("==")
                print(f"  ✓ {pkg_name} (v{version})")
            else:
                print(f"  ? {req} (version not found)")

def main():
    """Main function"""
    import argparse

    parser = argparse.ArgumentParser(description="Generate requirements.txt automatically")
    parser.add_argument("--path", "-p", default=".",
                       help="Project path (default: current directory)")
    parser.add_argument("--output", "-o", default="requirements.txt",
                       help="Output file name (default: requirements.txt)")
    parser.add_argument("--no-versions", action="store_true",
                       help="Don't include specific versions")
    parser.add_argument("--no-implicit", action="store_true",
                       help="Don't include implicit dependencies (like openpyxl for pandas)")
    parser.add_argument("--debug", action="store_true",
                       help="Enable debug mode for troubleshooting")

    args = parser.parse_args()

    generator = RequirementsGenerator(args.path)

    if args.debug:
        generator.enable_debug()

    generator.scan_project()
    generator.generate_requirements(args.output, not args.no_versions, not args.no_implicit)

if __name__ == "__main__":
    main()