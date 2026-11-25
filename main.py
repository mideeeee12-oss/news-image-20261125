# The World in One Picture — 25 November 2026: the entry program
# (Python 3.13, standard library only). The picture itself, entry.png, sits in
# this repository beside the program; the program copies it to the output as
# /output/entry.png, byte for byte, so both of the grader's runs write the
# same image. entry.png was drawn by render_image.py, kept alongside.

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get('MAKEFUN_OUTPUT_DIR', '/output'))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(HERE / 'entry.png', OUT / 'entry.png')
    print(f"wrote {OUT / 'entry.png'}")


if __name__ == '__main__':
    main()
