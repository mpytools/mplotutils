from mplotutils import xlabel_map, ylabel_map

from . import subplots_context


# test it does not error...
# TODO: write actual tests
def test_works():
    with subplots_context() as (f, ax):
        ylabel_map("ylabel", ax=ax)
        xlabel_map("ylabel", ax=ax)
