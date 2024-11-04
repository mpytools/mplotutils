import importlib

import pytest

import mplotutils as mpu

DEPRECATED_MODULES = {
    "cartopy_utils": (
        "cyclic_dataarray",
        "sample_data_map",
        "sample_dataarray",
        "xlabel_map",
        "xticklabels",
        "ylabel_map",
        "yticklabels",
    ),
    "colormaps": ("from_levels_and_cmap",),
    "map_layout": ("set_map_layout",),
    "mpl": ("_get_renderer",),
    "xrcompat": ("infer_interval_breaks",),
}


def test_00_deprecated_not_in_dir():

    dir = mpu.__dir__()

    for module in DEPRECATED_MODULES:
        assert module not in dir


def test_01_in_dir():

    dir = mpu.__dir__()

    assert "hatch" in dir


@pytest.mark.parametrize("mod", DEPRECATED_MODULES)
def test_01_deprecated_modules_from_import(mod):

    with pytest.warns(FutureWarning, match=f"``mplotutils.{mod}`` is deprecated"):
        importlib.__import__("mplotutils", fromlist=[mod])


@pytest.mark.parametrize("mod, functions", DEPRECATED_MODULES.items())
def test_depm3(mod, functions):

    module = importlib.import_module(f"mplotutils.{mod}")

    for function in functions:
        with pytest.warns(FutureWarning, match=f"``mplotutils.{mod}`` is deprecated"):
            getattr(module, function)


def test_fcn_warns():

    # NOTE: this is the only import that does not warn
    import mplotutils.cartopy_utils

    with pytest.warns(FutureWarning):
        mplotutils.cartopy_utils.sample_data_map(6, 6)
