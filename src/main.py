import os
import shutil


def copy_static_to_public(static_dir, public_dir):
    # Delete the contents of the destination directory
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
    os.makedirs(public_dir, exist_ok=True)

    # Recursively copy files and directories
    for root, dirs, files in os.walk(static_dir):
        for dir_name in dirs:
            src_dir = os.path.join(root, dir_name)
            dest_dir = os.path.join(
                public_dir, os.path.relpath(src_dir, static_dir))
            os.makedirs(dest_dir, exist_ok=True)
        for file_name in files:
            src_file = os.path.join(root, file_name)
            dest_file = os.path.join(
                public_dir, os.path.relpath(src_file, static_dir))
            shutil.copy2(src_file, dest_file)
            print(f"Copied: {dest_file}")

def main():
    static_dir = "static"
    public_dir = "public"
    copy_static_to_public(static_dir, public_dir)

if __name__ == "__main__":
    main()
