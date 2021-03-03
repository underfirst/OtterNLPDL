import pickle


def load_object(filepath):
    with open(filepath, "rb") as f:
        return pickle.load(f)
