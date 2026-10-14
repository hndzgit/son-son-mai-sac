import json
import re
import os
import html

def clean_text(text):
    text = html.unescape(text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

print("Parser module ready.")
