import json
import unittest

import faker

import fizz_engine
import fizz_server


class Error(Exception):
    pass


class HTTPError(Error):
    pass


class TestFizz(unittest.TestCase):

    def setUp(self):
        fizz_server.app.config["MAX_TERMS"] = 10
        self.app = fizz_server.app.test_client()
        self.fizz = fizz_engine.fizz_factory(10)
        self.fake = faker.Factory.create()

    def runFizzPath(self, path):
        result = self.app.get(path)
        if result.status_code != 200:
            raise HTTPError("Got response code %d when fetching path %s" % (
                result.status_code, path))
        ret_val = ""
        if result.get_data():
            ret_val = json.loads(result.get_data())
        return ret_val

    def test_fizz(self):

        # Test the null case
        self.assertEqual("", self.runFizzPath("/"))

        # Test normal operation for depths 1 through 10
        for term_count in range(1,11):
            for return_count in range(24, 1024):
                words = self.fake.words(term_count)
                path = "/%s/%d" % ("/".join(words), return_count)
                result = self.runFizzPath(path)
                # Path should register correctly
                self.assertEqual(path[1:], result["path"])
                # No Errors should be generated
                self.assertEqual([], result["errors"])
                # No Warnings should be generated
                self.assertFalse("warnings" in result)
                # The result should match calling the engine directly
                self.assertEqual(list(self.fizz.get_fizz(return_count, words)),
                                 result["data"])

        # Test warnings
        words = ["fizz", "", "buzz"]
        path = "/%s/%d" % ("/".join(words), return_count)
        result = self.runFizzPath(path)
        # Path should register correctly
        self.assertEqual(path[1:], result["path"])
        # No Errors should be generated
        self.assertEqual([], result["errors"])
        # One Warnings should be generated
        self.assertEqual(1, len(result["warnings"]))
        # The result should match calling the engine directly
        self.assertEqual(list(self.fizz.get_fizz(return_count, words)),
                         result["data"])

        # Test errors
        # Errors occur when either no terms or no count are provided, or
        # when the count is malformed.
        for path in ("/fizz/buzz", "/123", "/fizz/123/buzz"):
            result = self.runFizzPath(path)
            # Path should register correctly
            self.assertEqual(path[1:], result["path"])
            # One Error should be generated
            self.assertEqual(1, len(result["errors"]))
            # No Warnings should be generated
            self.assertFalse("warnings" in result)
            # The result should be empty
            self.assertEqual(None, result["data"])
