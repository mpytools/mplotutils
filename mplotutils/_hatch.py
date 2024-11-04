import warnings

import cartopy.crs as ccrs
import matplotlib as mpl
import numpy as np
import xarray as xr
from packaging.version import Version

import mplotutils as mpu

_HATCHES_PER_FIGURE = {}


from mplotutils._mpl import _maybe_gca

MPL_GE_310 = Version(Version(mpl.__version__).base_version) >= Version("3.10")


def hatch(da, hatch, *, ax=None, label=None, linewidth=None, color="0.1"):
    """add hatch pattern to an axes

    Parameters
    ----------
    da : xr.DataArray
        DataArray with the hatch information, must be boolean 2D array. Data of value
        `True` is hatched.
    hatch : str
        Hatch pattern, one of: '/', '\\', '|', '-', '+', 'x', 'o', 'O', '.', '*'.
        Hatching patterns can be repeated to increase the density.
    ax : matplotlib.axes, default: None
        Axes to draw the hatch on. If not given, uses the current axes or creates new
        axes.
    label : str
        label for a legend entry
    linewidth : float, default: 0.25
        Default thickness of the hatching. Note that only one linewidth per figure is
        supported (by matplotlib).
    color : matplotlib color, default: "0.1"
        Color of the hatch lines.

    Returns
    -------
    `~.contour.QuadContourSet`

    Notes
    -----
    Don't use this function to hatch levels of a contour plot - it's better to add
    hatches directly to `countourf`.
    """

    return _hatch(
        da,
        hatch,
        ax=ax,
        label=label,
        linewidth=linewidth,
        color=color,
        cyclic=False,
        transform=None,
    )


def hatch_map(
    da, hatch, *, ax=None, label=None, linewidth=None, color="0.1", transform=None
):
    """add hatch pattern to a regional cartopy map

    Parameters
    ----------
    da : xr.DataArray
        DataArray with the hatch information, must be boolean 2D array. Data of value
        `True` is hatched.
    hatch : str
        Hatch pattern, one of: '/', '\\', '|', '-', '+', 'x', 'o', 'O', '.', '*'.
        Hatching patterns can be repeated to increase the density.
    ax : matplotlib.axes, default: None
        Axes to draw the hatch on. If not given, uses the current axes or creates new
        axes.
    label : str
        label for a legend entry
    linewidth : float, default: 0.25
        Default thickness of the hatching. Note that only one linewidth per figure is
        supported (by matplotlib).
    color : matplotlib color, default: "0.1"
        Color of the hatch lines.
    transform : cartopy projection, optional
        Defines the transformation of the data. If None uses 'PlateCarree'.

    Returns
    -------
    `~.contour.QuadContourSet`

    Notes
    -----
    Don't use this function to hatch levels of a contour plot - it's better to add
    hatches directly to `countourf`.
    """

    if transform is None:
        transform = ccrs.PlateCarree()

    return _hatch(
        da,
        hatch,
        ax=ax,
        label=label,
        linewidth=linewidth,
        color=color,
        cyclic=False,
        transform=transform,
    )


def hatch_map_global(
    da, hatch, *, ax=None, label=None, linewidth=None, color="0.1", transform=None
):
    """add hatch pattern to a global cartopy map - adds a cyclic data point

    Parameters
    ----------
    da : xr.DataArray
        DataArray with the hatch information, must be boolean 2D array. Data of value
        `True` is hatched.
    hatch : str
        Hatch pattern, one of: '/', '\\', '|', '-', '+', 'x', 'o', 'O', '.', '*'.
        Hatching patterns can be repeated to increase the density.
    ax : matplotlib.axes, default: None
        Axes to draw the hatch on. If not given, uses the current axes or creates new
        axes.
    label : str
        label for a legend entry
    linewidth : float, default: 0.25
        Default thickness of the hatching. Note that only one linewidth per figure is
        supported (by matplotlib).
    color : matplotlib color, default: "0.1"
        Color of the hatch lines.
    transform : cartopy projection, optional
        Defines the transformation of the data. If None uses 'PlateCarree'.

    Returns
    -------
    `~.contour.QuadContourSet`

    Notes
    -----
    Don't use this function to hatch levels of a contour plot - it's better to add
    hatches directly to `countourf`.
    """

    if transform is None:
        transform = ccrs.PlateCarree()

    return _hatch(
        da,
        hatch,
        ax=ax,
        label=label,
        linewidth=linewidth,
        color=color,
        cyclic=True,
        transform=transform,
    )


def _hatch(
    da,
    hatch,
    *,
    ax=None,
    label=None,
    linewidth=None,
    color="0.1",
    cyclic=False,
    transform=None,
):

    if not isinstance(da, xr.DataArray):
        raise TypeError(f"Expected a xr.DataArray, got {type(da)}.")

    if not np.issubdtype(da.dtype, bool):
        raise TypeError(f"Expected a boolean array, got {da.dtype}")

    if da.ndim != 2:
        raise ValueError(f"Expected a 2D array, got {da.ndim=}")

    if ax is None:
        ax = _maybe_gca()

    fig = ax.figure

    if not MPL_GE_310:
        # only one linewidth is possible per figure (actually it is just read before
        # saving the figure, so the above is not 100 % correct)
        if linewidth is None:
            # only set linewidth if not yet set
            if not _HATCHES_PER_FIGURE.get(fig):
                mpl.rcParams["hatch.linewidth"] = 0.25
        else:
            if _HATCHES_PER_FIGURE.get(fig):
                warnings.warn(
                    "Setting more than one hatch `linewidth` per figure requires"
                    " matplotlib v3.10 or later Overwriting previous value of"
                    f" {_HATCHES_PER_FIGURE[fig]}."
                )

            mpl.rcParams["hatch.linewidth"] = linewidth

            _HATCHES_PER_FIGURE[fig] = linewidth
    else:
        if linewidth is None:
            mpl.rcParams["hatch.linewidth"] = 0.25
        else:
            mpl.rcParams["hatch.linewidth"] = linewidth

    mpl.rcParams["hatch.color"] = color

    if label is not None:
        # add an empty patch to generate a legend entry
        xy = np.full((0, 2), fill_value=np.nan)
        empty_legend_patch = mpl.patches.Polygon(
            xy,
            facecolor="none",
            ec="0.1",
            hatch=hatch,
            label=label,
        )

        # NOTE: manually overwrites the private _hatch_color property - allows to have
        # different ec and hatch color (so the box of the legend is black)
        empty_legend_patch._hatch_color = mpl.colors.to_rgba(
            mpl.rcParams["hatch.color"]
        )
        ax.add_patch(empty_legend_patch)

    if cyclic:
        _, lon_dim = da.dims
        da = mpu.cyclic_dataarray(da, lon_dim)

    return da.plot.contourf(
        ax=ax,
        hatches=["", hatch],
        levels=[0, 0.5, 1],
        colors="none",
        extend="neither",
        transform=transform,
        add_colorbar=False,
    )
