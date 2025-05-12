import os
from markdown_to_html_node import markdown_to_html_node
from extract_title import extract_title


def generate_page(from_path, template_path, dest_path, basepath="/"):
    # Read the markdown file
    with open(from_path, 'r', encoding='utf-8') as markdown_file:
        markdown_content = markdown_file.read()

    # Read the template file
    with open(template_path, 'r', encoding='utf-8') as template_file:
        template_content = template_file.read()

    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    # Extract the title
    title = extract_title(markdown_content)

    # Replace placeholders in the template
    full_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)

    # Replace href and src paths with basepath
    full_html = full_html.replace('href="/', 'href="'+basepath)
    full_html = full_html.replace('src="/', 'src="'+basepath)

    # Ensure the destination directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Write the full HTML to the destination file
    with open(dest_path, 'w', encoding='utf-8') as dest_file:
        dest_file.write(full_html)