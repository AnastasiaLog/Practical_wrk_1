from VFS_emulator import act
from config import parse_args
from script_runner import run_script
from vfs import VFS


if __name__ == "__main__":
  args = parse_args()

  print(f"VFS path: {args.vfs}")
  print(f"Prompt: {args.prompt}")
  print(f"Start script: {args.script}")

  if args.vfs:
    try:
      vfs = VFS.load(args.vfs)
      print(f"VFS loaded: {args.vfs}")
    except FileNotFoundError:
      print(f"Ошибка: VFS не найден: {args.vfs}")
      vfs = VFS()
    except ValueError as e:
      print(f"Ошибка: {e}")
      vfs = VFS()
  else:
    vfs = VFS()

  if args.script:
    run_script(args.script, args.prompt)
  while True:
    a = input(args.prompt)
    print(act(a))