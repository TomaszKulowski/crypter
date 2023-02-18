"""The collections of the tests for the main.py module"""
from argparse import ArgumentParser, ArgumentError
import sys

import pytest

from tools.crypter import Crypter
from main import Main


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
    'argv, missing, errors', [
        (['-m', 'encrypt', '-p', 'pass'], '--file --folder', SystemExit),
        (['-m', 'encrypt', '--file', 'a.txt'], '-p/--password', SystemExit),
        (['-p', 'pass', '--file', 'a.txt'], '-m/--mode', SystemExit),
        (['-m', 'append', '-p', 'pass', '--file', 'file_one.txt'], 'second file', ArgumentError)
    ]
)
def test_load_arguments_without_requirement(argv, missing, errors, mocker, capsys):
    """Check that the app raised an error when the required argument didn't pass"""
    output_line_one = """usage: crypter.py [-h] -m  -p PASSWORD [-v] (--file FILE [FILE ...] | --folder FOLDER) \
[-e {.csv,.json,.txt,.cr} [{.csv,.json,.txt,.cr} ...]] [-r {True,False}]
"""
    output_line_two = 'crypter.py: error: the following arguments are required: '
    mocker.patch.object(sys, 'argv', return_value=argv)
    mocker.patch.object(Main, '_start')
    main = Main()

    with pytest.raises(errors) as error:
        main._load_arguments(argv)
        main._validate_arguments()

    _, err = capsys.readouterr()

    if missing == 'second file':
        assert error.type == ArgumentError
        assert str(error.value) == 'append mode requires passing two files'

    elif missing == '--file --folder':
        assert error.type == SystemExit
        assert err == output_line_one + """crypter.py: error: \
one of the arguments --file --folder is required\n"""

    else:
        assert error.type == SystemExit
        assert err == output_line_one + output_line_two + missing + '\n'


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

