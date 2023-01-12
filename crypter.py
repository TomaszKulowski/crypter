import itertools
import os.path

from file_management import FileFactory
from protection import Protection


class Crypter:
    def __init__(self, password, remove_parent_file=False):
        self.password = password
        self.remove_parent_file = remove_parent_file

    def encrypt(self, file_path: str):
        file = FileFactory.get_file(file_path)
        data = file.load()
        encrypted_data = Protection(self.password).encrypt(data)
        if self.remove_parent_file:
            os.remove(file_path)
        #: change the extension to the encrypted file
        file.filename += '.cr'
        file.save(encrypted_data)

    def decrypt(self, file_path: str):
        file = FileFactory.get_file(file_path)
        data = file.load()
        decrypted_data = Protection(self.password).decrypt(data)
        if self.remove_parent_file:
            os.remove(file_path)
        _, file_extension = os.path.splitext(file_path)
        #: remove .cr extension
        file.file_path = file.file_path[:-len(file_extension)]
        file.save(decrypted_data)

    def append(self, path_to_encrypted_file, path_to_unencrypted_file):
        protection = Protection(self.password)

        encrypted_file = FileFactory.get_file(path_to_encrypted_file)
        encrypted_data = encrypted_file.load()
        decrypted_data = protection.decrypt(encrypted_data)
        unencrypted_file = FileFactory.get_file(path_to_unencrypted_file)
        unencrypted_data = unencrypted_file.load()
        result = decrypted_data + unencrypted_data
        encrypted_file.save(result)
