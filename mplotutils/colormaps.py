from mplotutils import _colormaps
from mplotutils._deprecate import _module_renamed_warning


def __getattr__(attr_name):
    attr = getattr(_colormaps, attr_name)
    _module_renamed_warning(attr_name, "colormaps")
    return attr
