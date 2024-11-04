import matplotlib as mpl
import matplotlib.pyplot as plt

from mplotutils._mpl import _maybe_gca

from . import figure_context


def test_maybe_gca():

    with figure_context():
        ax = _maybe_gca(aspect=1)

        assert isinstance(ax, mpl.axes.Axes)
        assert ax.get_aspect() == 1

    with figure_context():
        ax = _maybe_gca(aspect=1)

        assert isinstance(ax, mpl.axes.Axes)
        assert ax.get_aspect() == 1

    with figure_context():
        existing_axes = plt.axes()
        ax = _maybe_gca(aspect=1)

        # re-uses the existing axes
        assert existing_axes == ax
        # kwargs are ignored when reusing axes
        assert ax.get_aspect() == "auto"
