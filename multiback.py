import os
import datetime
import pathlib
import shutil
import json


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

def template_config(fname):
    """
    Generate a template config.json file which contains source/destination
    mappings.

    Args:
        fname: Name of file to write template config data to
    """
    templ = {}
    templ["sources"] = [
            "/home/anon/test1.txt",
            "/home/anon/test2.txt",
    ]
    templ["destinations"] = [
            "/home/anon/backup/",
            "/home/anon/backup2/",
    ]
    with open(os.path.abspath(fname), 'w') as outfile:
        json.dump(templ, outfile)

def read_config(cfg_file):
    """
    Read a configuration file which is assumed to contain source/destination
    mappings.

    Args:
        cfg_file: Name of configuration file

    Returns:
        valid: Configuration data is valid -> True, else False
        cfg_data: Dictionary with source/destination information
    """
    valid = False
    cfg_data = {}
    if not is_file(cfg_file):
        return (valid, cfg_data)
    with open(cfg_file, "r") as f:
        cfg_data = json.load(f)
    try:
        valid = len(cfg_data["sources"]) > 0 and len(cfg_data["destinations"]) > 0
    except KeyError:
        valid = False
    return (valid, cfg_data)

def validate_user_input(sources, destinations):
    """
    Make sure that the user input files and directories exist.

    Args:
        sources: Input source files
        destinations: Input destination directories
    
    Returns:
        valid: Flag indicating if there were any issues
        errors: List of error messages
    """
    valid = True
    errors = []
    for source in sources:
        if not is_file([source])[1][0]:
            errors.append("The source file `{}` does not exist".format(source))
    for destination in destinations:
        if not is_dir([destination])[1][0]:
            errors.append("The destination directory `{}` does not exist".format(destination))
    valid = len(errors) == 0
    return (valid, errors)

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

