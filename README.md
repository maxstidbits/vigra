VIGRA Computer Vision Library
=============================

[![Build Status](https://dev.azure.com/ullrichkoethe/vigra/_apis/build/status/ukoethe.vigra)](https://dev.azure.com/ullrichkoethe/vigra/_build/latest?definitionId=1)

                Copyright 1998-2013 by Ullrich Koethe


    This file is part of the VIGRA computer vision library.
    You may use, modify, and distribute this software according
    to the terms stated in the LICENSE.txt file included in
    the VIGRA distribution.

    The VIGRA Website is
        http://ukoethe.github.io/vigra/
    Please direct questions, bug reports, and contributions to
        ullrich.koethe@iwr.uni-heidelberg.de    or
        vigra@informatik.uni-hamburg.de


    THIS SOFTWARE IS PROVIDED AS IS AND WITHOUT ANY EXPRESS OR
    IMPLIED WARRANTIES, INCLUDING, WITHOUT LIMITATION, THE IMPLIED
    WARRANTIES OF MERCHANTIBILITY AND FITNESS FOR A PARTICULAR PURPOSE.

## Quick Start

### Installation via pip (Recommended)

```bash
# Install VIGRA with basic functionality
pip install vigra

# Install with additional features
pip install vigra[full]  # Complete feature set
pip install vigra[io]    # Enhanced image I/O support
pip install vigra[scientific]  # Scientific computing features
pip install vigra[viz]   # Visualization support
```

### Basic Usage

```python
import vigra
import numpy as np

# Load an image
image = vigra.impex.readImage('example.jpg')

# Apply Gaussian smoothing
smoothed = vigra.gaussianSmoothing(image, sigma=2.0)

# Display the result
vigra.show(smoothed)
```

## Installation

### System Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, or Linux
- **C++ Compiler**: 
  - Windows: Visual Studio 2019+ or Build Tools
  - macOS: Xcode Command Line Tools
  - Linux: GCC 7+ or Clang 6+

### Installation Methods

#### 1. Standard Installation (pip)

```bash
# Install latest stable version
pip install vigra

# Install with all optional dependencies
pip install vigra[full]
```

#### 2. Development Installation

```bash
# Clone the repository
git clone https://github.com/ukoethe/vigra.git
cd vigra

# Install in development mode
pip install -e .

# Install with development tools
pip install -e .[dev]
```

#### 3. From Source with Custom Configuration

```bash
# Install build dependencies
pip install setuptools wheel pybind11 numpy cmake

# Build and install
pip install .
```

### Optional Dependencies

VIGRA supports several optional feature sets:

| Feature Set | Install Command | Description |
|-------------|-----------------|-------------|
| **io** | `pip install vigra[io]` | Enhanced image I/O (Pillow) |
| **scientific** | `pip install vigra[scientific]` | Scientific computing (SciPy, scikit-image) |
| **viz** | `pip install vigra[viz]` | Visualization (Matplotlib) |
| **hdf5** | `pip install vigra[hdf5]` | HDF5 file format support |
| **full** | `pip install vigra[full]` | All features combined |
| **dev** | `pip install vigra[dev]` | Development tools (testing, linting) |

### System Dependencies

For full functionality, install these system libraries:

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install build-essential cmake
sudo apt-get install libpng-dev libjpeg-dev libtiff-dev
sudo apt-get install libfftw3-dev libhdf5-dev zlib1g-dev
```

#### macOS (Homebrew)
```bash
brew install cmake
brew install libpng jpeg libtiff
brew install fftw hdf5
```

#### Windows
- Install [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022)
- Optional: Install [vcpkg](https://vcpkg.io/) for C++ dependencies

## Troubleshooting

### Common Installation Issues

#### Missing C++ Compiler
```bash
# Error: Microsoft Visual C++ 14.0 is required
# Solution: Install Visual Studio Build Tools (Windows)

# Error: clang: command not found
# Solution: Install Xcode Command Line Tools (macOS)
xcode-select --install

# Error: gcc: command not found  
# Solution: Install build tools (Linux)
sudo apt-get install build-essential
```

#### Import Errors
```python
# Error: ImportError: No module named 'vigra.vigranumpycore'
# Solution: Reinstall with verbose output to see build errors
pip install --force-reinstall --verbose vigra
```

#### Missing System Libraries
```bash
# Error: fatal error: 'png.h' file not found
# Solution: Install system dependencies (see System Dependencies section)
```

### Getting Help

1. **Check error messages** - They provide specific guidance for resolution
2. **Verify system dependencies** - Ensure all required libraries are installed
3. **Update pip and setuptools** - `pip install --upgrade pip setuptools`
4. **Try development installation** - `pip install -e .` for more detailed error output

For additional help:
- 📖 [Installation Guide](INSTALLATION.md) - Detailed platform-specific instructions
- 🔄 [Migration Guide](MIGRATION_GUIDE.md) - Upgrading from CMake builds
- 🐛 [Issue Tracker](https://github.com/ukoethe/vigra/issues) - Report bugs and get support

## Migration from CMake Build

If you previously built VIGRA using CMake, the new pip-based installation is much simpler:

### Old Method (CMake)
```bash
mkdir build && cd build
cmake ..
make -j4
make install
```

### New Method (pip)
```bash
pip install vigra
```

See [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) for detailed migration instructions and compatibility notes.

## Documentation

### Online Documentation
- **Main Documentation**: http://ukoethe.github.io/vigra/#documentation
- **API Reference**: http://ukoethe.github.io/vigra/doc-release/vigra/
- **Python Bindings**: http://ukoethe.github.io/vigra/doc-release/vigranumpy/

### Local Documentation
If you downloaded an official release, documentation is available in:
- `$VIGRA_PATH/doc/vigra/index.html` - Main documentation
- `$VIGRA_PATH/doc/vigranumpy/` - Python API documentation

For development versions, generate documentation with:
```bash
pip install vigra[dev]
make doc  # Requires Sphinx
```

## What is VIGRA

VIGRA is a computer vision library that puts its main emphasis on flexible
algorithms, because algorithms represent the principal know-how of this field.
The library was consequently built using generic programming as introduced by
Stepanov and Musser and exemplified in the C++ Standard Template Library. By
writing a few adapters (image iterators and accessors) you can use VIGRA's
algorithms on top of your data structures, within your environment.
Alternatively, you can also use the data structures provided within VIGRA,
which can be easily adapted to a wide range of applications. VIGRA's
flexibility comes almost for free: Since the design uses compile-time
polymorphism (templates), performance of the compiled program approaches that
of a traditional, hand tuned, inflexible, solution.

### Key Features

- **Image Processing**: Filtering, morphology, segmentation, feature detection
- **Machine Learning**: Random forests, SVM support, clustering algorithms  
- **Mathematical Morphology**: Erosion, dilation, opening, closing operations
- **Multi-dimensional Arrays**: Efficient N-dimensional array operations
- **Graph Algorithms**: Shortest paths, minimum spanning trees, graph cuts
- **Python Integration**: Full Python bindings with NumPy compatibility

### Performance

VIGRA is designed for high performance:
- **Template-based**: Compile-time optimization
- **SIMD Support**: Vectorized operations where available
- **Memory Efficient**: Lazy evaluation and iterator-based design
- **Parallel Processing**: Multi-threading support for key algorithms

## Download

VIGRA can be downloaded at http://ukoethe.github.io/vigra/#download. The official development
repository is at https://github.com/ukoethe/vigra

## Contributing

We welcome contributions! Please see our [contribution guidelines](CONTRIBUTING.md) for details on:
- Code style and standards
- Testing requirements  
- Documentation updates
- Bug reports and feature requests

### Development Setup

```bash
# Clone and setup development environment
git clone https://github.com/ukoethe/vigra.git
cd vigra
pip install -e .[dev]

# Run tests
python -m pytest

# Code quality checks
black vigra/
ruff check vigra/
mypy vigra/
```

## Making a New Release

1. Update the version in the header file: [`include/vigra/config_version.hxx`](include/vigra/config_version.hxx)
2. Create a short release note in [`docsrc/credits_changelog.dxx`](docsrc/credits_changelog.dxx)
3. Create a merge request
4. Give "reasonable time" for others to review
5. Create a tag on the main branch following `Version-MAJOR-MINOR-PATCH` format

## License

VIGRA is released under the MIT License. See [`LICENSE.txt`](LICENSE.txt) for details.
