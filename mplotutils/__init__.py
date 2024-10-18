# flake8: noqa

from importlib.metadata import version as _get_version

from . import _colorbar, cartopy_utils, colormaps
from ._colorbar import *
from ._hatch import hatch, hatch_map, hatch_map_global
from ._savefig import autodraw
from .cartopy_utils import *
from .colormaps import *
from .map_layout import set_map_layout
from .mpl import _get_renderer
from .xrcompat import *

autodraw(True)

try:
    __version__ = _get_version("mplotutils")
except Exception:
    # Local copy or not installed with setuptools.
    # Disable minimum version checks on downstream libraries.
    __version__ = "999"
