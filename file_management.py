import sys
from abc import ABC, abstractmethod
import os
from json import dump, load


class File(ABC):
    def __init__(self, file_path):
        self.file_path = file_path

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def save(self, data):
        pass


class TXTFile(File):
    def load(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def save(self, data):
        with open(self.file_path, 'w', encoding='utf-8') as file:
            file.write(data)


class CRFile(File):
    def load(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def save(self, data):
        with open(self.file_path, 'w', encoding='utf-8') as file:
            file.write(data)


class JSONFile(File):
    def load(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def save(self, data):
        with open(self.file_path, 'w', encoding='utf-8') as file:
            file.write(data)


class FileFactory:
    @staticmethod
    def get_file(filename):
        _, file_extension = os.path.splitext(filename)
        class_name = getattr(sys.modules[__name__], file_extension[1:].upper() + 'File')
        return class_name(filename)
