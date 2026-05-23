#!/usr/bin/env python

"""Tests for `conda_env_export` package."""

import unittest
from click.testing import CliRunner

from conda_env_export import conda_env_export
from conda_env_export import cli


class TestConda_env_export(unittest.TestCase):
    """Tests for `conda_env_export` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert 'Show this message and exit.' in help_result.output

    def test_get_pip_deps_uses_iterated_packages(self):
        """Test pip export through the package iterator adapter."""
        class FakeRequirement(object):
            key = 'dependency'
            specs = [('>=', '2')]

        class FakePackage(object):
            def __init__(self, key, version, project_name, requirements=()):
                self.key = key
                self.version = version
                self.project_name = project_name
                self._requirements = requirements

            def requires(self):
                return self._requirements

        packages = [
            FakePackage('root', '1.0', 'Root', [FakeRequirement()]),
            FakePackage('dependency', '2.0', 'Dependency'),
        ]
        original = conda_env_export._iter_pip_packages
        conda_env_export._iter_pip_packages = lambda paths: packages
        try:
            nodes = conda_env_export.CondaEnvExport().get_pip_deps(
                ['/env/site-packages'], all=True)
        finally:
            conda_env_export._iter_pip_packages = original

        assert [str(node) for node in nodes] == [
            'Dependency==2.0',
            'Root==1.0',
        ]
