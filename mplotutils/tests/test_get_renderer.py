import matplotlib
import pytest

from mplotutils import _get_renderer

from . import figure_context, restore_backend


@pytest.mark.parametrize("backend", matplotlib.backends.backend_registry.list_builtin())
def test_get_renderer(backend):

    with restore_backend(backend):

        with figure_context() as f:
            _get_renderer(f)


def test_error_message_get_renderer():

    # it's a fallback so should never be triggered - here I test the error message only

    backend = matplotlib.get_backend()

    class FakeFig:
        def canvas(self): ...

    with pytest.raises(
        AttributeError,
        match=f"Could not find a renderer for the '{backend}' backend. Please raise an issue",
    ):
        _get_renderer(FakeFig())
