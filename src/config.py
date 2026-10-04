import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--vfs", default=None)
    parser.add_argument("--prompt", default="VFS> ")
    parser.add_argument("--script", default=None)
    return parser.parse_args()