import itertools

import matplotlib as mpl
import numpy as np
from matplotlib.colors import from_levels_and_colors


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

    Notes
    -----
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


def _color_palette(cmap, n_colors):
    # _color_palette is adapted from xarray:
    # https://github.com/pydata/xarray/blob/v0.10.2/xarray/plot/utils.py#L110
    # Used under the terms of xarrays's license, see licenses/XARRAY_LICENSE.

    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap

    colors_i = np.linspace(0, 1.0, n_colors)
    if isinstance(cmap, (list, tuple)):
        # expand or truncate the list of colors to n_colors
        cmap = list(itertools.islice(itertools.cycle(cmap), n_colors))
        cmap = ListedColormap(cmap)
        pal = cmap(colors_i)
    elif isinstance(cmap, str):
        # we have some sort of named palette
        try:
            # is this a matplotlib cmap?
            cmap = plt.get_cmap(cmap)
            pal = cmap(colors_i)
        except ValueError:
            # ValueError happens when mpl doesn't like a colormap, try seaborn
            try:
                from seaborn import color_palette

                pal = color_palette(cmap, n_colors=n_colors)
            except (ValueError, ImportError):
                # or maybe we just got a single color as a string
                cmap = ListedColormap([cmap] * n_colors)
                pal = cmap(colors_i)
    else:
        # cmap better be a LinearSegmentedColormap (e.g. viridis)
        pal = cmap(colors_i)

    return pal


def _get_label_attr(labelpad, size, weight):
    if labelpad is None:
        labelpad = mpl.rcParams["axes.labelpad"]

    if size is None:
        size = mpl.rcParams["axes.labelsize"]

    if weight is None:
        weight = mpl.rcParams["axes.labelweight"]

    return labelpad, size, weight
