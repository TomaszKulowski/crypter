class File:
    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def save(self, data):
        with open(self.file_path, 'w', encoding='utf-8') as file:
            file.write(data)
