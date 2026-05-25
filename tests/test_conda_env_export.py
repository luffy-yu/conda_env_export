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

    def test_make_yml_includes_pip_index_options(self):
        """Test pip index options are exported with pip requirements."""
        exporter = conda_env_export.CondaEnvExport()
        data, pip_data = exporter.make_yml(
            [conda_env_export.CondaNode('python', '3.11.14', 'defaults')],
            [conda_env_export.PipNode('torch', '2.8.0+cu128', 'torch')],
            '/tmp/test-env',
            'test-env',
            index_url='https://download.pytorch.org/whl/cu128',
            extra_index_urls=('https://example.com/simple',),
        )

        expected_pip_data = [
            '--index-url https://download.pytorch.org/whl/cu128',
            '--extra-index-url https://example.com/simple',
            'torch==2.8.0+cu128',
        ]
        assert data['dependencies'][-1] == {'pip': expected_pip_data}
        assert pip_data == expected_pip_data

    def test_make_yml_includes_pip_index_options_when_separate(self):
        """Test separate exports keep pip index options in both outputs."""
        exporter = conda_env_export.CondaEnvExport()
        data, pip_data = exporter.make_yml(
            [conda_env_export.CondaNode('python', '3.11.14', 'defaults')],
            [conda_env_export.PipNode('torch', '2.8.0+cu128', 'torch')],
            '/tmp/test-env',
            'test-env',
            separate=True,
            extra_index_urls=('https://example.com/simple',),
        )

        assert data['dependencies'][-1] == {
            'pip': ['--extra-index-url https://example.com/simple', '-r requirements.txt'],
        }
        assert pip_data == [
            '--extra-index-url https://example.com/simple',
            'torch==2.8.0+cu128',
        ]
