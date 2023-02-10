"""The collections with progress bar methods."""
from tqdm import tqdm


class ProgressBar:
    """Create a progress bar.

    Methods:
        set(current_byte: str): set the progress bar status to the passed value
    """
    def __init__(self, event_name: str, file_size: int):
        """Construct all the necessary attributes for the file object"""
        print(f'{event_name} data')
        self.progress_bar = tqdm(total=file_size)

    def set(self, current_byte: int):
        """Set the progress bar status to the passed value."""
        self.progress_bar.n = current_byte
        self.progress_bar.refresh()
