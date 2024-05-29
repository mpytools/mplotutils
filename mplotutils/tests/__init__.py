import contextlib

import matplotlib.pyplot as plt


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
def restore_backend():

    backend = plt.get_backend()

    try:
        yield
    except Exception:
        pass
    plt.switch_backend(backend)
