import matplotlib.pyplot as plt
import numpy as np
import pytest

from mplotutils import set_map_layout

from . import figure_context, get_rtol, subplots_context


def test_set_map_layout_deprecated_kwarg():

    with subplots_context() as (__, ax):
        with pytest.warns(
            FutureWarning, match="The 'axes' keyword has been renamed to 'obj'"
        ):
            set_map_layout(axes=ax)

    with pytest.raises(
        TypeError,
        match=r"set_map_layout\(\) missing 1 required positional argument: 'obj'",
    ):
        set_map_layout()

    with pytest.raises(TypeError, match="Cannot pass 'obj' and 'axes'"):
        set_map_layout(object, axes=object)


def test_map_layout_not_axes_error():

    with figure_context() as f:
        with pytest.raises(TypeError, match="Expected axes or an array of axes"):
            set_map_layout(f)

    with pytest.raises(TypeError, match="Expected axes or an array of axes"):
        set_map_layout(object)


def test_map_layout_subfigures_error():

    with figure_context() as f:
        sf = f.subfigures(1, 1)
        axs = sf.subplots(1, 2)

        with pytest.raises(RuntimeError, match="matplotlib SubFigure not supported"):
            set_map_layout(f.axes)

        with pytest.raises(RuntimeError, match="matplotlib SubFigure not supported"):
            set_map_layout(axs)


def test_set_map_layout_default_width():
    with subplots_context() as (f, ax):
        set_map_layout(ax)

        width = f.get_size_inches()[0] * 2.54
        np.testing.assert_allclose(width, 17.0, rtol=get_rtol(f))


@pytest.mark.parametrize(
    "nrow_ncol", [{"nrow": None, "ncol": None}, {"nrow": 1, "ncol": 1}]
)
def test_set_map_layout_no_borders(nrow_ncol):
    # width:height = 1:1
    with subplots_context() as (f, ax):
        ax.set_aspect("equal")
        ax.set(xlim=(0, 1), ylim=(0, 1))
        f.subplots_adjust(left=0, bottom=0, right=1, top=1)
        set_map_layout(ax, 10, **nrow_ncol)

        width, height = f.get_size_inches() * 2.54
        np.testing.assert_allclose((width, height), (10, 10), rtol=get_rtol(f))

    # width:height = 2:1
    with subplots_context() as (f, ax):
        ax.set_aspect("equal")
        ax.set(xlim=(0, 2), ylim=(0, 1))
        f.subplots_adjust(left=0, bottom=0, right=1, top=1)
        set_map_layout(ax, 10, **nrow_ncol)

        width, height = f.get_size_inches() * 2.54
        np.testing.assert_allclose((width, height), (10, 5), rtol=get_rtol(f))

    # width:height = 1:2
    with subplots_context() as (f, ax):
        ax.set_aspect("equal")
        ax.set(xlim=(0, 1), ylim=(0, 2))
        f.subplots_adjust(left=0, bottom=0, right=1, top=1)
        set_map_layout(ax, 10, **nrow_ncol)

        width, height = f.get_size_inches() * 2.54
        np.testing.assert_allclose((width, height), (10, 20), rtol=get_rtol(f))


@pytest.mark.parametrize("ax_to_arr", (lambda ax: [ax], lambda ax: np.array(ax)))
def test_set_map_layout_ax_arr(ax_to_arr):
    # width:height = 1:1
    with subplots_context() as (f, ax):
        ax.set_aspect("equal")
        ax.set(xlim=(0, 1), ylim=(0, 1))
        f.subplots_adjust(left=0, bottom=0, right=1, top=1)
        set_map_layout(ax_to_arr(ax), 10)

        width, height = f.get_size_inches() * 2.54
        np.testing.assert_allclose((width, height), (10, 10), rtol=get_rtol(f))


def test_set_map_layout_vert_borders():
    # width:height = 1:1
    with subplots_context() as (f, ax):
        ax.set_aspect("equal")
        ax.set(xlim=(0, 1), ylim=(0, 1))

        f.subplots_adjust(left=0, bottom=0.5, right=1, top=1)

        set_map_layout(ax, 10)

        width, height = f.get_size_inches() * 2.54
        np.testing.assert_allclose((width, height), (10, 20), rtol=get_rtol(f))

    # width:height = 1:1
    with subplots_context() as (f, ax):
        ax.set_aspect("equal")
        ax.set(xlim=(0, 1), ylim=(0, 1))

        f.subplots_adjust(left=0, bottom=0.0, right=1, top=0.8)

        set_map_layout(ax, 10)

        width, height = f.get_size_inches() * 2.54
        np.testing.assert_allclose((width, height), (10, 12.5), rtol=get_rtol(f))

    # width:height = 1:1
    with subplots_context() as (f, ax):
        ax.set_aspect("equal")
        ax.set(xlim=(0, 1), ylim=(0, 1))

        f.subplots_adjust(left=0, bottom=0.5, right=1, top=0.75)

        set_map_layout(ax, 10)

        width, height = f.get_size_inches() * 2.54
        np.testing.assert_allclose((width, height), (10, 40), rtol=get_rtol(f))


def test_set_map_layout_horz_borders():
    # width:height = 1:1
    with subplots_context() as (f, ax):
        ax.set_aspect("equal")
        ax.set(xlim=(0, 1), ylim=(0, 1))

        f.subplots_adjust(left=0.5, bottom=0.0, right=1, top=1)

        set_map_layout(ax, 10)

        width, height = f.get_size_inches() * 2.54
        np.testing.assert_allclose((width, height), (10, 5), rtol=get_rtol(f))

    # width:height = 1:1
    with subplots_context() as (f, ax):
        ax.set_aspect("equal")
        ax.set(xlim=(0, 1), ylim=(0, 1))

        f.subplots_adjust(left=0.25, bottom=0.0, right=0.75, top=1)

        set_map_layout(ax, 10)

        width, height = f.get_size_inches() * 2.54
        np.testing.assert_allclose((width, height), (10, 5), rtol=get_rtol(f))


def test_set_map_layout_two_axes_vert():
    # width:height = 1:1
    with subplots_context(2, 1) as (f, axs):
        for ax in axs:
            ax.set_aspect("equal")
            ax.set(xlim=(0, 1), ylim=(0, 1))

        f.subplots_adjust(left=0, bottom=0, right=1, top=1, hspace=0)

        set_map_layout(ax, 10)

        width, height = f.get_size_inches() * 2.54
        np.testing.assert_allclose((width, height), (10, 20), rtol=get_rtol(f))

    # width:height = 1:1
    with subplots_context(2, 1) as (f, axs):
        for ax in axs:
            ax.set_aspect("equal")
            ax.set(xlim=(0, 1), ylim=(0, 1))

        f.subplots_adjust(left=0, bottom=0, right=1, top=1, hspace=1)

        set_map_layout(ax, 10)

        width, height = f.get_size_inches() * 2.54
        np.testing.assert_allclose((width, height), (10, 30), rtol=get_rtol(f))


def test_set_map_layout_two_axes_horz():
    # width:height = 1:1
    with subplots_context(1, 2) as (f, axs):
        for ax in axs:
            ax.set_aspect("equal")
            ax.set(xlim=(0, 1), ylim=(0, 1))

        f.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0)

        set_map_layout(ax, 10)

        width, height = f.get_size_inches() * 2.54
        np.testing.assert_allclose((width, height), (10, 5), rtol=get_rtol(f))

    # width:height = 1:1
    with subplots_context(1, 2) as (f, axs):
        for ax in axs:
            ax.set_aspect("equal")
            ax.set(xlim=(0, 1), ylim=(0, 1))

        f.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=1)

        set_map_layout(ax, 10)

        width, height = f.get_size_inches() * 2.54
        np.testing.assert_allclose((width, height), (10, 10 / 3), rtol=get_rtol(f))


def test_set_map_layout_nrow_ncol_only_one_raises():
    with pytest.raises(ValueError, match="Must set none or both of 'nrow' and 'ncol'"):
        set_map_layout(object, width=17.0, nrow=1, ncol=None)

    with pytest.raises(ValueError, match="Must set none or both of 'nrow' and 'ncol'"):
        set_map_layout(object, width=17.0, nrow=None, ncol=1)


def test_set_map_layout_cartopy_2_2():
    import cartopy.crs as ccrs

    subplot_kw = {"projection": ccrs.PlateCarree()}
    with subplots_context(2, 2, subplot_kw=subplot_kw) as (f, axs):
        f.subplots_adjust(hspace=0, wspace=0, top=1, bottom=0, left=0, right=1)

        set_map_layout(axs, width=17)  # width is in cm

        result = f.get_size_inches() * 2.54
        expected = (17, 8.5)

        np.testing.assert_allclose(result, expected, rtol=get_rtol(f))


@pytest.mark.skipif(plt.get_backend().lower() != "macosx", reason="only for macosx")
@pytest.mark.parametrize("dpi", (100, 1000))
@pytest.mark.parametrize("size", ([17, 6], [10, 5]))
def test_set_size_inches_macosx(dpi, size):

    with figure_context() as f:

        f.set_dpi(dpi)

        size = np.array(size)

        f.set_size_inches(size / 2.54)

        result = f.get_size_inches() * 2.54

        expected_size = np.floor(size / 2.54 * dpi) / dpi * 2.54
        np.testing.assert_allclose(result, expected_size)
