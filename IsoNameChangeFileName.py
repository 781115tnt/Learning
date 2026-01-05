import subprocess
import os
import sys

folder = "/Volumes/3TB-A/working"

def rename_iso_to_volume_name(iso_path):
    iso_path = os.path.abspath(iso_path)

    # Mount ISO without opening Finder
    result = subprocess.check_output(
        ["hdiutil", "attach", "-nobrowse", iso_path],
        text=True
    )

    volume_path = None
    for line in result.splitlines():
        if "/Volumes/" in line:
            volume_path = line.split("\t")[-1]
            break

    if not volume_path or not os.path.exists(volume_path):
        raise RuntimeError("Mounted volume not found")

    volume_name = os.path.basename(volume_path)

    # Unmount ISO
    subprocess.check_call(["hdiutil", "detach", volume_path])

    # Sanitize filename
    safe_name = volume_name.replace("/", "_")

    new_path = os.path.join(
        os.path.dirname(iso_path),
        f"{safe_name}.iso"
    )

    # Avoid overwrite
    if os.path.exists(new_path):
        raise FileExistsError(f"Target exists: {new_path}")

    os.rename(iso_path, new_path)
    return new_path


def batch_rename(folder):
    for name in sorted(os.listdir(folder)):
        if not name.lower().endswith(".iso"):
            continue

        iso = os.path.join(folder, name)
        try:
            new_name = rename_iso_to_volume_name(iso)
            print(f"✔ {name} → {os.path.basename(new_name)}")
        except Exception as e:
            print(f"✘ {name}: {e}")


batch_rename(folder)