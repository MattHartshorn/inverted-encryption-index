import unittest
from src import aescypher
from src import keygen

class TestAesCypher(unittest.TestCase):
    plaintext = "0123456789abcdef".encode()

    def test_encrypt_notEqual(self):
        key = keygen.generate()
        cyphertext = aescypher.encrypt(self.plaintext, key)[0]
        self.assertNotEqual(self.plaintext, cyphertext)

    def test_encrypt(self):
        key = keygen.generate()
        cyphertext = aescypher.encrypt(self.plaintext, key)[0]
        self.assertNotEqual(self.plaintext, cyphertext)

    def test_encrypt_givenIV(self):
        key = keygen.generate()
        iv = keygen.generate(128)
        ivOutput = aescypher.encrypt(self.plaintext, key, iv)[1]
        self.assertEqual(iv, ivOutput)

    def test_encrypt_key128(self):
        key = keygen.generate(128)
        cyphertext = aescypher.encrypt(self.plaintext, key)[0]
        self.assertNotEqual(self.plaintext, cyphertext)

    def test_encrypt_key192(self):
        key = keygen.generate(192)
        cyphertext = aescypher.encrypt(self.plaintext, key)[0]
        self.assertNotEqual(self.plaintext, cyphertext)

    def test_encrypt_emptyPlaintext(self):
        key = keygen.generate()
        cyphertext = aescypher.encrypt("".encode(), key)[0]
        self.assertNotEqual(self.plaintext, cyphertext)

    def test_encrypt_blockSizeMismtch(self):
        key = keygen.generate()
        plaintext = "test".encode()
        cyphertext = aescypher.encrypt(plaintext, key)[0]
        self.assertNotEqual(plaintext, cyphertext)


    def test_decrypt(self):
        key = keygen.generate()
        cyphertext, iv = aescypher.encrypt(self.plaintext, key)        
        res = aescypher.decrypt(cyphertext, key, iv)
        self.assertEqual(self.plaintext, res)

    def test_decrypt_givenIV(self):
        key = keygen.generate()
        iv = keygen.generate(128)
        cyphertext = aescypher.encrypt(self.plaintext, key, iv)[0]        
        res = aescypher.decrypt(cyphertext, key, iv)
        self.assertEqual(self.plaintext, res)

    def test_decrypt_invalidKey(self):
        key = keygen.generate()
        cyphertext, iv = aescypher.encrypt(self.plaintext, key)

        invalid_key = keygen.generate()
        while (invalid_key == key):
            invalid_key = keygen.generate()
        
        res = aescypher.decrypt(cyphertext, invalid_key, iv)
        self.assertNotEqual(self.plaintext, res)

    def test_decrypt_key128(self):
        key = keygen.generate(128)
        cyphertext, iv = aescypher.encrypt(self.plaintext, key)        
        res = aescypher.decrypt(cyphertext, key, iv)
        self.assertEqual(self.plaintext, res)

    def test_decrypt_key192(self):
        key = keygen.generate(192)
        cyphertext, iv = aescypher.encrypt(self.plaintext, key)        
        res = aescypher.decrypt(cyphertext, key, iv)
        self.assertEqual(self.plaintext, res)

    def test_decrypt_emptyPlaintext(self):
        key = keygen.generate()
        plaintext = "".encode()
        cyphertext, iv = aescypher.encrypt(plaintext, key)
        res = aescypher.decrypt(cyphertext, key, iv)
        self.assertEqual(plaintext, res)

    def test_decrypt_char(self):
        key = keygen.generate()
        plaintext = "a".encode()
        cyphertext, iv = aescypher.encrypt(plaintext, key)
        res = aescypher.decrypt(cyphertext, key, iv)
        self.assertEqual(plaintext, res)

