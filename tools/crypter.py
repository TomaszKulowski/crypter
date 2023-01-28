"""The collection of the tools for encrypt and decrypt data in the file,
and append new data to the encrypted file."""
import os.path

from tools.file_management import File
from tools.protection import Protection


class Crypter:
    """The collections of tools to operate on files.

    Methods:
        encrypt(file_path: str): encrypt data in the passed file
        decrypt(file_path: str): decrypt data from the passed file
        append(path_to_encrypted_file, path_to_unencrypted_file): append new data to encrypted file
    """
    def __init__(self, password: str, remove_parent_file: bool = False):
        """Construct all the necessary attributes for the crypter object.

        Args:
            password (str): password to encrypt or decrypt the data
            remove_parent_file (bool): remove the original file after operation
        """
        self.password = password
        self.remove_parent_file = remove_parent_file
        self.file_path = None

    def encrypt(self, file_path: str):
        """Encrypt the data in the passed file.

        Args:
            file_path (str): path to the file
        """
        self.file_path = file_path
        file = File(self.file_path)
        data = file.load()
        encrypted_data = Protection(self.password).encrypt(data)
        if self.remove_parent_file:
            os.remove(self.file_path)
        #: change the extension to the encrypted file
        self.file_path += '.cr'
        file.file_path += self.file_path
        file.save(encrypted_data)

    def decrypt(self, file_path: str):
        """Decrypt the data in the passed file.

        Args:
            file_path (str): path to the file
        """
        self.file_path = file_path
        file = File(file_path)
        data = file.load()
        decrypted_data = Protection(self.password).decrypt(data)
        if self.remove_parent_file:
            os.remove(self.file_path)
        _, file_extension = os.path.splitext(file_path)
        #: remove .cr extension
        self.file_path = file.file_path[:-len(file_extension)]
        file.file_path = self.file_path
        file.save(decrypted_data)

    def append(self, path_to_encrypted_file: str, path_to_unencrypted_file: str):
        """Decrypt the passed encrypted file,
        append the data from the passed unencrypted file,
        and encrypt the file again.

        Args:
            path_to_encrypted_file (str): path to the encrypted file
            path_to_unencrypted_file (str): path with unencrypted data
        """
        protection = Protection(self.password)

        encrypted_file = File(path_to_encrypted_file)
        encrypted_data = encrypted_file.load()
        decrypted_data = protection.decrypt(encrypted_data)
        unencrypted_file = File(path_to_unencrypted_file)
        unencrypted_data = unencrypted_file.load()
        encrypted_result = protection.encrypt(decrypted_data + unencrypted_data)
        if self.remove_parent_file:
            os.remove(path_to_unencrypted_file)
        encrypted_file.save(encrypted_result)
