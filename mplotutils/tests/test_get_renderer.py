from contextlib import contextmanager

import matplotlib
import pytest

from . import figure_context


def get_renderer(f):

    if hasattr(f.canvas, "get_renderer"):
        return f.canvas.get_renderer()
    elif hasattr(f, "_get_renderer"):
        return f._get_renderer()

    backend = matplotlib.get_backend()

    raise AttributeError(
        f"Could not find a renderer for the '{backend}' backend. Please raise an issue"
    )


@contextmanager
def restore_backend():

    backend = matplotlib.get_backend()

    try:
        yield
    except Exception:
        matplotlib.use(backend)


@pytest.mark.parametrize("backend", matplotlib.rcsetup.all_backends)
def test_get_renderer(backend):

    with restore_backend():
        try:
            matplotlib.use(backend)
        except ImportError:
            pytest.skip(backend)

        with figure_context() as f:
            get_renderer(f)
