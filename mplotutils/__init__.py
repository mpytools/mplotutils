# flake8: noqa

from importlib.metadata import version as _get_version

from mplotutils import _colorbar, cartopy_utils, colormaps
from mplotutils._colorbar import colorbar
from mplotutils._hatch import hatch, hatch_map, hatch_map_global
from mplotutils._savefig import autodraw
from mplotutils.cartopy_utils import (
    cyclic_dataarray,
    sample_data_map,
    sample_dataarray,
    xlabel_map,
    xticklabels,
    ylabel_map,
    yticklabels,
)
from mplotutils.colormaps import from_levels_and_cmap
from mplotutils.map_layout import set_map_layout
from mplotutils.mpl import _get_renderer
from mplotutils.xrcompat import infer_interval_breaks

autodraw(True)

__all__ = [
    "_colorbar",
    "_get_renderer",
    "autodraw",
    "cartopy_utils",
    "colorbar",
    "colormaps",
    "cyclic_dataarray",
    "from_levels_and_cmap",
    "hatch_map_global",
    "hatch_map",
    "hatch",
    "infer_interval_breaks",
    "sample_data_map",
    "sample_dataarray",
    "set_map_layout",
    "xlabel_map",
    "xticklabels",
    "ylabel_map",
    "yticklabels",
]


try:
    __version__ = _get_version("mplotutils")
except Exception:
    # Local copy or not installed with setuptools.
    # Disable minimum version checks on downstream libraries.
    __version__ = "999"
