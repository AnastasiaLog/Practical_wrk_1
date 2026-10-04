import unittest
import os
import sys
import tempfile


from src.vfs import VFS


class TestVFS(unittest.TestCase):

    def _write_csv(self, text):
        f = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8")
        f.write(text)
        f.close()
        return f.name

    def test_load_minimal(self):
        path = self._write_csv("path,type,content\n/,dir,\n")
        vfs = VFS.load(path)
        self.assertEqual(vfs.root["name"], "/")
        os.unlink(path)

    def test_load_nested(self):
        path = self._write_csv(
            "path,type,content\n"
            "/,dir,\n"
            "/a,dir,\n"
            "/a/b,dir,\n"
            "/a/b/c,dir,\n"
            "/a/b/c/file.txt,file,hi\n"
        )
        vfs = VFS.load(path)
        node = vfs.root["children"]["a"]["children"]["b"]["children"]["c"]["children"]["file.txt"]
        self.assertEqual(node["content"], "hi")
        os.unlink(path)

    def test_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            VFS.load("no_such_file.csv")

    def test_broken_csv(self):
        path = self._write_csv("garbage\nwithout\nheaders\n")
        with self.assertRaises(ValueError):
            VFS.load(path)
        os.unlink(path)


if __name__ == "__main__":
    unittest.main()