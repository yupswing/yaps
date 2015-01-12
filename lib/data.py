import os
data_dir = 'data'

def filepath(kind, filename):
    '''Determine the path to a file in the data directory.'''
    fp = os.path.join(data_dir, kind, filename)
    return fp

def load(kind, filename, mode='rb'):
    '''Open a file in the data directory.'''
    return open(filepath(filename,kind), mode)

