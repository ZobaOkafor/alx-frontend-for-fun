#!/usr/bin/python3
"""
A script that converts a Markdown file to HTML.
"""
import sys
import os
import markdown


def markdown_to_html(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as md_file:
        text = md_file.read()
        html = markdown.markdown(text)

        with open(output_file, 'w', encoding='utf-8') as html_file:
            html_file.write(html)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html",
              file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.isfile(input_file):
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)

    markdown_to_html(input_file, output_file)
    sys.exit(0)
