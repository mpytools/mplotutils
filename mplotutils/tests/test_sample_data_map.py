import numpy as np
import pytest
import xarray as xr

from mplotutils import sample_data_map, sample_dataarray


@pytest.mark.parametrize("nlons", [5, 10])
@pytest.mark.parametrize("nlats", [10, 20])
def test_data_shape(nlons, nlats):
    lon, lat, data = sample_data_map(nlons, nlats)

    assert len(lon) == nlons
    assert len(lat) == nlats

    assert data.shape == (nlats, nlons)


def test_lat():
    __, lat, __ = sample_data_map(36, 9)

    expected_lat = np.arange(-80, 81, 20)
    np.testing.assert_allclose(lat, expected_lat)


def test_lon():
    lon, __, __ = sample_data_map(36, 9)

    expected_lon = np.arange(5, 356, 10)
    np.testing.assert_allclose(lon, expected_lon)


@pytest.mark.parametrize("nlon", [5, 10])
@pytest.mark.parametrize("nlat", [10, 20])
def test_sample_dataarray(nlon, nlat):
    data = sample_dataarray(nlon, nlat)

    assert isinstance(data, xr.DataArray)
    assert data.shape == (nlat, nlon)
