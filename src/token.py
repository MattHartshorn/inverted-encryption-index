import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from .commander import Command

def create(data):
    """Generates a token used to query the index or as index keys.
    Arguments:
    data -- A string or bytes of data that will be hashed into a token

    Returns:
    The token as a hexadecimal string
    """
    if (isinstance(data, str)):
        data = data.encode()
    elif(not isinstance(data, bytes)):
        raise TypeError("data must be of type 'str' or 'bytes'")

    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(data)
    return digest.finalize().hex()


def writeTokenFile(tokens, file):
    with open(file, "w") as fs:
        fs.writelines([t + "\n" for t in tokens])


def readTokenFile(file):
    with open(file, "r") as fs:
        return [t.strip() for t in fs.readlines()]


class TokenCommand(Command):
    def __init__(self):
        super().__init__("token", "Generates one or more encryption tokens used to search the index")
    
    def add_arguments(self):
        self.parser.add_argument("-o", "--output", 
            help="The output path in which the token is written",
            metavar="FILE")

        self.parser.add_argument("query", 
            help="One or more keywords required in all matching files",
            nargs="+")

    def run(self, args, parser):
        tokens = [create(keyword) for keyword in args.query]

        if (args.output == None):
            for token in tokens:
                print(token)
        else:
            try:
                writeTokenFile(tokens, args.output)
            except Exception as ex:
                parser.error(str(ex))