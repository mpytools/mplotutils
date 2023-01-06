import matplotlib.pyplot as plt
import numpy as np


def set_map_layout(axes, width=17.0, nrow=None, ncol=None):
    """set figure height, given width, taking axes' aspect ratio into account

    Needs to be called after all plotting is done.

    Parameters
    ----------
    axes : (Geo)Axes | iterable of (Geo)Axes
        Array with all axes of the figure.
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

    if (nrow is None and ncol is not None) or (nrow is not None and ncol is None):
        raise ValueError("Must set none or both of 'nrow' and 'ncol'")

    if isinstance(axes, plt.Axes):
        ax = axes
    else:
        # assumes the first of the axes is representative for all
        ax = np.asarray(axes).flat[0]

    # read figure data
    f = ax.get_figure()

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
