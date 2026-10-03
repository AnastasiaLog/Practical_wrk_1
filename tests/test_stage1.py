import unittest
from src.VFS_emulator import act


class TestAct(unittest.TestCase):

    def test_empty(self):
        self.assertEqual(act(""), "")

    def test_ls(self):
        self.assertEqual(act("ls"), "Команда: ls, Аргументы: []")

    def test_ls_with_args(self):
        self.assertEqual(act("ls /home"), "Команда: ls, Аргументы: ['/home']")

    def test_cd(self):
        self.assertEqual(act("cd /tmp"), "Команда: cd, Аргументы: ['/tmp']")

    def test_cd_too_many(self):
        self.assertEqual(act("cd /a /b"), "cd: too many arguments")

    def test_unknown(self):
        self.assertEqual(act("foo"), "foo: command not found")

    def test_exit(self):
        with self.assertRaises(SystemExit):
            act("exit")


if __name__ == "__main__":
    unittest.main()