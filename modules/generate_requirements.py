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
        # Check if it's literally the modules directory name
        if module_name == 'modules':
            return True
            
        module_path = self.project_path / f"{module_name}.py"
        package_path = self.project_path / module_name / "__init__.py"
        modules_package_path = self.project_path / "modules" / module_name / "__init__.py"
        modules_file_path = self.project_path / "modules" / f"{module_name}.py"
        
        return (module_path.exists() or 
                package_path.exists() or 
                modules_package_path.exists() or 
                modules_file_path.exists())

    def _extract_imports_from_file(self, file_path):
        """Extracts imports from a Python file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        self.imports.add(alias.name.split('.')[0])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        self.imports.add(node.module.split('.')[0])
                        
        except (SyntaxError, UnicodeDecodeError) as e:
            print(f"Error processing {file_path}: {e}")

    def _is_valid_package_name(self, package_name):
        """Validates if a package name is a real installable package"""
        # Skip obvious non-packages
        invalid_names = {
            'modules',  # Your local modules directory
            'src',      # Common source directory
            'lib',      # Common library directory
            'utils',    # Common utils directory/file
            'config',   # Common config file
            'main',     # Common main file
            'app',      # Common app file
            'test',     # Test files
            'tests',    # Test directory
        }
        
        if package_name in invalid_names:
            return False
            
        # Skip single letter names (usually variables)
        if len(package_name) <= 1:
            return False
            
        # Skip names that look like file extensions
        if package_name in ['py', 'txt', 'json', 'csv', 'xml']:
            return False
            
        return True

    def scan_project(self):
        """Scans the project looking for .py files in root directory and modules subdirectory"""
        print(f"Scanning project at: {self.project_path.absolute()}")
        
        python_files = []
        
        # Scan files in the root directory
        for py_file in self.project_path.glob("*.py"):
            python_files.append(py_file)
        
        # Scan files in the modules subdirectory (if it exists)
        modules_dir = self.project_path / "modules"
        if modules_dir.exists() and modules_dir.is_dir():
            for py_file in modules_dir.rglob("*.py"):
                python_files.append(py_file)
        
        if not python_files:
            print("No Python files found in the project root or modules directory")
            return
            
        print(f"Found {len(python_files)} Python files")
        
        # Filter out files in common directories that don't need analysis
        filtered_files = []
        for py_file in python_files:
            if any(part in str(py_file) for part in ['__pycache__', '.pytest_cache']):
                continue
            filtered_files.append(py_file)
        
        # Process files with progress bar
        for py_file in tqdm(filtered_files, desc="Analyzing files", unit="file"):
            self._extract_imports_from_file(py_file)

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
                    return pkg_resources.get_distribution(alternative_names[package_name]).version
                except pkg_resources.DistributionNotFound:
                    pass
            
            return None

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
        
        return name_mapping.get(import_name, import_name)

    def generate_requirements(self, output_file="requirements.txt", include_versions=True):
        """Generates the requirements.txt file"""
        # Filter imports
        external_packages = []
        
        for imp in sorted(self.imports):
            # Skip standard library modules
            if imp in self.stdlib_modules:
                continue
                
            # Skip built-in modules
            if imp in self.builtin_modules:
                continue
                
            # Skip local modules
            if self._is_local_module(imp):
                continue
                
            # Skip invalid package names
            if not self._is_valid_package_name(imp):
                continue
                
            # Skip relative imports and other special cases
            if imp.startswith('.') or imp == '':
                continue
                
            external_packages.append(imp)

        if not external_packages:
            print("No external dependencies found")
            return

        print(f"\nExternal dependencies found: {len(external_packages)}")
        
        # Generate requirements.txt
        requirements = []
        
        for package in tqdm(external_packages, desc="Processing packages", unit="pkg"):
            # Get the correct package name for installation
            correct_name = self._get_correct_package_name(package)
            
            if include_versions:
                version = self._get_package_version(package)
                if version:
                    requirements.append(f"{correct_name}=={version}")
                else:
                    requirements.append(correct_name)
            else:
                requirements.append(correct_name)

        # Write file
        output_path = self.project_path / output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(requirements))
            f.write('\n')

        print(f"\n✅ File {output_file} generated successfully!")
        print(f"📍 Location: {output_path.absolute()}")
        print(f"📦 Total dependencies: {len(requirements)}")
        
        # Show summary of packages
        print("\nPackages included:")
        for req in requirements:
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
    
    args = parser.parse_args()
    
    generator = RequirementsGenerator(args.path)
    generator.scan_project()
    generator.generate_requirements(args.output, not args.no_versions)
