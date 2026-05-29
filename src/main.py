import os
import shutil
import sys
from pathlib import Path

from mark_to_block import markdown_to_blocks, block_to_block_type, BlockType
from mark_to_html_node import markdown_to_html_node
from htmlnode import LeafNode, ParentNode, HTMLNode


def copy_directory(source, destination):
    
    if os.path.exists(path=destination):
        shutil.rmtree(path=destination)
    
    os.mkdir(destination)
    copy_contents(source=source, destination=destination)

def copy_contents(source, destination):

    for item in os.listdir(source):
        src_path = os.path.join(source, item)
        dst_path = os.path.join(destination, item)

        if os.path.isfile(src_path):
            print(f"Copying {src_path} to {dst_path}")
            shutil.copy(src_path, dst_path)
        else:
            os.mkdir(dst_path)
            copy_contents(src_path, dst_path)

def extract_title(markdown):
    split_lines = markdown.split("\n")
    for line in split_lines:
        if line.startswith("# "):
            return line[1:].strip()
    raise Exception("No title found")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"DEBUG generate_page called with: {from_path}")
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        from_md = f.read()
    with open(template_path) as f:
        temp_file = f.read()
    md_string = markdown_to_html_node(from_md).to_html()
    title = extract_title(from_md)

    filled = temp_file.replace("{{ Title }}", title).replace("{{ Content }}", md_string)
    filled = filled.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
    folder = os.path.dirname(dest_path)
    os.makedirs(folder, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(filled)

def generate_page_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    content_path_list = os.listdir(dir_path_content)
    for path in content_path_list:
        source_path = os.path.join(dir_path_content, path)
        dest_path = os.path.join(dest_dir_path, path)
        if not os.path.isfile(source_path):
            generate_page_recursive(source_path, template_path, dest_path, basepath)
        else:
            if source_path.endswith(".md"):
                dest_path = Path(dest_path).with_suffix(".html")
                print(f"About to generate: {source_path}")
                generate_page(source_path, template_path, dest_path, basepath)

if len(sys.argv) > 1:
    basepath = sys.argv[1]
else:
    basepath = "/"

def main():
    source = "static"
    destination = "public"
    try:
        copy_directory(source=source, destination=destination)
        print("Copy completed, Source: Static, Destination: Public")
    except Exception as e:
        print(f"Did not complete copy, Error: {e}")

    # generate_page("content/index.md", "template.html", "public/index.html")


    
    generate_page_recursive("content", "template.html", "public", basepath)
    

if __name__ == "__main__":
    main()

