import json


class DataExtractor:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_file(self):
        with open(self.file_path, "r") as file:
            return file.read()

    def extract_data(self):
        raise NotImplementedError


class TxtDataExtractor(DataExtractor):
    def extract_data(self):
        content = self.read_file()
        return content


class JsonDataExtractor(DataExtractor):
    def extract_data(self):
        content = self.read_file()
        return json.loads(content)
