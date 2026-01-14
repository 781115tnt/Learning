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
import sys
from PIL import Image
#For very very large images
Image.MAX_IMAGE_PIXELS = None


########################### WORKER FUNCTIONS ############################
def imagemagick_proc(task):
    return subprocess.run(task, shell=True)

def img2pdf_proc(task):
    pdf, images = task
    #print(f"Creating {pdf}...")
    with open(pdf, "wb") as f:
        f.write(img2pdf.convert([str(p) for p in images]))

def ghostscript_proc(cmd):
    return subprocess.run(cmd, shell=True)

########################### MULTIPROCESS-SAFE CODE ############################
if __name__ == "__main__":   # VERY IMPORTANT ON WINDOWS

    TIF = '.tif'
    PNG = '.png'
    OUTDIR = "_out"
    COLOR_FORMAT = "-colors 64 -define png:color-type=3"
    BW_FORMAT = "-monochrome -compress Group4"
    R600 = '-r600'
    R300 = '-r300'
    OUT_FILE_PREFIX = '_OUT_'

    max_process = psutil.cpu_count(logical=False)
    wdir = ' '.join(sys.argv[1:])
    wdir_path = Path(wdir)

    out_ext = PNG
    formatstr = COLOR_FORMAT

    resstr = R300
    rotatestr = ''
    blurstr = ''
    levelstr = "-level 30%,90%"
    rot = '0'

    cluster = '1'
    clusterstr = "-dMinFeatureSize=2"

    ########################### ASKING FOR OPTIONS ############################
    if not wdir_path.exists():
        input("WORKING DIRECTORY DOES NOT EXIST!!!")
        sys.exit(0)

    rot = input("Quay hinh luc xu ly (nhap 90, 180, 270):")
    if not (rot == '90' or rot == '180' or rot == '270') :
        print("-> Khong quay hinh!")
        rotatestr = ''
    else:
        print(f"-> Quay hinh {rot}")
        rotatestr = f"-rotate {rot}"

    dot = input("Xoa cham (Y?):")
    if dot == "y" or dot == "Y":
        print("-> Co Xoa Cham!")
        blurstr = "-blur 2x5"
        levelstr = "-level 45%,85%"
    else:
        print(f"-> Khong xoa cham!")

    bw = input("Ra file 1-bit (Y?):")
    if bw == 'y' or bw == 'Y':
        print("-> Ra file 1-bit!")
        out_ext = TIF
        formatstr = BW_FORMAT
    else:
        print(f"-> Ra file mau!")
    
    res = input("Resolution = 600dpi (Y?):")
    if res == 'y' or res == 'Y':
        print("-> Do phan giai 600dpi!")
        resstr = R600
    else:
        print("-> Do phan giai 300dpi!")    

    cluster = input("Min Cluster size (nhap 2, 3, 4)?:")
    if not (cluster == '2' or cluster == '3' or cluster == '4'):
        print("-> Khong set cluster!")
        clusterstr = ''
    else:
        clusterstr = f"-dMinFeatureSize={cluster}"
        print(f"-> Cluster={cluster}!")
    ########################### FLATEN FILES ############################
    #if False:
    if True:
        for d, _, filenames in os.walk(wdir_path):
            for f in filenames:
                full = Path(d) / f
                flat = "__xxx__".join(full.relative_to(wdir_path).parts)
                full.rename(wdir_path / flat)

        for x in wdir_path.iterdir():
            if x.is_dir(): shutil.rmtree(x)


    ########################### EXTRACTING PDF FILES ############################
    #if False:
    if True:
        jobs = []
        for pdf in Path(wdir).glob("*.pdf"):
            pdf.parent.joinpath(pdf.stem).mkdir(exist_ok=True)
            for pn in range(1, len(PdfReader(pdf).pages) + 1):
                cmd = f"gswin64c.exe -o \".\\{pdf.stem}\\{pn:010d}.tif\" -sDEVICE=tiff24nc -sCompression=lzw {resstr} -dUseCropBox {clusterstr} -dFirstPage={pn} -dLastPage={pn} \"{pdf.stem}\".pdf"
                jobs.append(cmd)
                #print(cmd)
        with ProcessPoolExecutor(max_workers=max_process) as pool:
            pool.map(ghostscript_proc, jobs)



    ########################### MAKE OUTDIRS ############################
    #if False:
    if True:
        subdirs = [p for p in wdir_path.glob('**/') if p.is_dir() and p != wdir_path and p.stem != OUTDIR]
        for sdir in subdirs: os.makedirs(sdir.joinpath(OUTDIR), exist_ok=True)


    ########################### PROCESSING IMAGES ############################
    #if False:
    if True:
        tfiles = glob.glob(f"{wdir}\\**\\*{TIF}", recursive=False)
        #print(tfiles)
        tasks = []
        for t in tfiles:
            tpath = Path(t)
            ofile = f"{tpath.parent.joinpath(OUTDIR).joinpath(tpath.stem)}{out_ext}"
            cmd = f"convert \"{t}\" -limit memory 16GiB -fuzz 15%  -fill \"red\" -opaque \"rgb(220,30,30)\" -fill \"blue\" -opaque \"rgb(30,30,170)\" -fill \"black\" -opaque \"rgb(20,20,20)\" {rotatestr} {blurstr} {levelstr} {formatstr} \"{ofile}\""
            tasks.append(cmd)  
        #for t in tasks: print(t)   
        with ProcessPoolExecutor(max_workers=max_process) as pool: pool.map(imagemagick_proc, tasks)
        
        print("PROCESSING IMAGES: DONE!!!")


    ########################### CREATING PDF ############################
    #if False:
    if True:
        subdirs = [p for p in wdir_path.glob('**/') if p.is_dir() and p != wdir_path and p.stem == OUTDIR]
        tasks = []
        for dir in subdirs:
            images = sorted(dir.glob(f"*{out_ext}"))
            pdf = wdir_path.joinpath(f"{OUT_FILE_PREFIX}{re.sub(r"-\d{6}", "", dir.parent.name)}.pdf")
            tasks.append((pdf, images))
        with ProcessPoolExecutor(max_workers=max_process) as pool:
            pool.map(img2pdf_proc, tasks)



    input("ALL DONE!!!!!!")