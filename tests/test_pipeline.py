import io, tempfile, unittest, urllib.error
from pathlib import Path

import agent


class TestGet(unittest.TestCase):
    def test_get_retries_on_429_then_succeeds(self):
        calls = []
        def opener(req, timeout):
            calls.append(1)
            if len(calls) < 2:
                raise urllib.error.HTTPError(req.full_url, 429, "x", {"Retry-After": "1"}, None)
            return io.BytesIO("ok".encode())
        slept = []
        self.assertEqual(agent.get("https://x", opener=opener, sleep=slept.append), "ok")
        self.assertEqual(slept, [1])

    def test_get_raises_after_three_failures(self):
        def opener(req, timeout): raise urllib.error.URLError("down")
        with self.assertRaises(RuntimeError):
            agent.get("https://x", opener=opener, sleep=lambda s: None)


class TestFallback(unittest.TestCase):
    def test_fallback_graph_has_no_dangling_edges(self):
        g = agent.fallback_graph(Path("out/brief.md").read_text(), Path("out/SRS.md").read_text())
        ids = {n["id"] for n in g["nodes"]}
        self.assertIn({"from": "F-10", "to": "FR-08", "label": "specified_by"}, g["edges"])
        self.assertTrue(all(e["from"] in ids and e["to"] in ids for e in g["edges"]))


class TestWiki(unittest.TestCase):
    def test_build_wiki_links_feature_to_requirement(self):
        import wiki
        d = Path(tempfile.mkdtemp())
        wiki.build_wiki(Path("out/brief.md").read_text(), Path("out/SRS.md").read_text(), d)
        self.assertIn("[[FR-08]]", (d / "F-10.md").read_text())
        self.assertIn("[[F-10]]", (d / "M2.md").read_text())
        self.assertIn("[[M2]]", (d / "index.md").read_text())
        self.assertEqual(wiki.broken_links(d), [])

    def test_broken_links_detects_missing_page(self):
        import wiki
        d = Path(tempfile.mkdtemp())
        (d / "index.md").write_text("[[F-99]]")
        self.assertEqual(wiki.broken_links(d), ["index.md -> F-99"])


class TestValidate(unittest.TestCase):
    def test_check_srs_flags_missing_section_and_unknown_feature(self):
        import validate
        errs = validate.check_srs("## Functional Requirements\nFR-01 ... F-99", "F-01")
        self.assertIn("missing section: Non-Functional Requirements", errs)
        self.assertIn("unknown feature: F-99", errs)

    def test_check_srs_ok_on_current_outputs(self):
        import validate
        self.assertEqual(validate.check_srs(Path("out/SRS.md").read_text(), Path("out/brief.md").read_text()), [])


if __name__ == "__main__":
    unittest.main()
