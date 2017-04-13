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


    def test_object(self):
        fe = fizz_engine.FizzEngine(10)
        self.assertEqual(10, len(fe._primes))
        for illegal_size in (0, -1):
            with self.assertRaises(ValueError):
                fe = fizz_engine.FizzEngine(illegal_size)


class TestFizzFactory(unittest.TestCase):

    def setUp(self):
        fizz_engine._ENGINE_CACHE.clear()

    def test_fizz_factory(self):
        self.assertEqual(0, len(fizz_engine._ENGINE_CACHE))

        fe1 = fizz_engine.fizz_factory(1)
        self.assertEqual(1, len(fizz_engine._ENGINE_CACHE))
        fizz_engine.fizz_factory(1)
        self.assertEqual(1, len(fizz_engine._ENGINE_CACHE))
        fe2 = fizz_engine.fizz_factory(2)
        self.assertEqual(2, len(fizz_engine._ENGINE_CACHE))
        self.assertEqual(fe1, fizz_engine.fizz_factory(1))
