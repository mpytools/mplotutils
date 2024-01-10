# flake8: noqa

from importlib.metadata import version as _get_version

from . import _colorbar, cartopy_utils, colormaps
from ._colorbar import *
from .cartopy_utils import *
from .colormaps import *
from .map_layout import set_map_layout
from .xrcompat import *

try:
    __version__ = _get_version("mplotutils")
except Exception:
    # Local copy or not installed with setuptools.
    # Disable minimum version checks on downstream libraries.
    __version__ = "999"
