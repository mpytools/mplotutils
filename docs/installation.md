# Installation

## Required dependencies

- Python (3.10 or later)
- [cartopy](http://scitools.org.uk/cartopy/) (0.22 or later)
- [matplotlib](http://matplotlib.org/) (3.8 or later)
- [numpy](http://www.numpy.org/) (1.24 or later)

## Optional dependencies

- [seaborn](https://seaborn.pydata.org/) (0.13 or later)
- [xarray](http://xarray.pydata.org/) (2023.9 or later)

## Instructions

mplotutils itself is a pure Python package, but its dependencies are not.
The easiest way to get them installed is to use [conda](http://conda.io/) or [mamba](https://mamba.readthedocs.io/en/latest/).

```bash
mamba install -c conda-forge cartopy xarray
```

mplotutils is not available from pypi or conda-forge, therefore it needs to be installed using pip directly from github.


### Install latest released version

mplotutils is now available on PyPi - install it with `pip`:

```bash
python -m pip install mplotutils
```


### Install development version

```bash
pip install git+https://github.com/mpytools/mplotutils
```
