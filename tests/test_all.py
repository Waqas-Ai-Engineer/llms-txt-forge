import os, sys, tempfile, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from llmstxt.extract import extract
from llmstxt.crawl import from_folder, from_site
from llmstxt.build import build
from llmstxt.validate import validate
from llmstxt.cli import main

SITE = os.path.join(os.path.dirname(__file__), "..", "examples", "site")


class T(unittest.TestCase):
    def test_extract(self):
        m = extract("<title>A</title><meta name='description' content='D'><a href='/x'>x</a>")
        self.assertEqual((m["title"], m["description"], m["links"]), ("A", "D", ["/x"]))

    def test_description_fallback_to_body(self):
        self.assertTrue(extract("<title>A</title><p>Same day emergency help here</p>")["description"].startswith("Same day"))

    def test_build_structure_and_noindex(self):
        txt = build(from_folder(SITE, "https://brightsmile.example"), "BrightSmile Dental")
        self.assertTrue(txt.startswith("# BrightSmile Dental\n\n> Family dental"))
        self.assertIn("## Services", txt)
        self.assertIn("## Optional", txt)
        self.assertNotIn("thank-you", txt)
        self.assertEqual([i for i in validate(txt) if i[0] == "error"], [])

    def test_optional_last(self):
        txt = build(from_folder(SITE, "https://x.example"), "X")
        self.assertGreater(txt.index("## Optional"), txt.index("## Services"))

    def test_validate_catches_errors(self):
        self.assertTrue(any(l == "error" for l, _ in validate("no title\n- bad")))

    def test_site_crawl_with_fake_fetch(self):
        pages = {"https://a.example/": "<title>Home</title><a href='/p'>p</a>", "https://a.example/p": "<title>P</title>"}
        def fetch(u):
            if u not in pages: raise IOError
            return pages[u]
        got = from_site("https://a.example/", 10, 0, fetch)
        self.assertEqual({g["url"] for g in got}, set(pages))

    def test_cli_generate_and_validate(self):
        with tempfile.TemporaryDirectory() as d:
            out = os.path.join(d, "llms.txt")
            self.assertEqual(main(["generate", SITE, "--name", "BrightSmile", "--base-url", "https://b.example", "--out", out, "--full"]), 0)
            self.assertTrue(os.path.exists(os.path.join(d, "llms-full.txt")))
            self.assertEqual(main(["validate", out]), 0)


if __name__ == "__main__":
    unittest.main()
