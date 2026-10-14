from bs4 import BeautifulSoup
import re
import html

def extract_structured_khampha():
    with open('KhamPha_raw.html', 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    main = soup.find('main')
    print("=== KHAM PHA TEXT ===")
    for el in main.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'li']):
        t = ' '.join(html.unescape(el.get_text()).split())
        if t and len(t) > 5:
            print(f"[{el.name}] {t}")

extract_structured_khampha()
