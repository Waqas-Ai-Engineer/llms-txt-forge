"""Page metadata extraction (stdlib html.parser)."""
from html.parser import HTMLParser
import re


class _P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""; self.desc = ""; self.h1 = ""; self.links = []
        self.noindex = False
        self._in = None; self._skip = 0; self.text = []; self._canon = ""

    def handle_starttag(self, tag, a):
        a = dict(a)
        if tag in ("script", "style", "nav", "footer", "noscript"):
            self._skip += 1
        if tag == "title": self._in = "title"
        elif tag == "h1" and not self.h1: self._in = "h1"
        elif tag == "meta":
            n = (a.get("name") or a.get("property") or "").lower()
            if n in ("description", "og:description") and not self.desc:
                self.desc = (a.get("content") or "").strip()
            if n == "robots" and "noindex" in (a.get("content") or "").lower():
                self.noindex = True
        elif tag == "a" and a.get("href"):
            self.links.append(a["href"])
        elif tag == "link" and (a.get("rel") or "").lower() == "canonical":
            self._canon = a.get("href", "")

    def handle_endtag(self, tag):
        if tag in ("script", "style", "nav", "footer", "noscript") and self._skip:
            self._skip -= 1
        if tag in ("title", "h1"):
            self._in = None

    def handle_data(self, d):
        if self._in == "title": self.title += d
        elif self._in == "h1": self.h1 += d
        if not self._skip and self._in != "title": self.text.append(d)


def extract(html):
    p = _P()
    p.feed(html)
    clean = lambda s: re.sub(r"\s+", " ", s).strip()
    body = clean(" ".join(p.text))
    desc = clean(p.desc)
    if not desc and body:
        h1 = clean(p.h1)
        b = body[len(h1):].strip() if h1 and body.startswith(h1) else body
        desc = b if len(b) <= 160 else b[:160].rsplit(" ", 1)[0].rstrip(",;:") + "..."
    title = clean(p.title) or clean(p.h1)
    return {"title": title, "description": desc, "links": p.links, "noindex": p.noindex, "text": body}
