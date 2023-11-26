import json


class Data:
    def __init__(self, file_path):
        self.file_path = file_path
        raw_data = self.read_file()
        data = Butlr32_Parser().parse_raw(raw_data)
        self.data = data

    def read_file(self):
        with open(self.file_path, "r") as file:
            return file.read()

    def pop_frame(self):
        raw_frame = self.data.pop(0)
        frame = Butlr32_Parser().parse_frame(raw_frame)
        return frame

    def get_length(self):
        return len(self.data)


class Butlr32_Parser:
    def parse_raw(self, raw_data):
        if not raw_data:
            raise Exception
        filtered_data = [
            data for data in raw_data.replace(", b", "").split('"')[1:] if data
        ]
        return filtered_data

    def parse_frame(self, raw_frame):
        clean_frame = (
            raw_frame.replace(",)", "")[1:].replace("'", '"').replace("       ", "")
        )
        frame = json.loads(clean_frame.split("array(")[1].split("),")[0])
        return frame


txt = Data("data\\standing_9_32x32_sensor.txt")
print(txt.pop_frame())
