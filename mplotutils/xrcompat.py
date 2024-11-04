from mplotutils import _xrcompat
from mplotutils._deprecate import _module_renamed_warning


def __getattr__(attr_name):
    attr = getattr(_xrcompat, attr_name)
    _module_renamed_warning(attr_name, "xrcompat")
    return attr
