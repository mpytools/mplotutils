from mplotutils import _mpl
from mplotutils._deprecate import _module_renamed_warning


def __getattr__(attr_name):
    attr = getattr(_mpl, attr_name)
    _module_renamed_warning(attr_name, "mpl")
    return attr
