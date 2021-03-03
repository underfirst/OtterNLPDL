from pathlib import Path


def search_project_top(base_dir):
    """
    base_dirから上10階層以内に.project_topっていう名前のファイルがあれば、
    そこがproject top directory。なければプログラムを停止する。
    :param base_dir:
    :return:
    """
    current = Path(base_dir)
    for i in range(10):
        parent = current.parent
        files = parent.glob(".project_top")
        for file in files:
            project_top = Path(file)
            return project_top.parent
        current = current.parent
    assert "No .project_top file in project top directory."