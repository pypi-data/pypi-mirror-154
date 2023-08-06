import functools




def split_duplicated(func):
    @functools.wraps(func)
    def wrapper(*args, keepends=True, **kwargs):
        for line in func(*args, **kwargs):
            yield from reversed(line.splitlines(keepends))
    return wrapper


def decode(func):
    @functools.wraps(func)
    def wrapper(*args, encoding=None, errors='strict', **kwargs):
        for line in func(*args, **kwargs):
            if encoding:
                yield line.decode(encoding=encoding, errors=errors)
            yield line
    return wrapper