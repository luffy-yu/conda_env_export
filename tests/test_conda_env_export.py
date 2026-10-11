#!/usr/bin/env python

"""Tests for `conda_env_export` package."""

import unittest
from unittest.mock import patch
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

    def test_locate_prefix_matches_complete_environment_name(self):
        exporter = conda_env_export.CondaEnvExport()
        output = (b'# conda environments:\n#\n'
                  b'ml-gpu                   /opt/conda/envs/ml-gpu\n'
                  b'ml                       /opt/conda/envs/ml\n')
        with patch.object(exporter, 'call_cmd', return_value=(output, b'')):
            self.assertEqual(exporter.locate_prefix('ml'),
                             '/opt/conda/envs/ml')
            self.assertIsNone(exporter.locate_prefix('missing'))

    def test_locate_prefix_does_not_return_partial_match(self):
        exporter = conda_env_export.CondaEnvExport()
        output = b'ml-gpu                   /opt/conda/envs/ml-gpu\n'
        with patch.object(exporter, 'call_cmd', return_value=(output, b'')):
            self.assertIsNone(exporter.locate_prefix('ml'))

    def test_locate_prefix_preserves_path(self):
        exporter = conda_env_export.CondaEnvExport()
        output = b'ml                    *  /opt/conda/envs/my * environment\n'
        with patch.object(exporter, 'call_cmd', return_value=(output, b'')):
            self.assertEqual(exporter.locate_prefix('ml'),
                             '/opt/conda/envs/my * environment')
