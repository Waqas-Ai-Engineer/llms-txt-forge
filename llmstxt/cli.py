import argparse
import sys
from .crawl import from_folder, from_site
from .build import build
from .validate import validate


def main(argv=None):
    p = argparse.ArgumentParser(prog="llmstxt", description="Generate and validate llms.txt files.")
    sub = p.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("generate", help="build llms.txt from a live site or a local HTML folder")
    g.add_argument("source", help="https://example.com or ./site-folder")
    g.add_argument("--name", required=True, help="site / business name (H1)")
    g.add_argument("--base-url", default="https://example.com", help="public URL for folder mode")
    g.add_argument("--summary", default="")
    g.add_argument("--max-pages", type=int, default=40)
    g.add_argument("--out", default="llms.txt")
    g.add_argument("--full", action="store_true", help="also write llms-full.txt")
    v = sub.add_parser("validate", help="check an existing llms.txt")
    v.add_argument("file")
    a = p.parse_args(argv)
    if a.cmd == "validate":
        issues = validate(open(a.file, encoding="utf-8").read())
        for lvl, msg in issues:
            print(f"{lvl.upper()}: {msg}")
        print("OK" if not any(l == "error" for l, _ in issues) else "FAILED")
        return 1 if any(l == "error" for l, _ in issues) else 0
    pages = from_site(a.source, a.max_pages) if a.source.startswith("http") else from_folder(a.source, a.base_url)
    if not pages:
        print("no pages found", file=sys.stderr)
        return 2
    res = build(pages, a.name, a.summary, full=a.full)
    txt, full = res if a.full else (res, None)
    open(a.out, "w", encoding="utf-8").write(txt)
    print(f"wrote {a.out} ({len(pages)} pages)")
    if full:
        open(a.out.replace(".txt", "-full.txt"), "w", encoding="utf-8").write(full)
    return 0


if __name__ == "__main__":
    sys.exit(main())
