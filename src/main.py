import os
import shutil
import sys

from markdown_blocks import generate_page
from textnode import TextNode, TextType

def copy_stuff(from_dir, to_dir):
    files = os.listdir(from_dir)
    for file in files:
        file_path = os.path.abspath(f"{from_dir}/{file}")
        if os.path.isfile(file_path):
            if not os.path.exists(to_dir):
                os.mkdir(to_dir)
            shutil.copy(file_path, to_dir)
        else:
            if not os.path.exists(f"{to_dir}/{file}"):
                os.mkdir(f"{to_dir}/{file}")
            copy_stuff(file_path, f"{to_dir}/{file}")

def generate_pages(from_path, to_path, template, basepath):
    content = os.listdir(from_path)
    for file in content:
        if file == "index.md":
            generate_page(f"{from_path}/index.md",
                          template,
                          f"{to_path}",
                          basepath)
        else:
            if not os.path.exists(f"{to_path}/{file}"):
                os.mkdir(f"{to_path}/{file}")
            generate_pages(f"{from_path}/{file}", f"{to_path}/{file}", template, basepath)


def main():
    try:
        basepath = sys.argv[1]
    except:
        basepath = "/"

    root_dir = os.getcwd()
    from_dir = os.path.abspath(f"{root_dir}/static/")
    to_dir = os.path.abspath(f"{root_dir}/docs/")
    if os.path.exists(to_dir):
        shutil.rmtree(to_dir)
    copy_stuff(from_dir, to_dir)
    generate_pages(f"{root_dir}/content/", f"{root_dir}/docs/", f"{root_dir}/template.html", basepath)
    print("s")

if __name__ == "__main__":
    main()