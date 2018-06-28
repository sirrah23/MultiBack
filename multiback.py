import os
import datetime
import pathlib
import shutil

"""
Given a list of directory names, make sure that each input
is an existing directory.

Args:
    dirs: A list of directory names

Returns:
    A tuple where the first item is a flag indicating if any input directory
    is missing and the second item is the list with a flag for each input
    directory name indicating whether or not the directory exists.
    True -> Exists
    False -> Does not exist
"""
def is_dir(dirs):
    is_dir_res = []
    any_missing = False
    for dir in dirs:
        e = os.path.isdir(dir)
        is_dir_res.append(e)
        if not e:
            any_missing = True
    return (any_missing, is_dir_res)

"""
Given a list of filenames, make sure that each input
is an existing file.

Args:
    dirs: A list of filenames

Returns:
    A tuple where the first item is a flag indicating if any input file
    is missing and the second item is the list with a flag for each input
    filename indicating whether or not the file exists.
    True -> Exists
    False -> Does not exist
"""
def is_file(files):
    is_file = []
    any_missing = False
    for file in files:
        e = os.path.isfile(file)
        is_file.append(e)
        if not e:
            any_missing = True
    return (any_missing, is_file)

def read_config(cfg):
    pass

def backup_file(src, dests):
    pass

def backup_files(srcs, dests):
    pass

"""
Generate a timestamp string with the formate `<YYYYMMDD>.<HHMMSS>`.

Returns:
    Timestamp string
"""
def timestamp_str():
    now = datetime.datetime.now()
    return "{:04}{:02}{:02}.{:02}{:02}{:02}".format(now.year, now.month, now.day, now.hour, now.minute, now.second)

"""
Given a filename and a timestamp string return the filename with the
timestamp embedded.

Args:
    fname: Filename to embed timestamp into
    tstamp: Timestamp string

Returns:
    fname with tstamp embedded

Examples:
    x = fname_timestamp("test.txt", "20180626.034516")
    print(x)  # test.20180626.034516.txt

    y = fname_timestamp("test.tar.gz", "20180626.034516")
    print(y)  # test.20180626.034516.tar.gz
"""
def fname_timestamp(fname, tstamp):
    p = pathlib.Path(fname)
    print(p.stem)
    print(p.suffixes)
    return "{}.{}{}".format(p.stem, tstamp, "".join(p.suffixes))

"""
Rename a given file.

Args:
    old_fname: Old filename
    new_fname: New filename
"""
def rename_file(old_fname, new_fname):
    os.rename(old_fname, new_fname)

"""
Copy a file to a given destination

Args:
    src_file: Source file
    dest_dir: Destination directory
"""
def copy_file(src_file, dest_dir):
    shutil.copy(src_file, dest_dir)

if __name__ == "__main__":
    print(timestamp_str())
    print(fname_timestamp("test.txt", "20180626.034516"))