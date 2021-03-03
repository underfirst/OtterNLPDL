import platform


def set_local_const(const, local_value):
    """
    :param const: default value in production
    :param local_value: default value in local (laptop) debug environment
    :return:
    """
    if platform.system() == "Darwin":
        return local_value
    return const