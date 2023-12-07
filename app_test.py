import unittest
import numpy as np
from data_structure import Data, Butlr32_Data, Esoil_Data, Butlr32_Parser
from visualizer import Pixel, PixelMap, SmoothPixelMap

DISPLAY_SIZE = 576
DISPLAY_POSITION = 40, 120
WHITE = 255, 255, 255


class TestingData(unittest.TestCase):
    def testDataConstruct(self):
        temp_class = Data("./data/2ppl_1_32x32_sensor.txt")
        self.assertEqual(temp_class.dimension, "32x32")
        self.assertEqual(temp_class.type, "txt")
        self.assertEqual(temp_class.file_path, "./data/2ppl_1_32x32_sensor.txt")


class TestingButlr32(unittest.TestCase):
    def testButlr32(self):
        temp_class = Butlr32_Data("./data/2ppl_1_32x32_sensor.txt")
        self.assertEqual(temp_class.get_length(), 2706)
        self.assertEqual(
            len(temp_class.pop_frame()), int(temp_class.dimension.split("x")[0])
        )
        self.assertEqual(temp_class.get_length(), 2705)
        self.assertEqual(temp_class.pop_frame().max(), 1)
        self.assertEqual(temp_class.pop_frame().min(), 0)
        self.assertEqual(temp_class.get_length(), 2703)


class TestingButlr32Parser(unittest.TestCase):
    def testButlrParser(self):
        temp_class = Data("./data/standing_9_32x32_sensor.txt")
        dim = int(temp_class.dimension.split("x")[0])
        raw = temp_class.read_file()
        data = Butlr32_Parser().parse_raw(raw)
        self.assertEqual(len(data[0]), len(data[2]))
        self.assertEqual(len(data[1]), len(data[3]))
        frame1 = Butlr32_Parser().parse_frame(data[0])
        frame2 = Butlr32_Parser().parse_frame(data[1])
        self.assertEqual(np.shape(frame1), (dim, dim))
        self.assertEqual(np.shape(frame2), (dim, dim))


class TestingESOIL(unittest.TestCase):
    def testESOIL(self):
        temp_class = Esoil_Data("./data/11_15_3x3_5.npy")
        dim = int(temp_class.dimension.split("x")[0])
        self.assertEqual(temp_class.get_length(), 174)
        self.assertEqual(len(temp_class.pop_frame()), dim)
        self.assertEqual(temp_class.pop_frame().max(), 1)
        self.assertEqual(temp_class.pop_frame().min(), 0)


class TestingPixel(unittest.TestCase):
    def testPixel(self):
        x = 10
        y = 20
        size = 40
        temp_class = Pixel(x, y, WHITE, size)
        self.assertEqual(temp_class.color, WHITE)


class TestingPixelMap(unittest.TestCase):
    def testPixelMap(self):
        array = np.random.random((20, 20))
        temp_class = PixelMap(array)
        self.assertEqual(temp_class.pixel_size, DISPLAY_SIZE / 20)
        self.assertEqual(len(temp_class.pixels), 20 * 20)
        self.assertEqual(
            temp_class.pixels[0].color, tuple(array[0][0] * x for x in WHITE)
        )


class TestingSmoothPixelMap(unittest.TestCase):
    def testSmoothPixelMap(self):
        array = np.random.random((45, 45))
        temp_class = SmoothPixelMap(array)
        self.assertEqual(temp_class.pixel_size, DISPLAY_SIZE / (45 * 2))
        self.assertEqual(len(temp_class.pixels), 10125)


if __name__ == "__main__":
    unittest.main()
