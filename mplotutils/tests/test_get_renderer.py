import matplotlib
import pytest

from mplotutils import _get_renderer

from . import figure_context, restore_backend


@pytest.mark.parametrize("backend", matplotlib.backends.backend_registry.list_builtin())
def test_get_renderer(backend):

    with restore_backend(backend):

        with figure_context() as f:
            _get_renderer(f)
