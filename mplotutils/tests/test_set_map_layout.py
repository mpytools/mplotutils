import numpy as np
import pytest

from mplotutils import set_map_layout

from . import subplots_context


def test_set_map_layout_default_width():
    with subplots_context() as (f, ax):
        set_map_layout(ax)

        assert f.get_size_inches()[0] * 2.54 == 17.0


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
        assert np.allclose((width, height), (10, 10))

    # width:height = 2:1
    with subplots_context() as (f, ax):
        ax.set_aspect("equal")
        ax.set(xlim=(0, 2), ylim=(0, 1))
        f.subplots_adjust(left=0, bottom=0, right=1, top=1)
        set_map_layout(ax, 10, **nrow_ncol)

        width, height = f.get_size_inches() * 2.54
        assert np.allclose((width, height), (10, 5))

    # width:height = 1:2
    with subplots_context() as (f, ax):
        ax.set_aspect("equal")
        ax.set(xlim=(0, 1), ylim=(0, 2))
        f.subplots_adjust(left=0, bottom=0, right=1, top=1)
        set_map_layout(ax, 10, **nrow_ncol)

        width, height = f.get_size_inches() * 2.54
        assert np.allclose((width, height), (10, 20))


@pytest.mark.parametrize("ax_to_arr", (lambda ax: [ax], lambda ax: np.array(ax)))
def test_set_map_layout_ax_arr(ax_to_arr):
    # width:height = 1:1
    with subplots_context() as (f, ax):
        ax.set_aspect("equal")
        ax.set(xlim=(0, 1), ylim=(0, 1))
        f.subplots_adjust(left=0, bottom=0, right=1, top=1)
        set_map_layout(ax_to_arr(ax), 10)

        width, height = f.get_size_inches() * 2.54
        assert np.allclose((width, height), (10, 10))


def test_set_map_layout_vert_borders():
    # width:height = 1:1
    with subplots_context() as (f, ax):
        ax.set_aspect("equal")
        ax.set(xlim=(0, 1), ylim=(0, 1))

        f.subplots_adjust(left=0, bottom=0.5, right=1, top=1)

        set_map_layout(ax, 10)

        width, height = f.get_size_inches() * 2.54
        assert np.allclose((width, height), (10, 20))

    # width:height = 1:1
    with subplots_context() as (f, ax):
        ax.set_aspect("equal")
        ax.set(xlim=(0, 1), ylim=(0, 1))

        f.subplots_adjust(left=0, bottom=0.0, right=1, top=0.8)

        set_map_layout(ax, 10)

        width, height = f.get_size_inches() * 2.54
        assert np.allclose((width, height), (10, 12.5))

    # width:height = 1:1
    with subplots_context() as (f, ax):
        ax.set_aspect("equal")
        ax.set(xlim=(0, 1), ylim=(0, 1))

        f.subplots_adjust(left=0, bottom=0.5, right=1, top=0.75)

        set_map_layout(ax, 10)

        width, height = f.get_size_inches() * 2.54
        assert np.allclose((width, height), (10, 40))


def test_set_map_layout_horz_borders():
    # width:height = 1:1
    with subplots_context() as (f, ax):
        ax.set_aspect("equal")
        ax.set(xlim=(0, 1), ylim=(0, 1))

        f.subplots_adjust(left=0.5, bottom=0.0, right=1, top=1)

        set_map_layout(ax, 10)

        width, height = f.get_size_inches() * 2.54
        assert np.allclose((width, height), (10, 5))

    # width:height = 1:1
    with subplots_context() as (f, ax):
        ax.set_aspect("equal")
        ax.set(xlim=(0, 1), ylim=(0, 1))

        f.subplots_adjust(left=0.25, bottom=0.0, right=0.75, top=1)

        set_map_layout(ax, 10)

        width, height = f.get_size_inches() * 2.54
        assert np.allclose((width, height), (10, 5))


def test_set_map_layout_two_axes_vert():
    # width:height = 1:1
    with subplots_context(2, 1) as (f, axs):
        for ax in axs:
            ax.set_aspect("equal")
            ax.set(xlim=(0, 1), ylim=(0, 1))

        f.subplots_adjust(left=0, bottom=0, right=1, top=1, hspace=0)

        set_map_layout(ax, 10)

        width, height = f.get_size_inches() * 2.54
        assert np.allclose((width, height), (10, 20))

    # width:height = 1:1
    with subplots_context(2, 1) as (f, axs):
        for ax in axs:
            ax.set_aspect("equal")
            ax.set(xlim=(0, 1), ylim=(0, 1))

        f.subplots_adjust(left=0, bottom=0, right=1, top=1, hspace=1)

        set_map_layout(ax, 10)

        width, height = f.get_size_inches() * 2.54
        assert np.allclose((width, height), (10, 30))


def test_set_map_layout_two_axes_horz():
    # width:height = 1:1
    with subplots_context(1, 2) as (f, axs):
        for ax in axs:
            ax.set_aspect("equal")
            ax.set(xlim=(0, 1), ylim=(0, 1))

        f.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0)

        set_map_layout(ax, 10)

        width, height = f.get_size_inches() * 2.54
        assert np.allclose((width, height), (10, 5))

    # width:height = 1:1
    with subplots_context(1, 2) as (f, axs):
        for ax in axs:
            ax.set_aspect("equal")
            ax.set(xlim=(0, 1), ylim=(0, 1))

        f.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=1)

        set_map_layout(ax, 10)

        width, height = f.get_size_inches() * 2.54
        assert np.allclose((width, height), (10, 10 / 3))


def test_set_map_layout_nrow_ncol_only_one_raises():
    with pytest.raises(ValueError, match="Must set none or both of 'nrow' and 'ncol'"):
        set_map_layout(None, width=17.0, nrow=1, ncol=None)

    with pytest.raises(ValueError, match="Must set none or both of 'nrow' and 'ncol'"):
        set_map_layout(None, width=17.0, nrow=None, ncol=1)


def test_set_map_layout_cartopy_2_2():
    import cartopy.crs as ccrs

    subplot_kw = {"projection": ccrs.PlateCarree()}
    with subplots_context(2, 2, subplot_kw=subplot_kw) as (f, axs):
        f.subplots_adjust(hspace=0, wspace=0, top=1, bottom=0, left=0, right=1)

        set_map_layout(axs, width=17)  # width is in cm

        result = f.get_size_inches() * 2.54
        expected = (17, 8.5)

        np.testing.assert_allclose(result, expected)
