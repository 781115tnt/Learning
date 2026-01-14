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
#pip install img2pdf psutil pypdf

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

    TIF = ".tif"
    PNG = ".png"
    OUTDIR = "_out"
    IM_COLOR_FORMAT = "-colors 64 -define png:color-type=3"
    IM_BW_FORMAT = "-monochrome -compress Group4"
    IM_PROC_STR = "-fuzz 15% -fill \"red\" -opaque \"rgb(220,30,30)\" -fill \"blue\" -opaque \"rgb(30,30,170)\" -fill \"black\" -opaque \"rgb(20,20,20)\""
    GS_24BIT_DEVICE= "-sDEVICE=png16m" #"-sDEVICE=tiff24nc -sCompression=lzw"
    GS_1BIT_DEVICE= "-sDEVICE=tiffg4"
    GS_R600 = "-r600"
    GS_R300 = "-r300"
    GS_OUT = "_GS"
    IM_OUT = "_IM"
    IGNORED_OUT = "__IGNORE"
    OUT_FILE_PREFIX = "_OUT_"


    max_process = psutil.cpu_count(logical=False)
    wdir = " ".join(sys.argv[1:])
    wdir_path = Path(wdir)

    im_output_ext = PNG
    gs_output_ext = PNG
    
    gs_resstr = GS_R300
    gs_cluster = "1"
    gs_clusterstr = "-dMinFeatureSize=2"
    gs_device = GS_24BIT_DEVICE

    im_formatstr = IM_COLOR_FORMAT
    im_rotatestr = " "
    im_blurstr = " "
    im_levelstr = "-level 30%,90%"
    im_rot = "0"
    im_procstr = IM_PROC_STR



    imgProc = False

    ########################### ASKING FOR OPTIONS ############################
    if not wdir_path.exists():
        input("WORKING DIRECTORY DOES NOT EXIST!!!")
        sys.exit(0)
    ignored_path = wdir_path / IGNORED_OUT
    gsout_path = wdir_path / GS_OUT
    imout_path = wdir_path / IM_OUT

    imgp = input("Khong xu ly dam/nhat/xoa cham khong (Y?)")
    if imgp == "y" or imgp == "Y":
        imgProc = False
        im_procstr = " "
        print("-> Khong thay doi dam/nhat/xoa cham!")
    else:
        imgProc = True
        print("-> Co thay doi dam/nhat/xoa cham!")

        im_rot = input("Quay hinh luc xu ly (nhap 90, 180, 270):")
        if not (im_rot == "90" or im_rot == "180" or im_rot == "270") :
            print("-> Khong quay hinh!")
            im_rotatestr = " "
        else:
            print(f"-> Quay hinh {im_rot}")
            im_rotatestr = f"-im_rotate {im_rot}"

        dot = input("Xoa cham (Y?):")
        if dot == "y" or dot == "Y":
            print("-> Co Xoa Cham!")
            im_blurstr = "-blur 2x5"
            im_levelstr = "-level 45%,85%"
        else:
            print(f"-> Khong xoa cham!")

    bw = input("Ra file 1-bit (Y?):")
    if bw == "y" or bw == "Y":
        print("-> Ra file 1-bit!")
        im_output_ext = TIF
        im_formatstr = IM_BW_FORMAT
        if imgProc:
            gs_device = GS_24BIT_DEVICE
            gs_output_ext = PNG
        else:
            gs_device = GS_1BIT_DEVICE
            gs_output_ext = TIF
    else:
        im_output_ext = PNG
        if imgProc:
            im_formatstr = IM_COLOR_FORMAT
            print(f"-> Ra file 64 mau!")
        else:
            
            im_formatstr = " "
            print(f"-> Ra file 24bit mau!")
    
    res = input("Resolution = 600dpi (Y?):")
    if res == "y" or res == "Y":
        print("-> Do phan giai 600dpi!")
        gs_resstr = GS_R600
    else:
        print("-> Do phan giai 300dpi!")    

    gs_cluster = input("Min Cluster size (nhap 2, 3, 4)?:")
    if not (gs_cluster == "2" or gs_cluster == "3" or gs_cluster == "4"):
        print("-> Khong set cluster!")
        gs_clusterstr = " "
    else:
        gs_clusterstr = f"-dMinFeatureSize={gs_cluster}"
        print(f"-> Cluster={gs_cluster}!")
    
    
    ########################### FLATEN FILES ############################
    #if False:
    if True:
        for d, _, filenames in os.walk(wdir_path):
            for f in filenames:
                fnlc = f.lower()
                if fnlc.endswith(".py") or fnlc.lower().endswith(".bat"): continue
                full = Path(d) / f
                flat = "__xxx__".join(full.relative_to(wdir_path).parts)
                full.copy(wdir_path / flat)
                #full.rename(wdir_path / flat)

        #for x in wdir_path.iterdir():
        #    if x.is_dir(): shutil.rmtree(x)

        ignored_path.mkdir(exist_ok=True)
        input("MOVE CAC FILES KHONG CAN XU LY VAO THU MUC __IGNORE, SAU DO NHAN ENTER DE TIEP TUC...")

    ########################### EXTRACTING PDF FILES ############################
    #if False:
    if True:
        gsout_path.mkdir(exist_ok=True)
        jobs = []
        for pdf in Path(wdir).glob("*.pdf"):
            #Ignore all pdfs in the IGNORED_OUT folder
            if pdf.parent.name == IGNORED_OUT: continue
            #Create output folder for each pdf
            pdfoutpath = (gsout_path / pdf.stem)
            pdfoutpath.mkdir(exist_ok=True)
            #Create command for each page
            for pn in range(1, len(PdfReader(pdf).pages) + 1):
                pnstr = f"{pn:010d}"
                cmd = f"gswin64c.exe -o \"{pdfoutpath / pnstr}{gs_output_ext}\" {gs_device} {gs_resstr} -dUseCropBox {gs_clusterstr} -dFirstPage={pn} -dLastPage={pn} \"{pdf.stem}\".pdf"
                jobs.append(cmd)
                #print(cmd)
        with ProcessPoolExecutor(max_workers=max_process) as pool:
            pool.map(ghostscript_proc, jobs)


    ########################### PROCESSING IMAGES ############################
    #if False:
    if True:
        #Create IM_OUT folder and subfolders
        imout_path.mkdir(exist_ok=True)
        for p in gsout_path.iterdir():
            if p.is_dir(): 
                (imout_path / p.name).mkdir(exist_ok=True)
        
        imgs = [f for f in gsout_path.rglob("*") if f.is_file()]

        if imgProc:
            tasks = []
            for tpath in imgs:
                ofile = imout_path / tpath.parent.name / tpath.name
                cmd = f"magick \"{str(tpath)}\" -limit memory 16GiB {im_procstr} {im_rotatestr} {im_blurstr} {im_levelstr} {im_formatstr} \"{str(ofile)}\""
                tasks.append(cmd)  
            #for t in tasks: print(t)   
            with ProcessPoolExecutor(max_workers=max_process) as pool: pool.map(imagemagick_proc, tasks)
            
        else:
            for tpath in imgs:
                ofile = imout_path / tpath.parent.name / tpath.name
                shutil.copy(tpath, ofile)

        print("PROCESSING IMAGES: DONE!!!")


    ########################### CREATING PDF ############################
    #if False:
    if True:
        subdirs = [d for d in imout_path.rglob("*") if d.is_dir()]
        tasks = []
        for dir in subdirs:
            images = sorted(dir.glob("*"))
            pdf = wdir_path / f"{OUT_FILE_PREFIX}{re.sub(r"-\d{6}", "", dir.name)}.pdf"
            tasks.append((pdf, images))
        with ProcessPoolExecutor(max_workers=max_process) as pool:
            pool.map(img2pdf_proc, tasks)




    input("ALL DONE!!!!!!")