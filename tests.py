import unittest
import ex3_Or_Othnay_Tal_Aharon


class FirstTest(unittest.TestCase):
    def runTest(self):
        self.assertEqual(True, True)  # add assertion here


class SecondTest(unittest.TestCase):
    def runTest(self):
        self.assertEqual(False, False)


if __name__ == '__main__':
    unittest.main()
