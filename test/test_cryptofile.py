import unittest
from src.cryptofile import CryptoFile
from src import keygen
from .helper import testFile

class TestCryptoFile(unittest.TestCase):
    hello_content = (testFile("data"), "hello_there.txt", "General Kenobi!")

    def test_filename_none(self):
        with self.assertRaises(TypeError):
            f = CryptoFile()
            f.read(None)

    def test_filename_empty(self):
        with self.assertRaises(IOError):
            CryptoFile("")

    def test_filename_notExist(self):
        with self.assertRaises(IOError):
            CryptoFile(testFile("data/test.txt"))
        
    def test_filename_dir(self):
        with self.assertRaises(IOError):
            CryptoFile(testFile("data"))

    def test_filename_read(self):
        f = CryptoFile(testFile("data/hello_there.txt"))
        self.assertEqual((f.path, f.filename, f.content), self.hello_content)

    def test_filename_read_empty(self):
        f = CryptoFile(testFile("data/empty.txt"))
        self.assertEqual(f.content, "")

    def test_filename_write_read(self):
        key = keygen.generate()
        f = CryptoFile(testFile("data/hello_there.txt"))

        ofile = testFile("out/hello_there.out")
        f.write(ofile, key)
        f2 = CryptoFile(ofile, key)
        
        self.assertEqual((f2.path, f2.filename, f2.content), self.hello_content)