import codecs


def readlines(filepath:str, callbacks=None, head=-1, verbose=True):
    """
    テキストを1行づつ読み込んで, 1行1アイテム形式のリストを返す.
    行末改行を落とす処理をdefaultでいれている.

    :param filepath:
    :param callbacks: [func(), func(), ...]. テキストの簡単な処理を行う関数を逐次実行したい場合のcallback関数リスト.
    :param head: n > -1を指定した場合, 頭n行のみを返す.
    :param verbose:
    :return:
    """
    result = list()
    if verbose:
        print("load", filepath)
    if callbacks is None:
        callbacks = [lambda x: x]
    with codecs.open(filepath, "r", "utf-8") as f:
        if head > -1:
            for line in f:
                line = line.strip()
                for callback in callbacks:
                    line = callback(line)
                result.append(line)
                head -= 1
                if head < 0:
                    break
            return result

        for line in f.readlines():
            line = line.strip()
            for callback in callbacks:
                    line = callback(line)
            result.append(line)
    return result
