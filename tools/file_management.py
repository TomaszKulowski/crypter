"""The collections to operate on files."""
from os import path

from tools.progress_bar import ProgressBar


class File:
    """Create object with path file.

    Methods:
        file_path: get current file path
        file_path(file_path: str): set new file path
        load(): return data from file
        save(data: str): save passed data to file
    """
    def __init__(self):
        """Construct all the necessary attributes for the file object"""
        self._file_path = None

    @property
    def file_path(self) -> str:
        """Get or set file path."""
        return self._file_path

    @file_path.setter
    def file_path(self, file_path: str):
        self._file_path = file_path

    @staticmethod
    def _strip_last_new_line_character(line: bytes) -> bytes:
        """Remove a new line character.
        The 10 number is a new line character in bytes."""
        if line:
            if line[-1] == 10:
                return line[:-1]
        return line

    def load(self) -> str:
        """Open and return data from the file."""
        result = b''
        if not path.isfile(self.file_path):
            raise FileNotFoundError('File not found')
        file_size = path.getsize(self.file_path)
        progress_bar = ProgressBar('load', file_size)
        with open(self.file_path, 'rb') as file:
            while file.tell() != file_size:
                data = self._strip_last_new_line_character(file.readline())
                result += data
                progress_bar.progress = file.tell()
            return result.decode('utf-8')

    def save(self, data: str):
        """Open and save passed data to the file."""
        progress_bar = ProgressBar('save', len(data))
        with open(self.file_path, 'w', encoding='utf-8') as file:
            for index, byte in enumerate(data, 1):
                progress_bar.progress = index
                file.write(byte)
