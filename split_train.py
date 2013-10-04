import sys
import os
import json

class change_dir():
    '''
    '''
    def __init__(self, newPath):
        self.newPath = newPath

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


def get_lines(reader, chunk_size = 1024):
    '''
    '''
    lines = []
    eof = False
    for i in range(chunk_size):
        try:
            lines.append(reader.next())
        except StopIteration:
            eof = True
            break
    return lines, eof

def parse_name(file_name):
    '''
    '''
    if '.' in file_name:
        fields = file_name.split('.')
        name = "".join(fields[:-1])
        ext = "." + fields[-1]
    else:
        name = file_name
        ext = ""
    print(name)
    return name, ext

def splitter(handle, base, ext):
    '''
    '''
    file_index = 0
    chunk_size = 1024

    cur_name = base + "_" +  str(file_index).zfill(3) + ext
    out = open(cur_name, 'w')
    lines = 0
    while True:
        chunk, eof = get_lines(handle, chunk_size)
        data_list = [ line for line in chunk ]
        out.write( "".join(data_list) )
        lines += chunk_size
        if eof:
            out.close()
            break

        if lines >= 100*chunk_size:
            out.close()
            file_index += 1
            cur_name = base + "_" + str(file_index).zfill(3) + ext
            out = open(cur_name, 'w')
            lines = 0

    return file_index + 1

def main(file_name):
    '''
    '''
    base_name, ext = parse_name(file_name)
    file_dir = os.path.dirname( os.path.abspath(file_name) )
    new_dir = file_dir + '/' + base_name.upper() + '_split'
    try:
        os.mkdir(new_dir)
    except OSError:
        # directory exists
        pass
    with open(file_name, 'rb') as handle, change_dir(new_dir):
        k = splitter(handle, base_name, ext)
    print(k)


if __name__ == '__main__':
    filename = sys.argv[1]
    print(filename)
    main(filename)


    
