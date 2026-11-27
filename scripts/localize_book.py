"""Đặt ngôn ngữ tiếng Việt và giữ đường dẫn đến các mục đã gộp."""

from html import escape
import os
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

# Các URL đã công bố dẫn tới nội dung tương ứng trong sách hiện tại.
base_url = os.environ.get("BASE_URL", "").rstrip("/")
old_pages = {
    "appendix": ("preprocessing", "imputation-six-features"),
    "text-rubric-audit": ("rubric-audit", "van-ban"),
}
for old_slug, (new_slug, section) in old_pages.items():
    if not (site / new_slug / "index.html").is_file():
        raise SystemExit(f"Không tìm thấy trang đích {new_slug} cho {old_slug}.")
    url = escape(f"{base_url}/{new_slug}/#{section}", quote=True)
    old_page = site / old_slug / "index.html"
    old_page.parent.mkdir(exist_ok=True)
    old_page.write_text(
        f'<!doctype html><html lang="vi"><head><meta charset="utf-8">'
        f'<meta http-equiv="refresh" content="0; url={url}">'
        f'<title>Tiền xử lý dữ liệu</title></head><body>'
        f'<p><a href="{url}">Đọc nội dung đã chuyển</a></p></body></html>\n',
        encoding="utf-8",
    )
