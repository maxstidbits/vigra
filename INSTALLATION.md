# VIGRA Installation Guide

This guide provides comprehensive installation instructions for the VIGRA Computer Vision Library using the modern setuptools/pip build system.

## Table of Contents

- [Quick Installation](#quick-installation)
- [System Requirements](#system-requirements)
- [Platform-Specific Instructions](#platform-specific-instructions)
  - [Windows](#windows)
  - [macOS](#macos)
  - [Linux](#linux)
- [Python Environment Setup](#python-environment-setup)
- [Installation Methods](#installation-methods)
- [Optional Dependencies](#optional-dependencies)
- [Development Installation](#development-installation)
- [Building from Source](#building-from-source)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)
- [Performance Optimization](#performance-optimization)

## Quick Installation

For most users, a simple pip install is sufficient:

```bash
# Install VIGRA with basic functionality
pip install vigra

# Install with all features (recommended)
pip install vigra[full]
```

## System Requirements

### Minimum Requirements
- **Python**: 3.8 or higher
- **pip**: 21.0 or higher
- **setuptools**: 61.0 or higher
- **wheel**: Latest version
- **C++ Compiler**: C++11 compatible

### Recommended Requirements
- **Python**: 3.10 or higher
- **NumPy**: 1.19.0 or higher
- **Memory**: 4GB RAM minimum, 8GB recommended
- **Disk Space**: 500MB for installation, 2GB for development

### Supported Platforms
- **Windows**: 10/11 (x64)
- **macOS**: 10.15+ (Intel and Apple Silicon)
- **Linux**: Ubuntu 18.04+, CentOS 7+, Debian 10+

## Platform-Specific Instructions

### Windows

#### Prerequisites

1. **Install Python**
   ```powershell
   # Download from python.org or use Microsoft Store
   # Verify installation
   python --version
   pip --version
   ```

2. **Install Visual Studio Build Tools**
   - Download [Visual Studio Build Tools 2022](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022)
   - Install with "C++ build tools" workload
   - Or install Visual Studio Community with C++ development tools

3. **Alternative: Install via Chocolatey**
   ```powershell
   # Install Chocolatey first (if not installed)
   Set-ExecutionPolicy Bypass -Scope Process -Force
   [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
   iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
   
   # Install build tools
   choco install visualstudio2022buildtools
   choco install visualstudio2022-workload-vctools
   ```

#### Installation

```powershell
# Update pip and setuptools
python -m pip install --upgrade pip setuptools wheel

# Install VIGRA
pip install vigra[full]

# Verify installation
python -c "import vigra; print(f'VIGRA {vigra.__version__} installed successfully')"
```

#### Optional System Dependencies (via vcpkg)

```powershell
# Install vcpkg
git clone https://github.com/Microsoft/vcpkg.git
cd vcpkg
.\bootstrap-vcpkg.bat

# Install libraries
.\vcpkg install libpng libjpeg-turbo tiff fftw3 hdf5 zlib
.\vcpkg integrate install
```

### macOS

#### Prerequisites

1. **Install Xcode Command Line Tools**
   ```bash
   xcode-select --install
   ```

2. **Install Homebrew** (if not installed)
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

3. **Install Python** (if using system Python is not preferred)
   ```bash
   brew install python@3.11
   ```

#### System Dependencies

```bash
# Install core dependencies
brew install cmake pkg-config

# Install image format libraries
brew install libpng jpeg libtiff

# Install scientific computing libraries
brew install fftw hdf5 openblas

# Install compression libraries
brew install zlib lz4 zstd
```

#### Installation

```bash
# Update pip and setuptools
python3 -m pip install --upgrade pip setuptools wheel

# Install VIGRA with all features
pip3 install vigra[full]

# Verify installation
python3 -c "import vigra; print(f'VIGRA {vigra.__version__} installed successfully')"
```

#### Apple Silicon (M1/M2) Specific Notes

```bash
# Ensure you're using native Python (not Rosetta)
python3 -c "import platform; print(platform.machine())"  # Should show 'arm64'

# If using conda, create native environment
conda create -n vigra python=3.11
conda activate vigra

# Install with native compilation
pip install vigra[full]
```

### Linux

#### Ubuntu/Debian

```bash
# Update package list
sudo apt-get update

# Install build essentials
sudo apt-get install build-essential cmake pkg-config

# Install Python development headers
sudo apt-get install python3-dev python3-pip python3-venv

# Install system dependencies
sudo apt-get install \
    libpng-dev libjpeg-dev libtiff-dev \
    libfftw3-dev libhdf5-dev \
    zlib1g-dev liblz4-dev \
    libopenblas-dev liblapack-dev

# Update pip and install VIGRA
python3 -m pip install --upgrade pip setuptools wheel
pip3 install vigra[full]
```

#### CentOS/RHEL/Fedora

```bash
# CentOS/RHEL 7/8
sudo yum groupinstall "Development Tools"
sudo yum install cmake3 python3-devel python3-pip

# Fedora
sudo dnf groupinstall "Development Tools"
sudo dnf install cmake python3-devel python3-pip

# Install system dependencies
sudo yum install \
    libpng-devel libjpeg-devel libtiff-devel \
    fftw3-devel hdf5-devel \
    zlib-devel lz4-devel \
    openblas-devel lapack-devel

# Install VIGRA
pip3 install --user vigra[full]
```

#### Arch Linux

```bash
# Install build tools
sudo pacman -S base-devel cmake python python-pip

# Install system dependencies
sudo pacman -S \
    libpng libjpeg-turbo libtiff \
    fftw hdf5 zlib lz4 \
    openblas lapack

# Install VIGRA
pip install vigra[full]
```

## Python Environment Setup

### Using Virtual Environments (Recommended)

```bash
# Create virtual environment
python -m venv vigra-env

# Activate environment
# Windows:
vigra-env\Scripts\activate
# macOS/Linux:
source vigra-env/bin/activate

# Install VIGRA
pip install vigra[full]
```

### Using Conda

```bash
# Create conda environment
conda create -n vigra python=3.11 numpy scipy matplotlib
conda activate vigra

# Install VIGRA
pip install vigra[full]

# Or install from conda-forge (if available)
conda install -c conda-forge vigra
```

### Using Poetry

```bash
# Initialize project with Poetry
poetry init
poetry add vigra[full]

# Or add to existing pyproject.toml
poetry add "vigra[full]"
```

## Installation Methods

### 1. Standard Installation

```bash
# Basic installation
pip install vigra

# With specific feature sets
pip install vigra[io]          # Image I/O support
pip install vigra[scientific]  # Scientific computing
pip install vigra[viz]         # Visualization
pip install vigra[hdf5]        # HDF5 support
pip install vigra[full]        # All features
```

### 2. Pre-release Installation

```bash
# Install latest development version
pip install --pre vigra

# Install from specific branch
pip install git+https://github.com/ukoethe/vigra.git@develop
```

### 3. Offline Installation

```bash
# Download wheel file
pip download vigra[full]

# Install offline
pip install vigra-*.whl
```

## Optional Dependencies

### Feature Sets

| Feature | Dependencies | Description |
|---------|-------------|-------------|
| **io** | Pillow≥8.0.0 | Enhanced image I/O formats |
| **scientific** | scipy≥1.6.0, scikit-image≥0.18.0 | Scientific computing |
| **viz** | matplotlib≥3.3.0 | Visualization and plotting |
| **hdf5** | h5py≥3.0.0 | HDF5 file format support |
| **qt** | PyQt5/PyQt6 | Qt-based GUI components |
| **full** | All above | Complete feature set |
| **dev** | Testing and development tools | For contributors |

### System Libraries (Optional but Recommended)

| Library | Purpose | Installation |
|---------|---------|-------------|
| **libpng** | PNG image support | `apt install libpng-dev` |
| **libjpeg** | JPEG image support | `apt install libjpeg-dev` |
| **libtiff** | TIFF image support | `apt install libtiff-dev` |
| **fftw3** | Fast Fourier transforms | `apt install libfftw3-dev` |
| **hdf5** | HDF5 file format | `apt install libhdf5-dev` |
| **zlib** | Compression support | `apt install zlib1g-dev` |

## Development Installation

### For Contributors

```bash
# Clone repository
git clone https://github.com/ukoethe/vigra.git
cd vigra

# Create development environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install in development mode
pip install -e .[dev]

# Run tests
python -m pytest

# Code quality checks
black vigra/
ruff check vigra/
mypy vigra/
```

### Custom Build Configuration

```bash
# Set environment variables for custom builds
export CC=gcc-9
export CXX=g++-9
export CMAKE_ARGS="-DCMAKE_BUILD_TYPE=Release"

# Install with custom configuration
pip install vigra --no-cache-dir
```

## Building from Source

### Prerequisites

```bash
# Install build dependencies
pip install setuptools wheel pybind11 numpy cmake
```

### Build Process

```bash
# Download source
git clone https://github.com/ukoethe/vigra.git
cd vigra

# Build and install
python setup.py build_ext --inplace
pip install .

# Or use build tool
pip install build
python -m build
pip install dist/vigra-*.whl
```

### Custom Build Options

```bash
# Build with specific features
export VIGRA_BUILD_FEATURES="core,io,scientific"
pip install .

# Build with debug information
export CMAKE_BUILD_TYPE=Debug
pip install . --no-cache-dir

# Build with specific compiler
export CC=clang CXX=clang++
pip install . --no-cache-dir
```

## Verification

### Basic Verification

```python
# Test basic import
import vigra
print(f"VIGRA version: {vigra.__version__}")

# Test core functionality
import numpy as np
image = np.random.rand(100, 100).astype(np.float32)
smoothed = vigra.gaussianSmoothing(image, sigma=1.0)
print("Basic functionality working!")
```

### Comprehensive Testing

```python
# Test all major components
def test_vigra_installation():
    import vigra
    import numpy as np
    
    # Test image processing
    image = np.random.rand(50, 50).astype(np.float32)
    
    # Test filtering
    smoothed = vigra.gaussianSmoothing(image, sigma=1.0)
    assert smoothed.shape == image.shape
    
    # Test feature detection
    try:
        corners = vigra.cornerResponseFunction(image)
        print("✓ Feature detection working")
    except Exception as e:
        print(f"⚠ Feature detection issue: {e}")
    
    # Test mathematical morphology
    try:
        binary = (image > 0.5).astype(np.uint8)
        eroded = vigra.binaryErosion(binary)
        print("✓ Mathematical morphology working")
    except Exception as e:
        print(f"⚠ Morphology issue: {e}")
    
    print("VIGRA installation verification complete!")

# Run verification
test_vigra_installation()
```

### Performance Benchmark

```python
import vigra
import numpy as np
import time

def benchmark_vigra():
    # Create test image
    image = np.random.rand(1000, 1000).astype(np.float32)
    
    # Benchmark Gaussian smoothing
    start = time.time()
    for _ in range(10):
        smoothed = vigra.gaussianSmoothing(image, sigma=2.0)
    duration = time.time() - start
    
    print(f"Gaussian smoothing: {duration/10:.3f}s per operation")
    print(f"Throughput: {image.size * 10 / duration / 1e6:.1f} Mpixels/s")

benchmark_vigra()
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Compilation Errors

**Error**: `Microsoft Visual C++ 14.0 is required`
```bash
# Solution: Install Visual Studio Build Tools
# Download from: https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022
```

**Error**: `fatal error: 'Python.h' file not found`
```bash
# Ubuntu/Debian
sudo apt-get install python3-dev

# CentOS/RHEL
sudo yum install python3-devel

# macOS
brew install python@3.11
```

**Error**: `clang: command not found`
```bash
# macOS
xcode-select --install

# Linux
sudo apt-get install build-essential
```

#### 2. Import Errors

**Error**: `ImportError: No module named 'vigra.vigranumpycore'`
```bash
# Check if C++ extensions built successfully
python -c "import vigra; print(vigra.__file__)"

# Reinstall with verbose output
pip uninstall vigra
pip install vigra --verbose
```

**Error**: `ImportError: DLL load failed` (Windows)
```bash
# Install Visual C++ Redistributable
# Download from Microsoft website

# Or install via chocolatey
choco install vcredist-all
```

#### 3. Dependency Issues

**Error**: `No module named 'numpy'`
```bash
# Install numpy first
pip install numpy
pip install vigra
```

**Error**: `ImportError: cannot import name 'vigranumpycore'`
```bash
# Check system dependencies
python -c "
import vigra
try:
    import vigra.vigranumpycore
    print('Core module loaded successfully')
except ImportError as e:
    print(f'Core module failed: {e}')
"
```

#### 4. Performance Issues

**Slow import times**
```bash
# Check for missing optimized libraries
python -c "
import numpy as np
np.show_config()  # Should show optimized BLAS/LAPACK
"

# Install optimized libraries
# Ubuntu: sudo apt-get install libopenblas-dev
# macOS: brew install openblas
```

**Memory errors during build**
```bash
# Limit parallel compilation
export MAX_JOBS=2
pip install vigra --no-cache-dir

# Or increase swap space (Linux)
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### Debug Installation

```bash
# Clean installation with debug output
pip uninstall vigra
pip cache purge
pip install vigra --no-cache-dir --verbose --force-reinstall

# Check build logs
pip install vigra 2>&1 | tee vigra_install.log
```

### Environment Diagnostics

```python
def diagnose_environment():
    import sys
    import platform
    import subprocess
    
    print("=== System Information ===")
    print(f"Platform: {platform.platform()}")
    print(f"Python: {sys.version}")
    print(f"Architecture: {platform.machine()}")
    
    print("\n=== Python Packages ===")
    try:
        import numpy
        print(f"NumPy: {numpy.__version__}")
    except ImportError:
        print("NumPy: Not installed")
    
    try:
        import vigra
        print(f"VIGRA: {vigra.__version__}")
    except ImportError:
        print("VIGRA: Not installed")
    
    print("\n=== Build Tools ===")
    tools = ['gcc', 'g++', 'clang', 'clang++', 'cmake', 'make']
    for tool in tools:
        try:
            result = subprocess.run([tool, '--version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                version = result.stdout.split('\n')[0]
                print(f"{tool}: {version}")
        except FileNotFoundError:
            print(f"{tool}: Not found")

diagnose_environment()
```

## Performance Optimization

### Compiler Optimizations

```bash
# Build with optimizations
export CFLAGS="-O3 -march=native -mtune=native"
export CXXFLAGS="-O3 -march=native -mtune=native"
pip install vigra --no-cache-dir --force-reinstall
```

### Memory Optimization

```python
# Configure NumPy for optimal performance
import os
os.environ['OMP_NUM_THREADS'] = '4'  # Adjust based on CPU cores
os.environ['OPENBLAS_NUM_THREADS'] = '4'
os.environ['MKL_NUM_THREADS'] = '4'

import vigra
```

### Multi-threading

```python
# Enable parallel processing where available
import vigra
vigra.set_num_threads(4)  # If available in your VIGRA build
```

## Getting Help

If you encounter issues not covered in this guide:

1. **Check the error message** - Most errors include specific guidance
2. **Search existing issues** - [GitHub Issues](https://github.com/ukoethe/vigra/issues)
3. **Create a new issue** - Include system information and error logs
4. **Community support** - VIGRA mailing list or Stack Overflow

### Useful Commands for Bug Reports

```bash
# System information
python -c "
import sys, platform
print(f'Python: {sys.version}')
print(f'Platform: {platform.platform()}')
print(f'Architecture: {platform.machine()}')
"

# Package versions
pip list | grep -E "(vigra|numpy|setuptools|pybind11)"

# Build environment
echo $CC $CXX $CFLAGS $CXXFLAGS
```

---

This installation guide should help you get VIGRA up and running on your system. For additional help, please refer to the [README.md](README.md) or [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md).