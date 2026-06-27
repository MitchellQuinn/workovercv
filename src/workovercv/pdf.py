from __future__ import annotations

from html import escape
from pathlib import Path


PDF_STYLES = """
@page {
  size: A4;
  margin: 0.75in;
}

body {
  color: #1f2933;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: 10.5pt;
  line-height: 1.45;
}

h1,
h2,
h3 {
  color: #111827;
  page-break-after: avoid;
}

h1 {
  border-bottom: 1px solid #d1d5db;
  font-size: 22pt;
  margin: 0 0 0.35in;
  padding-bottom: 0.12in;
}

h2 {
  font-size: 15pt;
  margin: 0.28in 0 0.12in;
}

h3 {
  font-size: 12pt;
  margin: 0.2in 0 0.08in;
}

p,
li {
  orphans: 3;
  widows: 3;
}

code {
  background: #f3f4f6;
  border-radius: 2px;
  font-family: "Cascadia Mono", "Consolas", monospace;
  font-size: 9pt;
  padding: 0.5pt 2pt;
}

pre {
  background: #f3f4f6;
  border: 1px solid #d1d5db;
  border-radius: 3px;
  font-size: 8.5pt;
  padding: 8pt;
  white-space: pre-wrap;
}

table {
  border-collapse: collapse;
  font-size: 8.5pt;
  margin: 0.12in 0;
  page-break-inside: auto;
  width: 100%;
}

tr {
  page-break-inside: avoid;
}

th,
td {
  border: 1px solid #d1d5db;
  padding: 4pt 5pt;
  vertical-align: top;
}

th {
  background: #f3f4f6;
  font-weight: 700;
}
"""


def write_pdf_from_markdown(markdown_text: str, target: Path, *, title: str) -> None:
    html = _markdown_to_html_document(markdown_text, title=title)
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        from weasyprint import HTML
    except (ImportError, OSError) as exc:
        raise RuntimeError(
            "PDF rendering requires the 'weasyprint' package. Install WorkOverCV with runtime dependencies and run "
            "'python -m weasyprint --info' to verify native PDF dependencies."
        ) from exc
    try:
        HTML(string=html, base_url=str(target.parent)).write_pdf(target)
    except Exception as exc:
        raise RuntimeError(f"PDF rendering failed for {target.name}: {exc}") from exc


def _markdown_to_html_document(markdown_text: str, *, title: str) -> str:
    try:
        import markdown as markdown_lib
    except ImportError as exc:
        raise RuntimeError(
            "PDF rendering requires the 'Markdown' package. Install WorkOverCV with runtime dependencies."
        ) from exc

    body = markdown_lib.markdown(
        markdown_text,
        extensions=["extra", "sane_lists"],
        output_format="html5",
    )
    escaped_title = escape(title)
    return (
        "<!doctype html>\n"
        '<html lang="en">\n'
        "<head>\n"
        '  <meta charset="utf-8">\n'
        f"  <title>{escaped_title}</title>\n"
        f"  <style>{PDF_STYLES}</style>\n"
        "</head>\n"
        "<body>\n"
        f"{body}\n"
        "</body>\n"
        "</html>\n"
    )
