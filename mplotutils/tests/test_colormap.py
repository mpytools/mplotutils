import matplotlib
import matplotlib.pyplot as plt
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


def test_from_levels_and_cmap_levels():
    levels = np.arange(-0.35, 0.2, 0.36)
    cmap, norm = mpu.from_levels_and_cmap(levels, "viridis")
    assert_cmap_norm(cmap, norm, levels, extend="neither")


def test_from_levels_and_cmap_color_list():
    cmap = plt.get_cmap("viridis").colors
    levels = [1, 2, 3]
    cmap, norm = mpu.from_levels_and_cmap(levels, cmap)
    assert_cmap_norm(cmap, norm, levels, extend="neither")


def test_from_levels_and_cmap_LinearSegmentedColormap():
    cmap = plt.cm.RdYlGn
    levels = [1, 2, 3]
    cmap, norm = mpu.from_levels_and_cmap(levels, cmap)
    assert_cmap_norm(cmap, norm, levels, extend="neither")


def test_from_levels_and_cmap_seaborn_cmap():
    pytest.importorskip("seaborn")

    levels = [1, 2, 3]
    cmap, norm = mpu.from_levels_and_cmap(levels, "tab10")
    assert_cmap_norm(cmap, norm, levels, extend="neither")


def test_from_levels_and_cmap_colorstring():

    levels = [1, 2, 3]
    cmap, norm = mpu.from_levels_and_cmap(levels, "0.1")
    assert_cmap_norm(cmap, norm, levels, extend="neither")

    np.testing.assert_equal(cmap.colors[0], np.array([0.1, 0.1, 0.1, 1.0]))
    np.testing.assert_equal(cmap.colors[1], np.array([0.1, 0.1, 0.1, 1.0]))


def test_from_levels_and_cmap_color_list_explicit():

    levels = [1, 2, 3, 4, 5]

    # ensure colors are repeated (although that can also be unexpected)
    cmap, norm = mpu.from_levels_and_cmap(levels, ["b", "k"])

    assert_cmap_norm(cmap, norm, levels, extend="neither")

    np.testing.assert_equal(cmap.colors[0], np.array([0.0, 0.0, 1.0, 1.0]))  # blue
    np.testing.assert_equal(cmap.colors[1], np.array([0.0, 0.0, 0.0, 1.0]))  # black
    np.testing.assert_equal(cmap.colors[2], np.array([0.0, 0.0, 1.0, 1.0]))  # blue
    np.testing.assert_equal(cmap.colors[3], np.array([0.0, 0.0, 0.0, 1.0]))  # black
