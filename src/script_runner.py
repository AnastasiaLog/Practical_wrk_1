from VFS_emulator import act

def run_script(path, prompt, vfs=None):
    try:
        f = open(path, encoding="utf-8")
    except FileNotFoundError:
        print(f"Ошибка: скрипт не найден: {path}")
        return

    with f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            print(f"{prompt}{line}")
            try:
                result = act(line, vfs)
                if result:
                    print(result)
            except SystemExit:
                return
            except Exception as e:
                print(f"Ошибка выполнения: {e}")
