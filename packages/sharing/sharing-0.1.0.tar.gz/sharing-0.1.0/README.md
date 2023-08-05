Sharing
=======

A library to share variables and configurations between modules of a same
project and managing their effects.

## Goal

When working on a big project composed of multiple packages, you sometime needs
to access to common variables and configurations from your different packages.

This library objectives are :
1. To create a **shared in memory variables repository** usable between your packages. No database, network or disk access required.
2. Allowing **hooks** registration to trigger function on shared variable update.
The variable update from library A can have a direct impact on the library B and
the hook allow to automatically trigger a registered function in B when the update occurred in A.

## Install

### Recommended install

Install using `pip` from pypi.org

```bash
pip install sharing
```

### Install from sources

Clone the repository and install:

```bash
git clone http://gitlab.guirimand.eu/tguirimand/sharing.git
cd sharing
pip install -e .
```

## Using the library

The package contains 3 variables grouper:
* `sh.shared`: to share generic variables
* `sh.config`: to share specific variables used in configuration
* `sh.counters`: to share counters (integers only)

### Sharing a variable between two packages :

From package A:

```python
import sharing as sh

my_variable = 12345
sh.shared.set('variable tag', my_variable)  # Creating the shared variable
```

From package B:

```python
import sharing as sh

my_variable = sh.shared.get('variable tag')  # None if it doesn't exists
sh.shared.set('variable tag', my_variable + 1)  # Updating the shared variable
```

### Creating a hook

A hook can be created using a decorator. To run the function `fu` every time the
shared variable using the `"bar"` tag is updated:

```python
@sh.shared.updatable(key="bar")
def fu():
    if sh.shared.get('bar')==3:
        print("bar has now the value 3")
    else:
        print("bar has been updated")
```
