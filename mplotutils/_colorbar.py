import warnings

import matplotlib.pyplot as plt
import numpy as np

from mplotutils._deprecate import _deprecate_positional_args


@_deprecate_positional_args("0.3")
def colorbar(
    mappable,
    ax1,
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
    """
    automatically resize colorbars on draw

    See below for Example

    Parameters
    ----------
    mappable : handle
        The `matplotlib.cm.ScalarMappable` described by this colorbar.
    ax1 : `matplotlib.axes.Axes`
        The axes to adjust the colorbar to.
    ax2 : `~matplotlib.axes.Axes`, default: None.
        If the colorbar should span more than one axes.
    orientation : 'vertical' | 'horizontal'. Default: 'vertical'.
        Orientation of the colorbar.
    aspect : float, default 20.
        The ratio of long to short dimensions of the colorbar Mutually exclusive with
        `size`.
    size : float, default: None
        Width of the colorbar as fraction of the axes width (vertical) or
        height (horizontal). Mutually exclusive with `aspect`.
    pad : float, default: None.
        Distance of the colorbar to the axes in Figure coordinates.
         Default: 0.05 (vertical) or 0.15 (horizontal).
    shift : 'symmetric' or float in 0..1, default: 'symmetric'
        Fraction of the total height that the colorbar is shifted upwards. See Note.
    shrink : None or float in 0..1, default: None.
        Fraction of the total height that the colorbar is shrunk. See Note.
    **kwargs : keyword arguments
        colorbar properties
        ============  ====================================================
        Property      Description
        ============  ====================================================
        *extend*      [ 'neither' | 'both' | 'min' | 'max' ]
                    If not 'neither', make pointed end(s) for out-of-
                    range values.  These are set for a given colormap
                    using the colormap set_under and set_over methods.
        *extendfrac*  [ *None* | 'auto' | length | lengths ]
                    If set to *None*, both the minimum and maximum
                    triangular colorbar extensions with have a length of
                    5% of the interior colorbar length (this is the
                    default setting). If set to 'auto', makes the
                    triangular colorbar extensions the same lengths as
                    the interior boxes (when *spacing* is set to
                    'uniform') or the same lengths as the respective
                    adjacent interior boxes (when *spacing* is set to
                    'proportional'). If a scalar, indicates the length
                    of both the minimum and maximum triangular colorbar
                    extensions as a fraction of the interior colorbar
                    length. A two-element sequence of fractions may also
                    be given, indicating the lengths of the minimum and
                    maximum colorbar extensions respectively as a
                    fraction of the interior colorbar length.
        *extendrect*  [ *False* | *True* ]
                    If *False* the minimum and maximum colorbar extensions
                    will be triangular (the default). If *True* the
                    extensions will be rectangular.
        *spacing*     [ 'uniform' | 'proportional' ]
                    Uniform spacing gives each discrete color the same
                    space; proportional makes the space proportional to
                    the data interval.
        *ticks*       [ None | list of ticks | Locator object ]
                    If None, ticks are determined automatically from the
                    input.
        *format*      [ None | format string | Formatter object ]
                    If None, the
                    :class:`~matplotlib.ticker.ScalarFormatter` is used.
                    If a format string is given, e.g., '%.3f', that is
                    used. An alternative
                    :class:`~matplotlib.ticker.Formatter` object may be
                    given instead.
        *drawedges*   [ False | True ] If true, draw lines at color
                    boundaries.
        ============  ====================================================

    Examples
    --------
    import matplotlib.pyplot as plt
    import mplotutils as mpu
    import cartopy.crs as ccrs

    # example with 1 axes

    f, ax = plt.subplots(subplot_kw={"projection": ccrs.PlateCarree()})
    h = ax.pcolormesh([[0, 1]])
    ax.coastlines()
    mpu.colorbar(h, ax)
    ax.set_global()

    # =========================
    # example with 2 axes

    f, axs = plt.subplots(2, 1, subplot_kw={"projection": ccrs.PlateCarree()})

    for ax in axs:
        ax.coastlines()
        ax.set_global()
        h = ax.pcolormesh([[0, 1]])

    cbar = mpu.colorbar(h, axs[0], axs[1])

    # =========================
    # example with 3 axes & 2 colorbars

    f, axs = plt.subplots(3, 1, subplot_kw={"projection": ccrs.PlateCarree()})

    for ax in axs:
        ax.coastlines()
        ax.set_global()

    h0 = ax.pcolormesh([[0, 1]])
    h1 = ax.pcolormesh([[0, 1]])
    h2 = ax.pcolormesh([[0, 1]], cmap='Blues')

    cbar = mpu.colorbar(h, axs[0], axs[1], size=0.05)
    cbar = mpu.colorbar(h, axs[2], size=0.05)

    plt.draw()

    Notes
    -----
    - ``shift='symmetric', shrink=None`` -> colorbar extends over the whole height
    - ``shift='symmetric', shrink=0.1`` -> colorbar is 10 % smaller, and centered
    - ``shift=0., shrink=0.1`` -> colorbar is 10 % smaller, and aligned with the bottom
    - ``shift=0.1, shrink=None`` -> colorbar is 10 % smaller, and aligned with the top

    See Also
    --------
    plt.colorbar
    """

    if orientation not in ("vertical", "horizontal"):
        raise ValueError("orientation must be 'vertical' or 'horizontal'")

    k = kwargs.keys()
    if ("anchor" in k) or ("panchor" in k):
        msg = "'anchor' and 'panchor' keywords not supported, use 'shrink' and 'shift'"
        raise ValueError(msg)

    # ensure 'ax' does not end up in plt.colorbar(**kwargs)
    if "ax" in k:
        if ax2 is not None:
            raise ValueError("Cannot pass `ax`, and `ax2`")
        # assume it is ax2 (it can't be ax1)
        ax2 = kwargs.pop("ax")

    f = ax1.get_figure()

    if ax2 is not None and f != ax2.get_figure():
        raise ValueError("'ax1' and 'ax2' must belong to the same figure")

    cbax = _get_cbax(f)

    cbar = plt.colorbar(mappable, orientation=orientation, cax=cbax, **kwargs)

    if orientation == "vertical":
        func = _resize_colorbar_vert(
            cbax,
            ax1,
            ax2=ax2,
            aspect=aspect,
            size=size,
            pad=pad,
            shift=shift,
            shrink=shrink,
        )
    else:
        func = _resize_colorbar_horz(
            cbax,
            ax1,
            ax2=ax2,
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
    ax1,
    ax2=None,
    aspect=None,
    size=None,
    pad=None,
    shift="symmetric",
    shrink=None,
):
    """
    automatically resize colorbars on draw

    see 'colorbar'

    Examples
    --------
    import matplotlib.pyplot as plt
    import mplotutils as mpu
    import cartopy.crs as ccrs

    f = plt.figure()
    ax = plt.axes(projection=ccrs.PlateCarree())
    h = ax.pcolormesh([[0, 1]])

    ax.coastlines()

    cbax = f.add_axes([0, 0, 0.1, 0.1])
    cbar = plt.colorbar(h, orientation='vertical', cax=cbax)

    func = mpu._resize_colorbar_vert(cbax, ax)
    f.canvas.mpl_connect('draw_event', func)

    ax.set_global()

    plt.draw()

    See Also
    --------
    _resize_colorbar_horz
    """

    shift, shrink = _parse_shift_shrink(shift, shrink)

    size, aspect, pad = _parse_size_aspect_pad(size, aspect, pad, "vertical")

    f = ax1.get_figure()

    # swap axes if ax1 is above ax2
    if ax2 is not None:
        posn1 = ax1.get_position()
        posn2 = ax2.get_position()

        ax1, ax2 = (ax1, ax2) if posn1.y0 < posn2.y0 else (ax2, ax1)

    if aspect is not None:
        anchor = (0, 0.5)
        cbax.set_anchor(anchor)
        cbax.set_box_aspect(aspect)

    # inner function is called by event handler
    def inner(event=None):

        pos1 = ax1.get_position()

        # determine total height of all axes
        if ax2 is None:
            full_height = pos1.height
        else:
            pos2 = ax2.get_position()
            full_height = pos2.y0 - pos1.y0 + pos2.height

        pad_scaled = pad * pos1.width

        # calculate position of cbax
        left = pos1.x0 + pos1.width + pad_scaled
        bottom = pos1.y0 + shift * full_height
        height = (1 - shrink) * full_height

        if aspect is None:
            size_scaled = size * pos1.width
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
    ax1,
    ax2=None,
    aspect=None,
    size=None,
    pad=None,
    shift="symmetric",
    shrink=None,
):
    """
    automatically resize colorbars on draw

    see 'colorbar'

    Examples
    --------
    import matplotlib.pyplot as plt
    import mplotutils as mpu
    import cartopy.crs as ccrs

    f = plt.figure()
    ax = plt.axes(projection=ccrs.PlateCarree())

    ax.coastlines()

    cbax = f.add_axes([0, 0, 0.1, 0.1])
    cbar = plt.colorbar(h, orientation='horizontal', cax=cbax)

    func = mpu._resize_colorbar_horz(cbax, ax)
    f.canvas.mpl_connect('draw_event', func)

    ax.set_global()

    plt.draw()

    See Also
    --------
    _resize_colorbar_vert
    """

    shift, shrink = _parse_shift_shrink(shift, shrink)

    size, aspect, pad = _parse_size_aspect_pad(size, aspect, pad, "horizontal")

    f = ax1.get_figure()

    if ax2 is not None:
        posn1 = ax1.get_position()
        posn2 = ax2.get_position()

        # swap axes if ax1 is right of ax2
        ax1, ax2 = (ax1, ax2) if posn1.x0 < posn2.x0 else (ax2, ax1)

    if aspect is not None:
        aspect = 1 / aspect
        anchor = (0.5, 1.0)
        cbax.set_anchor(anchor)
        cbax.set_box_aspect(aspect)

    def inner(event=None):

        posn1 = ax1.get_position()

        if ax2 is None:
            full_width = posn1.width
        else:
            posn2 = ax2.get_position()
            full_width = posn2.x0 - posn1.x0 + posn2.width

        pad_scaled = pad * posn1.height

        width = full_width - shrink * full_width

        if aspect is None:
            size_scaled = size * posn1.height
            height = size_scaled
        else:
            figure_aspect = np.divide(*f.get_size_inches())
            height = width * (aspect * figure_aspect)

        left = posn1.x0 + shift * full_width
        bottom = posn1.y0 - (pad_scaled + height)

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
