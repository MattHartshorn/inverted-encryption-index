import unittest
from src.keygen import generate

class TestKeyGen(unittest.TestCase):
    def test_generate_zero(self):
        with self.assertRaises(ValueError):
            generate(0)

    def test_generate_noparam(self):
        self.assertEqual(len(generate()), 32)

    def test_generate_128(self):
        self.assertEqual(len(generate(128)), 16)

    def test_generate_192(self):
        self.assertEqual(len(generate(192)), 24)

    def test_generate_256(self):
        self.assertEqual(len(generate(256)), 32)
