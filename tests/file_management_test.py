"""The collections of the tests for the file_management.py module."""
import builtins

from tools.file_management import File


def test_load_data_from_file(mocker):
    """Check that the data has been loaded correctly.

    Args:
        mocker (pytest_mock): mock the called methods
    """
    excepted_result = ' example excepted result '
    open_mock = mocker.mock_open(read_data=" example excepted result ")
    mocker.patch.object(builtins, 'open', new=open_mock)

    file_object = File('file.txt')
    result = file_object.load()

    assert result == excepted_result
    builtins.open.assert_called_once_with('file.txt', 'r', encoding='utf-8')


def test_save_data_to_file(mocker):
    """Check that the passed data has been saved correctly.

    Args:
        mocker (pytest_mock): mock the called methods
    """
    data = 'example data to save '
    open_mock = mocker.mock_open()
    mocker.patch.object(builtins, 'open', new=open_mock)

    file_object = File('file.txt')
    file_object.save(data)

    builtins.open.assert_called_once_with('file.txt', 'w', encoding='utf-8')
    builtins.open.return_value.__enter__.return_value.write.assert_called_once_with(data)
