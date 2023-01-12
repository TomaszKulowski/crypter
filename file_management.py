import sys
from abc import ABC, abstractmethod
import os
from json import dump, load


class File(ABC):
    def __init__(self, filename):
        self.filename = filename

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def save(self, data):
        pass


class TXTFile(File):
    def load(self):
        with open(self.filename, 'r', encoding='utf-8') as file:
            return file.read()

    def save(self, data):
        with open(self.filename, 'w', encoding='utf-8') as file:
            file.write(data)


class CRFile(File):
    def load(self):
        with open(self.filename, 'r', encoding='utf-8') as file:
            return file.read()

    def save(self, data):
        with open(self.filename, 'w', encoding='utf-8') as file:
            file.write(data)


class JSONFile(File):
    def load(self):
        with open(self.filename, 'r', encoding='utf-8') as file:
            return file.read()

    def save(self, data):
        with open(self.filename, 'w', encoding='utf-8') as file:
            file.write(data)


class FileFactory:
    @staticmethod
    def get_file(filename):
        _, file_extension = os.path.splitext(filename)
        class_name = getattr(sys.modules[__name__], file_extension[1:].upper() + 'File')
        return class_name(filename)
