"""Console script for conda_env_export."""
import sys
import click
from conda_env_export.conda_env_export import CondaEnvExport


@click.command()
@click.option('-n', '--name', help='Name of environment', type=click.STRING)
def main(name):
    try:
        cee = CondaEnvExport()
        cee.check_and_run(name)
    except AssertionError as e:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
