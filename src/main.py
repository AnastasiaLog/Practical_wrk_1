from VFS_emulator import act
from config import parse_args
from script_runner import run_script

if __name__ == "__main__":
  args = parse_args()

  print(f"VFS path: {args.vfs}")
  print(f"Prompt: {args.prompt}")
  print(f"Start script: {args.script}")

  if args.script:
    run_script(args.script, args.prompt)
  while True:
    a = input(args.prompt)
    print(act(a))
