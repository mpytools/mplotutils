import matplotlib.pyplot as plt
import pytest


@pytest.fixture(scope="function", autouse=True)
def assert_all_figures_closed():
    """meta-test to ensure all figures are closed at the end of a test"""
    yield None

    open_figs = len(plt.get_fignums())
    if open_figs:
        raise RuntimeError(
            f"tests did not close all figures ({open_figs} figures open)"
        )
