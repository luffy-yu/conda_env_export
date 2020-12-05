================
Conda Env Export
================


.. image:: https://img.shields.io/pypi/v/conda_env_export.svg
        :target: https://pypi.python.org/pypi/conda_env_export

.. image:: https://img.shields.io/travis/luffy-yu/conda_env_export.svg
        :target: https://travis-ci.com/luffy-yu/conda_env_export

.. image:: https://readthedocs.org/projects/conda-env-export/badge/?version=latest
        :target: https://conda-env-export.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Export conda env with pip to an yml file.


* Free software: MIT license
* Documentation: https://conda-env-export.readthedocs.io.


Features
--------

* Export conda env dependencies and pip requirements to an yml file.

* Easy to use

* Remove duplicated packages automatically


Usage
--------

To use Conda Env Export in a project:

.. code-block:: python

    import conda_env_export

To use Conda Env Export in a terminal:

.. code-block:: console

    $ conda-env-export --help
    Usage: conda-env-export [OPTIONS]

    Options:
      -n, --name TEXT       Name of environment  [default: `{activated}`]
      --conda-all           Output all conda deps  [default: False]
      --pip-all             Output all pip deps  [default: False]
      --reserve-duplicates  Reserve duplicates  [default: False]
      --help                Show this message and exit.

[RECOMMEND]

Export current activated env, just run:

.. code-block:: console

    $ conda-env-export

[RECOMMEND]

Export a named env, e.g. `py37`, run:

.. code-block:: console

    $ conda-env-export -n py37


Export with all conda deps and all pip deps of `py37`

.. code-block:: console

    $ conda-env-export -n py37 --conda-all --pip-all

Export with all conda deps and all pip deps of `py37`, and DO NOT remove duplicates

.. code-block:: console

    $ conda-env-export -n py37 --conda-all --pip-all --reserve-duplicates

Note: The operation of remove duplicates refers to remove those deps in pip, which are already in conda deps.


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
