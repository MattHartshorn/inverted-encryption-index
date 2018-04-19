import os
import json
from .cryptofile import CryptoFile
from . import token
import uuid
import base64

class CryptoIndex:
    def __init__(self):
        # Fields saved to output file
        self.index = {}
        self.directory = None

        self.indexFile = ".index"
        self.key = None
        self.unsavedFiles = []


    def load(self, directory=None, indexFile=None):
        if (directory == None and indexFile == None):
            directory = "."
        
        if (directory != None):
            self.directory = os.path.abspath(directory)

        # Get the index file path
        if (indexFile == None):
            indexFile = os.path.join(directory, self.indexFile)
        else:
            if (not os.path.isabs(indexFile)):
                indexFile = os.path.abspath(indexFile)
            self.indexFile = indexFile

        if (os.path.isfile(self.indexFile)):
            # Read index file
            with open(self.indexFile, "r") as fs:
                content = json.loads(fs.read())
                self.index = content["index"]
                
                if (self.directory == None):
                    self.directory = content["directory"]


    def setKey(self, key):
        if (key == None): 
            raise TypeError("key cannot be of NoneType")
        self.key = key


    def add(self, path, recursive=False):
        if (os.path.isdir(path)):
            # Form absolute path
            if (not os.path.isabs(path)):
                path = os.path.abspath(path)

            # Add files and directories
            for item in os.listdir(path):
                item = os.path.join(path, item)
                if (recursive or os.path.isfile(item)):
                    self.add(item, recursive)

        elif (os.path.isfile(path)):
            self.addFile(path)
        else:
            raise ValueError("path is not a valid file or directory")


    def addFile(self, filename):
        if (not os.path.isfile(filename)):
            raise ValueError("path is not a valid filepath")

        # Read file
        cfile = CryptoFile(filename)
        outputFilename = uuid.uuid4().hex

        # Index file contents
        for word in cfile.content.split():
            wordToken = token.create(word)
            if (wordToken in self.index):
                self.index[wordToken].append(outputFilename)
            else:
                self.index[wordToken] = [outputFilename]

        # Store unsaved files
        self.unsavedFiles.append((outputFilename, cfile))
        

    def find(self, query, isToken=False):
        # Convert all the items in the query to hash tokens and validate
        if (isinstance(query, str)):
            query = query.split()
        if (not isinstance(query, list)):
            raise TypeError("query must be of type 'str' or 'list'")

        # Find the files that contain all the query tokens
        res = set()
        for item in query:
            itemToken = item if isToken else token.create(item)

            if (itemToken in self.index):
                if (len(res) <= 0):
                    res = set(self.index[itemToken])
                else:
                    res = set.intersection(res, set(self.index[itemToken]))
            else:
                return []
        
        return list(res)


    def save(self, directory=None, indexFile=None):
        # Validate the input and state of the object
        if (directory == None and self.directory == None and indexFile == None):
            raise Exception("Cannot write files, output directory is not set")
        if (self.key == None):
            raise Exception("Cannot write files, ecryption key is not set")
        
        # Set or update the output directory and index file locations
        if (self.directory == None or directory != None):
            self.directory = directory
            
            if (indexFile != None):
                if (not os.path.isabs(indexFile)):
                    indexFile = os.path.abspath(indexFile)
                self.indexFile = indexFile

                if (self.directory == None):
                    self.directory = os.path.split(self.index)

        # Write index file
        content = json.dumps({ "index": self.index, "directory": self.directory })
        with open(self.indexFile, "w") as fs:
            fs.write(content)

        # Write unsaved crypto files
        for ufile in self.unsavedFiles:
            path = os.path.join(self.directory, ufile[0])
            ufile[1].write(path, self.key)

        self.unsavedFiles = []
    

    def getFilePaths(self, fileKeys):
        return [os.path.join(self.directory, key) for key in fileKeys]
