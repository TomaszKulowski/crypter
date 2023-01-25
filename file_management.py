"""The collections to operate on files."""


class File:
    """Create object with path file.

    Methods:
        load(): return data from file
        save(data: str): save passed data to file
    """
    def __init__(self, file_path: str):
        """Construct all the necessary attributes for the file object"""
        self.file_path = file_path

    def load(self) -> str:
        """Open and return data from the file."""
        with open(self.file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def save(self, data: str):
        """Open and save passed data to the file."""
        with open(self.file_path, 'w', encoding='utf-8') as file:
            file.write(data)
