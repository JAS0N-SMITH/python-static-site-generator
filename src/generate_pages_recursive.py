import os
from markdown_to_html_node import markdown_to_html_node
from extract_title import extract_title
from generate_page import generate_page

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # Walk through the content directory
    for root, _, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith('.md'):
                # Construct paths
                relative_path = os.path.relpath(root, dir_path_content)
                markdown_path = os.path.join(root, file)
                html_filename = os.path.splitext(file)[0] + '.html'
                dest_dir = os.path.join(dest_dir_path, relative_path)
                dest_path = os.path.join(dest_dir, html_filename)

                # Generate the page using the existing generate_page function
                generate_page(markdown_path, template_path, dest_path)


