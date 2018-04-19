import unittest
from src import token

class TestToken(unittest.TestCase):
    def test_typeError(self):
        with self.assertRaises(TypeError):
            token.create(["hello", "there"])
        
    def test_bytes(self):
        res = token.create(bytes(list(range(255))))
        self.assertEqual(len(res), 64)

    def test_bytes_empty(self):
        res = token.create(bytes([]))
        self.assertEqual(len(res), 64)

    def test_string_empty(self):
        res = token.create("")
        self.assertEqual(len(res), 64)

    def test_equality(self):
        res1 = token.create("hello world")
        res2 = token.create("hello world")
        self.assertEqual(res1, res2)

    def test_inequality(self):
        res1 = token.create("Hello there!")
        res2 = token.create("General Kenobi.")
        self.assertNotEqual(res1, res2)