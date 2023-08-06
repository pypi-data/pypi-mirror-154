from .utils import get_file_size
from .helpers import _validate_args, _extract_line
from .decorators import decode, split_duplicated




@decode
@split_duplicated
def readlines(bytesio, batch_size=1024, **encoding_kwargs):
    '''bytesio: file path or BufferedReader
       batch_size: size to be processed
       keepends: keep linesep
       encoding_kwargs: decoding info for results
    '''
    path, fp = _validate_args(bytesio, batch_size)
    content_length = get_file_size(fp)

    buf = b""
    for p in reversed(range(0, content_length, batch_size)):
        cut, *parsed = _extract_line(fp, p, batch_size, content_length)

        for line in reversed(parsed):
            yield line + buf
            buf = b""
            
        buf = cut + buf
    
    if path:
        fp.close()
    yield buf
