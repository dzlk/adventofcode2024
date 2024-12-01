import os


def readfile(filename):
    return open(filename).read().strip().split('\n')

def day_input_path(filepath, inputpath):
    return os.path.join(os.path.dirname(__file__), '..')