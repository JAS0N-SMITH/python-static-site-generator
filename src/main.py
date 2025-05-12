import os
import shutil
import sys
from generate_pages_recursive import generate_pages_recursive


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

def main():
    static_dir = "static"
    public_dir = "docs"  # Changed from 'public' to 'docs' for GitHub Pages
    template_file = "template.html"

    # Get basepath from CLI argument or default to '/'
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    # Copy static files to docs directory
    copy_static_to_public(static_dir, public_dir)

    # Generate pages recursively with basepath
    generate_pages_recursive(
        "content", template_file, public_dir, basepath)

if __name__ == "__main__":
    main()
