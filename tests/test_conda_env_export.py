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
