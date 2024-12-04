# Changelog

## v0.6.0 (04.12.2024)

Version 0.6.0 adds functions to draw hatches and stippling, adds support for `AxesGrid`, fixes some bugs, and bumps the supported versions.

### Breaking changes

- Removed support for python 3.9 ([#130](https://github.com/mpytools/mplotutils/pull/130)).
- The minimum versions of some dependencies were changed ([#132](https://github.com/mpytools/mplotutils/pull/132)).

  | Package     | Old    | New     |
  | ----------- | ------ | ------- |
  | cartopy     | 0.21   | 0.22    |
  | matplotlib  | 3.6    | 3.8     |
  | numpy       | 1.22   | 1.24    |
  | seaborn     | 0.12   | 0.13    |
  | xarray      | 2022.12| 2023.9  |

- The modules ``cartopy_utils``, ``colormaps``, ``map_layout``, ``mpl``, and ``xrcompat``
  were renamed (added a leading underscore) to indicate that they are private
  ([#141](https://github.com/mpytools/mplotutils/pull/141) and [#142](https://github.com/mpytools/mplotutils/pull/142)).

### Enhancements

- Added convenience functions to draw hatches and add stippling:

  1. `mpu.hatch`: for regular axes
  2. `mpu.hatch_map`: for cartopy GeoAxes
  3. `mpu.hatch_map_global`: as 2. but also adds a cyclic point to the array

  all three functions expect a 2D boolean `xr.DataArray` and a hatch pattern. Values that are `True` are hatched
  ([#123](https://github.com/mpytools/mplotutils/pull/123) and [#143](https://github.com/mpytools/mplotutils/pull/143)).


- Enable passing `AxesGrid` (from `mpl_toolkits.axes_grid1`) to `set_map_layout` ([#116](https://github.com/mpytools/mplotutils/pull/116)).
- Raise more informative error when a wrong type is passed to `set_map_layout` ([#121](https://github.com/mpytools/mplotutils/pull/121)).
- `set_map_layout` now raises an explicit error when the figure contains SubFigure ([#121](https://github.com/mpytools/mplotutils/pull/121)).
- Test upstream dependencies and fix compatibility with the upcoming pandas v3  ([#133](https://github.com/mpytools/mplotutils/pull/133)).

### Bug fixes

- Ensure the current axes (`plt.gca()`) is not changed by calling `mpu.colorbar(...)` ([#136](https://github.com/mpytools/mplotutils/pull/136)).

### Internal changes

- Align internal usage of `ListedColormaps` with changes in [matplotlib/matplotlib#29135](https://github.com/matplotlib/matplotlib/pull/29135)
  ([#145](https://github.com/mpytools/mplotutils/pull/145), and [#147](https://github.com/mpytools/mplotutils/pull/147)).

## v0.5.0 (27.03.2024)

Version v0.5.0 aligns passing multiple axes to `colorbar` with matplotlib.

### Breaking changes

- The `ax1` and `ax2` arguments of `mpu.colorbar` have been combined into `ax` ([#107](https://github.com/mpytools/mplotutils/pull/107))
  To update

   ```diff
   - mpu.colorbar(h, axs[0], axs[1])
   + mpu.colorbar(h, [axs[0], axs[1]])
   ```
   or
   ```diff
   - mpu.colorbar(h, axs[0], axs[1])
   + mpu.colorbar(h, axs)
   ```
- When passing `size` to `mpu.colorbar` it now uses the height/ width of _all_ passed axes to scale the colorbar. This is consistent with `plt.colorbar` but may lead to differences compared to the previous version ([#107](https://github.com/mpytools/mplotutils/pull/107)).
- Similarly for `pad`, which is also scaled by the height/ width of _all_ passed axes. This is consistent with `plt.colorbar` but may change the padding of the colorbar compared to the previous version ([#107](https://github.com/mpytools/mplotutils/pull/107)).


## v0.4.0 (23.02.2024)

Version 0.4.0 simplifies the way figures with a `mpu.colorbar` have to be saved  and
bumps the supported versions.

### Breaking changes

- Removed support for python 3.7 and python 3.8 ([#88](https://github.com/mpytools/mplotutils/pull/88)).
- The minimum versions of some dependencies were changed ([#88](https://github.com/mpytools/mplotutils/pull/88), [#91](https://github.com/mpytools/mplotutils/pull/91), and [#96](https://github.com/mpytools/mplotutils/pull/96)).

  | Package      | Old   | New     |
  | ------------ | ----- | -----   |
  | cartopy      | 0.18  | 0.21    |
  | matplotlib*  | 3.4   | 3.6     |
  | numpy        | 1.17  | 1.22    |
  | seaborn      | 0.11  | 0.12    |
  | xarray       | 0.15  | 2022.12 |


- `sample_data_map` now offsets the lon data such that the first grid cell does not wrap
  around ([#87](https://github.com/mpytools/mplotutils/pull/87)).

### Enhancements

- Calling `f.canvas.draw()` before `plt.savefig` is no longer necessary. This now happens
  automatically ([#98](https://github.com/mpytools/mplotutils/pull/98)).
- Add python 3.12 to list of supported versions ([#89](https://github.com/mpytools/mplotutils/pull/89)).

## v0.3.1 (09.02.2023)

Version v0.3.1 fixes a regression and an additional bug from v0.3.0. It's recommended to use this version.

### Bug fixes

- Fixed a bug in `set_map_layout`: the data ratio of a cartopy `GeoAxesSubplot` requires
  a `draw` to be correct ([#61](https://github.com/mpytools/mplotutils/pull/61)).
- Fix a regression introduced in [#33](https://github.com/mpytools/mplotutils/pull/33):
  `cyclic_dataarray` now correctly extrapolates the coordinates
  ([#58](https://github.com/mpytools/mplotutils/pull/58)).


## v0.3.0 (15.01.2023)

Version 0.3.0 includes some long-overdue bug fixes, modernization of the code, much better
test coverage and some enhancements.

mplotutils now uses the MIT license instead of GPL-3.0 ([#51](https://github.com/mpytools/mplotutils/pull/51))

### Deprecations

 * Deprecated `mpu.infer_interval_breaks` as this is no longer necessary with matplotlib v3.2
   and cartopy v0.21 ([#32](https://github.com/mpytools/mplotutils/pull/32)).
 * Deprecated a number of positional arguments, these are now keyword only, e.g. in
   `mpu.colorbar` ([#54](https://github.com/mpytools/mplotutils/pull/54)).

### Enhancements

 * Added ``nrow`` and ``ncol`` parameters to ``set_map_layout`` for use with a
   gridspec.
 * Allow passing list of axes to ``set_map_layout``, renamed the files and extended
   the test coverage ([#42](https://github.com/mpytools/mplotutils/pull/42)
   and [#43](https://github.com/mpytools/mplotutils/pull/43)).
 * Add function to create `xr.DataArray` sample data ([#53](https://github.com/mpytools/mplotutils/pull/53)).

### Bug fixes

 * Fixed compatibility of `mpu.colorbar` with `bbox_inches="tight"` for matplotlib 3.4 and
   newer and refactor and extend tests ([#26](https://github.com/mpytools/mplotutils/pull/26)
   and [#40](https://github.com/mpytools/mplotutils/pull/40)).

### Internal changes

 * Replaced `ax.get_geometry()` with `ax.get_subplotspec().get_geometry()`
   as the former was deprecated in matplotlib ([#8](https://github.com/mpytools/mplotutils/pull/8)).
 * Refactor `mpu.cyclic_dataarray` using `obj.pad` ([#33](https://github.com/mpytools/mplotutils/pull/33)).
 * Enabled CI on github actions ([#9](https://github.com/mpytools/mplotutils/pull/9)).
 * Formatted with black and isort, checked with flake8.

## v0.2.0 (01.06.2018)

Mayor release, mostly introducing the new `colorbar` functionality.

 * add `_color_palette` that selects colors from the whole range of the colormap. Previously
   we used the `seaborn` logic that excludes colors at the edge of the colorbar
   ([#1](https://github.com/mpytools/mplotutils/issues/1)).
 * the colorbar functionality was entirely redesigned:
   * new top-level function `mpu.colorbar`
   * added `aspect` keyword which defines the ratio of long to short side
   * the default width/ height is now `aspect=20` (was `size=0.04`)
   * `pad` and `size` are now scaled by the width/ height of the axes (was width/ height of the figure)
   * `pad` now uses the matplotlib default (0.05 for vertical bars and 0.15 for horizontal colorbars)
 * add `_is_monotonic` to `infer_interval_breaks`
 * renamed `sample_data_3d` to `sample_data_map`

## v0.1.0 (13.03.2018)

 * Functionality as developed for [pyvis](https://github.com/C2SM/pyvis/) (see below), packed into a module.
