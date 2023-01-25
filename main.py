"""Encypting files application"""
import argparse
import logging
import os
import sys

from tools.crypter import Crypter
from tools.exceptions import ArgumentException

# The .cr extension belongs to encrypted files
FILE_TYPES = ['.txt', '.cr', '.json', '.csv']


class Main:
    """Main class of the crypter application.

    Methods:
         load(): classmethod to init arguments and set verbose mode
    """
    def __init__(self):
        """Construct all the necessary attributes"""
        self.parser = argparse.ArgumentParser(
            prog='crypter.py',
            description='Encypting files application',
        )
        self.args = None

    def _load_arguments(self):
        """Init arguments"""
        self.parser.add_argument(
            '-m',
            '--mode',
            choices=['encrypt', 'decrypt', 'append'],
            required=True,
            metavar='',
            help="""Available modes: encrypt, decrypt, append;
            encrypt given file or files;
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
            nargs='+',
            help="""The extensions of files to be processed.
                 All supported extensions are processed by default""",
        )

        self.args = self.parser.parse_args()

    def _set_default_extensions(self):
        """Set default the file extensions.
        Not used "default" option in extension implementation,
        because there are some dependence.
        """
        if not self.args.extension and self.args.mode == 'decrypt':
            self.args.extension = ['.cr']
        else:
            self.args.extension = FILE_TYPES

    def _validate_arguments(self):
        """Validate the passed arguments."""
        if self.args.file and self.args.extension:
            raise ArgumentException('argument --file not allowed with argument --extension')

        if self.args.mode == 'decrypt' and None is not self.args.extension != ['.cr']:
            raise ArgumentException('argument --mode decrypt not allowed with argument --extension')

    def _set_verbose_mode(self):
        """Set verbose mode."""
        log_levels = [logging.NOTSET, logging.DEBUG, logging.INFO]
        level = log_levels[min(self.args.verbose, len(log_levels) - 1)]
        logging.basicConfig(level=level)
        print(level)

    @classmethod
    def load(cls):
        """Classmethod to init arguments and set verbose mode.

        Returns:
            (object): main object
        """
        app = cls()
        app._load_arguments()
        app._validate_arguments()
        app._set_verbose_mode()
        app._set_default_extensions()

        return app


if __name__ == '__main__':
    try:
        application = Main().load()
    except ArgumentException as error:
        print(error)
        sys.exit()
    crypter = Crypter(application.args.password)
    crypter_mode = getattr(crypter, application.args.mode)

    if application.args.folder:
        for directory in os.walk(application.args.folder):
            for file in directory[2]:
                if os.path.splitext(file)[1].lower() in application.args.extension:
                    crypter_mode(f'{directory[0]}/{file}')

    if application.args.file:
        if os.path.isfile(application.args.file):
            crypter_mode(application.args.file)
        else:
            print('File not exist')
