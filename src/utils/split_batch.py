def split_batch(l, batch_size):
    result = []
    current = []
    for l_i in l:
        if len(current) == batch_size:
            result.append(current)
            current = []
        current.append(l_i)
    if len(current) > 0:
        result.append(current)
    return result