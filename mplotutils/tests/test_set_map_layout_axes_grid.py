import numpy as np
import pytest
from mpl_toolkits.axes_grid1 import AxesGrid

from mplotutils import set_map_layout

from . import figure_context, get_rtol


def test_set_map_layout_default_width():
    with figure_context() as f:

        axgr = AxesGrid(f, 111, nrows_ncols=(1, 1))

        set_map_layout(axgr)

        width = f.get_size_inches()[0] * 2.54
        np.testing.assert_allclose(width, 17.0, rtol=get_rtol(f))


@pytest.mark.parametrize("xlim", (1, 2, 0.5))
def test_set_map_layout_no_borders(xlim):

    with figure_context() as f:

        axgr = AxesGrid(f, 111, nrows_ncols=(1, 1))

        axgr.axes_all[0].set(xlim=(0, xlim), ylim=(0, 1))

        f.subplots_adjust(left=0, bottom=0, right=1, top=1)

        set_map_layout(axgr, 10)

        width, height = f.get_size_inches() * 2.54
        height_exp = 10 / xlim

        np.testing.assert_allclose((width, height), (10, height_exp), rtol=get_rtol(f))


@pytest.mark.parametrize(
    "bottom, top, height_exp", ([0.5, 1, 20], [0, 0.8, 12.5], [0.5, 0.75, 40])
)
def test_set_map_layout_vert_borders(bottom, top, height_exp):

    # width:height = 1:1
    with figure_context() as f:

        axgr = AxesGrid(f, 111, nrows_ncols=(1, 1))
        axgr.axes_all[0].set(xlim=(0, 1), ylim=(0, 1))

        f.subplots_adjust(left=0, bottom=bottom, right=1, top=top)

        set_map_layout(axgr, 10)

        width, height = f.get_size_inches() * 2.54

        np.testing.assert_allclose((width, height), (10, height_exp), rtol=get_rtol(f))


@pytest.mark.parametrize("left, right, height_exp", ([0.5, 1, 5], [0.25, 0.75, 5]))
def test_set_map_layout_horz_borders(left, right, height_exp):
    # width:height = 1:1
    with figure_context() as f:

        axgr = AxesGrid(f, 111, nrows_ncols=(1, 1))
        axgr.axes_all[0].set(xlim=(0, 1), ylim=(0, 1))

        f.subplots_adjust(left=left, bottom=0, right=right, top=1)

        set_map_layout(axgr, 10)

        width, height = f.get_size_inches() * 2.54

        np.testing.assert_allclose((width, height), (10, height_exp), rtol=get_rtol(f))


def test_set_map_layout_two_axes_vert():
    # width:height = 1:1

    # no space between axes
    with figure_context() as f:

        axgr = AxesGrid(f, 111, nrows_ncols=(2, 1), axes_pad=0)
        axgr.axes_all[0].set(xlim=(0, 1), ylim=(0, 1))

        f.subplots_adjust(left=0, bottom=0, right=1, top=1)

        set_map_layout(axgr, 10)

        width, height = f.get_size_inches() * 2.54

        np.testing.assert_allclose((width, height), (10, 20), rtol=get_rtol(f))

    # 1 cm between axes
    with figure_context() as f:

        axgr = AxesGrid(f, 111, nrows_ncols=(2, 1), axes_pad=1 / 2.54)
        axgr.axes_all[0].set(xlim=(0, 1), ylim=(0, 1))

        f.subplots_adjust(left=0, bottom=0, right=1, top=1)

        set_map_layout(axgr, 10)

        width, height = f.get_size_inches() * 2.54

        np.testing.assert_allclose((width, height), (10, 20 + 1), rtol=get_rtol(f))


def test_set_map_layout_two_axes_vert_colorbars():

    with figure_context() as f:

        axgr = AxesGrid(
            f,
            111,
            nrows_ncols=(2, 1),
            axes_pad=0.05 / 2.54,
            cbar_mode="each",
            cbar_location="bottom",
            cbar_size=0.75 / 2.54,
            cbar_pad=0.1 / 2.54,
        )

        for ax in axgr.axes_all:
            ax.set(xlim=(0, 1), ylim=(0, 1))

        f.subplots_adjust(left=0, bottom=0, right=1, top=1)

        set_map_layout(axgr, 10)

        width, height = f.get_size_inches() * 2.54

        np.testing.assert_allclose(
            (width, height), (10, 20 + 2 * 0.75 + 2 * 0.1 + 0.05), rtol=get_rtol(f)
        )

    with figure_context() as f:

        axgr = AxesGrid(
            f,
            111,
            nrows_ncols=(2, 1),
            axes_pad=0,
            cbar_mode="edge",
            cbar_location="bottom",
            cbar_size="10%",
            cbar_pad="5%",
        )

        for ax in axgr.axes_all:
            ax.set(xlim=(0, 1), ylim=(0, 1))

        f.subplots_adjust(left=0, bottom=0, right=1, top=1)

        set_map_layout(axgr, 10)

        width, height = f.get_size_inches() * 2.54

        expected = (10, 20 + 1 + 0.5)
        np.testing.assert_allclose((width, height), expected, rtol=get_rtol(f))


def test_set_map_layout_two_axes_horz():
    # width:height = 1:1

    # no space between axes
    with figure_context() as f:

        axgr = AxesGrid(f, 111, nrows_ncols=(1, 2), axes_pad=0)
        axgr.axes_all[0].set(xlim=(0, 1), ylim=(0, 1))

        f.subplots_adjust(left=0, bottom=0, right=1, top=1)

        set_map_layout(axgr, 10)

        width, height = f.get_size_inches() * 2.54

        np.testing.assert_allclose((width, height), (10, 5), rtol=get_rtol(f))

    # 1 cm between axes
    with figure_context() as f:

        axgr = AxesGrid(f, 111, nrows_ncols=(1, 2), axes_pad=1 / 2.54)
        axgr.axes_all[0].set(xlim=(0, 1), ylim=(0, 1))

        f.subplots_adjust(left=0, bottom=0, right=1, top=1)

        set_map_layout(axgr, 10)

        width, height = f.get_size_inches() * 2.54

        expected = (10, 4.5)

        np.testing.assert_allclose((width, height), expected, rtol=get_rtol(f))


def test_set_map_layout_two_axes_horz_colorbars():

    with figure_context() as f:

        axgr = AxesGrid(
            f,
            111,
            nrows_ncols=(1, 2),
            axes_pad=1 / 2.54,
            cbar_mode="each",
            cbar_location="right",
            cbar_size=0.4 / 2.54,
            cbar_pad=0.1 / 2.54,
        )

        for ax in axgr.axes_all:
            ax.set(xlim=(0, 1), ylim=(0, 1))

        f.subplots_adjust(left=0, bottom=0, right=1, top=1)

        set_map_layout(axgr, 10)

        width, height = f.get_size_inches() * 2.54

        np.testing.assert_allclose((width, height), (10, 4), rtol=get_rtol(f))

    with figure_context() as f:

        axgr = AxesGrid(
            f,
            111,
            nrows_ncols=(1, 2),
            axes_pad=0,
            cbar_mode="edge",
            cbar_location="right",
            cbar_size="10%",
            cbar_pad="10%",
        )

        for ax in axgr.axes_all:
            ax.set(xlim=(0, 1), ylim=(0, 1))

        f.subplots_adjust(left=0, bottom=0, right=1, top=1)

        set_map_layout(axgr, 10)

        width, height = f.get_size_inches() * 2.54

        expected = (10, 10 / (1 + 1 + 0.1 + 0.1))
        np.testing.assert_allclose((width, height), expected, rtol=get_rtol(f))


@pytest.mark.parametrize("ncols, axes_pad", ([2, 10], [4, 2.5]))
def test_set_map_layout_horz_not_enough_space(ncols, axes_pad):

    with figure_context() as f:

        axgr = AxesGrid(f, 111, nrows_ncols=(1, ncols), axes_pad=axes_pad)

        for ax in axgr.axes_all:
            ax.set(xlim=(0, 1), ylim=(0, 1))

        f.subplots_adjust(left=0, bottom=0, right=1, top=1)

        with pytest.raises(ValueError, match="Not enough space on figure"):
            set_map_layout(axgr, 10)
