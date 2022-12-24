import numpy as np
import pytest

from mplotutils import set_map_layout

from . import subplots_context


def test_default_width():

    with subplots_context() as (f, ax):
        set_map_layout(ax)

        assert f.get_size_inches()[0] * 2.54 == 17.0


@pytest.mark.parametrize(
    "nrow_ncol", [{"nrow": None, "ncol": None}, {"nrow": 1, "ncol": 1}]
)
def test_no_borders(nrow_ncol):

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


def test_vert_borders():

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


def test_horz_borders():

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


def test_nrow_ncol_only_one_raises():

    with pytest.raises(ValueError, match="Must set none or both of 'nrow' and 'ncol'"):
        set_map_layout(None, width=17.0, nrow=1, ncol=None)

    with pytest.raises(ValueError, match="Must set none or both of 'nrow' and 'ncol'"):
        set_map_layout(None, width=17.0, nrow=None, ncol=1)
