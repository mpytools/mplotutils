import matplotlib.pyplot as plt

from mplotutils import xlabel_map, ylabel_map


# test it does not error...
def test_works():

    f, ax = plt.subplots()
    ylabel_map("ylabel", ax=ax)
    xlabel_map("ylabel", ax=ax)
