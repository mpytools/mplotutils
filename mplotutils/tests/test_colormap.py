import matplotlib
import numpy as np
import pytest

import mplotutils as mpu


def test_from_levels_and_cmap_not_list():

    with pytest.raises(ValueError, match="'levels' must be a list of levels"):
        mpu.from_levels_and_cmap(3, "Greys")


def assert_cmap_norm(cmap, norm, levels, extend):

    zeros = np.zeros(4)

    assert isinstance(cmap, matplotlib.colors.ListedColormap)

    assert cmap.N == len(levels) - 1
    assert cmap.colorbar_extend == extend
    np.testing.assert_allclose(cmap.get_bad(), zeros)

    if extend in ("both", "min"):
        assert np.not_equal(cmap.get_under(), zeros).all()
    else:
        assert np.equal(cmap.get_under(), zeros).all()

    if extend in ("both", "max"):
        assert np.not_equal(cmap.get_over(), zeros).all()
    else:
        assert np.equal(cmap.get_over(), zeros).all()

    assert isinstance(norm, matplotlib.colors.BoundaryNorm)
    np.testing.assert_allclose(norm.boundaries, levels)


def test_from_levels_and_cmap():

    levels = [1, 2, 3]
    extend = "neither"
    cmap, norm = mpu.from_levels_and_cmap(levels, "viridis", extend=extend)
    assert_cmap_norm(cmap, norm, levels, extend)


@pytest.mark.parametrize("extend", ("neither", "min", "max", "both"))
def test_from_levels_and_cmap_extend(extend):

    levels = [1, 2, 3]
    cmap, norm = mpu.from_levels_and_cmap(levels, "viridis", extend=extend)
    assert_cmap_norm(cmap, norm, levels, extend)
