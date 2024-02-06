================
Conda Env Export
================


.. image:: https://img.shields.io/pypi/v/conda_env_export.svg
        :target: https://pypi.python.org/pypi/conda_env_export

.. image:: https://api.travis-ci.com/luffy-yu/conda_env_export.svg?branch=master
        :target: https://app.travis-ci.com/github/luffy-yu/conda_env_export

.. image:: https://readthedocs.org/projects/conda-env-export/badge/?version=latest
        :target: https://conda-env-export.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png
        :target: https://www.buymeacoffee.com/luffyyu


Export conda env dependencies and pip requirements to ONE yml file.


* Free software: MIT license
* Documentation: https://conda-env-export.readthedocs.io.


Features
--------

* Easy to use

* Flexible options to export

* Support Windows, Linux, and Mac

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
      -n, --name TEXT           Name of environment  [default: `{activated}`]
      --conda-all               Output all conda deps  [default: False]
      --pip-all                 Output all pip deps  [default: False]
      --separate                Output to separate files  [default: False]
      --reserve-duplicates      Reserve duplicates  [default: False]
      --include TEXT            Force to include deps (ignore case)
      --exclude TEXT            Force to exclude deps (ignore case)
      --extra-pip-requirements  Output an extra `requirements.txt`  [default: False]
      --no-prefix               Remove `prefix` in target yml file  [default: False]
      --to-folder DIRECTORY     Where to output the file(s)  [default: ./]
      --to-file FILE            Filename of the output yml file  [default: `{activated}`]
      --help                    Show this message and exit.

[RECOMMEND]

Export current activated env, just run:

.. code-block:: console

    $ conda-env-export

[RECOMMEND]

Export a named env, e.g. `py37`, run:

.. code-block:: console

    $ conda-env-export -n py37

[RECOMMEND]

Export current activated env to separate files (`activated.yml` and `requirements.txt`), just run:

.. code-block:: console

    $ conda-env-export --separate

NOTE: `--separate` is different from `--extra-pip-requirements` in the output yml file,
where the yml from `--separate` doesn't explicitly list pip dependencies.
It will use `-r requirements.txt` instead.

[RECOMMEND]

Export current activated env and output an EXTRA pip requirements file, just run:

.. code-block:: console

    $ conda-env-export --extra-pip-requirements

WHY: Sometimes it'll fail to install some pip deps when executing `conda env create -f env.yml`,
so it's much more convenient to install pip deps via `pip install -r requirements.txt` rather than
`conda env update -f env.yml --prune`.

Export a named env and ensure that output MUST include `pip` and `PyYAML`, run:

.. code-block:: console

    $ conda-env-export -n py37 --include pip --include pyyaml

Export a named env and ensure that output MUST exclude `pip` and `PyYAML`, run:

.. code-block:: console

    $ conda-env-export -n py37 --exclude pip --exclude pyyaml

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
