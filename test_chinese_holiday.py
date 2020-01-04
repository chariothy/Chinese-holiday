import unittest
from datetime import datetime
from chinese_holiday import is_holiday

class HolidayTestCase(unittest.TestCase):
    def test_holiday(self):
        self.assertFalse(is_holiday('2019-10-10'))
        self.assertTrue(is_holiday('2019-10-1'))
        self.assertFalse(is_holiday('2019-10-12'))
        self.assertTrue(is_holiday('2019-12-22'))
        self.assertTrue(is_holiday('2020-1-1'))
        self.assertFalse(is_holiday('2020-2-1'))
        self.assertTrue(is_holiday('2020-4-5'))
        self.assertFalse(is_holiday('2020-10-10'))

if __name__ == '__main__':
    unittest.main()