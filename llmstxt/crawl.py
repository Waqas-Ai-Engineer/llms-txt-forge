"""Sources: local folder (offline) or live site (stdlib urllib, polite, same-origin)."""
import os
import re
import time
import urllib.request
from urllib.parse import urljoin, urlparse, urldefrag
from .extract import extract

UA = "llms-txt-forge/0.1 (+https://github.com/Waqas-Ai-Engineer/llms-txt-forge)"


def from_folder(root, base_url):
    pages = []
    for dp, _, fs in sorted(os.walk(root)):
        for f in sorted(fs):
            if not f.endswith((".html", ".htm")):
                continue
            full = os.path.join(dp, f)
            rel = os.path.relpath(full, root).replace(os.sep, "/")
            path = re.sub(r"index\.html?$", "", rel)
            path = re.sub(r"\.html?$", "", path)
            with open(full, encoding="utf-8", errors="replace") as fh:
                m = extract(fh.read())
            m["url"] = base_url.rstrip("/") + "/" + path.strip("/") if path.strip("/") else base_url.rstrip("/") + "/"
            pages.append(m)
    return pages


def _get(url, timeout=10):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        if "html" not in r.headers.get("Content-Type", "") and not url.endswith(("sitemap.xml",)):
            return ""
        return r.read(2_000_000).decode("utf-8", "replace")


def from_site(start, max_pages=40, delay=0.5, fetch=_get):
    host = urlparse(start).netloc
    seen, queue, pages = set(), [start], []
    try:
        sm = fetch(urljoin(start, "/sitemap.xml"))
        queue = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", sm)[:max_pages] or queue
    except Exception:
        pass
    while queue and len(pages) < max_pages:
        url = urldefrag(queue.pop(0))[0]
        if url in seen or urlparse(url).netloc != host:
            continue
        seen.add(url)
        try:
            html = fetch(url)
        except Exception:
            continue
        if not html:
            continue
        m = extract(html); m["url"] = url
        pages.append(m)
        queue += [urljoin(url, l) for l in m["links"] if not l.startswith(("mailto:", "tel:", "javascript:"))]
        time.sleep(delay)
    return pages
