# Installation

## Required dependencies

- Python (3.11 or later)
- [cartopy](http://scitools.org.uk/cartopy/) (0.23 or later)
- [matplotlib](http://matplotlib.org/) (3.9 or later)
- [numpy](http://www.numpy.org/) (1.26 or later)

## Optional dependencies

- [seaborn](https://seaborn.pydata.org/) (0.13 or later)
- [xarray](http://xarray.pydata.org/) (2024.7 or later)

## Instructions

### Install latest released version

mplotutils is now available on PyPi - and can be installed with `pip`:

```bash
python -m pip install mplotutils
```

Its not (yet) on conda-forge. To install it into a conda environment, add the required
dependencies first before using pip to install mplotutils as well:

```bash
mamba install -c conda-forge cartopy xarray
python -m pip install mplotutils
```

### Install development version

```bash
pip install git+https://github.com/mpytools/mplotutils
```
