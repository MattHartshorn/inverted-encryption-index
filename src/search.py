import os
from .commander import Command
from .keygen import readKeyFile
from .token import readTokenFile
from .cryptoindex import CryptoIndex
from .cryptofile import CryptoFile

class SearchCommand(Command):
    def __init__(self):
        super().__init__("search", "Searches the index for files that satisfy the provided query")
    
    def add_arguments(self):
        self.parser.add_argument("-k", "--keyFile",
            help="The path of the encryption key file",
            default="skaes.txt",
            metavar="FILE")
        self.parser.add_argument("-i", "--index", 
            help="The path of the index file",
            metavar="FILE")
        self.parser.add_argument("-d", "--dir", 
            help="The directory of the encrypted files",
            metavar="DIR")

        group = self.parser.add_mutually_exclusive_group(required=True)
        group.add_argument("-t", "--tokenFile", 
            help="The file that contains the search token(s)",
            metavar="FILE")
        group.add_argument("-q", "--query", 
            help="One or more keywords required in all matching files",
            nargs="+",
            metavar="WORDS")
    
    def run(self, args, parser):
        # Load the index file
        try:
            key = readKeyFile(args.keyFile)
        except Exception as ex:
            parser.error(str(ex))
            
        index = CryptoIndex()
        index.load(args.dir, args.index)
        index.setKey(key)

        # Get the search query 
        query = args.query
        if (query == None):
            query = readTokenFile(args.tokenFile)

        # Find files
        filenames = index.find(query, args.tokenFile != None)
        paths = index.getFilePaths(filenames)

        # Print files
        for i, path in enumerate(paths):
            if (os.path.isfile(path)):
                f = CryptoFile(path, key)
                print('{}: {{'.format(filenames[i]))
                print('    "filename: "{}"'.format(f.filename))
                print('    "content: "{}"'.format(f.content))
                print('}')
            else:
                print("{}: File not found".format(filenames[i]))

            if i != len(paths) - 1: print()
                


        
