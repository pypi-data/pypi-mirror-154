import os

SPEED_OF_LIGHT = 300_000_000


def local_file_path(path):
    root = os.path.split(__file__)[0]
    return os.path.join(root, path)
