"""The collections of the tests for the main.py module"""
from argparse import ArgumentParser, ArgumentError
import sys

import pytest

from tools.crypter_tool import Crypter
from crypter import Main


@pytest.mark.parametrize(
    'argv, argument', [
        ('-m', 'mode'),
        ('-p', 'password'),
        ('-v', 'verbose'),
        ('--file', 'file'),
        ('--folder', 'folder'),
        ('-e', 'extension'),
        ('-r', 'remove'),
    ]
)
def test_parser(argv, argument, mocker):
    """Check that the passed argument creates the attribute"""
    mocker.patch.object(sys, 'argv', return_value=argv)
    mocker.patch.object(ArgumentParser, 'parse_args', return_value=argument)
    main = Main()

    main._load_arguments(argv)

    assert main.args == argument


@pytest.mark.parametrize(
    'argv, expected_mode', [
        (['app_name', '-m', 'encrypt', '-p', 'pass', '--file', 'file.txt'], 'encrypt'),
        (['app_name', '-m', 'decrypt', '-p', 'pass', '--file', 'file.txt.cr'], 'decrypt'),
        (['app_name', '-m', 'append', '-p', 'pass', '--file', 'file.txt', 'file2.txt'], 'append'),
    ]
)
def test_called_to_entered_mode(argv, expected_mode, mocker):
    """Check that the passed mode is called"""
    mocker.patch.object(sys, 'argv', new=argv)
    mocker.patch.object(Crypter, expected_mode)

    main = Main()
    main.start()

    mode = getattr(Crypter, expected_mode)
    mode.assert_called_once()
