import cartopy.crs as ccrs
import numpy as np
import pytest
import shapely

import mplotutils as mpu

from . import subplots_context


@pytest.mark.parametrize("pass_ax", (True, False))
def test_yticklabels_robinson(pass_ax):
    with subplots_context(subplot_kw=dict(projection=ccrs.Robinson())) as (f, ax):
        ax.set_global()

        lat = np.arange(-90, 91, 20)

        ax_ = ax if pass_ax else None
        mpu.yticklabels(lat, ax=ax_, size=8)

        x_pos = -179.99

        # two elements are not added because they are beyond the map limits
        lat = lat[1:-1]

        for t, y_pos in zip(ax.texts, lat, strict=True):
            np.testing.assert_allclose((x_pos, y_pos), t.xy, atol=0.01)

        assert ax.texts[0].get_text() == "70°S"
        assert ax.texts[-1].get_text() == "70°N"


def test_yticklabels_robinson_180():
    proj = ccrs.Robinson(central_longitude=180)
    with subplots_context(subplot_kw=dict(projection=proj)) as (f, ax):
        ax.set_global()

        lat = np.arange(-90, 91, 20)

        mpu.yticklabels(lat, ax=ax, size=8)

        x_pos = 0.0

        # two elements are not added because they are beyond the map limits
        lat = lat[1:-1]

        for t, y_pos in zip(ax.texts, lat, strict=True):
            np.testing.assert_allclose((x_pos, y_pos), t.xy, atol=0.01)

        assert ax.texts[0].get_text() == "70°S"
        assert ax.texts[-1].get_text() == "70°N"


@pytest.mark.parametrize("pass_ax", (True, False))
def test_xticklabels_robinson(pass_ax):
    with subplots_context(subplot_kw=dict(projection=ccrs.Robinson())) as (f, ax):
        ax.set_global()

        lon = np.arange(-180, 181, 60)
        ax_ = ax if pass_ax else None
        mpu.xticklabels(lon, ax=ax_, size=8)

        # changed value with proj 9.8; https://github.com/mpytools/mplotutils/issues/202
        y_pos = -89.845635

        # two elements are not added because they are beyond the map limits
        lon = lon[1:-1]

        for t, x_pos in zip(ax.texts, lon, strict=True):
            np.testing.assert_allclose(t.xy, (x_pos, y_pos), atol=0.01)

        assert ax.texts[0].get_text() == "120°W"
        assert ax.texts[-1].get_text() == "120°E"


def test_xyticklabels_not_on_map():

    with subplots_context(subplot_kw=dict(projection=ccrs.PlateCarree())) as (f, ax):
        # restrict extent
        ax.set_extent([0, 180, -90, 0], ccrs.PlateCarree())

        with pytest.warns(match="no points found for xlabel"):
            mpu.xticklabels([180, 270, 360], ax=ax, size=8)

        with pytest.warns(match="no points found for ylabel"):
            mpu.yticklabels([0, 45, 90], ax=ax, size=8)


# TODO: https://github.com/mpytools/mplotutils/issues/48
# def test_xticklabels_robinson_180():

#     proj = ccrs.Robinson(central_longitude=180)
#     with subplots_context(subplot_kw=dict(projection=proj)) as (f, ax):

#         ax.set_global()

#         # lon = np.arange(-180, 181, 60)
#         lon = np.arange(0, 360, 60)


#         mpu.xticklabels(lon, ax=ax, size=8)

#         y_pos = -89.99

#         # two elements are not added because they are beyond the map limits
#         lon = lon[1:-1]
#         for t, x_pos in zip(ax.texts, lon, strict=True):

#             np.testing.assert_allclose((x_pos, y_pos), t.xy, atol=0.01)

#         assert ax.texts[0].get_text() == "60°E"
#         assert ax.texts[-1].get_text() == "60°W"


def test_determine_intersection():

    box = shapely.box(0, 0, 1, 1)

    # case 0 -> the expected two points top & bottom

    a = shapely.Point((0.5, -0.5))
    b = shapely.Point((0.5, 1.5))

    result = mpu._cartopy_utils._determine_intersection(box, a, b)
    expected = np.array([[0.5, 0.0], [0.5, 1.0]])

    np.testing.assert_allclose(result, expected)

    # case 1 -> only one intersection (not sure how this would happen)

    b = shapely.Point((0.5, 0.5))

    result = mpu._cartopy_utils._determine_intersection(box, a, b)
    expected = np.array([[0.5, 0.0]])
    np.testing.assert_allclose(result, expected)

    # case 2 -> intersection along a polygon edge

    b = shapely.Point((1, 1.5))
    a = shapely.Point((1, -0.5))

    result = mpu._cartopy_utils._determine_intersection(box, a, b)
    expected = np.array([[1.0, 0.0], [1.0, 1.0]])

    np.testing.assert_allclose(result, expected)

    # case 3 -> no intersection

    a = shapely.Point((1.5, -0.5))
    b = shapely.Point((1.5, 1.5))
    result = mpu._cartopy_utils._determine_intersection(box, a, b)

    expected = np.array([[]])

    np.testing.assert_allclose(result, expected)
