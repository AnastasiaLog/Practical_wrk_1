def act(a):
  b = a.split()
  if a == "exit":
    exit()
  if len(b) == 0:
    return ""
  if b[0] == "ls":
    return f"Команда: ls, Аргументы: {b[1:]}"
  elif b[0] == "cd":
    return f"Команда: cd, Аргументы: {b[1:]}"
  else:
    return f"{b[0]}: command not found"
