import unittest

import base


class TestClock(unittest.TestCase):
    def setUp(self):
        self.monotony = base.Monotony(debug=True)

    def tearDown(self):
        self.monotony.destroy()

    def test_clock_start(self):
        self.assertEqual(taskMgr.hasTaskNamed("RunClock"), True)

    def test_clock_toggle_off(self):
        # Clock running
        self.monotony.clock.double_pause = False
        self.monotony.clock.paused = False

        # toggle
        self.monotony.clock.toggle_clock()
        self.assertEqual(self.monotony.clock.paused, True)

    def test_clock_toggle_on(self):
        # Clock off
        self.monotony.clock.double_pause = False
        self.monotony.clock.paused = True

        # toggle
        self.monotony.clock.toggle_clock()

        self.assertEqual(self.monotony.clock.paused, False)



if __name__ == '__main__':
    unittest.main()
