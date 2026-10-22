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


if __name__ == "__main__":
    unittest.main()
