import os
import shutil

FILES_DIR = "/Volumes/DATA12TB/VIDEO TUTORIALS"
SUBDIRS_DIR = '/Volumes/3TB-B/New Courses 2'
DEST_DIR = "/Volumes/DATA12TB/VIDEO TUTORIALS/EXISTS"

os.makedirs(DEST_DIR, exist_ok=True)

# collect subdirectory names (no recursion)
subdirs = {
    d.lower().replace(' ','').replace('-', '').replace('.','').replace('_','')
    for d in os.listdir(SUBDIRS_DIR)
    if os.path.isdir(os.path.join(SUBDIRS_DIR, d))
}

for file in os.listdir(FILES_DIR):
    file_path = os.path.join(FILES_DIR, file)
    if not os.path.isfile(file_path):
        continue

    name_no_ext = os.path.splitext(file)[0].lower().replace(' ','').replace('-', '').replace('.','').replace('_','')

    if name_no_ext in subdirs:
        shutil.move(file_path, DEST_DIR)
        #print(file_path)
