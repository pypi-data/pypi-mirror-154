from io import BufferedReader



def _validate_args(bytesio, batch_size):
    path = False
    if isinstance(bytesio, str):
        path = True
        bytesio = open(path, 'rb')
    elif not isinstance(bytesio, BufferedReader):
        raise TypeError('The first argument to readlines must be a file path or a BufferedReader')
    if batch_size < 2:
        raise ValueError(f'batch_size is too small {batch_size}')
    return path, bytesio



def _extract_line(fp, pos, step, total):
    fp.seek(pos)
    remain = min(total-pos, step)
    while remain > 0:
        line = fp.readline()[:remain]
        remain -= len(line)
        yield line