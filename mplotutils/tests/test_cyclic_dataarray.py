import pytest
import xarray as xr

from mplotutils import cyclic_dataarray


@pytest.mark.parametrize("as_dataset", (True, False))
def test_cyclic_dataarray_missing_coord(as_dataset):
    da = xr.DataArray([1, 2, 3], dims=("x"), coords={"x": [0, 1, 2]}, name="data")
    data = da.to_dataset() if as_dataset else da

    with pytest.raises(KeyError, match="Did not find 'lon' in obj"):
        cyclic_dataarray(data)

    with pytest.raises(KeyError, match="Did not find 'longitude' in obj"):
        cyclic_dataarray(data, "longitude")


@pytest.mark.parametrize("as_dataset", (True, False))
def test_cyclic_dataarray_not_equally_spaced(as_dataset):
    da = xr.DataArray([1, 2, 3], dims=("x"), coords={"x": [0, 1, 2.1]}, name="data")
    data = da.to_dataset() if as_dataset else da

    with pytest.raises(ValueError, match=".*must be equally spaced"):
        cyclic_dataarray(data, coord="x")


@pytest.mark.parametrize("as_dataset", (True, False))
def test_cyclic_dataarray(as_dataset):
    data = [[1, 2, 3], [4, 5, 6]]

    y = xr.Variable("y", [1, 2], attrs={"foo": "bar"})
    x = xr.Variable("x", [0, 1, 2], attrs={"foo": "bar"})
    da = xr.DataArray(data, dims=("y", "x"), coords={"y": y, "x": x}, name="data")

    expected = [[1, 2, 3, 1], [4, 5, 6, 4]]
    x = xr.Variable("x", [0, 1, 2, 3], attrs={"foo": "bar"})
    da_expected = xr.DataArray(
        expected, dims=("y", "x"), coords={"y": y, "x": x}, name="data"
    )

    data = da.to_dataset() if as_dataset else da
    expected = da_expected.to_dataset() if as_dataset else da_expected

    result = cyclic_dataarray(data, "x")
    xr.testing.assert_identical(result, expected)

    # per default use 'lon'
    data = data.rename(x="lon")
    expected = expected.rename(x="lon")

    result = cyclic_dataarray(data)
    xr.testing.assert_identical(result, expected)
