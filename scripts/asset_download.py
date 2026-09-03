#!/usr/bin/env python3
"""Robust image download helpers for MCP/CDN asset URLs."""
from __future__ import annotations

import re
import socket
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import IO, Callable


DEFAULT_HEADERS = {
    "User-Agent": "ExcaliburBlogAssetDownloader/1.0",
    "Cache-Control": "no-cache",
}

DEFAULT_CHUNK_SIZE = 8 * 1024
MIN_RANGE_CHUNK = 2 * 1024
DEFAULT_TIMEOUT = 20
DEFAULT_RETRIES = 4
DEFAULT_MAX_BYTES = 25 * 1024 * 1024
PROGRESS_EVERY = 64 * 1024


ProgressFn = Callable[[str], None]


def _default_progress(message: str) -> None:
    print(message, file=sys.stderr, flush=True)


def _is_timeout(exc: BaseException) -> bool:
    if isinstance(exc, (TimeoutError, socket.timeout)):
        return True
    if isinstance(exc, urllib.error.URLError):
        reason = exc.reason
        if isinstance(reason, (TimeoutError, socket.timeout)):
            return True
        if reason is not None and _is_timeout(reason):
            return True
        text = str(reason or exc).lower()
        return "timed out" in text or "timeout" in text
    text = str(exc).lower()
    return "timed out" in text or "timeout" in text


def _request(url: str, *, headers: dict[str, str] | None = None, timeout: int = 20) -> urllib.response.addinfourl:
    merged = dict(DEFAULT_HEADERS)
    if headers:
        merged.update(headers)
    return urllib.request.urlopen(urllib.request.Request(url, headers=merged), timeout=timeout)


def _range_matches(value: str | None, start: int, end: int) -> bool:
    if not value:
        return False
    match = re.search(r"bytes\s+(\d+)-(\d+)/(\d+|\*)", value, flags=re.I)
    if not match:
        return False
    return int(match.group(1)) == start and int(match.group(2)) == end


def _read_exact_range(
    url: str,
    start: int,
    end: int,
    *,
    retries: int,
    timeout: int,
    retry_timeouts: bool = False,
) -> bytes:
    expected = end - start + 1
    last_error: Exception | None = None

    for attempt in range(1, retries + 1):
        try:
            with _request(url, headers={"Range": f"bytes={start}-{end}"}, timeout=timeout) as response:
                content_range = response.headers.get("content-range")
                if response.status != 206 or not _range_matches(content_range, start, end):
                    raise RuntimeError(
                        f"server did not honor Range {start}-{end}: "
                        f"status={response.status}, content-range={content_range!r}"
                    )
                data = response.read(expected)
                if len(data) != expected:
                    raise TimeoutError(f"short range read {start}-{end}: got {len(data)} of {expected}")
                return data
        except Exception as exc:  # noqa: BLE001 - retry network/CDN failures.
            last_error = exc
            if _is_timeout(exc) and not retry_timeouts:
                raise TimeoutError(f"range timeout {start}-{end}: {exc}") from exc
            time.sleep(min(2.0, 0.25 * attempt))

    if last_error is not None and _is_timeout(last_error):
        raise TimeoutError(f"failed to read range {start}-{end} from {url}: {last_error}") from last_error
    raise RuntimeError(f"failed to read range {start}-{end} from {url}: {last_error}")


def _content_range_total(value: str | None) -> int | None:
    if not value:
        return None
    match = re.search(r"/(\d+)\s*$", value)
    if not match:
        return None
    return int(match.group(1))


def probe_url(url: str, *, timeout: int = 15, retries: int = 3) -> dict[str, str | int | bool | None]:
    """Return cheap evidence about a remote asset without reading the full body."""
    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            with _request(url, headers={"Range": "bytes=0-15"}, timeout=timeout) as response:
                first = response.read(16)
                content_range = response.headers.get("content-range")
                return {
                    "status": response.status,
                    "content_type": response.headers.get("content-type"),
                    "content_length": response.headers.get("content-length"),
                    "content_range": content_range,
                    "range_supported": response.status == 206 and _range_matches(content_range, 0, 15),
                    "total_bytes": _content_range_total(content_range),
                    "signature_hex": first.hex(),
                }
        except Exception as exc:  # noqa: BLE001 - transient CDN/proxy errors.
            last_error = exc
            time.sleep(min(2.0, 0.25 * attempt))
    raise RuntimeError(f"failed to probe {url}: {last_error}")


def _resume_offset(dest: Path | None, total: int, progress: ProgressFn | None) -> int:
    if dest is None or not dest.is_file():
        return 0
    existing = dest.stat().st_size
    if existing <= 0:
        return 0
    if existing > total:
        dest.unlink()
        if progress:
            progress(f"RESUME reset dest larger than remote: {existing} > {total}")
        return 0
    if existing == total:
        if progress:
            progress(f"RESUME skip: dest already complete {existing}/{total}")
        return existing
    if progress:
        progress(f"RESUME from offset {existing}/{total}")
    return existing


def _open_dest(dest: Path, resume_from: int) -> IO[bytes]:
    dest.parent.mkdir(parents=True, exist_ok=True)
    mode = "r+b" if dest.exists() and resume_from > 0 else "wb"
    handle = dest.open(mode)
    if resume_from > 0:
        handle.seek(resume_from)
        handle.truncate(resume_from)
    return handle


def download_url_bytes(
    url: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
    retries: int = DEFAULT_RETRIES,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    min_chunk_size: int = MIN_RANGE_CHUNK,
    max_bytes: int = DEFAULT_MAX_BYTES,
    dest: str | Path | None = None,
    progress: bool | ProgressFn = True,
) -> tuple[bytes, dict[str, str | int | bool | None]]:
    """Download URL bytes using Range chunks when the CDN is unstable.

    Some MCP/CDN URLs return a useful HEAD/Range response but hang on a full
    GET or larger ranges. Start at ``chunk_size`` (8 KiB by default), shrink
    on timeout down to ``min_chunk_size`` (2 KiB), resume a partial ``dest``
    file, and print progress instead of hanging silently.

    CDN/result-URL stall is a download problem — not a reason to recreate a
    billed image task.
    """
    log: ProgressFn | None
    if progress is True:
        log = _default_progress
    elif progress is False:
        log = None
    else:
        log = progress

    dest_path = Path(dest) if dest is not None else None
    evidence = probe_url(url, timeout=timeout)
    total = evidence.get("total_bytes")
    current_chunk = max(min_chunk_size, chunk_size)
    evidence["chunk_size_start"] = current_chunk
    evidence["resumed_from"] = 0
    evidence["already_complete"] = False
    evidence["shrunk"] = False

    if evidence.get("range_supported") and isinstance(total, int) and total > 0:
        if total > max_bytes:
            raise RuntimeError(f"remote asset is too large: {total} bytes > {max_bytes}")

        offset = _resume_offset(dest_path, total, log)
        evidence["resumed_from"] = offset
        if dest_path is not None and offset == total:
            evidence["already_complete"] = True
            evidence["chunk_size_final"] = current_chunk
            return dest_path.read_bytes(), evidence

        if log:
            log(
                f"RANGE download start offset={offset}/{total} chunk={current_chunk} "
                f"timeout={timeout}s (CDN stall ≠ billed recreate)"
            )

        chunks: list[bytes] = []
        dest_fh = _open_dest(dest_path, offset) if dest_path is not None else None
        last_progress = offset
        try:
            while offset < total:
                end = min(total - 1, offset + current_chunk - 1)
                try:
                    piece = _read_exact_range(
                        url,
                        offset,
                        end,
                        retries=retries,
                        timeout=timeout,
                        retry_timeouts=current_chunk <= min_chunk_size,
                    )
                except TimeoutError as exc:
                    if current_chunk > min_chunk_size:
                        new_chunk = max(min_chunk_size, current_chunk // 2)
                        if log:
                            log(f"RANGE timeout at {offset}; shrink {current_chunk} -> {new_chunk}")
                        current_chunk = new_chunk
                        evidence["shrunk"] = True
                        continue
                    raise RuntimeError(
                        f"range download stalled at offset {offset}/{total} "
                        f"with min chunk {min_chunk_size}: {exc}"
                    ) from exc

                if dest_fh is not None:
                    dest_fh.write(piece)
                    dest_fh.flush()
                else:
                    chunks.append(piece)
                offset += len(piece)
                if log and (offset - last_progress >= PROGRESS_EVERY or offset >= total):
                    pct = 100.0 * offset / total
                    log(f"RANGE progress {offset}/{total} ({pct:.1f}%) chunk={current_chunk}")
                    last_progress = offset
        finally:
            if dest_fh is not None:
                dest_fh.close()

        data = dest_path.read_bytes() if dest_path is not None else b"".join(chunks)
        if len(data) != total:
            raise RuntimeError(f"range download length mismatch: got {len(data)} of {total}")
        evidence["chunk_size_final"] = current_chunk
        if log:
            log(f"RANGE download done {len(data)} bytes chunk_final={current_chunk}")
        return data, evidence

    # Fallback for servers without Range support: chunked full GET, not one hang-prone read.
    last_error: Exception | None = None
    if dest_path is not None and dest_path.is_file():
        dest_path.unlink()
    for attempt in range(1, retries + 1):
        try:
            if log:
                log(f"GET download attempt {attempt}/{retries} timeout={timeout}s (no Range)")
            with _request(url, timeout=timeout) as response:
                content_length = response.headers.get("content-length")
                if content_length and content_length.isdigit() and int(content_length) > max_bytes:
                    raise RuntimeError(f"remote asset is too large: {content_length} bytes > {max_bytes}")
                dest_fh = _open_dest(dest_path, 0) if dest_path is not None else None
                chunks = []
                got = 0
                last_progress = 0
                try:
                    while True:
                        piece = response.read(current_chunk)
                        if not piece:
                            break
                        got += len(piece)
                        if got > max_bytes:
                            raise RuntimeError(f"remote asset exceeds max_bytes={max_bytes}")
                        if dest_fh is not None:
                            dest_fh.write(piece)
                            dest_fh.flush()
                        else:
                            chunks.append(piece)
                        if log and (got - last_progress >= PROGRESS_EVERY):
                            log(f"GET progress {got} bytes chunk={current_chunk}")
                            last_progress = got
                finally:
                    if dest_fh is not None:
                        dest_fh.close()
                data = dest_path.read_bytes() if dest_path is not None else b"".join(chunks)
                evidence.update(
                    {
                        "status": response.status,
                        "content_type": response.headers.get("content-type"),
                        "content_length": response.headers.get("content-length"),
                        "chunk_size_final": current_chunk,
                    }
                )
                if log:
                    log(f"GET download done {len(data)} bytes")
                return data, evidence
        except Exception as exc:  # noqa: BLE001 - retry network/CDN failures.
            last_error = exc
            if dest_path is not None and dest_path.is_file():
                dest_path.unlink()
            time.sleep(min(2.0, 0.25 * attempt))

    raise RuntimeError(f"failed to download {url}: {last_error}")
