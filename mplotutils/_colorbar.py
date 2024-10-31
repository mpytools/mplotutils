import warnings

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
import numpy as np

from mplotutils._deprecate import _deprecate_positional_args


def _deprecate_ax1_ax2(ax, ax2, ax1):
    if ax is None:
        if ax1 is None:
            raise TypeError("colorbar() missing 1 required positional argument: 'ax'")

        if ax2 is None:
            ax = ax1
            warnings.warn(
                "`ax1` has been deprecated in favor of `ax`",
                FutureWarning,
                stacklevel=4,
            )

        else:
            ax = [ax1, ax2]
            warnings.warn(
                "`ax1` and `ax2` has been deprecated in favor of `ax`, i.e. pass ax=[ax1, ax2]",
                FutureWarning,
                stacklevel=4,
            )

    else:

        if ax1 is not None and ax2 is not None:
            raise TypeError("Cannot pass `ax`, and `ax2`")

        if ax2 is not None and np.ndim(ax) != 0:
            raise TypeError("Cannot pass ax2 in addition to a list of axes")

        if ax2 is not None:
            ax = [ax, ax2]

            warnings.warn(
                "Passing axes individually has been deprecated in favor of passing them"
                " as list, i.e. pass ``ax=[ax1, ax2]``, or ``ax=axs``",
                FutureWarning,
                stacklevel=4,
            )

    return ax


@_deprecate_positional_args("0.3")
def colorbar(
    mappable,
    ax=None,
    ax2=None,
    *,
    orientation="vertical",
    aspect=None,
    size=None,
    pad=None,
    shift="symmetric",
    shrink=None,
    **kwargs,
):
    """colorbar that adjusts to the axes height (and automatically resizes)

    See below for Example

    Parameters
    ----------
    mappable : handle
        The `matplotlib.cm.ScalarMappable` described by this colorbar.
    ax : `~matplotlib.axes.Axes` or iterable or `numpy.ndarray` of Axes
        One or more parent Axes of the colorbar.
    orientation : 'vertical' | 'horizontal'. Default: 'vertical'.
        Orientation of the colorbar.
    aspect : float, default 20.
        The ratio of long to short dimensions of the colorbar. Mutually exclusive with
        `size`.
    size : float, default: None
        Width of the colorbar as fraction of all parent axes width (vertical) or
        height (horizontal). Mutually exclusive with `aspect`.
    pad : float, default: None.
        Distance between axes and colorbar. In fraction of parent axes.
        Default: 0.05 (vertical) or 0.15 (horizontal).
    shift : 'symmetric' or float in 0..1, default: 'symmetric'
        Fraction of the total height that the colorbar is shifted up/ right. See Note.
    shrink : None or float in 0..1, default: None.
        Fraction of the total height that the colorbar is shrunk. See Note.
    **kwargs : keyword arguments
        See Other Parameters.

    Other Parameters
    ----------------
    location : None or {'left', 'right', 'top', 'bottom'}
        The location, relative to the parent Axes, where the colorbar Axes
        is created.  It also determines the *orientation* of the colorbar
        (colorbars on the left and right are vertical, colorbars at the top
        and bottom are horizontal).  If None, the location will come from the
        *orientation* if it is set (vertical colorbars on the right, horizontal
        ones at the bottom), or default to 'right' if *orientation* is unset.

    orientation : None or {'vertical', 'horizontal'}
        The orientation of the colorbar.  It is preferable to set the *location*
        of the colorbar, as that also determines the *orientation*; passing
        incompatible values for *location* and *orientation* raises an exception.

    fraction : float, default: 0.15
        Fraction of original Axes to use for colorbar.

    shrink : float, default: 1.0
        Fraction by which to multiply the size of the colorbar.

    extend : {'neither', 'both', 'min', 'max'}
        Make pointed end(s) for out-of-range values (unless 'neither').  These are
        set for a given colormap using the colormap set_under and set_over methods.

    extendfrac : {*None*, 'auto', length, lengths}
        If set to *None*, both the minimum and maximum triangular colorbar
        extensions will have a length of 5% of the interior colorbar length (this
        is the default setting).

        If set to 'auto', makes the triangular colorbar extensions the same lengths
        as the interior boxes (when *spacing* is set to 'uniform') or the same
        lengths as the respective adjacent interior boxes (when *spacing* is set to
        'proportional').

        If a scalar, indicates the length of both the minimum and maximum
        triangular colorbar extensions as a fraction of the interior colorbar
        length.  A two-element sequence of fractions may also be given, indicating
        the lengths of the minimum and maximum colorbar extensions respectively as
        a fraction of the interior colorbar length.

    extendrect : bool, default: False
        If *False* the minimum and maximum colorbar extensions will be triangular
        (the default).  If *True* the extensions will be rectangular.

    spacing : {'uniform', 'proportional'}
        For discrete colorbars (`.BoundaryNorm` or contours), 'uniform' gives each
        color the same space; 'proportional' makes the space proportional to the
        data interval.

    ticks : None or list of ticks or Locator
        If None, ticks are determined automatically from the input.

    format : None or str or Formatter
        If None, `~.ticker.ScalarFormatter` is used.
        Format strings, e.g., ``"%4.2e"`` or ``"{x:.2e}"``, are supported.
        An alternative `~.ticker.Formatter` may be given instead.

    drawedges : bool
        Whether to draw lines at color boundaries.

    label : str
        The label on the colorbar's long axis.

    boundaries, values : None or a sequence
        If unset, the colormap will be displayed on a 0-1 scale.
        If sequences, *values* must have a length 1 less than *boundaries*.  For
        each region delimited by adjacent entries in *boundaries*, the color mapped
        to the corresponding value in values will be used.
        Normally only useful for indexed colors (i.e. ``norm=NoNorm()``) or other
        unusual circumstances.

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> import mplotutils as mpu
    >>> import cartopy.crs as ccrs

    >>> # example data
    >>> da = mpu.sample_dataarray(36, 18)
    >>> # plotting options
    >>> opt = {"add_colorbar": False, "transform": ccrs.PlateCarree()}

    >>> # =========================
    >>> # example with 1 axes

    >>> f, ax = plt.subplots(subplot_kw={"projection": ccrs.PlateCarree()})
    >>> ax.coastlines() # doctest: +SKIP
    >>> ax.set_global()
    >>> h = da.plot(ax=ax, **opt)

    >>> cbar = mpu.colorbar(h, ax)

    >>> # =========================
    >>> # example with 2 axes

    >>> f, axs = plt.subplots(2, 1, subplot_kw={"projection": ccrs.PlateCarree()})

    >>> for ax in axs:
    ...     ax.coastlines() # doctest: +SKIP
    ...     ax.set_global()

    >>> h = da.plot(ax=axs[0], **opt)
    >>> h = da.plot(ax=axs[1], **opt)

    >>> cbar = mpu.colorbar(h, axs)

    >>> # =========================
    >>> # example with 3 axes & 2 colorbars

    >>> f, axs = plt.subplots(3, 1, subplot_kw={"projection": ccrs.PlateCarree()})

    >>> for ax in axs:
    ...     ax.coastlines() # doctest: +SKIP
    ...     ax.set_global()

    >>> h0 = da.plot(ax=axs[0], **opt)
    >>> h1 = da.plot(ax=axs[1], **opt)
    >>> h2 = da.plot(ax=axs[2], cmap='Blues', **opt)

    >>> cbar = mpu.colorbar(h0, [axs[0], axs[1]], size=0.05)
    >>> cbar = mpu.colorbar(h2, axs[2], size=0.05)

    Notes
    -----
    - ``shift='symmetric', shrink=None`` -> colorbar extends over the whole height
    - ``shift='symmetric', shrink=0.1`` -> colorbar is 10 % smaller, and centered
    - ``shift=0., shrink=0.1`` -> colorbar is 10 % smaller, and aligned with the bottom
    - ``shift=0.1, shrink=None`` -> colorbar is 10 % smaller, and aligned with the top
    - the ``anchor`` and ``panchor`` keywords are not supported

    See Also
    --------
    plt.colorbar
    """

    ax = _deprecate_ax1_ax2(ax, ax2, kwargs.pop("ax1", None))
    axs = np.asarray(ax).flatten()

    if orientation not in ("vertical", "horizontal"):
        raise ValueError("orientation must be 'vertical' or 'horizontal'")

    k = kwargs.keys()
    if ("anchor" in k) or ("panchor" in k):
        msg = "'anchor' and 'panchor' keywords not supported, use 'shrink' and 'shift'"
        raise ValueError(msg)

    if not all(isinstance(ax, mpl.axes.Axes) for ax in axs):
        raise TypeError("ax must be of Type mpl.axes.Axes")

    f = axs[0].get_figure()

    if not all(f == ax.get_figure() for ax in axs):
        raise TypeError("All passed axes must belong to the same figure")

    gca = plt.gca()
    cbax = _get_cbax(f)
    # ensure mpu.colorbar does not change the current axes
    plt.sca(gca)

    cbar = f.colorbar(mappable, orientation=orientation, cax=cbax, **kwargs)

    if orientation == "vertical":
        func = _resize_colorbar_vert(
            cbax,
            f,
            axs,
            aspect=aspect,
            size=size,
            pad=pad,
            shift=shift,
            shrink=shrink,
        )
    else:
        func = _resize_colorbar_horz(
            cbax,
            f,
            axs,
            aspect=aspect,
            size=size,
            pad=pad,
            shift=shift,
            shrink=shrink,
        )

    f.canvas.mpl_connect("draw_event", func)
    f.canvas.draw()

    return cbar


# ========================================================================


def _get_cbax(f):
    # when using f.add_axes(rect) with the same rect twice
    # it is the same axes, so we have to change rect
    # slightly each time this func is called

    n_axes = len(f.get_axes())
    pos_incr = n_axes / 10.0
    return f.add_axes([0, 0, 0.1, 0.1 + pos_incr])


def _resize_colorbar_vert(
    cbax,
    f,
    axs,
    aspect=None,
    size=None,
    pad=None,
    shift="symmetric",
    shrink=None,
):

    shift, shrink = _parse_shift_shrink(shift, shrink)

    size, aspect, pad = _parse_size_aspect_pad(size, aspect, pad, "vertical")

    if aspect is not None:
        anchor = (0, 0.5)
        cbax.set_anchor(anchor)
        cbax.set_box_aspect(aspect)

    # inner function is called by event handler
    def inner(event=None):

        # from mpl.colorbar (but not using ax.get_position(original=True).frozen())
        parents_bbox = mtransforms.Bbox.union([ax.get_position() for ax in axs])

        # determine total height of all axes
        full_height = parents_bbox.height

        pad_scaled = pad * parents_bbox.width

        # calculate position of cbax
        left = parents_bbox.x1 + pad_scaled

        bottom = parents_bbox.y0 + shift * full_height

        height = (1 - shrink) * full_height

        if aspect is None:
            size_scaled = size * parents_bbox.width
            width = size_scaled
        else:
            figure_aspect = np.divide(*f.get_size_inches())
            width = height / (aspect * figure_aspect)

        pos = [left, bottom, width, height]

        cbax.set_position(pos)

    return inner


# ====================================


def _resize_colorbar_horz(
    cbax,
    f,
    axs,
    aspect=None,
    size=None,
    pad=None,
    shift="symmetric",
    shrink=None,
):

    shift, shrink = _parse_shift_shrink(shift, shrink)

    size, aspect, pad = _parse_size_aspect_pad(size, aspect, pad, "horizontal")

    if aspect is not None:
        aspect = 1 / aspect
        anchor = (0.5, 1.0)
        cbax.set_anchor(anchor)
        cbax.set_box_aspect(aspect)

    def inner(event=None):

        # from mpl.colorbar (but not using ax.get_position(original=True).frozen())
        parents_bbox = mtransforms.Bbox.union([ax.get_position() for ax in axs])

        full_width = parents_bbox.width

        pad_scaled = pad * parents_bbox.height

        width = (1 - shrink) * full_width

        if aspect is None:
            size_scaled = size * parents_bbox.height
            height = size_scaled
        else:
            figure_aspect = np.divide(*f.get_size_inches())
            height = width * (aspect * figure_aspect)

        left = parents_bbox.x0 + shift * full_width
        bottom = parents_bbox.y0 - (pad_scaled + height)

        pos = [left, bottom, width, height]

        cbax.set_position(pos)

    return inner


# ====================================


def _parse_shift_shrink(shift, shrink):
    if shift == "symmetric":
        if shrink is None:
            shrink = 0

        shift = shrink / 2.0

    else:
        if shrink is None:
            shrink = shift

    if (shift < 0.0) or (shift > 1.0):
        raise ValueError("'shift' must be in 0...1")

    if (shrink < 0.0) or (shrink > 1.0):
        raise ValueError("'shrink' must be in 0...1")

    if shift > shrink:
        warnings.warn(
            "'shift' is larger than 'shrink', colorbar will extend beyond the axes"
        )

    return shift, shrink


# ==================================================================================================


def _parse_size_aspect_pad(size, aspect, pad, orientation):
    if (size is not None) and (aspect is not None):
        raise ValueError("Can only pass one of 'aspect' and 'size'")

    # default is aspect=20
    if (size is None) and (aspect is None):
        aspect = 20

    # default mpl setting
    if pad is None:
        pad = 0.05 if orientation == "vertical" else 0.15

    return size, aspect, pad
