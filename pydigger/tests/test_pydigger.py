from unittest import TestCase

import pydigger

class TestHi(TestCase):
    def test_is_string(self):
        s = pydigger.hi()
        self.assertEqual(s, "Hi from PyDigger")

