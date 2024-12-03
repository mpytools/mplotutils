import cartopy.crs as ccrs
import numpy as np

import mplotutils as mpu

from . import subplots_context


def test_yticklabels_robinson():
    with subplots_context(subplot_kw=dict(projection=ccrs.Robinson())) as (f, ax):
        ax.set_global()

        lat = np.arange(-90, 91, 20)

        mpu.yticklabels(lat, ax=ax, size=8)

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


def test_xticklabels_robinson():
    with subplots_context(subplot_kw=dict(projection=ccrs.Robinson())) as (f, ax):
        ax.set_global()

        lon = np.arange(-180, 181, 60)

        mpu.xticklabels(lon, ax=ax, size=8)

        y_pos = -89.99

        # two elements are not added because they are beyond the map limits
        lon = lon[1:-1]

        for t, x_pos in zip(ax.texts, lon, strict=True):
            np.testing.assert_allclose((x_pos, y_pos), t.xy, atol=0.01)

        assert ax.texts[0].get_text() == "120°W"
        assert ax.texts[-1].get_text() == "120°E"


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
