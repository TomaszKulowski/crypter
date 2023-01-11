import base64

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend


class Protection:
    def __init__(self, password):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            salt=b"\xfa\xb5\xf2\xaa\x8a\xc2",
            iterations=1024,
            length=32,
            backend=default_backend(),
        )

        self.key = Fernet(base64.urlsafe_b64encode(kdf.derive(bytes(password, 'utf-8'))))

    def encrypt(self, data: str) -> str:
        return self.key.encrypt(bytes(data, 'utf-8')).decode('utf-8')

    def decode(self, data: str) -> str:
        return self.key.decrypt(bytes(data, 'utf-8')).decode('utf-8')
