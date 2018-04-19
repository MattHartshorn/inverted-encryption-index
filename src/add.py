from .commander import Command
from .keygen import readKeyFile
from .cryptoindex import CryptoIndex

class AddCommand(Command):

    def __init__(self):
        super().__init__("add", "Adds a file to the searchable encryption index")
    
    def add_arguments(self):
        self.parser.add_argument("-k", "--keyFile",
            help="The path of the encryption key file",
            default="skaes.txt",
            metavar="FILE")
        self.parser.add_argument("-i", "--index", 
            help="The path of the index file",
            metavar="FILE")
        self.parser.add_argument("-d", "--dir", 
            help="The output directory of the encrypted files",
            metavar="DIR")

        self.parser.add_argument("path", help="File or directory of the files to add")
    
    def run(self, args, parser):
        try:
            key = readKeyFile(args.keyFile)
        except:
            parser.error("Unable to read keyfile '{0}'".format(args.keyFile))

        index = CryptoIndex()
        index.load(args.dir, args.index)

        index.setKey(key)
        index.add(args.path)
        index.save()
