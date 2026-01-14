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
    IM_COLOR_FORMAT = "-colors 64 -define png:color-type=3"
    IM_BW_FORMAT = "-monochrome -compress Group4"
    GS_24BIT_DEVICE= "-sDEVICE=tiff24nc -sCompression=lzw"
    GS_1BIT_DEVICE= "-sDEVICE=tiffg4"
    GS_R600 = '-r600'
    GS_R300 = '-r300'
    OUT_FILE_PREFIX = '_OUT_'

    max_process = psutil.cpu_count(logical=False)
    wdir = ' '.join(sys.argv[1:])
    wdir_path = Path(wdir)

    out_ext = PNG
    
    gs_resstr = GS_R300
    gs_cluster = '1'
    gs_clusterstr = "-dMinFeatureSize=2"
    gs_device = GS_24BIT_DEVICE

    im_formatstr = IM_COLOR_FORMAT
    im_im_rotatestr = ''
    im_blurstr = ''
    im_levelstr = "-level 30%,90%"
    im_rot = '0'



    imgProc = False

    ########################### ASKING FOR OPTIONS ############################
    if not wdir_path.exists():
        input("WORKING DIRECTORY DOES NOT EXIST!!!")
        sys.exit(0)      
    imgp = input("Khong xu ly dam/nhat/xoa cham khong (Y?)")
    if imgp == 'y' or imgp == 'Y':
        imgProc = False
        print("-> Khong thay doi dam/nhat/xoa cham!")
    else:
        imgProc = True
        print("-> Co thay doi dam/nhat/xoa cham!")

        im_rot = input("Quay hinh luc xu ly (nhap 90, 180, 270):")
        if not (im_rot == '90' or im_rot == '180' or im_rot == '270') :
            print("-> Khong quay hinh!")
            im_im_rotatestr = ''
        else:
            print(f"-> Quay hinh {im_rot}")
            im_im_rotatestr = f"-im_rotate {im_rot}"

        dot = input("Xoa cham (Y?):")
        if dot == "y" or dot == "Y":
            print("-> Co Xoa Cham!")
            im_blurstr = "-blur 2x5"
            im_levelstr = "-level 45%,85%"
        else:
            print(f"-> Khong xoa cham!")

    bw = input("Ra file 1-bit (Y?):")
    if bw == 'y' or bw == 'Y':
        print("-> Ra file 1-bit!")
        out_ext = TIF
        im_formatstr = IM_BW_FORMAT
        if imgProc:
            gs_device = GS_24BIT_DEVICE
        else:
            gs_device = GS_1BIT_DEVICE
    else:
        print(f"-> Ra file mau!")
    
    res = input("Resolution = 600dpi (Y?):")
    if res == 'y' or res == 'Y':
        print("-> Do phan giai 600dpi!")
        gs_resstr = GS_R600
    else:
        print("-> Do phan giai 300dpi!")    

    gs_cluster = input("Min Cluster size (nhap 2, 3, 4)?:")
    if not (gs_cluster == '2' or gs_cluster == '3' or gs_cluster == '4'):
        print("-> Khong set cluster!")
        gs_clusterstr = ''
    else:
        gs_clusterstr = f"-dMinFeatureSize={gs_cluster}"
        print(f"-> Cluster={gs_cluster}!")
    
    
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
                cmd = f"gswin64c.exe -o \".\\{pdf.stem}\\{pn:010d}.tif\" {gs_device} {gs_resstr} -dUseCropBox {gs_clusterstr} -dFirstPage={pn} -dLastPage={pn} \"{pdf.stem}\".pdf"
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
    if imgProc:
        tfiles = glob.glob(f"{wdir}\\**\\*{TIF}", recursive=False)
        #print(tfiles)
        tasks = []
        for t in tfiles:
            tpath = Path(t)
            if tpath.is_dir(): continue
            ofile = f"{tpath.parent.joinpath(OUTDIR).joinpath(tpath.stem)}{out_ext}"
            cmd = f"convert \"{t}\" -limit memory 16GiB -fuzz 15%  -fill \"red\" -opaque \"rgb(220,30,30)\" -fill \"blue\" -opaque \"rgb(30,30,170)\" -fill \"black\" -opaque \"rgb(20,20,20)\" {im_im_rotatestr} {im_blurstr} {im_levelstr} {im_formatstr} \"{ofile}\""
            tasks.append(cmd)  
        #for t in tasks: print(t)   
        with ProcessPoolExecutor(max_workers=max_process) as pool: pool.map(imagemagick_proc, tasks)
        
    else:
        tfiles = glob.glob(f"{wdir}\\**\\*", recursive=False)
        for t in tfiles:
            tpath = Path(t)
            if tpath.is_dir(): continue
            ofile = f"{tpath.parent.joinpath(OUTDIR).joinpath(tpath.name)}"
            tpath.move(ofile)

        print("PROCESSING IMAGES: DONE!!!")


    ########################### CREATING PDF ############################
    #if False:
    if True:
        subdirs = [p for p in wdir_path.glob('**/') if p.is_dir() and p != wdir_path and p.stem == OUTDIR]
        tasks = []
        for dir in subdirs:
            #images = sorted(dir.glob(f"*{out_ext}"))
            images = sorted(dir.glob("*"))
            pdf = wdir_path.joinpath(f"{OUT_FILE_PREFIX}{re.sub(r"-\d{6}", "", dir.parent.name)}.pdf")
            tasks.append((pdf, images))
        with ProcessPoolExecutor(max_workers=max_process) as pool:
            pool.map(img2pdf_proc, tasks)



    input("ALL DONE!!!!!!")