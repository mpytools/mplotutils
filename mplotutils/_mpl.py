import matplotlib


def _get_renderer(fig):

    if hasattr(fig.canvas, "get_renderer"):
        return fig.canvas.get_renderer()
    elif hasattr(fig, "_get_renderer"):
        return fig._get_renderer()

    backend = matplotlib.get_backend()

    raise AttributeError(
        f"Could not find a renderer for the '{backend}' backend. Please raise an issue"
    )


def _maybe_gca(**kwargs):

    import matplotlib.pyplot as plt

    # can call gcf unconditionally: either it exists or would be created by plt.axes
    f = plt.gcf()

    # only call gca if an active axes exists
    if f.axes:
        # can not pass kwargs to active axes
        return plt.gca()

    return plt.axes(**kwargs)
