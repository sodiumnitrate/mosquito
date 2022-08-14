import numpy as np
import os
import subprocess


def file_len(fname):
    x = subprocess.check_output(['wc','-l',fname])
    length = str(x).split()[0][2:]
    return int(length)

def tail(f,n=10):
    assert(n>0)
    pos, lines = n+1, []

    # set file pointer to end
    f.seek(0, os.SEEK_END)

    is_file_small = False

    while len(lines) <= n:
        try:
            f.seek(f.tell() - pos, os.SEEK_SET)
        except ValueError as e:
            # lines greater than file seeking size
            # seek to start
            f.seek(0, os.SEEK_SET)
            is_file_small = True
        finally:
            lines = f.readlines()
            if is_file_small:
                break

        pos*= 2
    return lines[-n:]



