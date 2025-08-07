#!/usr/bin/env python3
"""
VIGRA Computer Vision Library - Python Package

This is the main VIGRA Python package that provides computer vision and image
processing functionality through Python bindings to the VIGRA C++ library.

The package includes:
- Image I/O and processing functions
- Filtering and convolution operations
- Feature extraction and analysis
- Machine learning algorithms
- Graph-based algorithms
- Mathematical morphology operations
- Color space transformations

For detailed documentation, visit:
http://hci.iwr.uni-heidelberg.de/vigra/
"""

import sys
import os
import warnings
from pathlib import Path

# Version information
try:
    from ._version import version as __version__
except ImportError:
    # Fallback version if _version.py doesn't exist
    __version__ = "1.12.2"

# Package metadata
__author__ = "Ullrich Koethe"
__author_email__ = "ullrich.koethe@iwr.uni-heidelberg.de"
__license__ = "MIT"
__url__ = "http://hci.iwr.uni-heidelberg.de/vigra/"

# Documentation path
_vigra_path = os.path.abspath(os.path.dirname(__file__))
_vigra_doc_path = os.path.join(_vigra_path, 'doc', 'vigranumpy', 'index.html')

if not os.path.exists(_vigra_doc_path):
    _vigra_doc_path = "http://hci.iwr.uni-heidelberg.de/vigra/doc/vigranumpy/index.html"

# Windows DLL path handling
if sys.platform.startswith('win'):
    # On Windows, add subdirectory 'dlls' to the PATH to find required DLLs
    _vigra_dll_path = os.path.join(_vigra_path, 'dlls')
    if os.path.exists(_vigra_dll_path):
        os.environ['PATH'] = os.environ.get('PATH', '') + os.pathsep + _vigra_dll_path


def _create_fallback_module(module_name, error_message):
    """Create a fallback module that raises ImportError on attribute access."""
    import types
    
    class FallbackModule(types.ModuleType):
        def __init__(self, name, doc=None):
            super().__init__(name, doc)
            self.__name__ = name
            self.__doc__ = doc
        
        def __getattr__(self, name):
            if name.startswith('__'):
                return super().__getattribute__(name)
            raise ImportError(f"{self.__name__}.{name}: {self.__doc__}")
    
    module = FallbackModule(module_name, f"Import of module '{module_name}' failed.\n{error_message}")
    sys.modules[module_name] = module
    return module


# Core imports with graceful fallback
try:
    from . import vigranumpycore
    _core_available = True
except ImportError as e:
    warnings.warn(f"Failed to import vigranumpycore: {e}", ImportWarning)
    vigranumpycore = _create_fallback_module(
        'vigra.vigranumpycore',
        f"Core VIGRA functionality not available: {e}\n"
        "This usually means the C++ extensions were not built properly."
    )
    _core_available = False

# Import core array functionality
try:
    if _core_available:
        from . import arraytypes
        from .arraytypes import *
        
        # Set up standard array type
        standardArrayType = arraytypes.VigraArray
        defaultAxistags = arraytypes.VigraArray.defaultAxistags
    else:
        # Fallback to basic numpy functionality
        import numpy as np
        standardArrayType = np.ndarray
        defaultAxistags = None
        
except ImportError as e:
    warnings.warn(f"Failed to import arraytypes: {e}", ImportWarning)
    standardArrayType = None
    defaultAxistags = None

# Import main modules with graceful fallbacks
_modules_to_import = [
    'impex',      # Image I/O
    'filters',    # Filtering operations
    'sampling',   # Resampling and interpolation
    'analysis',   # Image analysis
    'learning',   # Machine learning
    'colors',     # Color space transformations
    'noise',      # Noise estimation
    'geometry',   # Geometric algorithms
    'histogram',  # Histogram operations
    'graphs',     # Graph algorithms
    'utilities',  # Utility functions
    'blockwise',  # Blockwise processing
]

# Import modules with error handling
for module_name in _modules_to_import:
    try:
        if _core_available:
            module = __import__(f'vigra.{module_name}', fromlist=[module_name])
            globals()[module_name] = module
        else:
            globals()[module_name] = _create_fallback_module(
                f'vigra.{module_name}',
                f"Module '{module_name}' not available because core extensions failed to load."
            )
    except ImportError as e:
        warnings.warn(f"Failed to import {module_name}: {e}", ImportWarning)
        globals()[module_name] = _create_fallback_module(
            f'vigra.{module_name}',
            f"Module '{module_name}' not available: {e}"
        )

# Optional FFTW-based Fourier module
try:
    if _core_available:
        from . import fourier
    else:
        fourier = _create_fallback_module(
            'vigra.fourier',
            "Fourier module not available because core extensions failed to load."
        )
except ImportError as e:
    fourier = _create_fallback_module(
        'vigra.fourier',
        f"Fourier module not available: {e}\n"
        "Make sure that the FFTW3 libraries are installed and found during compilation.\n"
        "They can be downloaded from http://www.fftw.org/."
    )

# Import commonly used functions into main namespace
if _core_available:
    try:
        # Image I/O functions
        from .impex import readImage, readVolume
        
        # Basic filtering
        from .filters import convolve, gaussianSmoothing
        
        # Resampling
        from .sampling import resize
        
        # Chunked array support
        from .vigranumpycore import (
            ChunkedArrayFull, ChunkedArrayLazy, 
            ChunkedArrayCompressed, ChunkedArrayTmpFile, 
            Compression
        )
        
        # Optional HDF5 support
        try:
            from .vigranumpycore import ChunkedArrayHDF5, HDF5Mode
        except ImportError:
            pass
            
    except ImportError as e:
        warnings.warn(f"Failed to import common functions: {e}", ImportWarning)

# HDF5 I/O functions (optional)
def readHDF5(filename_or_group, path_in_file, order=None):
    """Read an array from an HDF5 file.
    
    Parameters:
    -----------
    filename_or_group : str or h5py.Group
        Filename or group object referring to an already open HDF5 file
    path_in_file : str
        Name of the dataset to be read, including intermediate groups
    order : str, optional
        Desired axis order for VigraArray results
        
    Returns:
    --------
    array : numpy.ndarray or VigraArray
        The loaded array data
        
    Requires:
    ---------
    h5py module must be installed
    """
    try:
        import h5py
    except ImportError:
        raise ImportError("h5py module is required for HDF5 I/O operations")
    
    if isinstance(filename_or_group, h5py.Group):
        file = None
        group = filename_or_group
    else:
        file = h5py.File(filename_or_group, 'r')
        group = file['/']
    
    try:
        dataset = group[path_in_file]
        if not isinstance(dataset, h5py.Dataset):
            raise IOError(f"readHDF5(): '{path_in_file}' is not a dataset")
        
        data = dataset[...]
        axistags = dataset.attrs.get('axistags', None)
        
        if axistags is not None and _core_available:
            try:
                data = data.view(arraytypes.VigraArray)
                data.axistags = arraytypes.AxisTags.fromJSON(axistags)
                if order is None:
                    order = arraytypes.VigraArray.defaultOrder
                data = data.transposeToOrder(order)
            except Exception:
                # Fall back to plain numpy array if VigraArray fails
                pass
        else:
            if order == 'F':
                data = data.transpose()
            elif order not in [None, 'C', 'A']:
                raise IOError(f"readHDF5(): unsupported order '{order}'")
    finally:
        if file is not None:
            file.close()
    
    return data


def writeHDF5(data, filename_or_group, path_in_file, compression=None, chunks=None):
    """Write an array to an HDF5 file.
    
    Parameters:
    -----------
    data : array_like
        Array data to write
    filename_or_group : str or h5py.Group
        Filename or group object referring to an already open HDF5 file
    path_in_file : str
        Name of the dataset to be written, including intermediate groups
    compression : str, optional
        Compression method ('gzip', 'szip', 'lzf')
    chunks : bool or tuple, optional
        Chunking configuration
        
    Requires:
    ---------
    h5py module must be installed
    """
    try:
        import h5py
    except ImportError:
        raise ImportError("h5py module is required for HDF5 I/O operations")
    
    if isinstance(filename_or_group, h5py.Group):
        file = None
        group = filename_or_group
    else:
        file = h5py.File(filename_or_group, 'a')
        group = file['/']
    
    try:
        levels = path_in_file.split('/')
        for groupname in levels[:-1]:
            if groupname == '':
                continue
            g = group.get(groupname, default=None)
            if g is None:
                group = group.create_group(groupname)
            elif not isinstance(g, h5py.Group):
                raise IOError(f"writeHDF5(): invalid path '{path_in_file}'")
            else:
                group = g
        
        dataset = group.get(levels[-1], default=None)
        if dataset is not None:
            if isinstance(dataset, h5py.Dataset):
                del group[levels[-1]]
            else:
                raise IOError(f"writeHDF5(): cannot replace '{path_in_file}' because it is not a dataset")
        
        # Try to transpose to numpy order if it's a VigraArray
        try:
            data = data.transposeToNumpyOrder()
        except AttributeError:
            pass
        
        dataset = group.create_dataset(
            levels[-1],
            shape=data.shape,
            dtype=data.dtype,
            data=data,
            compression=compression,
            chunks=chunks
        )
        
        # Store axistags if available
        if hasattr(data, 'axistags'):
            dataset.attrs['axistags'] = data.axistags.toJSON()
    finally:
        if file is not None:
            file.close()


# Add HDF5 functions to impex module if available
if 'impex' in globals() and hasattr(globals()['impex'], '__dict__'):
    globals()['impex'].readHDF5 = readHDF5
    globals()['impex'].writeHDF5 = writeHDF5
    readHDF5.__module__ = 'vigra.impex'
    writeHDF5.__module__ = 'vigra.impex'


# Utility functions
def searchfor(searchstring):
    """Scan all vigra modules to find classes and functions containing 'searchstring' in their name."""
    for attr_name in globals().keys():
        attr = globals()[attr_name]
        if hasattr(attr, '__dict__'):
            contents = dir(attr)
            for cont in contents:
                if cont.upper().find(searchstring.upper()) >= 0:
                    print(f"{attr_name}.{cont}")


# Display functions (optional, requires matplotlib)
def imshow(image, show=True, **kwargs):
    """Display a scalar or RGB image using matplotlib.
    
    Parameters:
    -----------
    image : array_like
        Image to display (1 or 3 channels)
    show : bool
        Whether to call matplotlib.pyplot.show()
    **kwargs : dict
        Additional arguments passed to matplotlib.pyplot.imshow
    """
    try:
        import matplotlib.pyplot as plt
        import matplotlib.cm
        import numpy as np
    except ImportError:
        raise ImportError("matplotlib is required for image display functions")
    
    if not hasattr(image, 'axistags'):
        plot = plt.imshow(image, **kwargs)
        if show:
            plt.show()
        return plot
    
    # Handle VigraArray with axistags
    image = image.transposeToNumpyOrder()
    if image.channels == 1:
        image = image.dropChannelAxis().view(np.ndarray)
        cmap = kwargs.pop('cmap', matplotlib.cm.gray)
        norm = kwargs.pop('norm', matplotlib.cm.colors.Normalize())
        plot = plt.imshow(image, cmap=cmap, norm=norm, **kwargs)
    elif image.channels == 3:
        if image.dtype != np.uint8:
            # Convert to uint8 for display
            image_min, image_max = image.min(), image.max()
            if image_max > image_min:
                image = ((image - image_min) / (image_max - image_min) * 255).astype(np.uint8)
            else:
                image = np.zeros_like(image, dtype=np.uint8)
        plot = plt.imshow(image.view(np.ndarray), **kwargs)
    else:
        raise RuntimeError("vigra.imshow(): Image must have 1 or 3 channels.")
    
    if show:
        plt.show()
    return plot


def show():
    """Show matplotlib plots."""
    try:
        import matplotlib.pyplot as plt
        plt.show()
    except ImportError:
        raise ImportError("matplotlib is required for show() function")


# Package documentation
__doc__ = f'''VIGRA Computer Vision Library

HTML documentation is available at:
{_vigra_doc_path}

Help on individual functions can be obtained via their doc strings.

The following sub-modules group related functionality:

* arraytypes - VigraArray and axistags (automatically imported into 'vigra')
* ufunc      - improved array arithmetic (automatically used by VigraArray)
* impex      - image and array I/O
* colors     - color space transformations
* filters    - spatial filtering (e.g. smoothing)
* sampling   - image and array re-sampling and interpolation
* fourier    - Fourier transform and Fourier domain filters
* analysis   - image analysis and segmentation
* learning   - machine learning and classification
* noise      - noise estimation and normalization
* geometry   - geometric algorithms (e.g. convex hull)
* histogram  - histograms and channel representation
* graphs     - grid graphs / graphs / graph algorithms
* utilities  - priority queues and other utilities
* blockwise  - blockwise processing for large arrays

Version: {__version__}
'''

# Clean up namespace
del sys, os, warnings, Path