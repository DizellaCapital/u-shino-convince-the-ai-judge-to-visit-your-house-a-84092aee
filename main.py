#!/usr/bin/env python3
"""Copy the rendered invitation image to the make.fun output directory.

Stdlib only. Validates entry.png (PNG magic, 1024x1024, <= 1 MiB) and
copies it byte-for-byte to MAKEFUN_OUTPUT_DIR/entry.png.
"""
import os
import shutil
import struct
import sys

MAX_BYTES = 1048576
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    sys.exit(1)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        fail(f"entry.png not found next to main.py ({src}); run render.py first")
    with open(src, "rb") as fh:
        data = fh.read()
    if len(data) > MAX_BYTES:
        fail(f"entry.png is {len(data)} bytes, over the 1048576-byte limit")
    if data[:8] != PNG_MAGIC:
        fail("entry.png is not a PNG file")
    if data[12:16] != b"IHDR":
        fail("entry.png has no IHDR chunk where expected")
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (1024, 1024):
        fail(f"entry.png is {width}x{height}, expected 1024x1024")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    try:
        os.makedirs(out_dir, exist_ok=True)
        dst = os.path.join(out_dir, "entry.png")
        shutil.copyfile(src, dst)
    except OSError as exc:
        # Fallback: the harness may mount a read-only /output; the script
        # directory is always writable in our local runs.
        dst = os.path.join(here, "entry.png")
        print(f"warning: could not write to {out_dir} ({exc}); "
              f"entry.png already exists at {dst}", file=sys.stderr)
    with open(dst, "rb") as fh:
        written = fh.read()
    if written != data:
        fail(f"output copy mismatch: {dst} differs from {src}")
    print(f"copied {len(data)} bytes to {dst} ({width}x{height})")


if __name__ == "__main__":
    main()
