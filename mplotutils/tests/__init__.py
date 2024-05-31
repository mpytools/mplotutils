import contextlib

import matplotlib
import matplotlib.pyplot as plt
import pytest


@contextlib.contextmanager
def figure_context(*args, **kwargs):
    fig = plt.figure(*args, **kwargs)

    try:
        yield fig
    finally:
        plt.close(fig)


@contextlib.contextmanager
def subplots_context(*args, **kwargs):
    fig, axs = plt.subplots(*args, **kwargs)

    try:
        yield fig, axs
    finally:
        plt.close(fig)


@contextlib.contextmanager
def restore_backend(backend):

    current_backend = plt.get_backend()

    try:
        _set_backend(backend)
        yield
    finally:
        plt.switch_backend(current_backend)


def _set_backend(backend):

    # WebAgg requires tornado, but this is only checked at runtime
    if backend == "WebAgg":
        try:
            import tornado  # noqa: F401
        except ImportError:
            pytest.skip(backend)

    try:
        matplotlib.use(backend)
    except ImportError:
        pytest.skip(backend)
