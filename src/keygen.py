import os
from .commander import Command

def generate(bits=256):
    # There are only 3 valid AES key lengths
    if bits not in [128, 192, 256]: raise ValueError('Key length must be 128, 192, or 256 bits.')

    # Using OS native method method to generate the key
    return os.urandom(bits // 8)

def writeKeyFile(key, file):
    # Ensure that the directory exists
    dir = os.path.dirname(file)
    if (not os.path.exists(dir)): os.makedirs(dir)

    with open(file, "w") as fs:
        fs.write(key.hex())

def readKeyFile(file):
    with open(file, "r") as fs:
        return bytes.fromhex(fs.read())

class KeyGenCommand(Command):
    def __init__(self):
        super().__init__("keygen", "Generates a psuedorandom encryption key used for AES file encryption")
    
    def add_arguments(self):
        self.parser.add_argument("-s", "--size",
            help="The size of the key in bits",
            choices=[128, 192, 256],
            default=256,
            type=int)
        self.parser.add_argument("-o", "--output", 
            help="The output path in which the key is written",
            metavar="FILE")

    def run(self, args, parser):
        key = generate(args.size)

        if (args.output == None):
            print(key.hex())
        else:        
            writeKeyFile(key, args.output)
