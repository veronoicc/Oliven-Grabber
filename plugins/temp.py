import tempfile


def mkdtemp():
    tempdir = tempfile.mkdtemp(prefix='og')
    return tempdir
