import re
import zipfile
from os import makedirs, path
from pathlib import Path

from config.datapath import PROJECT_TOP


def zip_current_codebase(file_name):
    folder_path = path.join(PROJECT_TOP, "data", "codebase", )
    file_path = path.join(folder_path, f"{file_name}.zip")
    makedirs(folder_path, exist_ok=True)
    regex = re.compile(".*\.py")
    with zipfile.ZipFile(file_path, "w", compression=zipfile.ZIP_DEFLATED) as new_zip:
        for fp in Path(PROJECT_TOP, "src").glob("**/*"):
            fp = str(fp)
            if regex.match(fp):
                new_zip.write(fp, arcname=fp.replace(str(PROJECT_TOP), ""))
    return file_path


if __name__ == '__main__':
    zip_current_codebase("test")
