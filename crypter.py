from protection import Protection


class Crypter:
    def __init__(self):
        pass

    @staticmethod
    def _read_data(filename) -> str:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()

    @staticmethod
    def _save_data(filename, data: str):
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(data)

    def encrypt(self, password, filename: str):
        data = self._read_data(filename)
        encrypted_data = Protection(password).encrypt(data)
        self._save_data(filename + '.cr', encrypted_data)

    def decrypt(self, password):
        pass

    def append(self):
        pass
