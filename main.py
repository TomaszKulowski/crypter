import argparse
import logging
import os

from protection import Protection


class Main:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog='crypter.py',
            description='Application to encrypt text',
        )
        self.args = None

    def _load_arguments(self):
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
            help='Password to encrypt or decrypt'
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
            help='The path to the name of the file with data to be processed'
        )
        file_group.add_argument(
            '--folder',
            help='The path to the folder with files to be processed'
        )

        self.args = self.parser.parse_args()

    def _set_verbose_mode(self):
        log_levels = [logging.NOTSET, logging.DEBUG, logging.INFO]
        level = log_levels[min(self.args.verbose, len(log_levels) - 1)]
        logging.basicConfig(level=level)
        print(level)

    @classmethod
    def load(cls):
        app = cls()
        app._load_arguments()
        app._set_verbose_mode()

        return app


if __name__ == '__main__':
    app = Main().load()
    protection = Protection(app.args.password)
    protection_mode = getattr(protection, app.args.mode)
    with open(app.args.file) as file:
        pass

    # if app.args.folder:
    #     os.walk()
    # mode(app.args.)
