import unittest
import peak_detection


class TestPeakDetection(unittest.TestCase):
    def test_import_data(self):
        pass

    def test_buttworth_filter(self):
        pass

    def test_generate_all_attempts(self):
        pass

    def test_find_saturated_abs_peaks(self):
        pass

    def test_find_error_peaks(self):
        pass

    def test_error_filter(self):
        pass

    def test_shift(self):
        self.assertListEqual(
            peak_detection.shift([0, 1, 2, 3, 4, 5, 6]), [-6, -5, -4, -3, -2, -1, 0]
        )

    def test_get_thumb(self):
        x = [i for i in range(100)]
        self.assertEqual(peak_detection.get_thumb(x), 99)


if __name__ == "__main__":
    unittest.main()
