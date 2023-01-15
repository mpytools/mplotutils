# Installation

## Required dependencies

- Python (3.7 or later)
- [numpy](http://www.numpy.org/) (1.17 or later)
- [matplotlib](http://matplotlib.org/) (3.4 or later)
- [cartopy](http://scitools.org.uk/cartopy/) (0.18 or later)

## Optional dependencies

-   [seaborn](https://seaborn.pydata.org/) (0.11 or later)
-   [xarray](http://xarray.pydata.org/) (0.18 or later)

## Instructions

mplotutils itself is a pure Python package, but its dependencies are not.
The easiest way to get them installed is to use [conda](http://conda.io/) or [mamba](https://mamba.readthedocs.io/en/latest/).

```bash
mamba install -c conda-forge cartopy xarray
```

mplotutils is not available from pypi or conda-forge, therefore it needs to be installed using pip directly from github.

### Install development version

```bash
pip install git+https://github.com/mathause/mplotutils
```

### Install latest released version

Go to the [newest release on github](https://github.com/mathause/mplotutils/releases/latest), copy the URL of the `*.tar.gz` source file at the botton and then use pip to install it (i.e. `pip install ...`).
