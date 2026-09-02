"""Range-resume + shrink-on-timeout for Kie/CDN result downloads."""
from __future__ import annotations

import http.server
import sys
import threading
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from asset_download import download_url_bytes  # noqa: E402


PNG8 = bytes.fromhex("89504e470d0a1a0a")


class _RangeHandler(http.server.BaseHTTPRequestHandler):
    payload = PNG8 + (b"Q" * (24 * 1024 - 8))
    stall_if_range_gt = 2 * 1024
    stall_after_offset = 8 * 1024
    stall_seconds = 2.0
    seen_starts: list[int]

    def log_message(self, fmt: str, *args: object) -> None:
        return

    def do_GET(self) -> None:  # noqa: N802
        rng = self.headers.get("Range") or ""
        if not rng.startswith("bytes="):
            time.sleep(self.stall_seconds)
            self.send_error(500, "full GET forbidden in this fixture")
            return
        spec = rng.split("=", 1)[1]
        start_s, end_s = spec.split("-", 1)
        start = int(start_s)
        end = int(end_s) if end_s else len(self.payload) - 1
        end = min(end, len(self.payload) - 1)
        size = end - start + 1
        self.seen_starts.append(start)
        if start >= self.stall_after_offset and size > self.stall_if_range_gt:
            time.sleep(self.stall_seconds)
            return
        body = self.payload[start : end + 1]
        self.send_response(206)
        self.send_header("Content-Type", "image/png")
        self.send_header("Content-Range", f"bytes {start}-{end}/{len(self.payload)}")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


class AssetDownloadTest(unittest.TestCase):
    def setUp(self) -> None:
        _RangeHandler.seen_starts = []
        self.httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), _RangeHandler)
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()
        host, port = self.httpd.server_address[:2]
        self.url = f"http://{host}:{port}/canvas.png"

    def tearDown(self) -> None:
        self.httpd.shutdown()
        self.httpd.server_close()
        self.thread.join(timeout=2)

    def test_shrinks_range_after_timeout_and_completes(self) -> None:
        notes: list[str] = []
        data, evidence = download_url_bytes(
            self.url,
            timeout=1,
            retries=2,
            chunk_size=8 * 1024,
            min_chunk_size=2 * 1024,
            progress=notes.append,
        )
        self.assertEqual(data, _RangeHandler.payload)
        self.assertTrue(evidence.get("shrunk"))
        self.assertEqual(evidence.get("chunk_size_final"), 2 * 1024)
        self.assertTrue(any("shrink" in line for line in notes))
        self.assertTrue(any("RANGE progress" in line or "RANGE download done" in line for line in notes))

    def test_resumes_partial_dest_file(self) -> None:
        dest = Path(self.id().replace(".", "_"))
        dest = ROOT / "tests" / ".tmp-asset-download-resume.bin"
        dest.parent.mkdir(parents=True, exist_ok=True)
        prefix = _RangeHandler.payload[: 12 * 1024]
        dest.write_bytes(prefix)
        try:
            notes: list[str] = []
            data, evidence = download_url_bytes(
                self.url,
                dest=dest,
                timeout=1,
                retries=2,
                chunk_size=8 * 1024,
                min_chunk_size=2 * 1024,
                progress=notes.append,
            )
            self.assertEqual(data, _RangeHandler.payload)
            self.assertEqual(dest.read_bytes(), _RangeHandler.payload)
            self.assertEqual(evidence.get("resumed_from"), len(prefix))
            self.assertTrue(any("RESUME from offset" in line for line in notes))
            self.assertGreaterEqual(min(_RangeHandler.seen_starts), 0)
            self.assertTrue(any(start >= len(prefix) for start in _RangeHandler.seen_starts))
            # Probe always reads 0-15; remaining ranges must start at/after prefix.
            non_probe = [s for s in _RangeHandler.seen_starts if s > 15]
            self.assertTrue(non_probe)
            self.assertGreaterEqual(min(non_probe), len(prefix))
        finally:
            dest.unlink(missing_ok=True)

    def test_skips_when_dest_already_complete(self) -> None:
        dest = ROOT / "tests" / ".tmp-asset-download-complete.bin"
        dest.write_bytes(_RangeHandler.payload)
        try:
            notes: list[str] = []
            data, evidence = download_url_bytes(
                self.url,
                dest=dest,
                timeout=1,
                retries=1,
                progress=notes.append,
            )
            self.assertEqual(data, _RangeHandler.payload)
            self.assertTrue(evidence.get("already_complete"))
            self.assertEqual(evidence.get("resumed_from"), len(_RangeHandler.payload))
            self.assertTrue(any("already complete" in line for line in notes))
        finally:
            dest.unlink(missing_ok=True)

    def test_quad_apply_uses_dest_timeout_and_forbids_kie_recreate(self) -> None:
        apply_src = (ROOT / "scripts/excalibur_blog_quad_apply.py").read_text(encoding="utf-8")
        self.assertIn("dest=canvas_path", apply_src)
        self.assertIn("--timeout", apply_src)
        self.assertIn("CDN stall ≠ Kie createTask", apply_src)
        self.assertNotIn("cover_text_overlay", apply_src)


if __name__ == "__main__":
    unittest.main()
