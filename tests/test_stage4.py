import unittest
import os
import sys
import io
import tempfile
from contextlib import redirect_stdout

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from vfs import VFS
from VFS_emulator import act
from script_runner import run_script


class TestStage4Commands(unittest.TestCase):

    def _write_csv(self, text):
        f = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8")
        f.write(text)
        f.close()
        return f.name

    def setUp(self):
        self.path = self._write_csv(
            "path,type,content\n"
            "/,dir,\n"
            "/home,dir,\n"
            "/home/notes.txt,file,Hello world\n"
            "/home/readme.md,file,README content\n"
            "/tmp,dir,\n"
            "/tmp/log.txt,file,log entry\n"
        )
        self.vfs = VFS.load(self.path)

    def tearDown(self):
        os.unlink(self.path)

    # ls
    def test_ls_root(self):
        out = act("ls", self.vfs)
        self.assertIn("home", out)

    def test_ls_dir(self):
        out = act("ls /home", self.vfs)
        self.assertIn("notes.txt", out)

    def test_ls_missing(self):
        out = act("ls /nope", self.vfs)
        self.assertIn("no such", out)

    # cd
    def test_cd_valid(self):
        act("cd /home", self.vfs)
        self.assertEqual(self.vfs.cwd, "/home")

    def test_cd_missing(self):
        out = act("cd /nope", self.vfs)
        self.assertIn("no such", out)

    def test_cd_too_many(self):
        out = act("cd /a /b", self.vfs)
        self.assertIn("too many", out)

    # wc
    def test_wc_counts(self):
        out = act("wc /home/notes.txt", self.vfs)
        self.assertRegex(out, r"\d+ \d+ \d+")

    def test_wc_missing(self):
        out = act("wc /nope", self.vfs)
        self.assertIn("no such", out)

    # echo
    def test_echo(self):
        self.assertEqual(act("echo hello world", self.vfs), "hello world")

    def test_echo_empty(self):
        self.assertEqual(act("echo", self.vfs), "")

    # find
    def test_find_file(self):
        out = act("find notes.txt", self.vfs)
        self.assertIn("/home/notes.txt", out)

    def test_find_missing(self):
        out = act("find nope.txt", self.vfs)
        self.assertEqual(out, "")

    # unknown
    def test_unknown(self):
        self.assertEqual(act("foo", self.vfs), "foo: command not found")


class TestStartScript(unittest.TestCase):
    def _write(self, text):
        f = tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8")
        f.write(text)
        f.close()
        return f.name

    def _write_csv(self, text):
        f = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8")
        f.write(text)
        f.close()
        return f.name

    def setUp(self):
        self.csv_path = self._write_csv(
            "path,type,content\n"
            "/,dir,\n"
            "/home,dir,\n"
            "/home/notes.txt,file,Hello world\n"
            "/tmp,dir,\n"
            "/tmp/log.txt,file,log entry\n"
        )
        self.vfs = VFS.load(self.csv_path)

        self.script_path = self._write(
            "# Стартовый скрипт для Этапа 4\n"
            "ls\n"                          
            "cd /home\n"                    
            "ls /home\n"                    
            "wc /home/notes.txt\n"          
            "echo hello world\n"            
            "find notes.txt\n"              
            "# Обработка ошибок\n"
            "cd /no_such_dir\n"             
            "ls /no_such_dir\n"            
            "wc /no_such_file\n"            
            "cd /a /b\n"                    
            "foo\n"
        )

    def tearDown(self):
        os.unlink(self.csv_path)
        os.unlink(self.script_path)

    def test_script_runs_all_commands(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            run_script(self.script_path, "VFS> ", self.vfs)
        out = buf.getvalue()

        # ls
        self.assertIn("VFS> ls", out)
        self.assertIn("home", out)
        # cd
        self.assertIn("VFS> cd /home", out)
        # wc
        self.assertIn("VFS> wc /home/notes.txt", out)
        # echo
        self.assertIn("VFS> echo hello world", out)
        self.assertIn("hello world", out)
        # find
        self.assertIn("VFS> find notes.txt", out)
        # ошибки
        self.assertIn("VFS> cd /no_such_dir", out)
        self.assertIn("no such", out)
        self.assertIn("VFS> foo", out)
        self.assertIn("command not found", out)


if __name__ == "__main__":
    unittest.main()
