#!/usr/bin/env python3
"""
VIGRA Computer Vision Library - Python Build System
Modern setuptools-based build configuration for VIGRA with C++ extensions.
"""

import os
import re
import sys
import subprocess
import platform
from pathlib import Path
from typing import List, Dict, Optional, Tuple

from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext
from pybind11.setup_helpers import Pybind11Extension, build_ext as pybind11_build_ext
from pybind11 import get_cmake_dir
import pybind11
import numpy


class VigraExtension(Pybind11Extension):
    """Custom extension class for VIGRA C++ modules."""
    
    def __init__(self, name: str, sources: List[str], **kwargs):
        # Set default include directories
        include_dirs = kwargs.get('include_dirs', [])
        include_dirs.extend([
            'include',
            'vigranumpy/src/core',
            numpy.get_include(),
            pybind11.get_include(),
        ])
        kwargs['include_dirs'] = include_dirs
        
        # Set default compile flags
        extra_compile_args = kwargs.get('extra_compile_args', [])
        if platform.system() != 'Windows':
            extra_compile_args.extend([
                '-std=c++11',
                '-ftemplate-depth=900',
                '-O3',
                '-DNDEBUG',
            ])
        else:
            extra_compile_args.extend([
                '/std:c++11',
                '/O2',
                '/DNDEBUG',
                '/D_CRT_SECURE_NO_DEPRECATE',
                '/D_SCL_SECURE_NO_DEPRECATE',
            ])
        kwargs['extra_compile_args'] = extra_compile_args
        
        super().__init__(name, sources, **kwargs)


class VIGRABuildExt(pybind11_build_ext):
    """Custom build_ext command for VIGRA extensions."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dependencies = {}
        self.vigra_version = None
    
    def build_extensions(self):
        """Build all extensions with dependency detection."""
        print("Building VIGRA extensions...")
        
        # Extract version information
        self.vigra_version = self.get_vigra_version()
        print(f"Building VIGRA version: {self.vigra_version}")
        
        # Detect system dependencies
        self.detect_dependencies()
        
        # Configure extensions based on available dependencies
        self.configure_extensions()
        
        # Build extensions
        super().build_extensions()
    
    def get_vigra_version(self) -> str:
        """Extract version from vigra/include/vigra/config_version.hxx."""
        version_file = Path('include/vigra/config_version.hxx')
        if not version_file.exists():
            return "1.12.2"  # fallback version
        
        try:
            content = version_file.read_text()
            major = re.search(r'VIGRA_VERSION_MAJOR\s+(\d+)', content)
            minor = re.search(r'VIGRA_VERSION_MINOR\s+(\d+)', content)
            patch = re.search(r'VIGRA_VERSION_PATCH\s+(\d+)', content)
            
            if major and minor and patch:
                return f"{major.group(1)}.{minor.group(1)}.{patch.group(1)}"
        except Exception as e:
            print(f"Warning: Could not read version file: {e}")
        
        return "1.12.2"  # fallback version
    
    def detect_dependencies(self):
        """Detect available system dependencies."""
        print("Detecting system dependencies...")
        
        # Core dependencies
        self.dependencies = {
            'zlib': self.find_library('z', ['zlib.h']),
            'jpeg': self.find_library('jpeg', ['jpeglib.h']),
            'png': self.find_library('png', ['png.h']),
            'tiff': self.find_library('tiff', ['tiffio.h']),
            'fftw3': self.find_library('fftw3', ['fftw3.h']),
            'fftw3f': self.find_library('fftw3f', ['fftw3.h']),
            'hdf5': self.find_library('hdf5', ['hdf5.h']),
        }
        
        # Report findings
        for name, found in self.dependencies.items():
            status = "found" if found else "not found"
            print(f"  {name}: {status}")
    
    def find_library(self, lib_name: str, headers: List[str]) -> bool:
        """Check if a library and its headers are available."""
        try:
            # Try to compile a simple test program
            import tempfile
            import shutil
            
            with tempfile.TemporaryDirectory() as tmpdir:
                test_file = Path(tmpdir) / "test.c"
                test_file.write_text(f"""
                    {' '.join(f'#include <{h}>' for h in headers)}
                    int main() {{ return 0; }}
                """)
                
                # Try to compile
                result = subprocess.run([
                    'gcc', '-c', str(test_file), '-o', str(tmpdir / 'test.o')
                ], capture_output=True, text=True)
                
                return result.returncode == 0
        except Exception:
            return False
    
    def configure_extensions(self):
        """Configure extensions based on available dependencies."""
        for ext in self.extensions:
            if isinstance(ext, VigraExtension):
                self.configure_vigra_extension(ext)
    
    def configure_vigra_extension(self, ext: VigraExtension):
        """Configure a VIGRA extension based on available dependencies."""
        # Add system library paths
        if platform.system() == 'Darwin':  # macOS
            ext.library_dirs.extend([
                '/usr/local/lib',
                '/opt/homebrew/lib',
            ])
            ext.include_dirs.extend([
                '/usr/local/include',
                '/opt/homebrew/include',
            ])
        elif platform.system() == 'Linux':
            ext.library_dirs.extend([
                '/usr/lib',
                '/usr/local/lib',
                '/usr/lib/x86_64-linux-gnu',
            ])
            ext.include_dirs.extend([
                '/usr/include',
                '/usr/local/include',
            ])
        
        # Add libraries based on availability
        libraries = []
        defines = []
        
        if self.dependencies.get('zlib'):
            libraries.append('z')
            defines.append('HasZLIB')
        
        if self.dependencies.get('jpeg'):
            libraries.append('jpeg')
            defines.append('HasJPEG')
        
        if self.dependencies.get('png'):
            libraries.append('png')
            defines.append('HasPNG')
        
        if self.dependencies.get('tiff'):
            libraries.append('tiff')
            defines.append('HasTIFF')
        
        if self.dependencies.get('fftw3'):
            libraries.append('fftw3')
            defines.append('HasFFTW3')
        
        if self.dependencies.get('fftw3f'):
            libraries.append('fftw3f')
            defines.append('HasFFTW3F')
        
        if self.dependencies.get('hdf5'):
            libraries.append('hdf5')
            defines.append('HasHDF5')
        
        ext.libraries.extend(libraries)
        ext.define_macros.extend([(d, None) for d in defines])
        
        # Platform-specific configurations
        if platform.system() == 'Windows':
            ext.define_macros.extend([
                ('VIGRA_STATIC_LIB', None),
                ('_CRT_SECURE_NO_DEPRECATE', None),
                ('_SCL_SECURE_NO_DEPRECATE', None),
            ])


def get_vigra_extensions() -> List[Extension]:
    """Define VIGRA C++ extensions."""
    
    # Core vigranumpy extension
    vigranumpy_sources = []
    core_src_dir = Path('vigranumpy/src/core')
    if core_src_dir.exists():
        vigranumpy_sources.extend([
            str(f) for f in core_src_dir.glob('*.cxx')
        ])
    
    # Fallback sources if directory structure is different
    if not vigranumpy_sources:
        vigranumpy_sources = [
            'vigranumpy/src/core/vigranumpycore.cxx',  # main module
        ]
    
    extensions = [
        VigraExtension(
            'vigra.vigranumpycore',
            sources=vigranumpy_sources,
            language='c++',
            define_macros=[
                ('VIGRA_STATIC_LIB', None),
            ],
        ),
    ]
    
    # Optional FFTW extension
    fftw_src_dir = Path('vigranumpy/src/fourier')
    if fftw_src_dir.exists():
        fftw_sources = [str(f) for f in fftw_src_dir.glob('*.cxx')]
        if fftw_sources:
            extensions.append(
                VigraExtension(
                    'vigra.fourier',
                    sources=fftw_sources,
                    language='c++',
                    libraries=['fftw3f'],
                )
            )
    
    return extensions


def get_package_data() -> Dict[str, List[str]]:
    """Get package data files."""
    package_data = {
        'vigra': [
            '*.so',
            '*.pyd',
            '*.dll',
        ]
    }
    
    # Add documentation if available
    doc_dir = Path('vigranumpy/vigra/doc')
    if doc_dir.exists():
        package_data['vigra'].extend([
            'doc/vigra/*.*',
            'doc/vigra/documents/*.*',
            'doc/vigranumpy/*.*',
            'doc/vigranumpy/_static/*.*',
        ])
    
    return package_data


def get_long_description() -> str:
    """Get long description from README."""
    readme_file = Path('README.md')
    if readme_file.exists():
        return readme_file.read_text(encoding='utf-8')
    return "VIGRA Computer Vision Library - Python bindings"


def main():
    """Main setup function."""
    
    # Ensure we're in the right directory
    if not Path('include/vigra/config_version.hxx').exists():
        print("Error: This setup.py must be run from the VIGRA root directory")
        sys.exit(1)
    
    # Get extensions
    extensions = get_vigra_extensions()
    
    # Setup configuration
    setup(
        name='vigra',
        use_scm_version={
            'write_to': 'vigra/_version.py',
            'fallback_version': '1.12.2',
        },
        description='VIGRA Computer Vision Library - Python bindings',
        long_description=get_long_description(),
        long_description_content_type='text/markdown',
        author='Ullrich Koethe',
        author_email='ullrich.koethe@iwr.uni-heidelberg.de',
        url='http://hci.iwr.uni-heidelberg.de/vigra/',
        license='MIT',
        
        packages=find_packages(where='vigranumpy'),
        package_dir={'': 'vigranumpy'},
        package_data=get_package_data(),
        
        ext_modules=extensions,
        cmdclass={'build_ext': VIGRABuildExt},
        
        python_requires='>=3.8',
        install_requires=[
            'numpy>=1.19.0',
        ],
        
        setup_requires=[
            'setuptools>=61.0',
            'wheel',
            'pybind11>=2.10.0',
            'numpy>=1.19.0',
            'setuptools_scm>=6.0',
        ],
        
        extras_require={
            'io': ['Pillow>=8.0.0'],
            'scientific': ['scipy>=1.6.0', 'scikit-image>=0.18.0'],
            'viz': ['matplotlib>=3.3.0'],
            'hdf5': ['h5py>=3.0.0'],
            'full': [
                'Pillow>=8.0.0',
                'scipy>=1.6.0',
                'scikit-image>=0.18.0',
                'matplotlib>=3.3.0',
                'h5py>=3.0.0',
            ],
            'dev': [
                'pytest>=6.0.0',
                'pytest-cov>=2.10.0',
                'black>=21.0.0',
                'ruff>=0.1.0',
                'sphinx>=4.0.0',
            ],
        },
        
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: C++',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.11',
            'Programming Language :: Python :: 3.12',
            'Topic :: Scientific/Engineering :: Image Processing',
            'Topic :: Scientific/Engineering :: Artificial Intelligence',
        ],
        
        zip_safe=False,  # C++ extensions are not zip safe
    )


if __name__ == '__main__':
    main()