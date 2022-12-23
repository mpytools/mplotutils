# Changelog


## v0.3.0 (unreleased)

### Bug fixes

 * Fixed compatibility of `mpu.colorbar` with `bbox_inches="tight"` for matplotlib 3.4 and
   newer [#26](https://github.com/mathause/mplotutils/pull/26).

### Internal changes

 * Added ``nrow`` and ``ncol`` parameters to ``set_map_layout`` for use with a
   gridspec.
 * Replaced `ax.get_subplotspec().get_geometry()` with `ax.get_subplotspec().get_geometry()`
   as the former was deprecated in matplotlib (#8).
 * Enabled CI on github actions (#9).
 * Formatted with black and isort, checked with flake8.


## v0.2.0 (01.06.2018)

Mayor release, mostly introducing the new `colorbar` functionality.

 * add `_color_palette` that selects colors from the whole range of the colormap. Previously we used the `seaborn` logic that excludes colors at the edge of the colorbar (closes GH:#1).
 * the colorbar functionality was entirely redesigned:
   * new top-level function `mpu.colorbar`
   * added `aspect` keyword which defines the ratio of long to short side
   * the default width/ height is now `aspect=20` (was `size=0.04`)
   * `pad` and `size` are now scaled by the width/ height of the axes (was width/ height of the figure)
   * `pad` now uses the matplotlib default (0.05 for vertical bars and 0.15 for horizontal colorbars)
 * add `_is_monotonic` to `infer_interval_breaks`
 * renamed `sample_data_3d` to `sample_data_map`

## v0.1.0 (13.03.2018)

 * Functionality as developped for [pyvis](https://github.com/C2SM/pyvis/) (see below), packed into a module.