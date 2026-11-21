#!/usr/bin/env python3
"""Entrypoint for news-image-20261121 v1: copy the built entry.png to /output.

The image is built ahead of time by draw.py (a local build tool, never
imported here). This module only verifies the PNG and copies it, using
the standard library only, so the run is deterministic and offline.
"""
import hashlib
import os
import sys

MAX_BYTES = 1 * 1024 * 1024  # competition gate: image <= 1 MiB
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    with open(src, "rb") as fh:
        data = fh.read()
    if len(data) > MAX_BYTES:
        raise SystemExit(
            "entry.png is %d bytes, over the 1 MiB gate" % len(data))
    if not data.startswith(PNG_SIGNATURE):
        raise SystemExit("entry.png is not a PNG file")
    outdir = "/output"
    os.makedirs(outdir, exist_ok=True)
    dst = os.path.join(outdir, "entry.png")
    with open(dst, "wb") as fh:
        fh.write(data)
    digest = hashlib.sha256(data).hexdigest()
    print("wrote %s (%d bytes, sha256 %s)" % (dst, len(data), digest))
    return 0


if __name__ == "__main__":
    sys.exit(main())
