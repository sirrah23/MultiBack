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
    os.mkdir("./test/validate")
    os.mkdir("./test/validate/dest")

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

    create_file_with_content("./test/validate/test.txt", "Hello World")

def create_file_with_content(fname, content):
        with open(fname, "w+") as f:
            f.write(content)

def teardown_module():
    shutil.rmtree("./test")


class TestFileDirExist:

    def test_is_file_not_exist(self):
        assert is_file("./notexist.txt") == False

    def test_is_file_exists(self):
        assert is_file("./test/exist/exist1.txt") == True
        assert is_file("./test/exist/exist2.txt") == True

    def test_is_dir_not_exists(self):
        assert is_dir("./notexist") == False

    def test_is_dir_exists(self):
        assert is_dir("./test/exist") == True


class TestTimestamp:

    def test_filename_timestamp(self):
        fname = "test.txt"
        tstamp = "20180629.111516"
        assert fname_timestamp(fname, tstamp) == "test.20180629.111516.txt"


class TestFileManipulation:

    def test_rename(self):
        rename_file("./test/rename/r1.txt", "./test/rename/r2.txt")
        assert is_file("./test/rename/r1.txt") == False
        assert is_file("./test/rename/r2.txt") == True

    def test_copy_file(self):
        copy_file("./test/copy/c1.txt", "./test/copy/c2.txt")
        assert is_file("./test/copy/c1.txt") == True
        assert is_file("./test/copy/c2.txt") == True

    def test_path_filename(self):
        fpath = "/home/john/test.txt"
        assert path_filename(fpath) == "test.txt"


class TestBackup:

    def test_backup_file_no_rename(self):
        src = os.path.abspath("./test/backup/src/test.txt")
        dest = [os.path.abspath("./test/backup/dest_empty")]
        backup_file(src, dest)
        assert is_file(src) == True
        assert is_file(os.path.join(dest[0], "test.txt")) == True

    def test_backup_file_rename(self):
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

    def test_backup_files_no_rename(self):
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

    def test_backup_files_rename(self):
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


class TestConfig:

    def test_template_config(self):
        loc = os.path.abspath("./test/template/")
        loc = os.path.join(loc, fname_timestamp("config.json", timestamp_str()))
        template_config(loc)
        files = os.listdir("./test/template")
        assert len(files) == 1
        assert files[0].startswith("config") == True
        assert files[0].endswith(".json") == True

    def test_config_read(self):
        loc = os.path.abspath("./test/template/")
        loc = os.path.join(loc, fname_timestamp("config.json", timestamp_str()))
        template_config(loc)
        valid, cfg = read_config(loc)
        assert valid == True
        assert "/home/anon/test1.txt" in cfg["sources"]
        assert "/home/anon/test2.txt" in cfg["sources"]
        assert "/home/anon/backup/" in cfg["destinations"]
        assert "/home/anon/backup2/" in cfg["destinations"]


class TestUserInputValidation:

    def test_user_input_validation_errs(self):
        root = os.path.abspath("./test/validate")
        bad_file = os.path.join(root, "nosrc1.txt")
        bad_dir = os.path.join(root, "nosrc2/")
        valid, errors = validate_user_input([bad_file], [bad_dir])
        assert valid == False
        assert len(errors) == 2
        assert "The source file `{}` does not exist".format(bad_file) in errors
        assert "The destination directory `{}` does not exist".format(bad_dir) in errors

    def test_user_input_validation_no_errs(self):
        root = os.path.abspath("./test/validate")
        good_file = os.path.join(root, "test.txt")
        good_dir = os.path.join(root, "dest/")
        valid, errors = validate_user_input([good_file], [good_dir])
        assert valid == True
        assert len(errors) == 0
