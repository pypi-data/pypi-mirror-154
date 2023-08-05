# example_pkg_cloos

[![PyPI](https://img.shields.io/pypi/v/example_pkg_cloos)](https://pypi.org/project/example-pkg-cloos/)
[![PyPI - License](https://img.shields.io/pypi/l/example_pkg_cloos)](https://pypi.org/project/example-pkg-cloos/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/example-pkg-cloos)](https://pypi.org/project/example-pkg-cloos/)
[![Python package](https://github.com/netsandbox/python_example_pkg_cloos/actions/workflows/python-package.yml/badge.svg)](https://github.com/netsandbox/python_example_pkg_cloos/actions/workflows/python-package.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A example package to learn and test Python packaging.

<https://packaging.python.org/tutorials/packaging-projects/>

## Development workflow

Checkout git repository:

```shell
git clone git@github.com:cloos/python_example_pkg_cloos.git
```

Install package in 'development mode':

```shell
make develop
```

Run tests:

```shell
make test
```

Create Git tag:

```shell
git tag -m "release 0.0.1" 0.0.1
git push --tags
```

Upload to <https://test.pypi.org/>:

```shell
make upload_test

```

Upload to <https://pypi.org/>:

```shell
make upload
```

## Usage

```shell
pip install example-pkg-cloos
```

Cli:

```shell
example-pkg-cloos --help
```

Library:

```python
from example_pkg_cloos.utils import print_bar, print_foo

print_bar()
print_foo()
```
