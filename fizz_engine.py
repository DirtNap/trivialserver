"""A class to produce FizzBuzz-like results."""
import gmpy2

class FizzEngine(object):

    def __init__(self, max_size=64):
        if max_size < 1:
            raise AttributeError("max_size can not be negative.")

        self.max_size = max_size
        current = 3
        self._primes = [current]
        while len(self._primes) < self.max_size:
            current = int(gmpy2.next_prime(current))
            self._primes.append(current)

    def get_fizz(self, size, words=("Fizz", "Buzz")):
        """Process numbers with Fizz Buzz.

        This function generates a sequential list of integers, except that each
        integer is checked to see if it is a multiple of several consecutive
        prime numbers.  If so, the number ir replaced by some arbitrary string
        for each such prime factor.

        Arguments:
          size:  The count of numbers to process, indicating the length of the
                 generated iterator.
          words: A sequence of strings which should be used as replacement terms.
                 The first provided term will replace 3 and its multiples.  The
                 second term will replace 5, the third 7, then 11, and so on.

        Returns:
          A generator which yields the processed sequence.

        Raises:
          ValueError:  When the size of "words" is greater than
                       FizzEngine.max_size.
        """

         if len(words) > self.max_size:
            raise ValueError("Replacement of %d terms exceeds maximum of %d." % (
                len(words), self.max_size))

        terms = list(zip(words, self._primes))

        for i in range(1, size + 1):
            match = []
            if i > 2:
                for (w, p) in terms:
                    if i % p == 0:
                        match.append(w)
            if match:
                yield " ".join(match)
            else:
                yield str(i)
