from mplotutils import _map_layout
from mplotutils._deprecate import _module_renamed_warning


def __getattr__(attr_name):
    attr = getattr(_map_layout, attr_name)
    _module_renamed_warning(attr_name, "map_layout")
    return attr
