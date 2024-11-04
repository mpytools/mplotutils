# flake8: noqa

from importlib.metadata import version as _get_version

from mplotutils import _cartopy_utils, _colorbar, _colormaps
from mplotutils._cartopy_utils import (
    cyclic_dataarray,
    sample_data_map,
    sample_dataarray,
    xlabel_map,
    xticklabels,
    ylabel_map,
    yticklabels,
)
from mplotutils._colorbar import colorbar
from mplotutils._colormaps import from_levels_and_cmap
from mplotutils._deprecate import _module_renamed_warning_init
from mplotutils._hatch import hatch, hatch_map, hatch_map_global
from mplotutils._map_layout import set_map_layout
from mplotutils._mpl import _get_renderer
from mplotutils._savefig import autodraw
from mplotutils._xrcompat import infer_interval_breaks

autodraw(True)

__all__ = [
    "_colorbar",
    "_get_renderer",
    "autodraw",
    "_cartopy_utils",
    "colorbar",
    "_colormaps",
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


def __getattr__(attr):

    m = (
        "cartopy_utils",
        "colormaps",
        "map_layout",
        "mpl",
        "xrcompat",
    )

    import mplotutils

    if attr in m:

        _module_renamed_warning_init(attr)

        # NOTE: could use importlib.import_module() but it registers the function in
        # sys.modules such that the warning is only called once
        # return importlib.import_module(f".{attr}", "mplotutils")

        return getattr(mplotutils, f"_{attr}")

    # required for ipython tab completion
    raise AttributeError(f"module {__name__!r} has no attribute {attr!r}")
