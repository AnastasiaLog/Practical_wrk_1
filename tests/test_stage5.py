import unittest
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from vfs import VFS
from VFS_emulator import act


class TestMkdir(unittest.TestCase):

    def setUp(self):
        f = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8")
        f.write(
            "path,type,content\n"
            "/,dir,\n"
            "/home,dir,\n"
            "/home/notes.txt,file,Hello\n"
        )
        f.close()
        self.path = f.name
        self.vfs = VFS.load(self.path)

    def tearDown(self):
        os.unlink(self.path)

    def test_mkdir_creates(self):
        act("mkdir /home/newdir", self.vfs)
        self.assertIsNotNone(self.vfs.find("/home/newdir"))

    def test_mkdir_no_args(self):
        self.assertIn("missing", act("mkdir", self.vfs))

    def test_mkdir_existing(self):
        self.assertIn("already exists", act("mkdir /home", self.vfs))

    def test_mkdir_no_parent(self):
        self.assertIn("no such", act("mkdir /nope/x", self.vfs))

    def test_mkdir_in_memory_only(self):
        act("mkdir /home/newdir", self.vfs)
        with open(self.path, encoding="utf-8") as f:
            self.assertNotIn("newdir", f.read())


if __name__ == "__main__":
    unittest.main()