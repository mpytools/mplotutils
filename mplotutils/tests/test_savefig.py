import io

import matplotlib.pyplot as plt
import pytest

import mplotutils as mpu
from mplotutils.tests.test_colorbar import create_fig_aspect

from . import figure_context


def test_autodraw_orig_func():

    # NOTE plt.Figure.savefig is the overwritten one
    assert mpu._savefig.savefig_orig is not plt.Figure.savefig

    with mpu.autodraw(False):
        assert mpu._savefig.savefig_orig is plt.Figure.savefig

    with mpu.autodraw(False):
        with mpu.autodraw(True):
            assert mpu._savefig.savefig_orig is not plt.Figure.savefig

    with mpu.autodraw(False):
        savefig_autodraw = plt.Figure.savefig

    with mpu.autodraw(True):
        savefig_no_autodraw = plt.Figure.savefig

    assert savefig_no_autodraw is not savefig_autodraw

    mpu.autodraw(True)
    assert mpu._savefig.savefig_orig is not plt.Figure.savefig

    mpu.autodraw(False)
    assert mpu._savefig.savefig_orig is plt.Figure.savefig

    # restore to default
    mpu.autodraw(True)


def test_ensure_draw_method_called(monkeypatch):
    # this is a pseudo-mock test (I think the actual backend would need to be mocked)

    class DrawMethodCalled(Exception):
        pass

    def draw():
        raise DrawMethodCalled()

    with figure_context() as f:

        monkeypatch.setattr(f.canvas, "draw", draw)

        # not called when not autodrawing
        with mpu.autodraw(False):
            f.savefig(io.BytesIO())

        # called when autodrawing
        with pytest.raises(DrawMethodCalled):
            f.savefig(io.BytesIO())


def test_saved_figure_not_the_same_vertical():

    with figure_context() as f:
        create_fig_aspect(aspect=0.5, orientation="vertical")

        file_no_autodraw = io.BytesIO()

        with mpu.autodraw(False):
            f.savefig(file_no_autodraw)

        file_autodraw = io.BytesIO()
        with mpu.autodraw(True):
            f.savefig(file_autodraw)

        assert file_no_autodraw.getvalue() != file_autodraw.getvalue()


def test_saved_figure_not_the_same_horizontal():

    with figure_context() as f:
        create_fig_aspect(aspect=2, orientation="horizontal")
        # ensure the colorbar is actually on the figure
        f.subplots_adjust(bottom=0.5)

        file_no_autodraw = io.BytesIO()
        with mpu.autodraw(False):
            f.savefig(file_no_autodraw)

        file_autodraw = io.BytesIO()
        with mpu.autodraw(True):
            f.savefig(file_autodraw)

        assert file_no_autodraw.getvalue() != file_autodraw.getvalue()
