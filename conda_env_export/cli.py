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
@click.option('--separate', help='Output to separate files', is_flag=True, default=False, show_default=True)
@click.option('--reserve-duplicates', help='Reserve duplicates', is_flag=True, default=False, show_default=True)
@click.option('--include', help='Force to include deps (ignore case)', multiple=True)
@click.option('--exclude', help='Force to exclude deps (ignore case)', multiple=True)
@click.option('--extra-pip-requirements', help='Output an extra `requirements.txt`', is_flag=True, default=False,
              show_default=True)
@click.option('--no-prefix', help='Remove `prefix` in target yml file', is_flag=True, default=False, show_default=True)
@click.option('--to-folder', help='Where to output the file(s)',
              type=click.Path(exists=True, file_okay=False, dir_okay=True, writable=True),
              default='./', show_default=True)
@click.option('--to-file', help='Filename of the output yml file',
              type=click.Path(file_okay=True, dir_okay=False, writable=True),
              default=os.getenv('CONDA_DEFAULT_ENV') + '.yml' if os.getenv('CONDA_DEFAULT_ENV') else '',
              show_default=True)
def main(name, conda_all, pip_all, separate, reserve_duplicates, include, exclude, extra_pip_requirements, no_prefix,
         to_folder, to_file):
    try:
        include = set(map(lambda x: x.lower(), include))
        exclude = set(map(lambda x: x.lower(), exclude))
        # remove shared items in both include and exclude
        include, exclude = include.difference(exclude), exclude.difference(include)
        cee = CondaEnvExport()
        cee.check(name)
        cee.run(name, conda_all=conda_all, pip_all=pip_all, separate=separate, remove_duplicates=not reserve_duplicates,
                include=include, exclude=exclude, extra_pip_requirements=extra_pip_requirements, no_prefix=no_prefix,
                output_folder=to_folder, output_file=to_file)
    except AssertionError as e:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
