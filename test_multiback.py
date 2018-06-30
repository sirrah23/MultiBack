import os
import shutil
from multiback import *


# TODO: Re-organize this into a class-based test-suite for better
# maintainability...


def setup_module():
    os.mkdir("./test")
    os.mkdir("./test/exist")
    os.mkdir("./test/rename")
    os.mkdir("./test/copy")
    os.mkdir("./test/backup")
    os.mkdir("./test/backup/src")
    os.mkdir("./test/backup/dest_empty")
    os.mkdir("./test/backup/dest_populated")
    os.mkdir("./test/backups")
    os.mkdir("./test/backups/src")
    os.mkdir("./test/backups/dest_empty")
    os.mkdir("./test/backups/dest_populated")
    os.mkdir("./test/template")

    create_file_with_content("./test/exist/exist1.txt", "Hello World1")
    create_file_with_content("./test/exist/exist2.txt", "Hello World2")

    create_file_with_content("./test/rename/r1.txt", "Hello World")

    create_file_with_content("./test/copy/c1.txt", "Hello World")
    create_file_with_content("./test/copy/c1.txt", "Hello World")

    create_file_with_content("./test/backup/src/test.txt", "Hello World")
    create_file_with_content("./test/backup/dest_populated/test.txt", "Hello World")

    create_file_with_content("./test/backups/src/test.txt", "Hello World")
    create_file_with_content("./test/backups/src/test2.txt", "Hello World")
    create_file_with_content("./test/backups/src/test3.txt", "Hello World")
    create_file_with_content("./test/backups/dest_populated/test.txt", "Hello World")
    create_file_with_content("./test/backups/dest_populated/test2.txt", "Hello World")
    create_file_with_content("./test/backups/dest_populated/test3.txt", "Hello World")

def create_file_with_content(fname, content):
    with open(fname, "w+") as f:
        f.write(content)

def teardown_module():
    shutil.rmtree("./test")

def test_is_file_not_exist():
    assert is_file(["./notexist.txt"]) == (True, [False])

def test_is_file_exists():
    assert is_file(["./test/exist/exist1.txt", "./test/exist/exist2.txt"]) == (False, [True, True])

def test_is_dir_not_exists():
    assert is_dir(["./notexist"]) == (True, [False])

def test_is_dir_exists():
    assert is_dir(["./test/exist"]) == (False, [True])

def test_filename_timestamp():
    fname = "test.txt"
    tstamp = "20180629.111516"
    assert fname_timestamp(fname, tstamp) == "test.20180629.111516.txt"

def test_rename():
    rename_file("./test/rename/r1.txt", "./test/rename/r2.txt")
    assert is_file(["./test/rename/r1.txt"])[1][0] == False
    assert is_file(["./test/rename/r2.txt"])[1][0] == True

def test_copy_file():
    copy_file("./test/copy/c1.txt", "./test/copy/c2.txt")
    assert is_file(["./test/copy/c1.txt"])[1][0] == True
    assert is_file(["./test/copy/c2.txt"])[1][0] == True

def test_path_filename():
    fpath = "/home/john/test.txt"
    assert path_filename(fpath) == "test.txt"

def test_backup_file_no_rename():
    src = os.path.abspath("./test/backup/src/test.txt")
    dest = [os.path.abspath("./test/backup/dest_empty")]
    backup_file(src, dest)
    assert is_file([src])[1][0] == True
    assert is_file([os.path.join(dest[0], "test.txt")])[1][0] == True

def test_backup_file_rename():
    src = os.path.abspath("./test/backup/src/test.txt")
    dest = [os.path.abspath("./test/backup/dest_populated")]
    backup_file(src, dest)
    files = os.listdir(dest[0])
    assert len(files) == 2
    assert files[0].startswith("test") == True
    assert files[0].endswith(".txt") == True
    assert files[1].startswith("test") == True
    assert files[0].endswith(".txt") == True
    assert files[0] != files[1]

def test_backup_files_no_rename():
    srcs = [
        os.path.abspath("./test/backups/src/test.txt"),
        os.path.abspath("./test/backups/src/test2.txt"),
        os.path.abspath("./test/backups/src/test3.txt")
    ]
    dest = [os.path.abspath("./test/backups/dest_empty")]
    backup_files(srcs, dest)
    files = os.listdir(dest[0])
    assert len(files) == 3
    assert "test.txt" in files
    assert "test2.txt" in files
    assert "test3.txt" in files

def test_backup_files_rename():
    srcs = [
        os.path.abspath("./test/backups/src/test.txt"),
        os.path.abspath("./test/backups/src/test2.txt"),
        os.path.abspath("./test/backups/src/test3.txt")
    ]
    dest = [os.path.abspath("./test/backups/dest_populated")]
    backup_files(srcs, dest)
    files = os.listdir(dest[0])
    assert len(files) == 6
    counts = [0, 0, 0]
    for file in files:
        if file.startswith("test2"):
            counts[1] += 1
        elif file.startswith("test3"):
            counts[2] += 1
        elif file.startswith("test"):
            counts[0] += 1
    assert counts == [2, 2, 2]

def test_template_config():
    loc = os.path.abspath("./test/template/")
    loc = os.path.join(loc, fname_timestamp("config.json", timestamp_str()))
    template_config(loc)
    files = os.listdir("./test/template")
    assert len(files) == 1
    assert files[0].startswith("config") == True
    assert files[0].endswith(".json") == True

