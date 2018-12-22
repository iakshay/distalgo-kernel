DistAlgo Kernel for Jupter
===========

``distalgo_kernel`` is Jupyter Kernel for [DistAlgo](https://github.com/DistAlgo/distalgo)

Installation
------------
To install ``distalgo_kernel`` from PyPI::

    pip install distalgo_kernel
    python -m distalgo_kernel.install

Using the DistAlgo kernel
---------------------
**Notebook**: The *New* menu in the notebook should show an option for an DistAlgo notebook.

**Console frontends**: To use it with the console frontends, add ``--kernel distalgo_kernel`` to
their command line arguments::

    jupyter console --kernel distalgo_kernel

Todo
-----
- Support running processes
- Improve error stack trace
