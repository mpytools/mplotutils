import cartopy.crs as ccrs
import matplotlib.pyplot as plt

import mplotutils as mpu


def plot_map_no_mpu():
    """plot 2 x 2 global maps _not_ using mplotutils"""

    # create example data
    lon, lat, data = mpu.sample_data_map(30, 30)

    # create figure and axes
    f, axs = plt.subplots(2, 2, subplot_kw={"projection": ccrs.Robinson()})
    axs = axs.flatten()

    # plot data to each axes
    for ax in axs:
        mappable = ax.pcolormesh(lon, lat, data, transform=ccrs.PlateCarree())
        ax.coastlines()

    # add colorbar
    f.colorbar(mappable=mappable, ax=axs)

    f.suptitle("Without mplotutils")


def plot_map_mpu():
    """plot 2 x 2 global maps using mplotutils"""

    # create example data
    lon, lat, data = mpu.sample_data_map(30, 30)

    # create figure and axes
    f, axs = plt.subplots(2, 2, subplot_kw={"projection": ccrs.Robinson()})
    axs = axs.flatten()

    # plot data to each axes
    for ax in axs:
        mappable = ax.pcolormesh(lon, lat, data, transform=ccrs.PlateCarree())
        ax.coastlines()

    # add colorbar using mplotutils
    mpu.colorbar(mappable=mappable, ax=axs)

    # adjust the margins manually
    f.subplots_adjust(left=0.025, right=0.85, top=0.9, bottom=0.05)

    # ensure the figure has the correct size
    mpu.set_map_layout(axs)

    f.suptitle("With mplotutils")


if __name__ == "__main__":
    opt = {"dpi": 200, "facecolor": "0.9", "transparent": False}

    plot_map_no_mpu()
    plt.savefig("example_no_mpu.png", **opt)

    plot_map_mpu()
    plt.savefig("example_mpu.png", **opt)
