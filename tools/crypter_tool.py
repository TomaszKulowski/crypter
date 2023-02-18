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

    def encrypt(self, file_path: str):
        """Encrypt the data in the passed file.

        Args:
            file_path (str): path to the file
        """
        file = File()
        file.file_path = file_path
        data = file.load()
        encrypted_data = Protection(self.password).encrypt(data)
        if self.remove_parent_file:
            os.remove(file_path)
        #: change the extension to the encrypted file
        file.file_path = file_path + '.cr'
        file.save(encrypted_data)

    def decrypt(self, file_path: str):
        """Decrypt the data in the passed file.

        Args:
            file_path (str): path to the file
        """
        file = File()
        file.file_path = file_path
        data = file.load()
        decrypted_data = Protection(self.password).decrypt(data)
        if self.remove_parent_file:
            os.remove(file_path)
        _, file_extension = os.path.splitext(file_path)
        #: remove .cr extension
        file.file_path = file.file_path[:-len(file_extension)]
        file.save(decrypted_data)

    def append(self, files: list):
        """Decrypt the passed encrypted file,
        append the data from the passed unencrypted file,
        and encrypt the file again.

        Args:
            files(list): with encrypted and unencrypted file path
        """
        protection = Protection(self.password)
        file = File()

        # load data from the unencrypted file
        file.file_path = list(file for file in files if not file.endswith('.cr'))[0]
        unencrypted_data = file.load()

        if self.remove_parent_file:
            os.remove(file.file_path)

        # load data from the encrypted file
        file.file_path = list(file for file in files if file.endswith('.cr'))[0]
        encrypted_data = file.load()

        # decrypt the data and append it to the unencrypted data,
        # protect it, and save it to the file
        decrypted_data = protection.decrypt(encrypted_data)
        encrypted_result = protection.encrypt(decrypted_data + unencrypted_data)
        file.save(encrypted_result)
