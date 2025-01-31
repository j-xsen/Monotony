from objects.player.stat import Stat

import unittest

class TestStat(unittest.TestCase):
    def test_add_overflow(self):
        high_value = Stat(98)
        high_value += 25
        self.assertEqual(high_value.value, 100)

    def test_add_max(self):
        high_value = Stat(100)
        high_value += 100
        self.assertEqual(high_value.value, 100)

    def test_add_negative_overflow(self):
        low_value = Stat(0)
        low_value += -50
        self.assertEqual(low_value.value, 0)

    def test_sub_overflow(self):
        low_value = Stat(2)
        low_value -= 25
        self.assertEqual(low_value.value, 0)

    def test_sub_min(self):
        low_value = Stat(0)
        low_value -= 100
        self.assertEqual(low_value.value, 0)

    def test_sub_negative_overflow(self):
        high_value = Stat(100)
        high_value -= -50
        self.assertEqual(high_value.value, 100)


if __name__ == '__main__':
    unittest.main()
