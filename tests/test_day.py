import unittest

from objects.clock import Day


class TestDay(unittest.TestCase):
    def test_day_set(self):
        new_day = Day()
        new_day.set(2)
        self.assertEqual(new_day.index, 2)

    def test_day_forward(self):
        new_day = Day()
        new_day.forward()
        self.assertEqual(new_day.index, 2)


if __name__ == '__main__':
    unittest.main()
