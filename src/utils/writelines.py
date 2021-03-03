import codecs
from os import makedirs, path


def writelines(filepath, data_list):
    par_dir = path.abspath(path.join(filepath, path.pardir))
    makedirs(par_dir, exist_ok=True)
    with codecs.open(filepath, "w", "utf-8") as f:
        for line in data_list:
            f.write(line + "\n")
