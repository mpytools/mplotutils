import cartopy.crs as ccrs
import matplotlib as mpl
import numpy as np
import xarray as xr

import mplotutils as mpu


def hatch(ax, da, hatch, label=None, linewidth=0.25, color="0.1"):
    """add hatch pattern to a cartopy map

    Parameters
    ----------
    ax : matplotlib.axes
        Axes to draw the hatch on.
    da : xr.DataArray
        DataArray with the hatch information. Data of value `True` is hatched.
    hatch : str
        Hatch pattern.
    label : str
        label for a legend entry
    linewidth : float, default: 0.25
        Default thickness of the hatching.
    color : matplotlib color, default: "0.1"
        Color of the hatch lines.
    """

    _hatch(
        ax,
        da,
        hatch,
        label=label,
        linewidth=linewidth,
        color=color,
        cyclic=False,
        transform=ax.transData,
    )


def hatch_regional_map(
    ax, da, hatch, label=None, linewidth=0.25, color="0.1", transform=None
):
    """add hatch pattern to a regional cartopy map

    Parameters
    ----------
    ax : matplotlib.axes
        Axes to draw the hatch on.
    da : xr.DataArray
        DataArray with the hatch information. Data of value `True` is hatched.
    hatch : str
        Hatch pattern.
    label : str
        label for a legend entry
    linewidth : float, default: 0.25
        Default thickness of the hatching.
    color : matplotlib color, default: "0.1"
        Color of the hatch lines.

    """

    if transform is None:
        transform = ccrs.PlateCarree()

    _hatch(
        ax,
        da,
        hatch,
        label=label,
        linewidth=linewidth,
        color=color,
        cyclic=False,
        transform=transform,
    )


def hatch_global_map(
    ax, da, hatch, label=None, linewidth=0.25, color="0.1", transform=None
):
    """add hatch pattern to a global cartopy map

    Parameters
    ----------
    ax : matplotlib.axes
        Axes to draw the hatch on.
    da : xr.DataArray
        DataArray with the hatch information. Data of value `True` is hatched.
    hatch : str
        Hatch pattern.
    label : str
        label for a legend entry
    linewidth : float, default: 0.25
        Default thickness of the hatching.
    color : matplotlib color, default: "0.1"
        Color of the hatch lines.

    """

    if transform is None:
        transform = ccrs.PlateCarree()

    _hatch(
        ax,
        da,
        hatch,
        label=label,
        linewidth=linewidth,
        color=color,
        cyclic=True,
        transform=transform,
    )


def _hatch(
    ax, da, hatch, label=None, linewidth=0.25, color="0.1", cyclic=False, transform=None
):

    if not isinstance(da, xr.DataArray):
        raise TypeError(f"Expected a xr.DataArray, got {type(da)}.")

    if not np.issubdtype(da.dtype, bool):
        raise TypeError(f"Expected a boolean array, got {da.dtype}")

    if da.ndim != 2:
        raise ValueError(f"Expected a 2D array, got {da.ndim=}")

    if label is not None:
        # add an empty patch to generate a legend entry
        xy = np.full((0, 2), fill_value=np.nan)
        empty_legend_patch = mpl.patches.Polygon(
            xy,
            facecolor="none",
            ec=color,
            lw=linewidth,
            hatch=hatch,
            label=label,
        )
        ax.add_patch(empty_legend_patch)

    # contourf has trouble if no gridcell is True
    # if da.sum() == 0:
    #     return legend_handle

    if cyclic:
        _, lon_dim = da.dims
        da = mpu.cyclic_dataarray(da, lon_dim)

    # plot "True"
    levels = [0.95, 1.05]
    hatches = [hatch, ""]

    # TODO: check if values changed from non-default
    mpl.rcParams["hatch.linewidth"] = linewidth
    mpl.rcParams["hatch.color"] = color

    # unfortunately cannot set hatch options via context manager
    # with mpl.rc_context({"hatch.linewidth": linewidth, "hatch.color": color}):
    da.plot.contourf(
        ax=ax,
        levels=levels,
        hatches=hatches,
        colors="none",
        extend="neither",
        transform=transform,
        add_colorbar=False,
    )

    # return legend_handle
