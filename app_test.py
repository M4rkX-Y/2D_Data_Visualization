import unittest
import numpy as np
from data_structure import Data, Butlr32_Data, Esoil_Data
from visualizer import PixelMap, SmoothPixelMap

DISPLAY_SIZE = 576
DISPLAY_POSITION = 40, 120
WHITE = 255, 255, 255


class TestingDataStructure(unittest.TestCase):
    def testDataConstruct(self):
        temp_class = Data("./data/2ppl_1_32x32_sensor.txt")
        self.assertEqual(temp_class.dimension, "32x32")
        self.assertEqual(temp_class.type, "txt")
        self.assertEqual(temp_class.file_path, "./data/2ppl_1_32x32_sensor.txt")

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

    def testESOIL(self):
        temp_class = Esoil_Data("./data/11_15_3x3_5.npy")
        self.assertEqual(temp_class.get_length(), 174)
        self.assertEqual(
            len(temp_class.pop_frame()), int(temp_class.dimension.split("x")[0])
        )
        self.assertEqual(temp_class.pop_frame().max(), 1)
        self.assertEqual(temp_class.pop_frame().min(), 0)


class TestingVisualizater(unittest.TestCase):
    def testPixelMap(self):
        array = np.random.random((20, 20))
        temp_class = PixelMap(array)
        self.assertEqual(temp_class.pixel_size, DISPLAY_SIZE / 20)
        self.assertEqual(len(temp_class.pixels), 20 * 20)
        self.assertEqual(
            temp_class.pixels[0].color, tuple(array[0][0] * x for x in WHITE)
        )

    def testSmoothPixelMap(self):
        array = np.random.random((45, 45))
        temp_class = SmoothPixelMap(array)
        self.assertEqual(temp_class.pixel_size, DISPLAY_SIZE / (45 * 2))
        self.assertEqual(len(temp_class.pixels), 10125)


if __name__ == "__main__":
    unittest.main()
