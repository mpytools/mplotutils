from mplotutils import _cartopy_utils
from mplotutils._deprecate import _module_renamed_warning


def __getattr__(attr_name):
    attr = getattr(_cartopy_utils, attr_name)
    _module_renamed_warning(attr_name, "cartopy_utils")
    return attr
