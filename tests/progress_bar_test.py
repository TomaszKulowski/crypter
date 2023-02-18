"""The collections of the tests for the progress_bar.py module."""
import pytest
from tqdm import tqdm

from tools.progress_bar import ProgressBar


def test_create_progress_bar(mocker):
    """Check that the progress bar object is created correctly.

    Args:
        mocker (pytest_mock): mock to called methods
    """
    mocker.patch.object(tqdm, '__new__')

    ProgressBar('event_name', 123)

    tqdm.__new__.assert_called_once_with(tqdm, total=123)


@pytest.mark.parametrize(
    'value, expected_value', [
        (0, 0),
        (1, 1),
        (50, 50),
        (1024, 1024),
    ]
)
def test_set_progress_bar_position(value: int, expected_value: int, mocker):
    """Check that the progress was changed to the passed value.

    Args:
        value (int): to set the current progress bar status
        expected_value (int): expected result
        mocker (pytest_mock): mock to called methods
    """
    mocker.patch.object(tqdm, '__new__')
    progress_bar = ProgressBar('save', 1024)

    progress_bar.progress = value

    assert tqdm.__new__.return_value.n == expected_value


@pytest.mark.parametrize(
    'incorrect_value', [
        -1,
        1025,
    ]
)
def test_set_progress_bar_position_to_incorrect_value(incorrect_value: int, mocker):
    """Check that the app raises an error
    if the progress bar will be set to the incorrect value.

    Args:
        incorrect_value (int): To set the incorrect value of the progress bar status
        mocker (pytest_mock): mock to called methods
    """
    mocker.patch.object(tqdm, '__new__')
    progress_bar = ProgressBar('save', 1024)

    with pytest.raises(ValueError) as error:
        progress_bar.progress = incorrect_value

    assert error.type == ValueError
    assert str(error.value) == 'incorrect progress bar value'
