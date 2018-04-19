import os
import json
import base64
from . import aescypher


class CryptoFile:
    path = None
    filename = None
    content = None

    def __init__(self, filename=None, key=None):
        if (filename != None):
            self.read(filename, key)

    def read(self, filename, key=None):
        with open(filename, "rb") as fs:
            if (key == None):
                self.path, self.filename = os.path.split(filename)
                self.content = fs.read().decode()
            else:
                # Read iv and cyphertext from base64
                content = fs.read()
                iv = content[:aescypher.BLOCK_SIZE]
                cyphertext = content[aescypher.BLOCK_SIZE:]

                # Decrypt and load data
                data = json.loads(aescypher.decrypt(cyphertext, key, iv).decode())
                self.path = data["path"]
                self.filename = data["filename"]
                self.content = data["content"]

    def write(self, filename, key):
        # Encode to bytes and encrypt
        data = json.dumps({"path": self.path, "filename": self.filename, "content": self.content }).encode()
        cyphertext, iv = aescypher.encrypt(data, key)

        # Ensure that the directory exists
        dir = os.path.dirname(filename)
        if (not os.path.exists(dir)): os.makedirs(dir)

        with open(filename, "wb") as fs:
            fs.write(iv + cyphertext)
