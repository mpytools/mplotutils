import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from cartopy.mpl.geoaxes import GeoAxes
from mpl_toolkits.axes_grid1 import AxesGrid

import mplotutils as mpu


def plot_map_axes_grid():

    # create example data
    da = mpu.sample_dataarray(30, 30)

    axes_class = (GeoAxes, {"projection": ccrs.Robinson()})

    f = plt.figure()

    axgr = AxesGrid(
        f,
        111,
        axes_class=axes_class,
        nrows_ncols=(1, 2),
        axes_pad=0.5 / 2.54,
        cbar_mode="single",
        cbar_location="bottom",
        cbar_size="10%",
        # see https://github.com/matplotlib/matplotlib/issues/28343
        cbar_pad=0.0 / 2.54,
    )

    for ax in axgr.axes_all:
        mappable = da.plot(ax=ax, transform=ccrs.PlateCarree(), add_colorbar=False)
        ax.coastlines()

    cbax = axgr.cbar_axes[0]

    cbax.colorbar(mappable)

    f.subplots_adjust(left=0.05, right=0.95)  # , bottom=0, top=1)

    return f, axgr


def plot_map_no_mpu():
    """plot 2 x 2 global maps _not_ using mplotutils"""

    f, __ = plot_map_axes_grid()

    print(f.get_size_inches())  # * 2.54)

    f.suptitle("AxesGrid - without mplotutils")


def plot_map_mpu():
    """plot 2 x 2 global maps using mplotutils"""

    f, axgr = plot_map_axes_grid()

    # ensure the figure has the correct size
    mpu.set_map_layout(axgr, width=6.4 * 2.54)

    print(f.get_size_inches())  # * 2.54)

    f.suptitle("AxesGrid - with mplotutils")


if __name__ == "__main__":
    opt = {"dpi": 200, "facecolor": "0.9", "transparent": False}

    plot_map_no_mpu()
    plt.savefig("example_axes_grid_no_mpu.png", **opt)

    plot_map_mpu()
    plt.savefig("example_axes_grid_mpu.png", **opt)
