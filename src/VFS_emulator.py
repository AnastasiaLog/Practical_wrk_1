def act(a, vfs=None):
  b = a.split()
  if not b:
    return ""
  cmd, args = b[0], b[1:]

  if cmd == "exit":
    raise SystemExit(0)

  elif cmd == "ls":
    if vfs is None:
      return f"Команда: ls, Аргументы: {args}"
    path = args[0] if args else None
    try:
      return "\n".join(vfs.ls(path))
    except FileNotFoundError as e:
      return str(e)

  elif cmd == "cd":
    if vfs is None:
      if len(args) > 1:
        return "cd: too many arguments"
      return f"Команда: cd, Аргументы: {args}"
    if not args:
      return "cd: missing argument"
    if len(args) > 1:
      return "cd: too many arguments"
    try:
      vfs.cd(args[0])
      return ""
    except (FileNotFoundError, NotADirectoryError) as e:
      return str(e)

  elif cmd == "wc":
    if not args:
      return "wc: missing argument"
    node = vfs.find(args[0]) if vfs else None
    if node is None or node["type"] != "file":
      return f"wc: {args[0]}: no such file"
    content = node["content"]
    return f"{len(content.splitlines())} {len(content.split())} {len(content)}"

  elif cmd == "echo":
    return " ".join(args)

  elif cmd == "find":
    if not args:
      return "find: missing argument"
    result = []
    _find_rec(vfs.root, "/", args[0], result)
    return "\n".join(result)

  elif cmd == "mkdir":
    if vfs is None:
      return f"Команда: mkdir, Аргументы: {args}"
    if not args:
      return "mkdir: missing argument"
    try:
      vfs.mkdir(args[0])
      return ""
    except (FileNotFoundError, FileExistsError, ValueError) as e:
      return str(e)

  else:
    return f"{cmd}: command not found"


def _find_rec(node, path, name, result):
  if node["name"] == name:
    result.append(path)
  for child in node.get("children", {}).values():
    child_path = path.rstrip("/") + "/" + child["name"]
    _find_rec(child, child_path, name, result)
