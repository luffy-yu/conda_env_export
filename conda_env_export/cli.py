"""Console script for conda_env_export."""
import os
import sys
import click
from conda_env_export.conda_env_export import CondaEnvExport


@click.command()
@click.option('-n', '--name', help='Name of environment', type=click.STRING,
              default=os.getenv('CONDA_DEFAULT_ENV'), show_default=True)
@click.option('--conda-all', help='Output all conda deps', is_flag=True, default=False, show_default=True)
@click.option('--pip-all', help='Output all pip deps', is_flag=True, default=False, show_default=True)
@click.option('--reserve-duplicates', help='Reserve duplicates', is_flag=True, default=False, show_default=True)
def main(name, conda_all, pip_all, reserve_duplicates):
    try:
        cee = CondaEnvExport()
        cee.check(name)
        cee.run(name, conda_all=conda_all, pip_all=pip_all, remove_duplicates=not reserve_duplicates)
    except AssertionError as e:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
