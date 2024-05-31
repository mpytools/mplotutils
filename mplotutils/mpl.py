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
