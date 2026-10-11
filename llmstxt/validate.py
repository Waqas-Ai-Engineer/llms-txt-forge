"""Validate an llms.txt against the llmstxt.org structure."""
import re

LINK = re.compile(r"^- \[[^\]]+\]\((https?://[^)\s]+)\)(?::\s.+)?$")


def validate(text):
    issues = []
    lines = text.splitlines()
    if not lines or not lines[0].startswith("# "):
        issues.append(("error", "First line must be an H1 title ('# Name')."))
    if not any(l.startswith("> ") for l in lines[:5]):
        issues.append(("warn", "Missing blockquote summary near the top ('> ...')."))
    if not any(l.startswith("## ") for l in lines):
        issues.append(("error", "No H2 sections found."))
    seen = set()
    for i, l in enumerate(lines, 1):
        if l.startswith("- ") and not LINK.match(l):
            issues.append(("error", f"Line {i}: list item is not '- [title](https://url): note'."))
        m = LINK.match(l)
        if m:
            if m.group(1) in seen:
                issues.append(("warn", f"Line {i}: duplicate URL {m.group(1)}."))
            seen.add(m.group(1))
    if not seen:
        issues.append(("error", "No links found."))
    if len(text) > 100_000:
        issues.append(("warn", "File is very large; keep llms.txt concise."))
    return issues
