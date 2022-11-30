import numpy as np

from mplotutils import sample_data_map


def test_data_shape():

    nlons = 10
    nlats = 20

    lon, lat, data = sample_data_map(nlons, nlats)

    assert len(lon) == nlons
    assert len(lat) == nlats

    assert data.shape == (nlats, nlons)

    nlons = 5
    nlats = 10

    lon, lat, data = sample_data_map(nlons, nlats)

    assert len(lon) == nlons
    assert len(lat) == nlats

    assert data.shape == (nlats, nlons)


def test_lat():

    __, lat, __ = sample_data_map(36, 9)

    expected_lat = np.arange(-80, 81, 20)
    assert np.allclose(lat, expected_lat)


def test_lon():

    lon, __, __ = sample_data_map(36, 9)

    expected_lon = np.arange(0, 351, 10)
    assert np.allclose(lon, expected_lon)
