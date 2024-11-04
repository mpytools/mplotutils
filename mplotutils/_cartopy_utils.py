import warnings

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
import shapely.geometry
from cartopy.mpl.gridliner import LATITUDE_FORMATTER, LONGITUDE_FORMATTER

from mplotutils._colormaps import _get_label_attr
from mplotutils._deprecate import _deprecate_positional_args


def sample_data_map(nlons, nlats):
    """Returns `lons`, `lats`, and fake `data`

    Parameters
    ----------
    nlons : int
        Number of longitude grid cells.
    nlats : int
        Number of latitude grid cells.

    Returns
    -------
    lon : ndarray
        Array of the longitude coordinates.
    lat : ndarray
        Array of the latitude coordinates.
    data : ndarray
        Sample data.

    Notes
    -----
    adapted from:
    http://scitools.org.uk/cartopy/docs/v0.15/examples/axes_grid_basic.html
    """

    dlat = 180.0 / nlats / 2
    dlon = 360.0 / nlons / 2

    lat = np.linspace(-90 + dlat, 90 - dlat, nlats)
    lon = np.linspace(dlon, 360 - dlon, nlons)

    lons, lats = np.meshgrid(np.deg2rad(lon), np.deg2rad(lat))
    wave = 0.75 * (np.sin(2 * lats) ** 8) * np.cos(4 * lons)
    mean = 0.5 * np.cos(2 * lats) * ((np.sin(2 * lats)) ** 2 + 2)
    data = wave + mean

    return lon, lat, data


def sample_dataarray(nlon, nlat):
    """Returns `lons`, `lats`, and fake `data`

    Parameters
    ----------
    nlon : int
        Number of longitude grid cells.
    nlat : int
        Number of latitude grid cells.

    Returns
    -------
    data : xr.DataArray
        Sample data with coordinates.

    Notes
    -----
    adapted from:
    http://scitools.org.uk/cartopy/docs/v0.15/examples/axes_grid_basic.html
    """

    import xarray as xr

    lon, lat, data = sample_data_map(nlons=nlon, nlats=nlat)

    return xr.DataArray(data, dims=("lat", "lon"), coords={"lon": lon, "lat": lat})


def cyclic_dataarray(obj, coord="lon"):
    """Add a cyclic coordinate point to a DataArray or Dataset along a dimension.

    Parameters
    ----------
    obj : xr.Dataset | xr.DataArray
        Object to add the cyclic data point to.
    coord : str, default: "lon"
        Name of the

    Returns
    -------
    obj_cyclic : xr.Dataset | xr.DataArray
        The same as `obj` with a cyclic data point added.

    Examples
    --------
    >>> import xarray as xr
    >>> data = xr.DataArray(
    ...     [[1, 2, 3], [4, 5, 6]],
    ...     coords={'x': [1, 2], 'y': range(3)},
    ...     dims=['x', 'y']
    ... )
    >>> data_cyclic = cyclic_dataarray(data, 'y')
    >>> data_cyclic
    <xarray.DataArray (x: 2, y: 4)> Size: 64B
    array([[1, 2, 3, 1],
           [4, 5, 6, 4]])
    Coordinates:
      * x        (x) int64 16B 1 2
      * y        (y) int64 32B 0 1 2 3

    """

    if coord not in obj.coords:
        raise KeyError(f"Did not find '{coord}' in obj")

    obj = obj.pad({coord: (0, 1)}, mode="wrap")

    # extrapolate the coords
    diff = obj[coord].isel({coord: slice(None, -1)}).diff(coord)

    if not np.allclose(diff, diff[0]):
        raise ValueError(f"The coordinate '{coord}' must be equally spaced")

    # the data is not writable (pandas 3) - a copy is required
    lon = obj[coord].variable

    arr = np.array(lon.data)
    arr[-1] = arr[-2] + diff[0]

    lon = type(lon)(lon.dims, arr, attrs=lon.attrs, encoding=lon.encoding)

    return obj.assign_coords({coord: lon})


@_deprecate_positional_args("0.3")
def ylabel_map(s, *, labelpad=None, size=None, weight=None, y=0.5, ax=None, **kwargs):
    """add ylabel to cartopy plot

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

    Notes
    -----
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
        **kwargs,
    )

    return h


@_deprecate_positional_args("0.3")
def xlabel_map(s, *, labelpad=None, size=None, weight=None, x=0.5, ax=None, **kwargs):
    """add xlabel to cartopy plot

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

    Notes
    -----
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
        **kwargs,
    )

    return h


@_deprecate_positional_args("0.3")
def yticklabels(
    y_ticks,
    *,
    labelpad=None,
    size=None,
    weight=None,
    ax=None,
    ha="right",
    va="center",
    bbox_props=dict(ec="none", fc="none"),
    **kwargs,
):
    """draw yticklabels on map plots - may or may not work

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

    # get ax if necessary
    if ax is None:
        ax = plt.gca()

    ax.figure.canvas.draw()

    labelpad, size, weight = _get_label_attr(labelpad, size, weight)

    boundary_pc = _get_boundary_platecarree(ax)

    # ensure labels are on rhs and not in the middle
    if len(boundary_pc.geoms) == 1:
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
        warnings.warn(msg)

    # get a transform instance that mpl understands
    transform = ccrs.PlateCarree()._as_mpl_transform(ax)

    if np.isscalar(labelpad):
        labelpad = [labelpad, 0]

    # loop through points
    for y in y_label_points:
        msg = LATITUDE_FORMATTER(y)

        x = _determine_intersection(boundary_pc, [lonmin, y], [lonmax, y])

        if x.size > 0:
            x = x[:, 0].min()
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
                **kwargs,
            )


@_deprecate_positional_args("0.3")
def xticklabels(
    x_ticks,
    *,
    labelpad=None,
    size=None,
    weight=None,
    ax=None,
    ha="center",
    va="top",
    bbox_props=dict(ec="none", fc="none"),
    **kwargs,
):
    """draw xticklabels on map plots - may or may not work

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

    # get ax if necessary
    if ax is None:
        ax = plt.gca()

    ax.figure.canvas.draw()

    # proj = ccrs.PlateCarree()
    # points = shapely.geometry.MultiPoint([shapely.geometry.Point(x, 0) for x in x_ticks])
    # points = proj.project_geometry(points, proj)
    # x_ticks = [x.x for x in points.geoms]

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
        warnings.warn(msg)

    # get a transform instance that mpl understands
    transform = ccrs.PlateCarree()._as_mpl_transform(ax)

    # loop through points
    for x in x_label_points:
        msg = LONGITUDE_FORMATTER(x)

        y = _determine_intersection(boundary_pc, [x, -90], [x, 90])
        if y.size > 0:
            y = y[:, 1].min()

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
                **kwargs,
            )


def _get_boundary_platecarree(ax):
    # get the bounding box of the map in lat/ lon coordinates
    # after ax._get_extent_geom
    proj = ccrs.PlateCarree()
    boundary_poly = shapely.geometry.Polygon(ax.spines["geo"].get_path().vertices)
    eroded_boundary = boundary_poly.buffer(-ax.projection.threshold / 100)
    boundary_pc = proj.project_geometry(eroded_boundary, ax.projection)

    # boundary_pc = proj.project_geometry(boundary_poly, ax.projection)

    return boundary_pc


def _determine_intersection(polygon, xy1, xy2):
    p1 = shapely.geometry.Point(xy1)
    p2 = shapely.geometry.Point(xy2)
    ls = shapely.geometry.LineString([p1, p2])

    intersection = polygon.boundary.intersection(ls)

    if isinstance(intersection, shapely.geometry.MultiPoint):
        arr = np.array([x.coords for x in intersection.geoms]).squeeze()
    elif isinstance(intersection, shapely.geometry.Point):
        arr = np.array([intersection.coords]).squeeze()
        arr = np.atleast_2d(arr)
    elif isinstance(intersection, shapely.geometry.LineString):
        if intersection.is_empty:
            return np.array([])
        else:
            return np.array(intersection.coords)
    else:
        raise TypeError(f"Unexpected type: {type(intersection)}")

    return arr
