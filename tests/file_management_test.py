"""The collections of the tests for the file_management.py module."""
import builtins
from os import path

import pytest

from tools.file_management import File
from tools.progress_bar import ProgressBar


def test_file_path_setter():
    """Check that the file path is set correctly when the passed file is exist.

    Args:
        mocker (pytest_mock): mock the called methods
    """
    file = File()
    file.file_path = 'file.txt'

    assert file.file_path == 'file.txt'


def test_strip_last_new_line_without_new_line_char_at_end():
    """Check that the passed data isn't changed when the new line char is missing"""
    data = b'some data'
    file = File()
    result = file._strip_last_new_line_character(data)

    assert result == data


def test_strip_last_new_line_with_new_line_at_end():
    """Check that the one new line char is removed"""
    data = b'some data\n\n'
    file = File()
    result = file._strip_last_new_line_character(data)

    assert result == data[:-1]


def test_successfully_load_data_from_file(mocker):
    """Check that the data has been loaded correctly.

    Args:
        mocker (pytest_mock): mock the called methods
    """
    excepted_result = ' example excepted result '
    mocker.patch.object(builtins, 'open', new=mocker.mock_open())
    builtins.open.return_value.tell.side_effect = [1, 2, 2]
    builtins.open.return_value.readline.return_value = b' example excepted result '
    mocker.patch.object(path, 'getsize', return_value=2)
    mocker.patch.object(path, 'isfile', return_value=True)
    mocker.patch.object(ProgressBar, '__new__')

    file_object = File()
    file_object.file_path = 'file.txt'
    result = file_object.load()

    builtins.open.assert_called_once_with('file.txt', 'rb')
    ProgressBar.__new__.assert_called_once_with(ProgressBar, 'load', 2)
    assert result == excepted_result


def test_save_data_to_file(mocker):
    """Check that the passed data has been saved correctly.

    Args:
        mocker (pytest_mock): mock the called methods
    """
    data = 'example data to save '
    mocker.patch.object(builtins, 'open', new=mocker.mock_open())
    mocker.patch.object(path, 'isfile', return_value=True)
    mocker.patch.object(ProgressBar, '__new__')

    file_object = File()
    file_object.file_path = 'file.txt'
    file_object.save(data)

    builtins.open.assert_called_once_with('file.txt', 'w', encoding='utf-8')
    ProgressBar.__new__.assert_called_once_with(ProgressBar, 'save', len(data))
    assert builtins.open.return_value.__enter__.return_value.write.call_count == len(data)


def test_load_data_file_not_exist(mocker):
    """Check that the file path is not set as file_path,
    and error is raised.

    Args:
        mocker (pytest_mock): mock the called methods
    """
    mocker.patch.object(path, 'isfile', return_value=False)

    file = File()
    file.file_path = 'file.txt'
    with pytest.raises(FileNotFoundError, match='File not found') as error:
        file.load()

    path.isfile.assert_called_once_with('file.txt')
    assert error.type == FileNotFoundError
    assert str(error.value) == 'File not found'
