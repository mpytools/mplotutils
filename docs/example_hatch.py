import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

import mplotutils as mpu


def main():

    # read example data
    air = xr.tutorial.open_dataset("air_temperature").air
    air = air.resample(time="d").mean()

    mean, std = air.mean("time"), air.std("time")

    anomaly = air.isel(time=3) - mean

    # create plot
    f, ax = plt.subplots(subplot_kw={"projection": ccrs.PlateCarree()})

    ax.coastlines()

    h = anomaly.plot(ax=ax, transform=ccrs.PlateCarree(), add_colorbar=False)

    # only for illustration purposes
    signif = np.abs(anomaly) >= std

    mpu.hatch_map(signif, "///", ax=ax, color="0.2", label="significant", linewidth=0.5)

    ax.legend()

    # adjust the margins manually
    f.subplots_adjust(left=0.025, right=0.85, top=0.9, bottom=0.05)

    # ensure the figure has the correct size
    mpu.set_map_layout(ax)

    mpu.colorbar(h, ax)

    ax.set_title("Temperature")


if __name__ == "__main__":

    main()

    plt.savefig("example_hatch.png", dpi=200)
