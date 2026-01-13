import subprocess
from concurrent.futures import ProcessPoolExecutor
import glob
import os
from pathlib import Path
import re



proc_dir = "Z:\\_SCAN\\toshiba_m3\\_PYPROC"
orig_ext = '.tif'
out_ext = '.png'


def move_files():
    pdf_out_path = Path(proc_dir)

    subdirs = [x for x in pdf_out_path.iterdir() if x.is_dir()]

    for dir in subdirs:
        images = dir.joinpath("_out").glob("*.png")
        for im in images:
            im.rename(im.parent.parent.joinpath(f"{im.name}"))

if __name__ == "__main__":   # VERY IMPORTANT ON WINDOWS
    move_files()
    input("DONE!!!!!!")