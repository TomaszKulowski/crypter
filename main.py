"""Application to encrypt files"""
import argparse
import logging
import os

from crypter import Crypter

FILE_TYPES = ['.txt', '.cr', '.json']


class Main:
    """Main class of the crypter application.

    Methods:
         load(): classmethod to init arguments and set verbose mode
    """
    def __init__(self):
        """Construct all the necessary attributes"""
        self.parser = argparse.ArgumentParser(
            prog='crypter.py',
            description='Application to encrypt files',
        )
        self.args = None

    def _load_arguments(self):
        """Init arguments"""
        self.parser.add_argument(
            '-m',
            '--mode',
            choices=['encrypt', 'decrypt', 'append'],
            required=True,
            help="""encrypt given file or files;
            decrypt encrypted file or files;
            append -> decrypt file, append text and encrypt the file again""",
        )
        self.parser.add_argument(
            '-p',
            '--password',
            metavar='PASSWORD',
            required=True,
            help='Password to encrypt or decrypt',
        )
        self.parser.add_argument(
            '-v',
            '--verbose',
            action='count',
            default=0,
            help='Verbose mode',
        )
        file_group = self.parser.add_mutually_exclusive_group(required=True)
        file_group.add_argument(
            '--file',
            help='The path to the name of the file with data to be processed',
        )
        file_group.add_argument(
            '--folder',
            help='The path to the folder with files to be processed',
        )
        self.parser.add_argument(
            '-e',
            '--extension',
            choices=FILE_TYPES,
            default=FILE_TYPES,
            nargs='+',
            help="""The extensions of files to be processed.
                 All supported extensions are processed by default""",
        )

        self.args = self.parser.parse_args()

    def _set_verbose_mode(self):
        """Set verbose mode"""
        log_levels = [logging.NOTSET, logging.DEBUG, logging.INFO]
        level = log_levels[min(self.args.verbose, len(log_levels) - 1)]
        logging.basicConfig(level=level)
        print(level)

    @classmethod
    def load(cls):
        """Classmethod to init arguments and set verbose mode

        Returns:
            (object): main object
        """
        app = cls()
        app._load_arguments()
        app._set_verbose_mode()

        return app


if __name__ == '__main__':
    app = Main().load()
    crypter = Crypter(app.args.password)
    crypter_mode = getattr(crypter, app.args.mode)

    if app.args.folder:
        for directory in os.walk(app.args.folder):
            for file in directory[2]:
                if os.path.splitext(file)[1] in app.args.extension:
                    crypter_mode(f'{directory[0]}/{file}')

    if app.args.file:
        if os.path.isfile(app.args.file):
            crypter_mode(app.args.file)
        else:
            print('File not exist')
