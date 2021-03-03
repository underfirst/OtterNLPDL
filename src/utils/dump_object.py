import pickle
from os import makedirs, path


def dump_object(obj, filepath):
    makedirs(path.dirname(filepath), exist_ok=True)
    with open(filepath, "wb") as f:
        pickle.dump(obj, f)
