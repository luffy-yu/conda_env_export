#!/usr/bin/env python

"""The setup script."""

import sys
from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

# https://github.com/luffy-yu/conda_env_export/issues/6
# ruamel.yaml>=0.11.14,<0.18 the front comes from conda, and the rear is to fix deprecated load() function.
requirements = ['setuptools', 'Click>=7.0', 'cytoolz>=0.11.0', 'PyYAML>=5.1', 'ruamel.yaml>=0.11.14,<0.18',
                'conda==4.3.16.2']

setup_requirements = []

test_requirements = []

setup(
    author="Luffy Yu",
    author_email='yuliuchuan@gmail.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    description="Export conda env dependencies and pip requirements to ONE yml file.",
    entry_points={
        'console_scripts': [
            'conda-env-export=conda_env_export.cli:main',
        ],
    },
    install_requires=requirements,
    dependency_links=[
            'https://github.com/luffy-yu/conda-4.3.16/releases/download/v4.3.16.2/conda-4.3.16.2.tar.gz#egg=conda'
    ],
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='conda_env_export',
    name='conda_env_export',
    packages=find_packages(include=['conda_env_export', 'conda_env_export.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/luffy-yu/conda_env_export',
    version='0.6.1',
    zip_safe=False,
)
