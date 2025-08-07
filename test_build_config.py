#!/usr/bin/env python3
"""
Test script to validate VIGRA build configuration files.
"""

import sys
import os
from pathlib import Path

def test_pyproject_toml():
    """Test if pyproject.toml is valid."""
    print("Testing pyproject.toml...")
    
    try:
        import tomllib
    except ImportError:
        try:
            import tomli as tomllib
        except ImportError:
            print("  Warning: No TOML parser available, skipping pyproject.toml validation")
            return True
    
    pyproject_path = Path("pyproject.toml")
    if not pyproject_path.exists():
        print("  ERROR: pyproject.toml not found")
        return False
    
    try:
        with open(pyproject_path, "rb") as f:
            config = tomllib.load(f)
        
        # Check required sections
        required_sections = ["build-system", "project"]
        for section in required_sections:
            if section not in config:
                print(f"  ERROR: Missing required section: {section}")
                return False
        
        # Check build system
        build_system = config["build-system"]
        if "requires" not in build_system:
            print("  ERROR: Missing 'requires' in build-system")
            return False
        
        if "build-backend" not in build_system:
            print("  ERROR: Missing 'build-backend' in build-system")
            return False
        
        # Check project metadata
        project = config["project"]
        required_project_fields = ["name", "description", "authors"]
        for field in required_project_fields:
            if field not in project:
                print(f"  ERROR: Missing required project field: {field}")
                return False
        
        print("  ✓ pyproject.toml is valid")
        return True
        
    except Exception as e:
        print(f"  ERROR: Failed to parse pyproject.toml: {e}")
        return False


def test_setup_py():
    """Test if setup.py is valid Python and has required components."""
    print("Testing setup.py...")
    
    setup_path = Path("setup.py")
    if not setup_path.exists():
        print("  ERROR: setup.py not found")
        return False
    
    try:
        # Test if setup.py is valid Python
        with open(setup_path, 'r') as f:
            setup_code = f.read()
        
        compile(setup_code, setup_path, 'exec')
        
        # Check for required components
        required_imports = [
            "from setuptools import setup",
            "from setuptools import Extension",
            "from pybind11",
            "import numpy"
        ]
        
        missing_imports = []
        for required_import in required_imports:
            if required_import not in setup_code:
                missing_imports.append(required_import)
        
        if missing_imports:
            print(f"  WARNING: Some expected imports not found: {missing_imports}")
        
        # Check for key functions/classes
        required_components = [
            "class VigraExtension",
            "class VIGRABuildExt",
            "def get_vigra_extensions",
            "def main"
        ]
        
        missing_components = []
        for component in required_components:
            if component not in setup_code:
                missing_components.append(component)
        
        if missing_components:
            print(f"  ERROR: Missing required components: {missing_components}")
            return False
        
        print("  ✓ setup.py is valid")
        return True
        
    except SyntaxError as e:
        print(f"  ERROR: Syntax error in setup.py: {e}")
        return False
    except Exception as e:
        print(f"  ERROR: Failed to validate setup.py: {e}")
        return False


def test_vigra_init():
    """Test if vigra/__init__.py is valid."""
    print("Testing vigra/__init__.py...")
    
    init_path = Path("vigra/__init__.py")
    if not init_path.exists():
        print("  ERROR: vigra/__init__.py not found")
        return False
    
    try:
        # Test if __init__.py is valid Python
        with open(init_path, 'r') as f:
            init_code = f.read()
        
        compile(init_code, init_path, 'exec')
        
        # Check for key components
        required_components = [
            "__version__",
            "__author__",
            "def readHDF5",
            "def writeHDF5",
            "def imshow"
        ]
        
        missing_components = []
        for component in required_components:
            if component not in init_code:
                missing_components.append(component)
        
        if missing_components:
            print(f"  WARNING: Some expected components not found: {missing_components}")
        
        print("  ✓ vigra/__init__.py is valid")
        return True
        
    except SyntaxError as e:
        print(f"  ERROR: Syntax error in vigra/__init__.py: {e}")
        return False
    except Exception as e:
        print(f"  ERROR: Failed to validate vigra/__init__.py: {e}")
        return False


def test_version_extraction():
    """Test version extraction from config_version.hxx."""
    print("Testing version extraction...")
    
    version_file = Path("include/vigra/config_version.hxx")
    if not version_file.exists():
        print("  ERROR: include/vigra/config_version.hxx not found")
        return False
    
    try:
        import re
        
        with open(version_file, 'r') as f:
            content = f.read()
        
        # Extract version components
        major_match = re.search(r'VIGRA_VERSION_MAJOR\s+(\d+)', content)
        minor_match = re.search(r'VIGRA_VERSION_MINOR\s+(\d+)', content)
        patch_match = re.search(r'VIGRA_VERSION_PATCH\s+(\d+)', content)
        
        if not all([major_match, minor_match, patch_match]):
            print("  ERROR: Could not extract version components")
            return False
        
        version = f"{major_match.group(1)}.{minor_match.group(1)}.{patch_match.group(1)}"
        print(f"  ✓ Extracted version: {version}")
        
        # Check if version matches what's in _version.py
        version_py = Path("vigra/_version.py")
        if version_py.exists():
            with open(version_py, 'r') as f:
                version_py_content = f.read()
            if version in version_py_content:
                print("  ✓ Version matches vigra/_version.py")
            else:
                print("  WARNING: Version mismatch with vigra/_version.py")
        
        return True
        
    except Exception as e:
        print(f"  ERROR: Failed to extract version: {e}")
        return False


def test_directory_structure():
    """Test if the directory structure is correct."""
    print("Testing directory structure...")
    
    required_files = [
        "pyproject.toml",
        "setup.py",
        "vigra/__init__.py",
        "vigra/_version.py",
        "include/vigra/config_version.hxx"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"  ERROR: Missing required files: {missing_files}")
        return False
    
    # Check for vigranumpy source structure
    vigranumpy_paths = [
        "vigranumpy/src/core",
        "vigranumpy/lib"
    ]
    
    missing_vigranumpy = []
    for path in vigranumpy_paths:
        if not Path(path).exists():
            missing_vigranumpy.append(path)
    
    if missing_vigranumpy:
        print(f"  WARNING: Missing vigranumpy paths: {missing_vigranumpy}")
        print("  This may affect the build process")
    
    print("  ✓ Directory structure is acceptable")
    return True


def main():
    """Run all tests."""
    print("VIGRA Build Configuration Validation")
    print("=" * 40)
    
    # Change to the vigra directory if we're not already there
    if Path("vigra").exists() and not Path("pyproject.toml").exists():
        os.chdir("vigra")
        print("Changed to vigra directory")
    
    tests = [
        test_directory_structure,
        test_version_extraction,
        test_pyproject_toml,
        test_setup_py,
        test_vigra_init,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"  ERROR: Test failed with exception: {e}")
            results.append(False)
        print()
    
    # Summary
    print("Summary:")
    print("=" * 40)
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✓ All {total} tests passed!")
        print("\nThe VIGRA build configuration appears to be ready.")
        print("\nNext steps:")
        print("1. Install build dependencies: pip install -e .")
        print("2. Build the package: python -m build")
        print("3. Test the installation: python -c 'import vigra; print(vigra.__version__)'")
        return 0
    else:
        print(f"✗ {total - passed} out of {total} tests failed")
        print("\nPlease fix the issues above before proceeding with the build.")
        return 1


if __name__ == "__main__":
    sys.exit(main())