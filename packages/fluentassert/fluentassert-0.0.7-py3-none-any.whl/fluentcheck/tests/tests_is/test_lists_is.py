import unittest

from fluentcheck import Is
from fluentcheck.exceptions import CheckError


class TestIsListsAssertions(unittest.TestCase):

    def test_is_contains_chars_only_pass(self):
        obj = ['abyss', 'apple']
        pattern = "apple"
        with self.assertRaises(CheckError):
            Is(obj).list_contains(pattern)
