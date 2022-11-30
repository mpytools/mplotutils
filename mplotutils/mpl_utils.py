import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import six
from matplotlib.colors import from_levels_and_colors

# =============================================================================


def from_levels_and_cmap(levels, cmap, extend="neither"):
    """
    create mpl colormap from levels and the name of the colorbar

    Parameters
    ----------
    levels : sequence of numbers
        The quantization levels used to construct the :class:`BoundaryNorm`.
        Values ``v`` are quantizized to level ``i`` if
        ``lev[i] <= v < lev[i+1]``.
    cmap : string
        Valid colormap identifier.
    extend : {'neither', 'min', 'max', 'both'}, optional
        The behaviour when a value falls out of range of the given levels.
        See :func:`~matplotlib.pyplot.contourf` for details.

    ..note::
      Adapted from xarray.

    """
    if np.isscalar(levels):
        raise ValueError("'levels' must be a list of levels")

    if extend == "both":
        ext_n = 2
    elif extend in ["min", "max"]:
        ext_n = 1
    else:
        ext_n = 0

    # subtract 1 because there is one less level than numbers
    n_colors = len(levels) + ext_n - 1

    pal = _color_palette(cmap, n_colors)

    cmap, norm = from_levels_and_colors(levels, pal, extend=extend)

    return cmap, norm


# -----------------------------------------------------------------------------

# _color_palette is adapted from xarray:
# https://github.com/pydata/xarray/blob/v0.10.2/xarray/plot/utils.py#L110
# Used under the terms of xarrays's license, see licenses/XARRAY_LICENSE.


def _color_palette(cmap, n_colors):
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap

    colors_i = np.linspace(0, 1.0, n_colors)
    if isinstance(cmap, (list, tuple)):
        # we have a list of colors
        cmap = ListedColormap(cmap, N=n_colors)
        pal = cmap(colors_i)
    elif isinstance(cmap, six.string_types):
        # we have some sort of named palette
        try:
            # is this a matplotlib cmap?
            cmap = plt.get_cmap(cmap)
            pal = cmap(colors_i)
        except ValueError:
            # ValueError happens when mpl doesn't like a colormap, try seaborn
            try:
                from seaborn.apionly import color_palette

                pal = color_palette(cmap, n_colors=n_colors)
            except (ValueError, ImportError):
                # or maybe we just got a single color as a string
                cmap = ListedColormap([cmap], N=n_colors)
                pal = cmap(colors_i)
    else:
        # cmap better be a LinearSegmentedColormap (e.g. viridis)
        pal = cmap(colors_i)

    return pal


# =============================================================================


def set_map_layout(axes, width=17.0, nrow=None, ncol=None):
    """
    set figure height, given width

    Needs to be called after all plotting is done.

    Parameters
    ----------
    axes : ndarray of (Geo)Axes
        Array with all axes of the figure.
    width : float, default: 17
        Width of the full figure in cm.
    nrow : integer, default: None
        manually set the number of rows of subplots. Good when using gridspec.
        However, subplots must span the same number of gridspec rows & columns.
        Either none or both of 'nrow' and 'ncol' must be set.
    ncol : integer, default: None
        As nrow but for the number of rows.

    ..note: only works if all the axes have the same aspect ratio.
    """

    if (nrow is None and ncol is not None) or (nrow is not None and ncol is None):
        raise ValueError("Must set none or both of 'nrow' and 'ncol'")

    if isinstance(axes, plt.Axes):
        ax = axes
    else:
        # assumes the first of the axes is representative for all
        ax = axes.flat[0]

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


# =============================================================================


def _get_label_attr(labelpad, size, weight):

    if labelpad is None:
        labelpad = mpl.rcParams["axes.labelpad"]

    if size is None:
        size = mpl.rcParams["axes.labelsize"]

    if weight is None:
        weight = mpl.rcParams["axes.labelweight"]

    return labelpad, size, weight
