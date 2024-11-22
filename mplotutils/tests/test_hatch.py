import cartopy.crs as ccrs
import matplotlib as mpl
import numpy as np
import pytest
import xarray as xr
from packaging.version import Version

import mplotutils as mpu

from . import assert_no_warnings, subplots_context

MPL_GE_310 = Version(Version(mpl.__version__).base_version) >= Version("3.10")
requires_mpl_ge_310 = pytest.mark.skipif(not MPL_GE_310, reason="requires mpl >= 3.10")


HATCH_FUNCTIONS = (
    pytest.param(mpu.hatch, id="hatch"),
    pytest.param(mpu.hatch_map, id="hatch_map"),
    pytest.param(mpu.hatch_map_global, id="hatch_map_global"),
)


@pytest.mark.parametrize("obj", (None, xr.Dataset(), np.array([])))
@pytest.mark.parametrize("function", HATCH_FUNCTIONS)
def test_hatch_not_a_dataarray(obj, function):

    with pytest.raises(TypeError, match="Expected a xr.DataArray"):
        function(obj, "*")


@pytest.mark.parametrize("dtype", (float, int))
@pytest.mark.parametrize("function", HATCH_FUNCTIONS)
def test_hatch_not_bool(dtype, function):

    da = xr.DataArray(np.ones((3, 3), dtype=dtype))

    with pytest.raises(TypeError, match="Expected a boolean array"):
        function(da, "*")


@pytest.mark.parametrize("ndim", (1, 3))
@pytest.mark.parametrize("function", HATCH_FUNCTIONS)
def test_hatch_not_2D(ndim, function):

    da = xr.DataArray(np.ones([3] * ndim, dtype=bool))

    with pytest.raises(ValueError, match="Expected a 2D array"):
        function(da, "*")


@pytest.mark.parametrize("function", HATCH_FUNCTIONS)
def test_hatch_pattern(function):

    da = xr.DataArray(
        np.ones([3, 3], dtype=bool),
        dims=("lat", "lon"),
        coords={"lat": [0, 1, 2], "lon": [1, 2, 3]},
    )

    subplot_kw = {"projection": ccrs.PlateCarree()}

    with subplots_context(1, 1, subplot_kw=subplot_kw) as (__, ax):

        h = function(da, "*", ax=ax)
        assert h.hatches == ["", "*"]
        h = function(da, "//", ax=ax)
        assert h.hatches == ["", "//"]


@pytest.mark.parametrize("function", HATCH_FUNCTIONS)
def test_hatch_label(function):

    da = xr.DataArray(
        np.ones([3, 3], dtype=bool),
        dims=("lat", "lon"),
        coords={"lat": [0, 1, 2], "lon": [1, 2, 3]},
    )

    subplot_kw = {"projection": ccrs.PlateCarree()}

    # test label with default color
    with subplots_context(1, 1, subplot_kw=subplot_kw) as (__, ax):

        function(da, "*", ax=ax, label="label")

        legend = ax.legend()
        h = legend.legend_handles

        assert len(h) == 1

        (rect,) = h

        assert rect.get_label() == "label"
        assert mpl.colors.to_rgba("0.1") == rect._hatch_color

    # test 2 labels with non-default color
    with subplots_context(1, 1, subplot_kw=subplot_kw) as (__, ax):

        function(da, "*", ax=ax, label="label0", color="#2ca25f")
        function(da, "*", ax=ax, label="label1", color="#2ca25f")

        legend = ax.legend()
        h = legend.legend_handles

        assert len(h) == 2

        for i, rect in enumerate(h):
            assert rect.get_label() == f"label{i}"
            assert mpl.colors.to_rgba("#2ca25f") == rect._hatch_color


@pytest.mark.skipif(MPL_GE_310, reason="only for mpl < 3.10")
@pytest.mark.parametrize("function", HATCH_FUNCTIONS)
def test_hatch_linewidth_mpl_lt_310(function):

    da = xr.DataArray(
        np.ones([3, 3], dtype=bool),
        dims=("lat", "lon"),
        coords={"lat": [0, 1, 2], "lon": [1, 2, 3]},
    )

    subplot_kw = {"projection": ccrs.PlateCarree()}

    # test linewidth default width
    with subplots_context(1, 1, subplot_kw=subplot_kw) as (__, ax):
        function(da, "*", ax=ax)

        assert mpl.rcParams["hatch.linewidth"] == 0.25

    # changing away from the default linewidth does not raise a warning
    with subplots_context(1, 1, subplot_kw=subplot_kw) as (__, ax):

        function(da, "*", ax=ax)
        assert mpl.rcParams["hatch.linewidth"] == 0.25

        with assert_no_warnings():
            function(da, "*", ax=ax, linewidth=1)

        assert mpl.rcParams["hatch.linewidth"] == 1

    # changing away from the linewidth does raise a warning
    with subplots_context(1, 1, subplot_kw=subplot_kw) as (__, ax):

        function(da, "*", ax=ax, linewidth=2)
        assert mpl.rcParams["hatch.linewidth"] == 2

        with pytest.warns(match="Setting more than one hatch `linewidth`"):
            function(da, "*", ax=ax, linewidth=1)

        assert mpl.rcParams["hatch.linewidth"] == 1


@requires_mpl_ge_310
@pytest.mark.filterwarnings("ignore:Passing 'N' to ListedColormap is deprecated")
@pytest.mark.parametrize("function", HATCH_FUNCTIONS)
def test_hatch_linewidth_mpl_ge_310(function):

    da = xr.DataArray(
        np.ones([3, 3], dtype=bool),
        dims=("lat", "lon"),
        coords={"lat": [0, 1, 2], "lon": [1, 2, 3]},
    )

    subplot_kw = {"projection": ccrs.PlateCarree()}

    # test linewidth default width
    with subplots_context(1, 1, subplot_kw=subplot_kw) as (__, ax):
        q = function(da, "*", ax=ax)
        assert q.get_hatch_linewidth() == 0.25
        assert mpl.rcParams["hatch.linewidth"] == 0.25

    # changing away from the default linewidth does not raise a warning
    with subplots_context(1, 1, subplot_kw=subplot_kw) as (__, ax):

        q = function(da, "*", ax=ax)
        assert q.get_hatch_linewidth() == 0.25
        assert mpl.rcParams["hatch.linewidth"] == 0.25

        with assert_no_warnings():
            q = function(da, "*", ax=ax, linewidth=1)

        assert q.get_hatch_linewidth() == 1
        assert mpl.rcParams["hatch.linewidth"] == 1

        q = function(da, "*", ax=ax)
        assert q.get_hatch_linewidth() == 0.25
        assert mpl.rcParams["hatch.linewidth"] == 0.25

    # changing away from the linewidth does NOT raise a warning
    with subplots_context(1, 1, subplot_kw=subplot_kw) as (__, ax):

        q = function(da, "*", ax=ax, linewidth=2)
        assert q.get_hatch_linewidth() == 2
        assert mpl.rcParams["hatch.linewidth"] == 2

        with assert_no_warnings():
            q = function(da, "*", ax=ax, linewidth=1)

        assert q.get_hatch_linewidth() == 1
        assert mpl.rcParams["hatch.linewidth"] == 1


@pytest.mark.parametrize("function", HATCH_FUNCTIONS)
def test_hatch_color(function):

    da = xr.DataArray(
        np.ones([3, 3], dtype=bool),
        dims=("lat", "lon"),
        coords={"lat": [0, 1, 2], "lon": [1, 2, 3]},
    )

    subplot_kw = {"projection": ccrs.PlateCarree()}

    # test default color
    with subplots_context(1, 1, subplot_kw=subplot_kw) as (__, ax):
        h = function(da, "*", ax=ax)

        assert mpl.colors.to_rgba("0.1") == h._hatch_color

    # different colors can be set
    with subplots_context(1, 1, subplot_kw=subplot_kw) as (__, ax):

        h = function(da, "*", ax=ax, color="#2ca25f")
        assert mpl.colors.to_rgba("#2ca25f") == h._hatch_color

        h = function(da, "*", ax=ax, color="#e5f5f9")
        assert mpl.colors.to_rgba("#e5f5f9") == h._hatch_color


def test_hatch_bbox():

    da = xr.DataArray(
        np.ones([3, 3], dtype=bool),
        dims=("lat", "lon"),
        coords={"lat": [0, 1, 2], "lon": [1, 2, 3]},
    )

    subplot_kw = {"projection": ccrs.PlateCarree()}

    # test hatch
    with subplots_context(1, 1) as (__, ax):
        h = mpu.hatch(da, "*", ax=ax)

        bbox = h.get_datalim(ax.transData)

        assert bbox.x0 == 1
        assert bbox.x1 == 3
        assert bbox.y0 == 0
        assert bbox.y1 == 2

    # test hatch
    with subplots_context(1, 1, subplot_kw=subplot_kw) as (__, ax):
        h = mpu.hatch_map(da, "*", ax=ax)

        bbox = h.get_datalim(ax.transData)

        assert bbox.x0 == 1
        assert bbox.x1 == 3
        assert bbox.y0 == 0
        assert bbox.y1 == 2

    # test hatch_global_map
    with subplots_context(1, 1, subplot_kw=subplot_kw) as (__, ax):
        h = mpu.hatch_map_global(da, "*", ax=ax)

        bbox = h.get_datalim(ax.transData)

        assert bbox.x0 == 1
        assert bbox.x1 == 4  # this is 4 because it's wrapped around
        assert bbox.y0 == 0
        assert bbox.y1 == 2
