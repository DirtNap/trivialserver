import unittest
import fizz_engine

class TestFizzEngine(unittest.TestCase):

    def setUp(self):
        self.fizz_engine = fizz_engine.FizzEngine(5)

    def test_get_fizz(self):

        self.assertEqual(list(self.fizz_engine.get_fizz(15)),
                         ["1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8",
                          "Fizz", "Buzz", "11", "Fizz", "13", "14", "Fizz Buzz"])

        self.assertEqual(5, self.fizz_engine.max_size)
        self.fizz_engine.get_fizz(15, ('a', 'b', 'c', 'd', 'e', 'f'))
        with self.assertRaises(ValueError):
            list(self.fizz_engine.get_fizz(15, ('a', 'b', 'c', 'd', 'e', 'f')))
