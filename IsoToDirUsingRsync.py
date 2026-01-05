import subprocess
import tempfile
import shutil
from pathlib import Path

ISO_DIR = Path('/Volumes/DATA12TB/VIDEO TUTORIALS/Python/')   # folder containing .iso files
OUTPUT_BASE = Path('/Volumes/3TB-A/New Courses 1')              # output dirs created here

def run(cmd):
    subprocess.run(cmd, check=True)

for iso in ISO_DIR.glob("*.iso"):
    out_dir = OUTPUT_BASE / iso.stem

    if out_dir.exists():
        print(f"Skipping (already exists): {out_dir}")
        continue

    print(f"Processing: {iso.name}")

    mount_dir = Path(tempfile.mkdtemp(prefix="iso_mount_"))

    try:
        # Mount ISO
        run([
            "hdiutil", "attach", str(iso),
            "-mountpoint", str(mount_dir),
            "-nobrowse",
            "-readonly"
        ])

        # Rsync contents
        run([
            "rsync",
            "-av",
            #"--dry-run",
            f"{mount_dir}/",
            f"{out_dir}/"
        ])

    finally:
        # Always unmount & cleanup
        subprocess.run(
            ["hdiutil", "detach", str(mount_dir)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        shutil.rmtree(mount_dir, ignore_errors=True)

print("Done.")
