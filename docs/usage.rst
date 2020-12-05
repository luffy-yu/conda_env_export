=====
Usage
=====

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
