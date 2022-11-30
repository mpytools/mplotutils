import matplotlib.pyplot as plt
import numpy as np
from pytest import raises

from mplotutils.colorbar_utils import (
    _get_cbax,
    _parse_shift_shrink,
    _parse_size_aspect_pad,
    _resize_colorbar_horz,
    _resize_colorbar_vert,
    colorbar,
)


def test_parse_shift_shrink():

    # test code for _parse_shift_shrink
    assert _parse_shift_shrink("symmetric", None) == (0.0, 0.0)

    assert _parse_shift_shrink("symmetric", 1) == (0.5, 1)

    assert _parse_shift_shrink(1, None) == (1, 1)

    assert _parse_shift_shrink(1, 1) == (1, 1)

    assert _parse_shift_shrink(0.5, 0.5) == (0.5, 0.5)

    with raises(AssertionError):
        _parse_shift_shrink(-0.1, 0)

    with raises(AssertionError):
        _parse_shift_shrink(1.1, 0)

    with raises(AssertionError):
        _parse_shift_shrink(0, -0.1)

    with raises(AssertionError):
        _parse_shift_shrink(0, 1.1)


# =============================================================================


def test_parse_size_aspect_pad():
    """
    size, aspect, pad = _parse_size_aspect_pad(size, aspect, pad, 'horizontal')
    """

    res = _parse_size_aspect_pad(0.1, None, 0.1, "horizontal")
    exp = (0.1, None, 0.1)
    assert res == exp

    res = _parse_size_aspect_pad(None, None, 0.1, "horizontal")
    exp = (10, 20, 0.1)
    assert res == exp

    res = _parse_size_aspect_pad(None, 20, 0.1, "horizontal")
    exp = (10, 20, 0.1)
    assert res == exp

    with raises(ValueError):
        _parse_size_aspect_pad(1, 1, 0.1, "horizontal")

    res = _parse_size_aspect_pad(None, None, None, "horizontal")
    exp = (10, 20, 0.15)
    assert res == exp

    res = _parse_size_aspect_pad(None, None, None, "vertical")
    exp = (10, 20, 0.05)
    assert res == exp


# =============================================================================


def _easy_cbar_vert(**kwargs):

    f, ax = plt.subplots()

    f.subplots_adjust(left=0, bottom=0, right=0.8, top=1)

    # simplest 'mappable'
    h = ax.pcolormesh([[0, 1]])

    # create colorbar
    cbax = f.add_axes([0, 0, 0.1, 0.1])

    cbar = plt.colorbar(h, orientation="vertical", cax=cbax)

    func = _resize_colorbar_vert(cbax, ax, **kwargs)
    f.canvas.mpl_connect("draw_event", func)

    f.canvas.draw()

    return f, cbar


def test_resize_colorbar_vert():

    # test pad=0, size=0.2
    f, cbar = _easy_cbar_vert(size=0.2, pad=0)

    pos = cbar.ax.get_position()
    res = [pos.x0, pos.y0, pos.width, pos.height]
    exp = [0.8, 0, 0.2 * 0.8, 1.0]

    np.testing.assert_allclose(res, exp)

    # -----------------------------------------------------------

    f.subplots_adjust(left=0, bottom=0.1, right=0.8, top=0.9)
    f.canvas.draw()

    pos = cbar.ax.get_position()
    res = [pos.x0, pos.y0, pos.width, pos.height]
    exp = [0.8, 0.1, 0.2 * 0.8, 0.8]

    np.testing.assert_allclose(res, exp)

    plt.close()

    # ===========================================================

    # test pad=0, aspect=5
    f, cbar = _easy_cbar_vert(aspect=5, pad=0)

    pos = cbar.ax.get_position()

    # don't test width if aspect is given, but also test aspect
    res = [pos.x0, pos.y0, pos.height]
    exp = [0.8, 0, 1.0]
    np.testing.assert_allclose(res, exp)

    assert cbar.ax.get_aspect() == 5

    plt.close()

    # ===========================================================

    # test pad=0, aspect=default (=20)
    f, cbar = _easy_cbar_vert(pad=0)

    pos = cbar.ax.get_position()

    # don't test width if aspect is given, but also test aspect
    res = [pos.x0, pos.y0, pos.height]
    exp = [0.8, 0, 1.0]
    np.testing.assert_allclose(res, exp)

    assert cbar.ax.get_aspect() == 20

    plt.close()

    # ===========================================================

    # pad=0.05, size=0.1

    f, cbar = _easy_cbar_vert(size=0.1, pad=0.05)

    pos = cbar.ax.get_position()
    res = [pos.x0, pos.y0, pos.width, pos.height]
    exp = [0.8 + 0.8 * 0.05, 0, 0.8 * 0.1, 1.0]

    np.testing.assert_allclose(res, exp)

    plt.close()

    # ===========================================================

    # shift='symmetric', shrink=0.1
    # --> colorbar is 10 % smaller, and centered

    f, cbar = _easy_cbar_vert(size=0.2, pad=0.0, shrink=0.1)

    pos = cbar.ax.get_position()
    res = [pos.x0, pos.y0, pos.width, pos.height]
    exp = [0.8, 0.05, 0.2 * 0.8, 0.9]

    np.testing.assert_allclose(res, exp)

    plt.close()

    # ===========================================================

    # shift=0., shrink=0.1
    # --> colorbar is 10 % smaller, and aligned with the bottom

    f, cbar = _easy_cbar_vert(size=0.2, pad=0.0, shrink=0.1, shift=0.0)

    pos = cbar.ax.get_position()
    res = [pos.x0, pos.y0, pos.width, pos.height]
    exp = [0.8, 0.0, 0.2 * 0.8, 0.9]

    np.testing.assert_allclose(res, exp)

    plt.close()

    # ===========================================================

    # shift=0.1, shrink=None
    # --> colorbar is 10 % smaller, and aligned with the top

    f, cbar = _easy_cbar_vert(size=0.2, pad=0.0, shrink=None, shift=0.1)

    pos = cbar.ax.get_position()
    res = [pos.x0, pos.y0, pos.width, pos.height]
    exp = [0.8, 0.1, 0.2 * 0.8, 0.9]

    np.testing.assert_allclose(res, exp)

    plt.close()


# =============================================================================
# =============================================================================


def _easy_cbar_horz(**kwargs):

    f, ax = plt.subplots()

    f.subplots_adjust(left=0, bottom=0.2, right=1, top=1)

    # simplest 'mappable'
    h = ax.pcolormesh([[0, 1]])

    # create colorbar
    cbax = f.add_axes([0, 0, 0.1, 0.1])

    cbar = plt.colorbar(h, orientation="horizontal", cax=cbax)

    func = _resize_colorbar_horz(cbax, ax, **kwargs)
    f.canvas.mpl_connect("draw_event", func)

    f.canvas.draw()

    return f, cbar


def test_resize_colorbar_horz():

    # test pad=0, size=0.2
    f, cbar = _easy_cbar_horz(size=0.2, pad=0)

    pos = cbar.ax.get_position()
    res = [pos.x0, pos.y0, pos.width, pos.height]
    exp = [0, 0.2 * (1 - 0.8), 1, 0.2 * 0.8]

    # adding atol because else 5e-17 != 0
    np.testing.assert_allclose(res, exp, atol=1e-08)

    # -----------------------------------------------------------

    f.subplots_adjust(left=0.1, bottom=0.2, right=0.9, top=1)
    f.canvas.draw()

    pos = cbar.ax.get_position()
    res = [pos.x0, pos.y0, pos.width, pos.height]
    exp = [0.1, 0.2 * (1 - 0.8), 0.8, 0.2 * 0.8]

    np.testing.assert_allclose(res, exp, atol=1e-08)

    plt.close()

    # ===========================================================

    # test pad=0, aspect=5
    f, cbar = _easy_cbar_horz(aspect=5, pad=0)

    pos = cbar.ax.get_position()

    # don't test width if aspect is given, but also test aspect
    res = [pos.x0, pos.y0 + pos.height, pos.width]
    exp = [0.0, 0.2, 1.0]
    np.testing.assert_allclose(res, exp)

    assert cbar.ax.get_aspect() == 1.0 / 5

    plt.close()

    # ===========================================================

    # test pad=0, aspect=default (=20)
    f, cbar = _easy_cbar_horz(pad=0)

    pos = cbar.ax.get_position()

    # don't test width if aspect is given, but also test aspect
    res = [pos.x0, pos.y0 + pos.height, pos.width]
    exp = [0.0, 0.2, 1.0]
    np.testing.assert_allclose(res, exp)

    assert cbar.ax.get_aspect() == 1.0 / 20

    plt.close()

    # ===========================================================

    # pad=0.05, size=0.1

    f, cbar = _easy_cbar_horz(size=0.1, pad=0.05)

    pos = cbar.ax.get_position()
    res = [pos.x0, pos.y0, pos.width, pos.height]
    exp = [0.0, 0.2 - 0.15 * 0.8, 1, 0.1 * 0.8]

    np.testing.assert_allclose(res, exp, atol=1e-08)

    plt.close()

    # ===========================================================

    # shift='symmetric', shrink=0.1
    # --> colorbar is 10 % smaller, and centered

    f, cbar = _easy_cbar_horz(size=0.2, pad=0.0, shrink=0.1)

    pos = cbar.ax.get_position()
    res = [pos.x0, pos.y0, pos.width, pos.height]
    exp = [0.05, 0.2 * (1 - 0.8), 0.9, 0.2 * 0.8]

    np.testing.assert_allclose(res, exp, atol=1e-08)

    plt.close()

    # ===========================================================

    # shift=0., shrink=0.1
    # --> colorbar is 10 % smaller, and aligned with lhs

    f, cbar = _easy_cbar_horz(size=0.2, pad=0.0, shrink=0.1, shift=0.0)

    pos = cbar.ax.get_position()
    res = [pos.x0, pos.y0, pos.width, pos.height]
    exp = [0.0, 0.2 * (1 - 0.8), 0.9, 0.2 * 0.8]

    np.testing.assert_allclose(res, exp, atol=1e-08)

    plt.close()

    # ===========================================================

    # shift=0.1, shrink=None
    # --> colorbar is 10 % smaller, and aligned with rhs

    f, cbar = _easy_cbar_horz(size=0.2, pad=0.0, shrink=None, shift=0.1)

    pos = cbar.ax.get_position()
    res = [pos.x0, pos.y0, pos.width, pos.height]
    exp = [0.1, 0.2 * (1 - 0.8), 0.9, 0.2 * 0.8]

    np.testing.assert_allclose(res, exp, atol=1e-08)

    plt.close()


# =============================================================================


def test_colorbar():

    # only test high level functionality
    f1, ax1 = plt.subplots()
    h = ax1.pcolormesh([[0, 1]])

    with raises(AssertionError):
        colorbar(h, ax1, orientation="wrong")

    with raises(RuntimeError):
        colorbar(h, ax1, anchor=5)

    with raises(RuntimeError):
        colorbar(h, ax1, panchor=5)

    with raises(AssertionError):
        f2, ax2 = plt.subplots()
        colorbar(h, ax1, ax2)


# =============================================================================


def test_get_cbax():

    f, ax = plt.subplots()

    cbax = _get_cbax(f)

    assert isinstance(cbax, plt.Axes)

    assert len(f.get_axes()) == 2

    _get_cbax(f)
    assert len(f.get_axes()) == 3

    _get_cbax(f)
    assert len(f.get_axes()) == 4

    _get_cbax(f)
    assert len(f.get_axes()) == 5
