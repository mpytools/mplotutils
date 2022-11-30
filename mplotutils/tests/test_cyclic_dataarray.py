import numpy as np
import xarray as xr

from mplotutils.cartopy_utils import cyclic_dataarray


def test_cyclic_dataarray():

    data = xr.DataArray(
        [[1, 2, 3], [4, 5, 6]], coords={"x": [1, 2], "y": range(3)}, dims=["x", "y"]
    )

    res = cyclic_dataarray(data, "y")

    expected_data = np.asarray([[1, 2, 3, 1], [4, 5, 6, 4]])

    np.testing.assert_allclose(res, expected_data)

    np.testing.assert_allclose(res.y, [0, 1, 2, 3])
    np.testing.assert_allclose(res.x, [1, 2])

    # per default use 'lon'
    data = xr.DataArray(
        [[1, 2, 3], [4, 5, 6]], coords={"x": [1, 2], "lon": range(3)}, dims=["x", "lon"]
    )

    res = cyclic_dataarray(data)
    np.testing.assert_allclose(res, expected_data)
