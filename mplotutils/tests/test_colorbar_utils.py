import matplotlib.pyplot as plt
import numpy as np
import pytest

from mplotutils._colorbar import (
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

    with pytest.raises(ValueError, match="'shift' must be in 0...1"):
        _parse_shift_shrink(-0.1, 0)

    with pytest.raises(ValueError, match="'shift' must be in 0...1"):
        _parse_shift_shrink(1.1, 0)

    with pytest.raises(ValueError, match="'shrink' must be in 0...1"):
        _parse_shift_shrink(0, -0.1)

    with pytest.raises(ValueError, match="'shrink' must be in 0...1"):
        _parse_shift_shrink(0, 1.1)

    with pytest.warns(UserWarning, match="'shift' is larger than 'shrink'"):
        _parse_shift_shrink(0.6, 0.3)


def test_parse_size_aspect_pad():
    """
    size, aspect, pad = _parse_size_aspect_pad(size, aspect, pad, 'horizontal')
    """

    with pytest.raises(ValueError, match="Can only pass one of 'aspect' and 'size'"):
        _parse_size_aspect_pad(1, 1, 0.1, "horizontal")

    result = _parse_size_aspect_pad(0.1, None, 0.1, "horizontal")
    assert result == (0.1, None, 0.1)

    result = _parse_size_aspect_pad(None, None, 0.1, "horizontal")
    assert result == (None, 20, 0.1)

    result = _parse_size_aspect_pad(None, 10, 0.1, "horizontal")
    assert result == (None, 10, 0.1)

    result = _parse_size_aspect_pad(None, 20, 0.1, "horizontal")
    assert result == (None, 20, 0.1)

    result = _parse_size_aspect_pad(None, None, None, "horizontal")
    assert result == (None, 20, 0.15)

    result = _parse_size_aspect_pad(None, None, None, "vertical")
    assert result == (None, 20, 0.05)


# =============================================================================


def test_colorbar_differnt_figures():

    _, ax1 = plt.subplots()
    _, ax2 = plt.subplots()

    h = ax1.pcolormesh([[0, 1]])

    with pytest.raises(ValueError, match="must belong to the same figure"):
        colorbar(h, ax1, ax2)


def test_colorbar_ax_and_ax2_error():

    _, (ax1, ax2, ax3) = plt.subplots(3, 1)
    h = ax1.pcolormesh([[0, 1]])

    with pytest.raises(ValueError, match="Cannot pass `ax`, and `ax2`"):
        colorbar(h, ax1, ax2, ax=ax3)


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

    np.testing.assert_allclose(res, exp, atol=1e-08)

    # -----------------------------------------------------------

    f.subplots_adjust(left=0, bottom=0.1, right=0.8, top=0.9)
    f.canvas.draw()

    pos = cbar.ax.get_position()
    res = [pos.x0, pos.y0, pos.width, pos.height]
    exp = [0.8, 0.1, 0.2 * 0.8, 0.8]

    np.testing.assert_allclose(res, exp, atol=1e-08)

    plt.close()

    # ===========================================================

    # test pad=0, aspect=5
    f, cbar = _easy_cbar_vert(aspect=5, pad=0)

    pos = cbar.ax.get_position()

    # don't test width if aspect is given, but also test aspect
    res = [pos.x0, pos.y0, pos.height]
    exp = [0.8, 0, 1.0]
    np.testing.assert_allclose(res, exp, atol=1e-08)

    assert cbar.ax.get_box_aspect() == 5

    plt.close()

    # ===========================================================

    # test pad=0, aspect=default (=20)
    f, cbar = _easy_cbar_vert(pad=0)

    pos = cbar.ax.get_position()

    # don't test width if aspect is given, but also test aspect
    res = [pos.x0, pos.y0, pos.height]
    exp = [0.8, 0, 1.0]
    np.testing.assert_allclose(res, exp, atol=1e-08)

    assert cbar.ax.get_box_aspect() == 20

    plt.close()

    # ===========================================================

    # pad=0.05, size=0.1

    f, cbar = _easy_cbar_vert(size=0.1, pad=0.05)

    pos = cbar.ax.get_position()
    res = [pos.x0, pos.y0, pos.width, pos.height]
    exp = [0.8 + 0.8 * 0.05, 0, 0.8 * 0.1, 1.0]

    np.testing.assert_allclose(res, exp, atol=1e-08)

    plt.close()

    # ===========================================================

    # shift='symmetric', shrink=0.1
    # --> colorbar is 10 % smaller, and centered

    f, cbar = _easy_cbar_vert(size=0.2, pad=0.0, shrink=0.1)

    pos = cbar.ax.get_position()
    res = [pos.x0, pos.y0, pos.width, pos.height]
    exp = [0.8, 0.05, 0.2 * 0.8, 0.9]

    np.testing.assert_allclose(res, exp, atol=1e-08)

    plt.close()

    # ===========================================================

    # shift=0., shrink=0.1
    # --> colorbar is 10 % smaller, and aligned with the bottom

    f, cbar = _easy_cbar_vert(size=0.2, pad=0.0, shrink=0.1, shift=0.0)

    pos = cbar.ax.get_position()
    res = [pos.x0, pos.y0, pos.width, pos.height]
    exp = [0.8, 0.0, 0.2 * 0.8, 0.9]

    np.testing.assert_allclose(res, exp, atol=1e-08)

    plt.close()

    # ===========================================================

    # shift=0.1, shrink=None
    # --> colorbar is 10 % smaller, and aligned with the top

    f, cbar = _easy_cbar_vert(size=0.2, pad=0.0, shrink=None, shift=0.1)

    pos = cbar.ax.get_position()
    res = [pos.x0, pos.y0, pos.width, pos.height]
    exp = [0.8, 0.1, 0.2 * 0.8, 0.9]

    np.testing.assert_allclose(res, exp, atol=1e-08)

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
    np.testing.assert_allclose(res, exp, atol=1e-08)

    assert cbar.ax.get_box_aspect() == 1.0 / 5

    plt.close()

    # ===========================================================

    # test pad=0, aspect=default (=20)
    f, cbar = _easy_cbar_horz(pad=0)

    pos = cbar.ax.get_position()

    # don't test width if aspect is given, but also test aspect
    res = [pos.x0, pos.y0 + pos.height, pos.width]
    exp = [0.0, 0.2, 1.0]
    np.testing.assert_allclose(res, exp, atol=1e-08)

    assert cbar.ax.get_box_aspect() == 1.0 / 20

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

    with pytest.raises(ValueError):
        colorbar(h, ax1, orientation="wrong")

    with pytest.raises(ValueError):
        colorbar(h, ax1, anchor=5)

    with pytest.raises(ValueError):
        colorbar(h, ax1, panchor=5)


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
