import numpy as np
import os
import subprocess
import io

def file_len(fname):
    x = subprocess.check_output(['wc','-l',fname])
    length = str(x).split()[0][2:]
    return int(length)

def tail(f,n=10):
    if not isinstance(f, io.IOBase):
        assert(isinstance(f, str))
        f = open(f,'r')
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


def check_if_end_of_file_contains(file_name,contained_string,n=10):
    if not os.path.exists(file_name):
        return False
    f = open(file_name,'r')

    lines =tail(f,n=n)
    for line in lines:
        if contained_string in line:
            return True

    return False


def get_running_job_list(user_name):
    '''
    Function to get list of jobs (in any status) by the given user. Designed to
    be used on Yale's Grace cluster, it may not work on any arbitrary system
    running Slurm.
    '''
    job_list = subprocess.check_output(['squeue', '-u', user_name]).split()
    job_id = []
    for field in job_list:
        field_str = str(field)[2:-1]
        if len(field_str) == 8 and field_str.isnumeric():
            print(field_str)
            job_id.append(field_str)

    return job_id
