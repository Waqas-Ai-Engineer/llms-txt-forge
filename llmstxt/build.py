"""Build llms.txt per the llmstxt.org format: H1, blockquote summary, H2 sections of links."""
from urllib.parse import urlparse

SECTION_NAMES = {"services": "Services", "service": "Services", "blog": "Blog", "docs": "Docs",
                 "pricing": "Pricing", "about": "About", "contact": "Contact", "products": "Products",
                 "faq": "FAQ", "case-studies": "Case Studies", "guides": "Guides"}
OPTIONAL = {"Blog", "Case Studies"}


def _section(url):
    parts = [p for p in urlparse(url).path.split("/") if p]
    if not parts:
        return "Main"
    if len(parts) == 1:
        return SECTION_NAMES.get(parts[0].lower(), "Main")
    return SECTION_NAMES.get(parts[0].lower(), parts[0].replace("-", " ").title())


def build(pages, name, summary="", include_noindex=False, full=False):
    pages = [p for p in pages if p["title"] and (include_noindex or not p["noindex"])]
    if not summary:
        home = next((p for p in pages if urlparse(p["url"]).path in ("", "/")), None)
        summary = home["description"] if home else ""
    out = [f"# {name}", ""]
    if summary:
        out += [f"> {summary}", ""]
    groups = {}
    for p in pages:
        groups.setdefault(_section(p["url"]), []).append(p)
    order = sorted(groups, key=lambda s: (s in OPTIONAL, s != "Main", s))
    for sec in order:
        out.append(f"## {'Optional' if sec in OPTIONAL else sec}")
        out.append("")
        for p in groups[sec]:
            d = f": {p['description']}" if p["description"] else ""
            out.append(f"- [{p['title']}]({p['url']}){d}")
        out.append("")
    txt = "\n".join(out).rstrip() + "\n"
    if not full:
        return txt
    fl = [f"# {name}", ""]
    for p in pages:
        fl += [f"## {p['title']}", f"Source: {p['url']}", "", p["text"], ""]
    return txt, "\n".join(fl)
