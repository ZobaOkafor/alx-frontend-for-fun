#!/usr/bin/python3
"""
A script that converts a Markdown file to HTML with custom transformations.
"""
import sys
import os
import re
import hashlib


def markdown_to_html(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as md_file:
        lines = md_file.readlines()

    html_content = []
    in_ul, in_ol, in_p = False, False, False

    def close_lists():
        nonlocal in_ul, in_ol
        if in_ul:
            html_content.append("</ul>")
            in_ul = False
        if in_ol:
            html_content.append("</ol>")
            in_ol = False

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("#"):
            close_lists()
            if in_p:
                html_content.append("</p>")
                in_p = False
            level = len(stripped.split(' ')[0])
            html_content.append(
                f"<h{level}>{stripped[level:].strip()}</h{level}>")

        elif stripped.startswith("- "):
            if in_ol:
                html_content.append("</ol>")
                in_ol = False
            if not in_ul:
                html_content.append("<ul>")
                in_ul = True
            html_content.append(
                f"    <li>{parse_custom_syntax(stripped[2:].strip())}</li>")

        elif stripped.startswith("* "):
            if in_ul:
                html_content.append("</ul>")
                in_ul = False
            if not in_ol:
                html_content.append("<ol>")
                in_ol = True
            html_content.append(
                f"    <li>{parse_custom_syntax(stripped[2:].strip())}</li>")

        else:
            close_lists()
            if not stripped and in_p:
                html_content.append("</p>")
                in_p = False
            elif stripped:
                if not in_p:
                    html_content.append("<p>")
                    in_p = True
                html_content.append(
                        f"    {parse_custom_syntax(stripped)}<br/>")

    close_lists()
    if in_p:
        html_content[-1] = html_content[-1].rstrip("<br/>")
        html_content.append("</p>")

    with open(output_file, 'w', encoding='utf-8') as html_file:
        html_file.write("\n".join(html_content))


def parse_custom_syntax(text):
    text = re.sub(
        r'\[\[(.*?)\]\]',
        lambda x: hashlib.md5(x.group(1).encode('utf-8')).hexdigest(),
        text
    )
    text = re.sub(
        r'\(\((.*?)\)\)',
        lambda x: x.group(1)
                          .replace('c', '')
                          .replace('C', ''),
        text
    )
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'__(.*?)__', r'<em>\1</em>', text)
    return text


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html",
              file=sys.stderr)
        sys.exit(1)

    input_file, output_file = sys.argv[1], sys.argv[2]

    if not os.path.isfile(input_file):
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)

    markdown_to_html(input_file, output_file)
    sys.exit(0)
