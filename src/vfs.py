import csv


class VFS:
    def __init__(self):
        self.root = {"name": "/", "type": "dir", "children": {}}
        self.cwd = "/"

    @classmethod
    def load(cls, path):
        vfs = cls()
        try:
            with open(path, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                if reader.fieldnames is None or "path" not in reader.fieldnames:
                    raise ValueError("нет колонки path")
                for row in reader:
                    vfs._add(row["path"], row["type"], row.get("content", ""))
        except FileNotFoundError:
            raise FileNotFoundError(f"VFS не найден: {path}")
        except (KeyError, csv.Error) as e:
            raise ValueError(f"Неверный формат VFS: {e}")
        return vfs

    def _add(self, path, type_, content):
        if path == "/":
            return
        parts = [p for p in path.split("/") if p]
        node = self.root
        for part in parts[:-1]:
            node = node["children"][part]
        name = parts[-1]
        if type_ == "dir":
            node["children"][name] = {"name": name, "type": "dir", "children": {}}
        else:
            node["children"][name] = {"name": name, "type": "file", "content": content}

    def find(self, path):
        if path == "/":
            return self.root
        node = self.root
        for part in path.strip("/").split("/"):
            if part not in node.get("children", {}):
                return None
            node = node["children"][part]
        return node

    def ls(self, path=None):
        if path is None:
            path = self.cwd
        node = self.find(path)
        if node is None:
            raise FileNotFoundError(f"ls: {path}: no such directory")
        if node["type"] == "file":
            return [node["name"]]
        return sorted(node["children"].keys())

    def cd(self, path):
        if path == "/":
            self.cwd = "/"
            return
        node = self.find(path)
        if node is None:
            raise FileNotFoundError(f"cd: {path}: no such directory")
        if node["type"] != "dir":
            raise NotADirectoryError(f"cd: {path}: not a directory")
        self.cwd = path