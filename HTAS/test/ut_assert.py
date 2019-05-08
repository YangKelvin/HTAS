import unittest

class AssertTest(unittest.TestCase):

    def test_equal(self):
        EXPECT = 'abc'
        ACTUAL = 'abc'
        self.assertEqual(EXPECT, ACTUAL)

if __name__ == '__main__':
    unittest.main()