"""Kontrollerar alla interna länkar i _site/ mot en mängd med de byggda filerna.

    python bygg/lankkoll.py
"""
import posixpath
import re
import sys
from pathlib import Path

UT = Path(__file__).resolve().parent.parent / "_site"
MAL = re.compile(r'(?:href|src)="([^"#?]+)')


def main():
    filer = {p.relative_to(UT).as_posix() for p in UT.rglob("*") if p.is_file()}
    unika, trasiga = set(), {}
    for fil in sorted(filer):
        if not fil.endswith(".html") or fil == "404.html":
            continue
        bas = posixpath.dirname(fil)
        for url in set(MAL.findall((UT / fil).read_text(encoding="utf-8"))):
            if url.startswith(("http:", "https:", "mailto:")):
                continue
            mal = posixpath.normpath(posixpath.join(bas, url))
            if url.endswith("/") or mal == ".":
                mal = "index.html" if mal == "." else f"{mal}/index.html"
            unika.add(mal)
            if mal not in filer:
                trasiga.setdefault(mal, fil)
    print(f"{len(unika)} unika länkmål, {len(trasiga)} trasiga.")
    for mal, fil in list(trasiga.items())[:20]:
        print(f"  {mal}  (från {fil})")
    return 1 if trasiga else 0


if __name__ == "__main__":
    sys.exit(main())
