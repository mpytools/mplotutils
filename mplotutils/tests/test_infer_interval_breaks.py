import numpy as np
import pytest
from numpy.testing import assert_array_equal  # noqa: F401

from mplotutils._xrcompat import _infer_interval_breaks, infer_interval_breaks


def test_infer_interval_breaks_warns():
    with pytest.warns(FutureWarning):
        infer_interval_breaks(np.array([1, 2, 3]), np.array([1, 2, 3]))


def test__infer_interval_breaks():
    assert_array_equal([-0.5, 0.5, 1.5], _infer_interval_breaks([0, 1]))
    assert_array_equal(
        [-0.5, 0.5, 5.0, 9.5, 10.5], _infer_interval_breaks([0, 1, 9, 10])
    )

    # make a bounded 2D array that we will center and re-infer
    xref, yref = np.meshgrid(np.arange(6), np.arange(5))
    cx = (xref[1:, 1:] + xref[:-1, :-1]) / 2
    cy = (yref[1:, 1:] + yref[:-1, :-1]) / 2
    x = _infer_interval_breaks(cx, axis=1)
    x = _infer_interval_breaks(x, axis=0)
    y = _infer_interval_breaks(cy, axis=1)
    y = _infer_interval_breaks(y, axis=0)
    np.testing.assert_allclose(xref, x)
    np.testing.assert_allclose(yref, y)

    # test that warning is raised for non-monotonic inputs
    # with raises(ValueError):
    #     _infer_interval_breaks(np.array([0, 2, 1]))


@pytest.mark.filterwarnings("ignore:It's no longer necessary")
def test_infer_interval_breaks():
    # 1D
    lon = np.arange(5, 356, 10)
    lat = np.arange(-85, 86, 10)

    lon_expected = np.arange(0, 361, 10)
    lat_expected = np.arange(-90, 91, 10)

    lon_result, lat_result = infer_interval_breaks(lon, lat)

    np.testing.assert_allclose(lon_expected, lon_result)
    np.testing.assert_allclose(lat_expected, lat_result)

    # 2D, as above

    xref, yref = np.meshgrid(np.arange(6), np.arange(5))
    cx = (xref[1:, 1:] + xref[:-1, :-1]) / 2
    cy = (yref[1:, 1:] + yref[:-1, :-1]) / 2

    x, y = infer_interval_breaks(cx, cy)

    np.testing.assert_allclose(xref, x)
    np.testing.assert_allclose(yref, y)


@pytest.mark.filterwarnings("ignore:It's no longer necessary")
def test_infer_interval_breaks_clip():
    # no clip
    lon = np.arange(5, 356, 10)
    lat = np.arange(-90, 91, 10)

    lon_expected = np.arange(0, 361, 10)
    lat_expected = np.arange(-95, 96, 10)

    lon_result, lat_result = infer_interval_breaks(lon, lat)

    np.testing.assert_allclose(lon_expected, lon_result)
    np.testing.assert_allclose(lat_expected, lat_result)

    # clip
    lat_expected[0] = -90
    lat_expected[-1] = 90

    lon_result, lat_result = infer_interval_breaks(lon, lat, clip=True)

    np.testing.assert_allclose(lon_expected, lon_result)
    np.testing.assert_allclose(lat_expected, lat_result)
