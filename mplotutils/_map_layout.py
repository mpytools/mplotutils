import warnings

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1 import AxesGrid

from mplotutils._deprecate import _deprecate_positional_args
from mplotutils._mpl import _get_renderer


@_deprecate_positional_args("0.3")
def set_map_layout(obj=None, width=17.0, *, nrow=None, ncol=None, axes=None):
    """set figure height, given width, taking axes' aspect ratio into account

    Needs to be called after all plotting is done.

    Parameters
    ----------
    obj : (Geo)Axes | iterable of (Geo)Axes | AxesGrid
        Array with all axes of the figure or mpl_toolkits.axes_grid1 AxesGrid.
    width : float, default: 17
        Width of the full figure in cm.
    nrow : integer, default: None
        manually set the number of rows of subplots. Good when using gridspec.
        However, subplots must span the same number of gridspec rows & columns.
        Either none or both of 'nrow' and 'ncol' must be set.
    ncol : integer, default: None
        As nrow but for the number of rows.

    Notes
    -----
    Only works if all the axes have the same aspect ratio.
    """

    if axes is not None and obj is not None:
        raise TypeError("Cannot pass 'obj' and 'axes'")

    if axes is not None:
        warnings.warn("The 'axes' keyword has been renamed to 'obj'", FutureWarning)
        obj = axes

    if obj is None:
        raise TypeError(
            "set_map_layout() missing 1 required positional argument: 'obj'"
        )

    if isinstance(obj, AxesGrid):
        _set_map_layout_axes_grid(obj, width, nrow, ncol)
    else:
        _set_map_layout_axes(obj, width, nrow, ncol)


def _set_map_layout_axes(axs, width, nrow, ncol):

    if (nrow is None and ncol is not None) or (nrow is not None and ncol is None):
        raise ValueError("Must set none or both of 'nrow' and 'ncol'")

    # assumes the first of the axes is representative for all
    ax = np.asarray(axs).flat[0]

    if not isinstance(ax, plt.Axes):
        raise TypeError(f"Expected axes or an array of axes, got {type(ax)}")

    # read figure data
    f = ax.get_figure()

    if isinstance(f, mpl.figure.SubFigure) or f.subfigs:
        raise RuntimeError("matplotlib SubFigure not supported")

    # getting the correct data ratio of geoaxes requires draw
    f.canvas.draw()

    bottom = f.subplotpars.bottom
    top = f.subplotpars.top
    left = f.subplotpars.left
    right = f.subplotpars.right
    hspace = f.subplotpars.hspace
    wspace = f.subplotpars.wspace

    # data ratio is the aspect
    aspect = ax.get_data_ratio()

    if nrow is None and ncol is None:
        # get geometry tells how many subplots there are
        nrow, ncol, __, __ = ax.get_subplotspec().get_geometry()

    # width of one plot, taking into account
    # left * wf, (1-right) * wf, ncol * wp, (1-ncol) * wp * wspace
    wp = (width - width * (left + (1 - right))) / (ncol + (ncol - 1) * wspace)

    # height of one plot
    hp = wp * aspect

    # height of figure
    height = (hp * (nrow + ((nrow - 1) * hspace))) / (1.0 - (bottom + (1 - top)))

    f.set_figwidth(width / 2.54)
    f.set_figheight(height / 2.54)


def _set_map_layout_axes_grid(axgr, width, nrow, ncol):

    if nrow is not None or ncol is not None:
        raise TypeError("Cannot pass 'nrow' or 'ncol' for and 'AxesGrid'")

        # assumes the first of the axes is representative for all
    ax = axgr.axes_all[0]

    f = ax.get_figure()

    # getting the correct data ratio of geoaxes requires draw
    f.canvas.draw()

    bottom = f.subplotpars.bottom
    top = f.subplotpars.top
    left = f.subplotpars.left
    right = f.subplotpars.right

    width_fraction = right - left
    height_fraction = top - bottom

    inner_width = width_fraction * width

    renderer = _get_renderer(f)

    # divider get_*_sizes contains the relative and absolute sizes of all plot elements
    # (subplots, colorbars, pad & colorbar pad)

    divider = axgr.get_divider()

    vertical_sizes = divider.get_vertical_sizes(renderer)
    vs_rel = vertical_sizes[:, 0].sum()
    vs_abs = vertical_sizes[:, 1].sum() * 2.54

    horizontal_sizes = divider.get_horizontal_sizes(renderer)
    hs_rel = horizontal_sizes[:, 0].sum()
    hs_abs = horizontal_sizes[:, 1].sum() * 2.54

    inner_height = (inner_width - hs_abs) / hs_rel * vs_rel + vs_abs

    if inner_height <= 0:
        raise ValueError("Not enough space on figure")

    height = inner_height / height_fraction

    f.set_size_inches(width / 2.54, height / 2.54)
