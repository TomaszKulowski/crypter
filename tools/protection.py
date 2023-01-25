"""The collection of the tools for encrypt and decrypt data."""
import base64

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend


class Protection:
    """The collection of the tools for encrypt and decrypt data.

    Methods:
        encrypt(data: str) -> str: return encrypted passed data
        decrypt(data: str) -> str: return decrypted passed encrypted data
    """
    def __init__(self, password: str):
        """Construct all the necessary attributes for the protection object.

        Args:
            password (str): password to encrypt or decrypt data
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            salt=b"\xfa\xb5\xf2\xaa\x8a\xc2",
            iterations=1024,
            length=32,
            backend=default_backend(),
        )

        self.key = Fernet(base64.urlsafe_b64encode(kdf.derive(bytes(password, 'utf-8'))))

    def encrypt(self, data: str) -> str:
        """Encrypt the passed data.

        Args:
            data (str): data to encrypt

        Returns:
             (str): with encrypted data
        """
        return self.key.encrypt(bytes(data, 'utf-8')).decode('utf-8')

    def decrypt(self, data: str) -> str:
        """Encrypt the passed data.

        Args:
            data (str): encrypted data to decrypt

        Returns:
             (str): with decrypted data
        """
        return self.key.decrypt(bytes(data, 'utf-8')).decode('utf-8')
