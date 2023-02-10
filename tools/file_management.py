"""The collections to operate on files."""
from os.path import getsize

from tools.progress_bar import ProgressBar


class File:
    """Create object with path file.

    Methods:
        load(): return data from file
        save(data: str): save passed data to file
    """
    def __init__(self, file_path: str):
        """Construct all the necessary attributes for the file object"""
        self.file_path = file_path

    @staticmethod
    def _strip_new_line_character(line):
        """Remove a new line character.
        The 10 number is a new line character in bytes."""
        if line[-1] == 10:
            return line[:-1]
        return line

    def load(self) -> str:
        """Open and return data from the file."""
        result = b''
        file_size = getsize(self.file_path)
        progress_bar = ProgressBar(self.load.__name__, file_size)
        with open(self.file_path, 'rb') as file:
            while file.tell() != file_size:
                data = self._strip_new_line_character(file.readline())
                result += data
                progress_bar.set(file.tell())
            return result.decode('utf-8')

    def save(self, data: str):
        """Open and save passed data to the file."""
        progress_bar = ProgressBar(self.save.__name__, len(data))
        with open(self.file_path, 'w', encoding='utf-8') as file:
            for index, byte in enumerate(data, 1):
                progress_bar.set(index)
                file.write(byte)
