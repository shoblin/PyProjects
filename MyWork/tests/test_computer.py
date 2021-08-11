import unittest
import Computers as cmp


class MyTestCase(unittest.TestCase):
    def test_correct_timezone(self):
        test_computer = cmp.Computer('Fra-Test01-tr01.')

        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
