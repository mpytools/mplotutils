# code by M.Hauser

import cartopy.crs as ccrs
import cartopy.util as cutil
import matplotlib.pyplot as plt
import numpy as np
import shapely.geometry as sgeom
from cartopy.mpl.gridliner import LATITUDE_FORMATTER, LONGITUDE_FORMATTER

from .mpl_utils import _get_label_attr

# =============================================================================


def sample_data_map(nlons, nlats):
    """Returns `lons`, `lats`, and fake `data`

    adapted from:
    http://scitools.org.uk/cartopy/docs/v0.15/examples/axes_grid_basic.html
    """

    dlat = 180.0 / nlats / 2
    dlon = 360.0 / nlons

    lat = np.linspace(-90 + dlat, 90 - dlat, nlats)
    lon = np.linspace(0, 360 - dlon, nlons)

    lons, lats = np.meshgrid(np.deg2rad(lon), np.deg2rad(lat))
    wave = 0.75 * (np.sin(2 * lats) ** 8) * np.cos(4 * lons)
    mean = 0.5 * np.cos(2 * lats) * ((np.sin(2 * lats)) ** 2 + 2)
    data = wave + mean

    return lon, lat, data


# =============================================================================


# from xarray
def infer_interval_breaks(x, y, clip=False):
    """find edges of gridcells, given their centers"""

    if len(x.shape) == 1:
        x = _infer_interval_breaks(x)
        y = _infer_interval_breaks(y)
    else:
        # we have to infer the intervals on both axes
        x = _infer_interval_breaks(x, axis=1)
        x = _infer_interval_breaks(x, axis=0)
        y = _infer_interval_breaks(y, axis=1)
        y = _infer_interval_breaks(y, axis=0)

    if clip:
        y = np.clip(y, -90, 90)

    return x, y


# from xarray
def _infer_interval_breaks(coord, axis=0):
    """
    >>> _infer_interval_breaks(np.arange(5))
    array([-0.5,  0.5,  1.5,  2.5,  3.5,  4.5])
    >>> _infer_interval_breaks([[0, 1], [3, 4]], axis=1)
    array([[-0.5,  0.5,  1.5],
           [ 2.5,  3.5,  4.5]])
    """

    if not _is_monotonic(coord, axis=axis):
        raise ValueError(
            "The input coordinate is not sorted in increasing "
            "order along axis %d. This can lead to unexpected "
            "results. Consider calling the `sortby` method on "
            "the input DataArray. To plot data with categorical "
            "axes, consider using the `heatmap` function from "
            "the `seaborn` statistical plotting library." % axis
        )

    coord = np.asarray(coord)
    deltas = 0.5 * np.diff(coord, axis=axis)
    if deltas.size == 0:
        deltas = np.array(0.0)
    first = np.take(coord, [0], axis=axis) - np.take(deltas, [0], axis=axis)
    last = np.take(coord, [-1], axis=axis) + np.take(deltas, [-1], axis=axis)
    trim_last = tuple(
        slice(None, -1) if n == axis else slice(None) for n in range(coord.ndim)
    )
    return np.concatenate([first, coord[trim_last] + deltas, last], axis=axis)


# from xarray
def _is_monotonic(coord, axis=0):
    """
    >>> _is_monotonic(np.array([0, 1, 2]))
    True
    >>> _is_monotonic(np.array([2, 1, 0]))
    True
    >>> _is_monotonic(np.array([0, 2, 1]))
    False
    """
    coord = np.asarray(coord)

    if coord.shape[axis] < 3:
        return True
    else:
        n = coord.shape[axis]
        delta_pos = coord.take(np.arange(1, n), axis=axis) >= coord.take(
            np.arange(0, n - 1), axis=axis
        )
        delta_neg = coord.take(np.arange(1, n), axis=axis) <= coord.take(
            np.arange(0, n - 1), axis=axis
        )

    return np.all(delta_pos) or np.all(delta_neg)


# =============================================================================


def cyclic_dataarray(da, coord="lon"):
    """
    Add a cyclic coordinate point to a DataArray along a specified named dimension.

    >>> import xarray as xr
    >>> data = xr.DataArray([[1, 2, 3], [4, 5, 6]],
    ...                      coords={'x': [1, 2], 'y': range(3)},
    ...                      dims=['x', 'y'])
    >>> data_cyclic = cyclic_dataarray(data, 'y')
    >>> data_cyclic
    <xarray.DataArray (x: 2, y: 4)>
    array([[1, 2, 3, 1],
           [4, 5, 6, 4]])
    Coordinates:
      * x        (x) int64 1 2
      * y        (y) int64 0 1 2 3

    Notes
    -----
    After: https://github.com/darothen/plot-all-in-ncfile/blob/master/plot_util.py

    """
    import xarray as xr

    assert isinstance(da, xr.DataArray)

    lon_idx = da.dims.index(coord)
    cyclic_data, cyclic_coord = cutil.add_cyclic_point(
        da.values, coord=da.coords[coord], axis=lon_idx
    )

    # Copy and add the cyclic coordinate and data
    new_coords = dict(da.coords)
    new_coords[coord] = cyclic_coord
    new_values = cyclic_data

    new_da = xr.DataArray(new_values, dims=da.dims, coords=new_coords)

    # Copy the attributes for the re-constructed data and coords
    for att, val in da.attrs.items():
        new_da.attrs[att] = val
    for c in da.coords:
        for att in da.coords[c].attrs:
            new_da.coords[c].attrs[att] = da.coords[c].attrs[att]

    return new_da


# =============================================================================


def ylabel_map(s, labelpad=None, size=None, weight=None, y=0.5, ax=None, **kwargs):
    """
    add ylabel to cartopy plot

    Parameters
    ----------
    s : string
        text to display
    labelpad : float, optional
        Distance of labels to axes. Defaults to mpl.rcParams['axes.labelpad']
        which is usually 4.
    size : float or fontsize, optional
        Fontsize, defaults to mpl.rcParams['axes.labelsize'], usually
        'medium'.
    weight : string, optional
        Fontweight, defaults to mpl.rcParams['axes.labelweight'], usually
        'normal'.
    y : float
        y position in axes coordinates. Default 0.5
    ax : matplotlib axis
        axis to add the label
    **kwargs : keyword arguments
        see matplotlib text help

    Returns
    -------
    h : handle
        text handle of the created text field
    ..note::
    http://stackoverflow.com/questions/35479508/cartopy-set-xlabel-set-ylabel-not-ticklabels

    """
    if ax is None:
        ax = plt.gca()

    labelpad, size, weight = _get_label_attr(labelpad, size, weight)

    va = kwargs.pop("va", "bottom")
    ha = kwargs.pop("ha", "center")
    rotation = kwargs.pop("rotation", "vertical")
    rotation_mode = kwargs.pop("rotation_mode", "anchor")

    transform = kwargs.pop("transform", ax.transAxes)

    h = ax.annotate(
        s,
        xy=(0, y),
        xycoords=transform,
        xytext=(-labelpad, 0),
        textcoords="offset points",
        va=va,
        ha=ha,
        rotation=rotation,
        rotation_mode=rotation_mode,
        size=size,
        weight=weight,
        **kwargs
    )

    return h


# =============================================================================


def xlabel_map(s, labelpad=None, size=None, weight=None, x=0.5, ax=None, **kwargs):
    """
    add xlabel to cartopy plot

    Parameters
    ----------
    s : string
        text to display
    labelpad : float, optional
        Distance of labels to axes. Defaults to mpl.rcParams['axes.labelpad']
        which is usually 4.
    size : float or fontsize, optional
        Fontsize, defaults to mpl.rcParams['axes.labelsize'], usually
        'medium'.
    weight : string, optional
        Fontweight, defaults to mpl.rcParams['axes.labelweight'], usually
        'normal'.
    x : float, optional
        x position in axes coordinates. Default 0.5
    ax : matplotlib axis
        axis to add the label
    **kwargs : keyword arguments
        see matplotlib text help

    Returns
    -------
    h : handle
        text handle of the created text field
    ..note::
    http://stackoverflow.com/questions/35479508/cartopy-set-xlabel-set-ylabel-not-ticklabels

    """
    if ax is None:
        ax = plt.gca()

    labelpad, size, weight = _get_label_attr(labelpad, size, weight)

    va = kwargs.pop("va", "top")
    ha = kwargs.pop("ha", "center")
    rotation = kwargs.pop("rotation", "horizontal")
    rotation_mode = kwargs.pop("rotation_mode", "anchor")

    transform = kwargs.pop("transform", ax.transAxes)

    h = ax.annotate(
        s,
        xy=(x, 0),
        xycoords=transform,
        xytext=(0, -labelpad),
        textcoords="offset points",
        va=va,
        ha=ha,
        rotation=rotation,
        rotation_mode=rotation_mode,
        size=size,
        weight=weight,
        **kwargs
    )

    return h


# =============================================================================


def yticklabels(
    y_ticks,
    labelpad=None,
    size=None,
    weight=None,
    ax=None,
    ha="right",
    va="center",
    bbox_props=dict(ec="none", fc="none"),
    **kwargs
):

    """
    draw yticklabels on map plots - may or may not work

    Parameters
    ----------
    y_ticks : 1D array
        Position of the y_ticks.
    labelpad : float, optional
        Distance of labels to axes. Defaults to mpl.rcParams['axes.labelpad']
        which is usually 4.
    size : float or fontsize, optional
        Fontsize, defaults to mpl.rcParams['axes.labelsize'], usually
        'medium'.
    weight : string, optional
        Fontweight, defaults to mpl.rcParams['axes.labelweight'], usually
        'normal'.
    ax : GeoAxes, optional
        Axes to add the labels to. Default plt.gca(.
    ha : string
        Horizontal alignment, default: 'right'.
    va : string
        Vertical alignment, default: 'center'.
    bbox_props : dict
        Properties of the bounding box. Default: dict(ec='none', fc='none')
    **kwargs : additional arguments
        Passed to ax.annotate

    """

    plt.draw()

    # get ax if necessary
    if ax is None:
        ax = plt.gca()

    labelpad, size, weight = _get_label_attr(labelpad, size, weight)

    boundary_pc = _get_boundary_platecarree(ax)

    # ensure labels are on rhs and not in the middle
    if len(boundary_pc) == 1:
        lonmin, lonmax = -180, 180
    else:
        lonmin, lonmax = 0, 360

    # get the y_limit
    y_lim = boundary_pc.bounds[1::2]

    # remove all points not on map for labeling
    y_label_points = [y for y in y_ticks if y_lim[0] <= y <= y_lim[1]]

    if not y_label_points:
        msg = (
            "WARN: no points found for ylabel\n"
            "y_lim is: {:0.2f} to {:0.2f}".format(y_lim[0], y_lim[1])
        )
        print(msg)

    # get a transform instance that mpl understands
    transform = ccrs.PlateCarree()._as_mpl_transform(ax)

    if np.isscalar(labelpad):
        labelpad = [labelpad, 0]

    # loop through points
    for y in y_label_points:

        msg = LATITUDE_FORMATTER(y)

        x = _determine_intersection(boundary_pc, [lonmin, y], [lonmax, y])

        if x.size > 0:
            x = x[0, 0]
            lp = labelpad[0] + labelpad[1] * np.abs(y) / 90

            ax.annotate(
                msg,
                xy=(x, y),
                xycoords=transform,
                ha=ha,
                va=va,
                size=size,
                weight=weight,
                xytext=(-lp, 0),
                textcoords="offset points",
                bbox=bbox_props,
                **kwargs
            )


def xticklabels(
    x_ticks,
    labelpad=None,
    size=None,
    weight=None,
    ax=None,
    ha="center",
    va="top",
    bbox_props=dict(ec="none", fc="none"),
    **kwargs
):

    """
    draw xticklabels on map plots - may or may not work

    Parameters
    ----------
    x_ticks : 1D array
        Position of the x ticks.
    labelpad : float, optional
        Distance of labels to axes. Defaults to mpl.rcParams['axes.labelpad']
        which is usually 4.
    size : float or fontsize, optional
        Fontsize, defaults to mpl.rcParams['axes.labelsize'], usually
        'medium'.
    weight : string, optional
        Fontweight, defaults to mpl.rcParams['axes.labelweight'], usually
        'normal'.
    ax : GeoAxes, optional
        Axes to add the labels to. Default plt.gca(.
    ha : string
        Horizontal alignment, default: 'center'.
    va : string
        Vertical alignment, default: 'top'.
    bbox_props : dict
        Properties of the bounding box. Default: dict(ec='none', fc='none')
    **kwargs : additional arguments
        Passed to ax.annotate

    """

    plt.draw()

    # get ax if necessary
    if ax is None:
        ax = plt.gca()

    labelpad, size, weight = _get_label_attr(labelpad, size, weight)

    boundary_pc = _get_boundary_platecarree(ax)

    # get the x_limit
    x_lim = boundary_pc.bounds[::2]

    # remove all points not on map for labeling
    x_label_points = [x for x in x_ticks if x_lim[0] <= x <= x_lim[1]]

    if not x_label_points:
        msg = (
            "WARN: no points found for xlabel\n"
            "x_lim is: {:0.2f} to {:0.2f}".format(x_lim[0], x_lim[1])
        )
        print(msg)

    # get a transform instance that mpl understands
    transform = ccrs.PlateCarree()._as_mpl_transform(ax)

    # loop through points
    for x in x_label_points:

        msg = LONGITUDE_FORMATTER(x)

        y = _determine_intersection(boundary_pc, [x, -90], [x, 90])
        if y.size > 0:
            y = y[0, 1]

            ax.annotate(
                msg,
                xy=(x, y),
                xycoords=transform,
                ha=ha,
                va=va,
                size=size,
                weight=weight,
                xytext=(0, -labelpad),
                textcoords="offset points",
                bbox=bbox_props,
                **kwargs
            )


def _get_boundary_platecarree(ax):
    # get the bounding box of the map in lat/ lon coordinates
    # after ax._get_extent_geom
    proj = ccrs.PlateCarree()
    boundary_poly = sgeom.Polygon(ax.outline_patch.get_path().vertices)
    eroded_boundary = boundary_poly.buffer(-ax.projection.threshold / 100)
    boundary_pc = proj.project_geometry(eroded_boundary, ax.projection)

    return boundary_pc


def _determine_intersection(polygon, xy1, xy2):

    p1 = sgeom.Point(xy1)
    p2 = sgeom.Point(xy2)
    ls = sgeom.LineString([p1, p2])

    return np.asarray(polygon.boundary.intersection(ls))
