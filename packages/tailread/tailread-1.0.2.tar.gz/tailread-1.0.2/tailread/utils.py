def get_file_size(fp):
    tmp = fp.tell()
    fp.seek(0, 2)
    size = fp.tell()
    fp.seek(tmp)
    return size
