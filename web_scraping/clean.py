import os
import re
import sys
import docx
import requests
from bs4 import BeautifulSoup

#clean.py
def replace_chars(text):
    chars_to_replace = [f"[{i}]" for i in range(1, 100)]
    for char in chars_to_replace:
        text = text.replace(char, ' ')
    text = text.replace('\t', '   ')  # Replace tab with three spaces
    return text

def clean_text_file(filename):
    if not os.path.isfile(filename):
        print(f'Error: {filename} does not exist')
        sys.exit(1)

    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()

    # Replace multiple consecutive new lines with a single new line and add three spaces instead of new line
    text = re.sub(r'\n+', '   ', text.strip())

    # Replace 3 or more spaces with 2 spaces
    text = re.sub(r' {3,}', '  ', text)

    doc = docx.Document()
    doc.add_paragraph(text, style='Normal')
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = docx.shared.Pt(12)

    doc_file_name = os.path.splitext(filename)[0] + '.docx'

    doc.save(doc_file_name)

    os.remove(filename)

