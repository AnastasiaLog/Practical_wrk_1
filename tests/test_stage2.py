import unittest
import os
import sys
import io
import tempfile
from contextlib import redirect_stdout

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from config import parse_args
from script_runner import run_script


class TestParseArgs(unittest.TestCase):

    def test_parse_vfs(self):
        sys.argv = ["main.py", "--vfs", "vfs/minimal.csv"]
        self.assertEqual(parse_args().vfs, "vfs/minimal.csv")

    def test_parse_prompt(self):
        sys.argv = ["main.py", "--prompt", "custom> "]
        self.assertEqual(parse_args().prompt, "custom> ")

    def test_parse_script(self):
        sys.argv = ["main.py", "--script", "scripts/start.txt"]
        self.assertEqual(parse_args().script, "scripts/start.txt")


class TestRunScript(unittest.TestCase):

    def _write(self, text):
        f = tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8")
        f.write(text)
        f.close()
        return f.name

    def test_run_simple_script(self):
        path = self._write("ls\ncd /home\n")
        try:
            run_script(path, "VFS> ")
        finally:
            os.unlink(path)

    def test_comments_are_skipped(self):
        path = self._write("# комментарий\nls\n")
        try:
            run_script(path, "VFS> ")
        finally:
            os.unlink(path)

    def test_output_shows_input_and_result(self):
        path = self._write("ls\n")
        buf = io.StringIO()
        try:
            with redirect_stdout(buf):
                run_script(path, "VFS> ")
        finally:
            os.unlink(path)
        out = buf.getvalue()
        self.assertIn("VFS> ls", out)
        self.assertIn("Команда: ls, Аргументы: []", out)

    def test_missing_file_prints_error(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            run_script("no_such_file.txt", "VFS> ")
        self.assertIn("не найден", buf.getvalue())


if __name__ == "__main__":
    unittest.main()