"""Top-level package for Conda Env Export."""

__author__ = """Luffy Yu"""
__email__ = 'yuliuchuan@gmail.com'
__version__ = '0.6.1'

# WARNING  Error during upload. Retry with the --verbose option for more details.
# ERROR    HTTPError: 400 Bad Request from https://upload.pypi.org/legacy/
#          Can't have direct dependency: conda@
#          https://github.com/luffy-yu/conda-4.3.16/releases/download/v4.3.16.2/conda-4.3.16.2.tar.gz#egg=conda==4.3.16.2.
#          See https://packaging.python.org/specifications/core-metadata for more information.
# Install conda within the command, rather than set it in the `install_requires`. See conda_env_export.py Line 280
__conda__ = 'https://github.com/luffy-yu/conda-4.3.16/releases/download/v4.3.16.2/conda-4.3.16.2.tar.gz'