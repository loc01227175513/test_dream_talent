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


class TestStage(unittest.TestCase):
    def tearDown(self):
        for n in ("t_empty.md", "t_cached.md"):
            (agent.OUT / n).unlink(missing_ok=True)

    def test_stage_does_not_cache_empty_output(self):
        with self.assertRaises(SystemExit):
            agent.stage("t_empty.md", "p", run=lambda p: "  ")
        self.assertFalse((agent.OUT / "t_empty.md").exists())

    def test_stage_uses_cache(self):
        (agent.OUT / "t_cached.md").write_text("cached")
        self.assertEqual(agent.stage("t_cached.md", "p", run=lambda p: 1 / 0), "cached")


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


if __name__ == "__main__":
    unittest.main()
