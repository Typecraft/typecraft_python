#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_tc_xml_python
----------------------------------

Tests for `tc_xml_python` module.
"""

import pytest

from contextlib import contextmanager
from click.testing import CliRunner

from tc_xml_python import tc_xml_python
from tc_xml_python import cli


class TestTc_xml_python(object):

    @classmethod
    def setup_class(cls):
        pass

    def test_command_line_interface(self):
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'tc_xml_python.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output

    @classmethod
    def teardown_class(cls):
        pass

