import matplotlib.pyplot as plt
import numpy as np
import pytest

import mplotutils as mpu
from mplotutils._colorbar import _get_cbax, _parse_shift_shrink, _parse_size_aspect_pad

from . import figure_context, subplots_context


def assert_position(cbar, expected):

    pos = cbar.ax.get_position()
    result = [pos.x0, pos.y0, pos.width, pos.height]

    np.testing.assert_allclose(result, expected, atol=1e-08)


def assert_aspect(cbar, expected):

    assert cbar.ax.get_box_aspect() == expected
    # the aspect is given in pixel space (i.e. the size of the figure matters)
    np.testing.assert_allclose(cbar.ax.bbox.height / cbar.ax.bbox.width, expected)


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


def test_colorbar_different_figures():

    with figure_context() as f1, figure_context() as f2:
        ax1 = f1.subplots()
        ax2 = f2.subplots()

        h = ax1.pcolormesh([[0, 1]])

        with pytest.raises(ValueError, match="must belong to the same figure"):
            mpu.colorbar(h, ax1, ax2)


def test_colorbar_ax_and_ax2_error():

    with figure_context() as f:
        ax1, ax2, ax3 = f.subplots(3, 1)
        h = ax1.pcolormesh([[0, 1]])

        with pytest.raises(ValueError, match="Cannot pass `ax`, and `ax2`"):
            mpu.colorbar(h, ax1, ax2, ax=ax3)


def create_figure_subplots(nrows=1, ncols=1, orientation="vertical"):

    f = plt.gcf()

    axs = f.subplots(nrows=nrows, ncols=ncols, squeeze=False)

    if orientation == "vertical":
        right = 0.8
        bottom = 0.0
    elif orientation == "horizontal":
        right = 1
        bottom = 0.2
    else:
        raise ValueError(orientation)

    f.subplots_adjust(left=0, bottom=bottom, right=right, top=1, hspace=0, wspace=0)

    # simplest 'mappable'
    h = axs[0, 0].pcolormesh([[0, 1]])

    axs = axs.item() if axs.size == 1 else axs.squeeze()

    return h, axs


def colorbar_one_ax_vertical(**kwargs):

    h, ax = create_figure_subplots()
    cbar = mpu.colorbar(h, ax, **kwargs)
    return cbar


def colorbar_one_ax_horizontal(**kwargs):

    h, ax = create_figure_subplots(orientation="horizontal")
    cbar = mpu.colorbar(h, ax, orientation="horizontal", **kwargs)
    return cbar


def test_colorbar_vertical_aspect():

    with figure_context(figsize=(5, 5)):

        # test pad=0, aspect=5
        cbar = colorbar_one_ax_vertical(aspect=5, pad=0)

        expected = [0.8, 0, 0.2, 1.0]
        plt.gcf().canvas.draw()

        assert_position(cbar, expected)
        assert_aspect(cbar, 5)

    with figure_context(figsize=(4, 2)):

        cbar = colorbar_one_ax_vertical(aspect=20, pad=0)

        expected = [0.8, 0.0, 0.025, 1]
        assert_position(cbar, expected)
        assert_aspect(cbar, 20)

    with figure_context(figsize=(2, 4)):

        cbar = colorbar_one_ax_vertical(aspect=20, pad=0)

        expected = [0.8, 0.0, 0.1, 1]
        assert_position(cbar, expected)
        assert_aspect(cbar, 20)

    with figure_context(figsize=(5, 5)):

        # test pad=0, aspect=default (=20)
        cbar = colorbar_one_ax_vertical(pad=0)

        expected = [0.8, 0, 1 / 20, 1.0]
        assert_position(cbar, expected)
        assert_aspect(cbar, 20)


def test_colorbar_vertical_size():

    with figure_context() as f:

        # test pad=0, size=0.2
        cbar = colorbar_one_ax_vertical(size=0.2, pad=0)

        expected = [0.8, 0, 0.2 * 0.8, 1.0]
        assert_position(cbar, expected)

        # -----------------------------------------------------------

        f.subplots_adjust(left=0, bottom=0.1, right=0.8, top=0.9)
        f.canvas.draw()
        expected = [0.8, 0.1, 0.2 * 0.8, 0.8]
        assert_position(cbar, expected)

    with figure_context():

        # pad=0.05, size=0.1

        cbar = colorbar_one_ax_vertical(size=0.1, pad=0.05)

        expected = [0.8 + 0.8 * 0.05, 0, 0.8 * 0.1, 1.0]
        assert_position(cbar, expected)

    with figure_context():

        # shift='symmetric', shrink=0.1
        # --> colorbar is 10 % smaller, and centered

        cbar = colorbar_one_ax_vertical(size=0.2, pad=0.0, shrink=0.1)

        expected = [0.8, 0.05, 0.2 * 0.8, 0.9]
        assert_position(cbar, expected)

    with figure_context():
        # shift=0., shrink=0.1
        # --> colorbar is 10 % smaller, and aligned with the bottom

        cbar = colorbar_one_ax_vertical(size=0.2, pad=0.0, shrink=0.1, shift=0.0)

        expected = [0.8, 0.0, 0.2 * 0.8, 0.9]
        assert_position(cbar, expected)

    with figure_context():
        # shift=0.1, shrink=None
        # --> colorbar is 10 % smaller, and aligned with the top

        cbar = colorbar_one_ax_vertical(size=0.2, pad=0.0, shrink=None, shift=0.1)

        expected = [0.8, 0.1, 0.2 * 0.8, 0.9]
        assert_position(cbar, expected)


def test_colorbar_horizontal_aspect():

    with figure_context(figsize=(5, 5)):

        # test pad=0, aspect=5
        cbar = colorbar_one_ax_horizontal(aspect=5, pad=0)

        expected = [0.0, 0.0, 1.0, 0.2]
        assert_position(cbar, expected)
        assert_aspect(cbar, 1 / 5)

    with figure_context(figsize=(4, 2)):

        # test pad=0, aspect=5
        cbar = colorbar_one_ax_horizontal(aspect=20, pad=0)

        expected = [0.0, 0.1, 1.0, 0.1]
        assert_position(cbar, expected)
        assert_aspect(cbar, 1 / 20)

    with figure_context(figsize=(2, 4)):

        # test pad=0, aspect=5
        cbar = colorbar_one_ax_horizontal(aspect=20, pad=0)

        # f.canvas.draw()

        expected = [0.0, 0.175, 1.0, 0.025]
        assert_position(cbar, expected)
        assert_aspect(cbar, 1 / 20)

    with figure_context(figsize=(5, 5)):
        # test pad=0, aspect=default (=20)

        cbar = colorbar_one_ax_horizontal(pad=0)

        expected = [0.0, 0.2 - 1 / 20, 1.0, 1 / 20]
        assert_position(cbar, expected)
        assert_aspect(cbar, 1 / 20)


def test_colorbar_horizontal_size():

    with figure_context() as f:
        # test pad=0, size=0.2
        cbar = colorbar_one_ax_horizontal(size=0.2, pad=0)

        expected = [0, 0.2 * (1 - 0.8), 1, 0.2 * 0.8]
        assert_position(cbar, expected)

        # -----------------------------------------------------------

        f.subplots_adjust(left=0.1, bottom=0.2, right=0.9, top=1)
        f.canvas.draw()

        expected = [0.1, 0.2 * (1 - 0.8), 0.8, 0.2 * 0.8]
        assert_position(cbar, expected)

    with figure_context():
        # pad=0.05, size=0.1

        cbar = colorbar_one_ax_horizontal(size=0.1, pad=0.05)

        expected = [0.0, 0.2 - 0.15 * 0.8, 1, 0.1 * 0.8]
        assert_position(cbar, expected)

    with figure_context():
        # shift='symmetric', shrink=0.1
        # --> colorbar is 10 % smaller, and centered

        cbar = colorbar_one_ax_horizontal(size=0.2, pad=0.0, shrink=0.1)
        expected = [0.05, 0.2 * (1 - 0.8), 0.9, 0.2 * 0.8]
        assert_position(cbar, expected)

    with figure_context():
        # shift=0., shrink=0.1
        # --> colorbar is 10 % smaller, and aligned with lhs

        cbar = colorbar_one_ax_horizontal(size=0.2, pad=0.0, shrink=0.1, shift=0.0)

        expected = [0.0, 0.2 * (1 - 0.8), 0.9, 0.2 * 0.8]
        assert_position(cbar, expected)

    with figure_context():
        # shift=0.1, shrink=None
        # --> colorbar is 10 % smaller, and aligned with rhs

        cbar = colorbar_one_ax_horizontal(size=0.2, pad=0.0, shrink=None, shift=0.1)

        expected = [0.1, 0.2 * (1 - 0.8), 0.9, 0.2 * 0.8]
        assert_position(cbar, expected)


def test_colorbar_vertical_two_axes():

    # use two horizontal axes
    with figure_context():
        h, axs = create_figure_subplots(1, 2)

        cbar = mpu.colorbar(h, axs[0], axs[1], size=0.2, pad=0)
        expected = [0.8, 0, 0.2 * 0.8 * 0.5, 1.0]
        assert_position(cbar, expected)

    # use two vertical axes
    with figure_context():
        h, axs = create_figure_subplots(2, 1)

        cbar = mpu.colorbar(h, axs[0], axs[1], size=0.2, pad=0)

        expected = [0.8, 0.0, 0.2 * 0.8, 1]
        assert_position(cbar, expected)

        # exchange the axes
        cbar = mpu.colorbar(h, axs[1], axs[0], size=0.2, pad=0)

        expected = [0.8, 0.0, 0.2 * 0.8, 1]
        assert_position(cbar, expected)

    # use ax instead of ax2
    with figure_context():
        h, axs = create_figure_subplots(2, 1)

        cbar = mpu.colorbar(h, axs[0], ax=axs[1], size=0.2, pad=0)

        expected = [0.8, 0.0, 0.2 * 0.8, 1]
        assert_position(cbar, expected)

    # only use one of the two axes
    with figure_context():
        h, axs = create_figure_subplots(2, 1)

        cbar = mpu.colorbar(h, axs[0], size=0.2, pad=0)

        expected = [0.8, 0.5, 0.2 * 0.8, 0.5]
        assert_position(cbar, expected)

        cbar = mpu.colorbar(h, axs[1], size=0.2, pad=0)

        expected = [0.8, 0, 0.2 * 0.8, 0.5]
        assert_position(cbar, expected)


def test_colorbar_horizontal_two_axes():

    # use two horizontal axes
    with figure_context():
        h, axs = create_figure_subplots(2, 1, orientation="horizontal")

        cbar = mpu.colorbar(
            h, axs[0], axs[1], size=0.2, pad=0, orientation="horizontal"
        )

        height = 0.2 * 0.8 * 0.5
        expected = [0.0, 0.2 - height, 1.0, height]
        assert_position(cbar, expected)

    # use two horizontal axes
    with figure_context():
        h, axs = create_figure_subplots(1, 2, orientation="horizontal")

        cbar = mpu.colorbar(
            h, axs[0], axs[1], size=0.2, pad=0, orientation="horizontal"
        )

        height = 0.2 * 0.8
        expected = [0.0, 0.2 - height, 1, height]
        assert_position(cbar, expected)

        # exchange the axes
        cbar = mpu.colorbar(
            h, axs[1], axs[0], size=0.2, pad=0, orientation="horizontal"
        )

        height = 0.2 * 0.8
        expected = [0.0, 0.2 - height, 1, height]
        assert_position(cbar, expected)

    # use ax instead of ax2
    with figure_context():
        h, axs = create_figure_subplots(1, 2, orientation="horizontal")

        cbar = mpu.colorbar(
            h, axs[0], ax=axs[1], size=0.2, pad=0, orientation="horizontal"
        )

        height = 0.2 * 0.8
        expected = [0.0, 0.2 - height, 1, height]
        assert_position(cbar, expected)

    # only use one of the two axes
    with figure_context():
        h, axs = create_figure_subplots(1, 2, orientation="horizontal")

        cbar = mpu.colorbar(h, axs[0], size=0.2, pad=0, orientation="horizontal")

        height = 0.2 * 0.8
        expected = [0.0, 0.2 - height, 0.5, height]
        assert_position(cbar, expected)

        cbar = mpu.colorbar(h, axs[1], size=0.2, pad=0, orientation="horizontal")

        height = 0.2 * 0.8
        expected = [0.5, 0.2 - height, 0.5, height]
        assert_position(cbar, expected)


def test_colorbar_errors():

    with subplots_context() as (f, ax):

        h = ax.pcolormesh([[0, 1]])

        with pytest.raises(
            ValueError, match="orientation must be 'vertical' or 'horizontal'"
        ):
            mpu.colorbar(h, ax, orientation="wrong")

        with pytest.raises(ValueError, match="'anchor' and 'panchor'"):
            mpu.colorbar(h, ax, anchor=5)

        with pytest.raises(ValueError, match="'anchor' and 'panchor'"):
            mpu.colorbar(h, ax, panchor=5)

        with pytest.raises(ValueError, match="'anchor' and 'panchor'"):
            mpu.colorbar(h, ax, panchor=5, anchor=5)


def test_get_cbax():

    with subplots_context() as (f, ax):

        cbax = _get_cbax(f)

        assert isinstance(cbax, plt.Axes)

        assert len(f.get_axes()) == 2

        _get_cbax(f)
        assert len(f.get_axes()) == 3

        _get_cbax(f)
        assert len(f.get_axes()) == 4

        _get_cbax(f)
        assert len(f.get_axes()) == 5
