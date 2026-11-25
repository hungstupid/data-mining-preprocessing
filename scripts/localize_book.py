"""Khai báo ngôn ngữ của báo cáo trong HTML tĩnh do book-theme sinh ra."""

from pathlib import Path
import re

site = Path("_build/html")
pages = sorted(site.rglob("index.html"))
if not pages:
    raise SystemExit("Dựng HTML bằng jupyter book build --html trước.")

for page in pages:
    html = page.read_text(encoding="utf-8")
    html_vi, count = re.subn(r'(<html\b[^>]*\blang=")[^"]+(")', r"\g<1>vi\2", html, count=1)
    if count != 1:
        raise SystemExit(f"Không tìm thấy thuộc tính lang trong {page}.")
    page.write_text(html_vi, encoding="utf-8")
