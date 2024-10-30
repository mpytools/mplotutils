#!/usr/bin/env bash

# forcibly remove packages to avoid artifacts
conda uninstall -y --force \
  cartopy \
  matplotlib-base \
  numpy \
  packaging \
  pandas \
  xarray
# to limit the runtime of Upstream CI
python -m pip install \
    -i https://pypi.anaconda.org/scientific-python-nightly-wheels/simple \
    --no-deps \
    --pre \
    --upgrade \
    matplotlib \
    numpy \
    pandas \
    shapely \
    xarray
python -m pip install \
    --no-deps \
    --upgrade \
    git+https://github.com/mwaskom/seaborn \
    git+https://github.com/pypa/packaging \
    git+https://github.com/SciTools/cartopy
