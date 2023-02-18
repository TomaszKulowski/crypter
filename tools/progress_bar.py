"""The collections with progress bar methods."""
from tqdm import tqdm


class ProgressBar:
    """Create a progress bar.

    Methods:
        progress: get the current progress of the progress bar
        progress(current_byte: str): set the progress bar status to the passed value
    """
    def __init__(self, event_name: str, file_size: int):
        """Construct all the necessary attributes for the file object"""
        print(f'{event_name} data')
        self._progress = None
        self.file_size = file_size
        self.progress_bar = tqdm(total=self.file_size)

    @property
    def progress(self):
        """Get or set current progress"""
        return self._progress

    @progress.setter
    def progress(self, current_byte: int):
        if 0 > current_byte or current_byte > self.file_size:
            raise ValueError('incorrect progress bar value')
        self.progress_bar.n = current_byte
        self.progress_bar.refresh()
