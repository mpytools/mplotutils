import matplotlib.pyplot as plt


def colorbar(
    mappable,
    ax1,
    ax2=None,
    orientation="vertical",
    aspect=None,
    size=None,
    pad=None,
    shift="symmetric",
    shrink=None,
    **kwargs
):
    """
    automatically resize colorbars on draw

    See below for Example

    Parameters
    ----------
    mappable : handle
        The return value of 'ax.contourf', 'ax.pcolormesh' etc to
        which the colorbar applies.
    ax1 : Axes
        Axes to adjust the colorbar to.
    ax2 : Axes, optional
        If the colorbar should span more than one Axes. Default: None.
    orientation : 'vertical' | 'horizontal', optional
        Orientation of the colorbar. Default: 'vertical'.
    aspect : float, optional
        The ratio of long to short dimensions of the colorbar. Default 20.
        Mutually exclusive with 'size'.
    size : float
        Width of the colorbar as fraction of the axes width (vertical) or
        height (horizontal). Mutually exclusive with 'aspect'. Default: None.
    pad : float
        Distance of the colorbar to the axes in Figure coordinates.
         Default: 0.05 (vertical) or 0.15 (horizontal).
    shift : 'symmetric' or float in 0..1
        Fraction of the total height that the colorbar is shifted upwards.
        See Note. Default: 'symmetric'
    shrink : None or float in 0..1
        Fraction of the total height that the colorbar is shrunk.
        See Note. Default: None.
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

    f = plt.figure()
    ax = plt.axes(projection=ccrs.PlateCarree())
    h = ax.pcolormesh([[0, 1]])

    ax.coastlines()

    mpu.colorbar(h, ax)

    ax.set_global()

    # =========================
    # example with 2 axes

    f, axes = plt.subplots(2, 1, subplot_kw=dict(projection=ccrs.Robinson()))

    for ax in axes:
        ax.coastlines()
        ax.set_global()
        h = ax.pcolormesh([[0, 1]])

    cbar = mpu.colorbar(h, axes[0], axes[1])

    cbar.set_label('[°C]', labelpad=10)

    # =========================
    # example with 3 axes & 2 colorbars

    f, axes = plt.subplots(3, 1, subplot_kw=dict(projection=ccrs.Robinson()))

    for ax in axes:
        ax.coastlines()
        ax.set_global()

    h0 = ax.pcolormesh([[0, 1]])
    h1 = ax.pcolormesh([[0, 1]])
    h2 = ax.pcolormesh([[0, 1]], cmap='Blues')

    cbar = mpu.colorbar(h, axes[0], axes[1], size=0.05)

    cbar = mpu.colorbar(h, axes[2], size=0.05)

    plt.draw()

    Notes
    -----
    shift='symmetric', shrink=None  -> colorbar extends over the whole height
    shift='symmetric', shrink=0.1   -> colorbar is 10 % smaller, and centered
    shift=0., shrink=0.1            -> colorbar is 10 % smaller, and aligned
                                       with the bottom
    shift=0.1, shrink=None          -> colorbar is 10 % smaller, and aligned
                                       with the top

    See Also
    --------
    _resize_colorbar_horz
    """

    orientations = ("vertical", "horizontal")
    if orientation not in orientations:
        raise ValueError("orientation must be 'vertical' or 'horizontal'")

    k = kwargs.keys()
    if ("anchor" in k) or ("panchor" in k):
        msg = "'anchor' and 'panchor' keywords not supported, use 'shrink' and 'shift'"
        raise ValueError(msg)

    # ensure 'ax' does not end up in plt.colorbar(**kwargs)
    if "ax" in k:
        # assume it is ax2 (it can't be ax1)
        ax2 = kwargs.pop("ax")

    f = ax1.get_figure()

    if ax2 is not None:
        f2 = ax2.get_figure()
        assert f == f2, "'ax1' and 'ax2' must belong to the same figure"

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

    func = mpu.colorbar_utils_resize_colorbar_vert(cbax, ax)
    f.canvas.mpl_connect('draw_event', func)

    ax.set_global()

    plt.draw()

    See Also
    --------
    _resize_colorbar_horz
    """

    shift, shrink = _parse_shift_shrink(shift, shrink)

    size, aspect, pad = _parse_size_aspect_pad(size, aspect, pad, "vertical")

    # swap axes if ax1 is above ax2
    if ax2 is not None:
        posn1 = ax1.get_position()
        posn2 = ax2.get_position()

        ax1, ax2 = (ax1, ax2) if posn1.y0 < posn2.y0 else (ax2, ax1)

    if aspect is not None:
        anchor = (0, 0.5)
        cbax.set_aspect(aspect, anchor=anchor, adjustable="box")

    # inner function is called by event handler
    def inner(event=None):

        posn1 = ax1.get_position()

        # determine total height of all axes
        if ax2 is not None:
            posn2 = ax2.get_position()
            full_height = posn2.y0 - posn1.y0 + posn2.height
        else:
            full_height = posn1.height

        pad_scaled = pad * posn1.width
        size_scaled = size * posn1.width

        # calculate position
        left = posn1.x0 + posn1.width + pad_scaled
        bottom = posn1.y0 + shift * full_height
        height = full_height - shrink * full_height
        # ignored if aspect is set
        width = size_scaled

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

    func = mpu.colorbar_utils._resize_colorbar_horz(cbax, ax)
    f.canvas.mpl_connect('draw_event', func)

    ax.set_global()

    plt.draw()

    See Also
    --------
    _resize_colorbar_vert
    """

    shift, shrink = _parse_shift_shrink(shift, shrink)

    size, aspect, pad = _parse_size_aspect_pad(size, aspect, pad, "horizontal")

    if ax2 is not None:
        posn1 = ax1.get_position()
        posn2 = ax2.get_position()

        # swap axes if ax1 is right of ax2
        ax1, ax2 = (ax1, ax2) if posn1.x0 < posn2.x0 else (ax2, ax1)

    if aspect is not None:
        aspect = 1 / aspect
        anchor = (0.5, 1.0)
        cbax.set_aspect(aspect, anchor=anchor, adjustable="box")

    def inner(event=None):

        posn1 = ax1.get_position()

        if ax2 is not None:
            posn2 = ax2.get_position()
            full_width = posn2.x0 - posn1.x0 + posn2.width
        else:
            full_width = posn1.width

        pad_scaled = pad * posn1.height
        size_scaled = size * posn1.height

        left = posn1.x0 + shift * full_width
        bottom = posn1.y0 - (pad_scaled + size_scaled)
        width = full_width - shrink * full_width

        # ignored if aspect is set
        height = size_scaled

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

    assert (shift >= 0.0) & (shift <= 1.0), "'shift' must be in 0...1"
    assert (shrink >= 0.0) & (shrink <= 1.0), "'shrink' must be in 0...1"

    if shift > shrink:
        msg = (
            "Warning: 'shift' is larger than 'shrink', colorbar\n"
            "will extend beyond the axes!"
        )
        print(msg)

    return shift, shrink


# ==================================================================================================


def _parse_size_aspect_pad(size, aspect, pad, orientation):

    if (size is not None) and (aspect is not None):
        raise ValueError("you can only pass one of 'aspect' and 'size'")

    # default is aspect=20
    if (size is None) and (aspect is None):
        aspect = 20

    # we need a large size so it is not limiting for set_aspect
    if aspect is not None:
        size = 10

    # default mpl setting
    if pad is None:
        pad = 0.05 if orientation == "vertical" else 0.15

    return size, aspect, pad
