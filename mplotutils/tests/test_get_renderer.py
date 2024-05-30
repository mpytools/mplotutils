import matplotlib
import numpy as np
import pytest

from . import figure_context, restore_backend, subplots_context


def get_renderer(f):

    if hasattr(f.canvas, "get_renderer"):
        return f.canvas.get_renderer()
    elif hasattr(f, "_get_renderer"):
        return f._get_renderer()

    backend = matplotlib.get_backend()

    raise AttributeError(
        f"Could not find a renderer for the '{backend}' backend. Please raise an issue"
    )


@pytest.mark.parametrize("backend", matplotlib.rcsetup.all_backends)
def test_get_renderer(backend):

    with restore_backend():
        try:
            matplotlib.use(backend)
        except ImportError:
            pytest.skip(backend)

        with figure_context() as f:
            get_renderer(f)


def test_set_size():

    with subplots_context() as (f, ax):

        f.set_size_inches(17, 6)
        np.testing.assert_allclose(f.get_size_inches(), (17, 6))

    with subplots_context() as (f, ax):

        f.set_size_inches(17 / 2.54, 6 / 2.54)

        print(f.get_size_inches().__repr__())
        print(type(f.get_size_inches()))
        print(f"{f.canvas.device_pixel_ratio=}")
        print(f"{f.dpi=}")

        scale = f.dpi / f.canvas.device_pixel_ratio

        print(f"{scale=}")

        import inspect

        print()
        print(inspect.getsource(f.set_size_inches))
        print()

        np.testing.assert_allclose(f.get_size_inches() * 2.54, (17, 6))

        f.set_dpi(1000)

        f.set_size_inches(17 / 2.54, 6 / 2.54)
        np.testing.assert_allclose(f.get_size_inches() * 2.54, (17, 6))

        f.set_dpi(10)

        f.set_size_inches(17 / 2.54, 6 / 2.54)
        np.testing.assert_allclose(f.get_size_inches() * 2.54, (17, 6))
