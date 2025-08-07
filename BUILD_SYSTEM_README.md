# VIGRA Modern Python Build System

This document describes the new setuptools/pip-based build system for VIGRA, replacing the previous CMake-only build approach with a modern Python packaging solution.

## Overview

The new build system provides:
- Modern Python packaging with `pyproject.toml`
- Automatic dependency detection and graceful fallbacks
- Cross-platform C++ extension building
- Backward compatibility with existing vigranumpy API
- Support for optional dependencies and feature sets

## Files Created

### Core Build Files

1. **`pyproject.toml`** - Modern Python packaging configuration
   - Build system requirements (setuptools, pybind11, numpy)
   - Project metadata and dependencies
   - Optional dependency groups (io, scientific, viz, hdf5, full, dev)
   - Tool configurations (black, ruff, mypy, pytest)

2. **`setup.py`** - Custom build logic for C++ extensions
   - Version extraction from `vigra/include/vigra/config_version.hxx`
   - Automatic dependency detection (ZLIB, TIFF, JPEG, PNG, FFTW, HDF5)
   - Platform-specific build configurations
   - Custom extension classes for VIGRA modules

3. **`vigra/__init__.py`** - Python package initialization
   - Graceful import handling with fallbacks
   - Backward compatibility with existing API
   - HDF5 I/O functions
   - Display utilities (imshow, show)
   - Comprehensive error handling

4. **`vigra/_version.py`** - Version information
   - Centralized version management
   - Compatible with setuptools_scm

## Key Features

### Dependency Detection
The build system automatically detects available system libraries:
- **ZLIB** - Compression support
- **JPEG** - JPEG image format support
- **PNG** - PNG image format support  
- **TIFF** - TIFF image format support
- **FFTW3/FFTW3F** - Fast Fourier Transform support
- **HDF5** - HDF5 file format support

Missing dependencies are handled gracefully with informative error messages.

### Optional Dependencies
The package defines several optional dependency groups:

```bash
# Basic image I/O
pip install vigra[io]

# Scientific computing features
pip install vigra[scientific]

# Visualization support
pip install vigra[viz]

# HDF5 file format support
pip install vigra[hdf5]

# Complete feature set
pip install vigra[full]

# Development tools
pip install vigra[dev]
```

### Cross-Platform Support
- **Windows**: Automatic MSVC configuration and DLL handling
- **macOS**: Homebrew and MacPorts library detection
- **Linux**: Standard system library paths

## Building and Installation

### Prerequisites
```bash
# Install build dependencies
pip install setuptools wheel pybind11 numpy cmake
```

### Development Installation
```bash
# Install in development mode
pip install -e .

# With optional dependencies
pip install -e .[full]
```

### Building Distribution Packages
```bash
# Install build tools
pip install build

# Build wheel and source distribution
python -m build
```

### Testing the Installation
```bash
# Test basic import
python -c "import vigra; print(vigra.__version__)"

# Test with features
python -c "import vigra; print('VIGRA loaded successfully')"
```

## Version Management

The version is extracted from `vigra/include/vigra/config_version.hxx`:
- `VIGRA_VERSION_MAJOR` - Major version number
- `VIGRA_VERSION_MINOR` - Minor version number  
- `VIGRA_VERSION_PATCH` - Patch version number

Current version: **1.12.2**

## Backward Compatibility

The new build system maintains full backward compatibility with existing vigranumpy code:
- All existing imports continue to work
- API remains unchanged
- Graceful fallbacks for missing components
- Informative error messages for unavailable features

## Extension Modules

The build system creates the following C++ extension modules:
- **`vigra.vigranumpycore`** - Core VIGRA functionality
- **`vigra.fourier`** - FFTW-based Fourier transforms (optional)

## Error Handling

The package includes comprehensive error handling:
- Missing C++ extensions result in informative ImportError messages
- Optional modules gracefully degrade when dependencies are unavailable
- Clear instructions for resolving dependency issues

## Development Workflow

1. **Setup Development Environment**:
   ```bash
   pip install -e .[dev]
   ```

2. **Run Tests**:
   ```bash
   python test_build_config.py
   ```

3. **Code Quality**:
   ```bash
   black vigra/
   ruff check vigra/
   mypy vigra/
   ```

4. **Build and Test**:
   ```bash
   python -m build
   pip install dist/vigra-*.whl
   ```

## Migration from CMake Build

For users migrating from the CMake-based build:

1. **Old approach**:
   ```bash
   mkdir build && cd build
   cmake ..
   make
   make install
   ```

2. **New approach**:
   ```bash
   pip install .
   ```

The new system is much simpler and integrates better with Python packaging tools.

## Troubleshooting

### Common Issues

1. **Missing C++ Compiler**:
   - Windows: Install Visual Studio Build Tools
   - macOS: Install Xcode Command Line Tools
   - Linux: Install build-essential

2. **Missing Dependencies**:
   - Install system libraries (e.g., `libpng-dev`, `libjpeg-dev`)
   - Use package manager (apt, brew, yum)

3. **Import Errors**:
   - Check that extensions built successfully
   - Verify all dependencies are available
   - Check error messages for specific missing components

### Getting Help

- Check the error messages - they provide specific guidance
- Ensure all system dependencies are installed
- Verify Python and pip versions are compatible
- Check that the C++ compiler is properly configured

## Future Enhancements

Potential improvements for future versions:
- Conda packaging support
- Automated CI/CD builds for multiple platforms
- Binary wheel distribution
- Enhanced dependency detection
- Performance optimizations

---

This build system provides a solid foundation for modern VIGRA Python packaging while maintaining full compatibility with existing code.