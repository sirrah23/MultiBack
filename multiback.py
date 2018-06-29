import os
import datetime
import pathlib
import shutil


def is_dir(dirs):
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
    is_dir_res = []
    any_missing = False
    for dir in dirs:
        e = os.path.isdir(dir)
        is_dir_res.append(e)
        if not e:
            any_missing = True
    return (any_missing, is_dir_res)

def is_file(files):
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
    """
    Write a given file to each one or more destination directories. If the
    filename already exists at the destination then rename it with a
    timestamp before writing the given file over.

    Args:
        src: Source File
        dests: List of destination directories
    """
    ts = timestamp_str()
    src_fname = path_filename(src)
    for dest in dests:
        curr_file = os.path.join(dest, src_fname)
        if is_file([curr_file])[1][0]:
            rename_file(curr_file, os.path.join(dest, fname_timestamp(src_fname, ts)))
        copy_file(src, dest)

def backup_files(srcs, dests):
    """
    Write each given file to a pool of destination directories. If the
    filename being written to the destination already exists there it is
    renamed with a timestamp before any file-writes take place.

    Args:
        srcs: List of src files
        dests: List of destination directories
    """
    for src in srcs:
        backup_file(src, dests)

def timestamp_str():
    """
    Generate a timestamp string with the formate `<YYYYMMDD>.<HHMMSS>`.

    Returns:
        Timestamp string
    """
    now = datetime.datetime.now()
    return "{:04}{:02}{:02}.{:02}{:02}{:02}".format(now.year, now.month, now.day, now.hour, now.minute, now.second)

def fname_timestamp(fname, tstamp):
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
    p = pathlib.Path(fname)
    return "{}.{}{}".format(p.stem, tstamp, "".join(p.suffixes))

def rename_file(old_fname, new_fname):
    """
    Rename a given file.

    Args:
        old_fname: Old filename
        new_fname: New filename
    """
    os.rename(old_fname, new_fname)

def copy_file(src_file, dest_dir):
    """
    Copy a file to a given destination

    Args:
        src_file: Source file
        dest_dir: Destination directory
    """
    shutil.copy(src_file, dest_dir)

def path_filename(fpath):
    """
    Return the filename associated with a filepath.

    Args:
        fpath: File path
    
    Returns:
        Filename
    """
    return pathlib.Path(fpath).name


if __name__ == "__main__":
    pass