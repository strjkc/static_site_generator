import os
import shutil

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

def generate_pages(from_path, to_path):
    content = os.listdir(from_path)
    for file in content:
        if file == "index.md":
            generate_page(f"{from_path}/index.md",
                          "/home/stra/bootdev/projects/static_site_generator/template.html",
                          f"{to_path}")
        else:
            if not os.path.exists(f"{to_path}/{file}"):
                os.mkdir(f"{to_path}/{file}")
            generate_pages(f"{from_path}/{file}", f"{to_path}/{file}")


def main():
    node = TextNode("text", TextType.BOLD, "https://asdf.com")
    from_dir = os.path.abspath("/home/stra/bootdev/projects/static_site_generator/static/")
    to_dir = os.path.abspath("/home/stra/bootdev/projects/static_site_generator/public/")
    if os.path.exists(to_dir):
        shutil.rmtree(to_dir)
    copy_stuff(from_dir, to_dir)
    generate_pages("/home/stra/bootdev/projects/static_site_generator/content/", "/home/stra/bootdev/projects/static_site_generator/public/")


main()