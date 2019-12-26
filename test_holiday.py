import unittest
from datetime import datetime
from holiday import is_holiday

class HolidayTestCase(unittest.TestCase):
    def test_holiday(self):
        self.assertEqual(is_holiday('2019-10-10'), False)
        self.assertEqual(is_holiday('2019-10-1'), True)
        self.assertEqual(is_holiday('2019-10-12'), False)
        self.assertEqual(is_holiday('2019-12-22'), True)
        self.assertEqual(is_holiday('2020-1-1'), True)
        self.assertEqual(is_holiday('2020-2-1'), False)
        self.assertEqual(is_holiday('2020-4-5'), True)
        self.assertEqual(is_holiday('2020-10-10'), False)

if __name__ == '__main__':
    unittest.main()