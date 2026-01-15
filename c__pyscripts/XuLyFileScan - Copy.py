import subprocess
from concurrent.futures import ProcessPoolExecutor
import glob
import os
import img2pdf
from pathlib import Path
import re
import psutil
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



########################### MULTIPROCESS-SAFE CODE ############################
if __name__ == "__main__":   # VERY IMPORTANT ON WINDOWS

    TIF = '.tif'
    PNG = '.png'
    OUTDIR = "_out"
    COLOR_FORMAT = "-colors 64 -define png:color-type=3"
    BW_FORMAT = "-monochrome -compress Group4"
    RENAMEME = "renameme"

    max_process = psutil.cpu_count(logical=False)

    wdir = " ".join(sys.argv[1:]).rstrip().lstrip()
    if not wdir:
        wdir = os.getcwd()
    #print(wdir)
    wdir_path = Path(wdir)

    out_ext = PNG
    formatstr = COLOR_FORMAT

    rotatestr = ""
    blurstr = ""
    levelstr = "-level 30%,90%"
    rot = 0

    ########################### ASKING FOR OPTIONS ############################
    if not wdir_path.exists():
        input("WORKING DIRECTORY DOES NOT EXIST!!!")
        sys.exit(0)

    try:
        rot = int(input("Quay hinh luc xu ly (nhap 0, 90, 180, 270):"))
    except  (ValueError, TypeError):
        #print(TypeError)
        rot = -1
    finally:
        if not (rot == 0 or rot == 90 or rot == 180 or rot == 270) :
            print("Nhap sai gia tri -> Khong quay hinh!")
        else:
            rotatestr = f"-rotate {rot}"

    dot = input("Xoa cham? (Y/N):")
    if dot == "y" or dot == "Y":
        blurstr = "-blur 2x5"
        levelstr = "-level 45%,85%"

    bw = input("Ra file 1-bit? (Y/N):")
    if bw == 'y' or bw == 'Y':
        out_ext = TIF
        formatstr = BW_FORMAT


    ########################### MAKE OUTDIRS ############################
    #if False:
    if True:
        #move all outside files into noname folder
        osfs = [f for f in wdir_path.glob("*") if f.is_file()]
        if len(osfs) > 0:
            ren_path = wdir_path / RENAMEME
            os.makedirs(ren_path, exist_ok=True)
            for f in osfs:
                f.rename(ren_path / f.name)
            print("LUU Y: CO FILE DE NGOAI THU MUC -> CAC FILE NAY SE DE TRONG renameme.pdf!!!!!!!!")

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
            cmd = f"magick \"{t}\" -limit memory 16GiB -fuzz 15%  -fill \"red\" -opaque \"rgb(220,30,30)\" -fill \"blue\" -opaque \"rgb(30,30,170)\" -fill \"black\" -opaque \"rgb(20,20,20)\" {rotatestr} {blurstr} {levelstr} {formatstr} \"{ofile}\""
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
            pdf = wdir_path.joinpath(f"{re.sub(r"-\d{6}", "", dir.parent.name)}.pdf")
            tasks.append((pdf, images))
        with ProcessPoolExecutor(max_workers=max_process) as pool:
            pool.map(img2pdf_proc, tasks)



    input("ALL DONE!!!!!!")