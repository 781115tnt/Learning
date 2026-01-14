import subprocess
from concurrent.futures import ProcessPoolExecutor
import glob
import os
import img2pdf
from pathlib import Path
import re
import psutil
import shutil
from pypdf import PdfReader






#Support rotation: 0, 90, 180, 270
rot = 0

strdir = ".\\"
wdir = Path(strdir)

max_process = psutil.cpu_count(logical=False)
orig_ext = '.tif'
out_ext = '.png'

def flat_file_structure():
    for dirpath, _, filenames in os.walk(wdir):
        for f in filenames:
            full = Path(dirpath) / f
            flat = "__xxx__".join(full.relative_to(wdir).parts)
            full.rename(wdir / flat)
            #print(f"{full} -> {wdir / flat}")
    for x in wdir.iterdir():
        if x.is_dir():
            shutil.rmtree(x)





def ghostscript_proc(task):
    filename, pagenumber = task
    cmd = f"gswin64c.exe -o \".\\{filename}\\{pagenumber}.tif\" -sDEVICE=tiff24nc -sCompression=lzw -r300 -dUseCropBox  -dFirstPage={pagenumber} -dLastPage={pagenumber} \"{filename}\".pdf"
    print(cmd)
    return subprocess.run(cmd, shell=True)

def extract_pdf():
    jobs = []
    for pdf in Path(strdir).glob("*.pdf"):
        pdf.parent.joinpath(pdf.stem).mkdir(exist_ok=True)
        for pn in range(1, len(PdfReader(pdf).pages) + 1):
            jobs.append((pdf.stem, pn))

    with ProcessPoolExecutor(max_workers=max_process) as pool:
        pool.map(ghostscript_proc, jobs)

def imagemagick_proc(task):
    inp, out = task
    if rot == 0 :
        #cmd = f"convert \"{inp}\" -limit memory 16GiB -level 30%,90% -colors 64 -define png:color-type=3 \"{out}\""
        cmd = f"convert \"{inp}\" -limit memory 16GiB -fuzz 15%  -fill \"red\"  -opaque \"rgb(220,30,30)\" -fill \"blue\"  -opaque \"rgb(30,30,170)\" -fill \"black\" -opaque \"rgb(20,20,20)\" -fill \"white\" -opaque \"rgb(220,220,220)\"  -level 30%,90% -colors 64  -define png:color-type=3 \"{out}\""
    else:
        #cmd = f"convert \"{inp}\" -limit memory 16GiB -level 30%,90% -colors 64 -define png:color-type=3 -rotate {rot} \"{out}\""
        cmd = f"convert \"{inp}\" -limit memory 16GiB -fuzz 15%  -fill \"red\"  -opaque \"rgb(220,30,30)\" -fill \"blue\"  -opaque \"rgb(30,30,170)\" -fill \"black\" -opaque \"rgb(20,20,20)\" -level 30%,90% -colors 64  -define png:color-type=3 -rotate {rot} \"{out}\""
        
    return subprocess.run(cmd, shell=True)

def process_image():
    all_files = glob.glob(f"{strdir}\\**\\*.tif", recursive=True)
    jobs = []
    for origimg in all_files:
        outimg = f"{os.path.splitext(origimg)[0]}{out_ext}"
        jobs.append((origimg, outimg))  
    with ProcessPoolExecutor(max_workers=max_process) as pool:
        pool.map(imagemagick_proc, jobs)
    
    print("PROCESSING IMAGES: DONE!!!")

def img2pdf_proc(dir):
    images = sorted(dir.glob(f"*{out_ext}"))
    pdf = wdir.joinpath(f"__OUT_{re.sub(r"-\d{6}", "", dir.name)}.pdf")
    print(f"Creating {pdf}...")
    with open(pdf, "wb") as f:
        f.write(img2pdf.convert([str(p) for p in images]))

def create_pdf():
    subdirs = [x for x in wdir.iterdir() if x.is_dir()]

    with ProcessPoolExecutor(max_workers=max_process) as pool:
        pool.map(img2pdf_proc, subdirs)


if __name__ == "__main__":   # VERY IMPORTANT ON WINDOWS
    flat_file_structure()
    extract_pdf()
    process_image() 
    create_pdf()
    input("DONE!!!!!!")
