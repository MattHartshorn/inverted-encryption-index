import os

def testFile(filename=None):
    directory = os.path.dirname(__file__)
    return directory if filename == None else os.path.join(directory, filename)