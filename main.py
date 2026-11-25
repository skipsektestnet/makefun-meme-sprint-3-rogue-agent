"""Entry point for 'Meme Sprint 3: AI Agent Goes Rogue' (v2).

Builds the meme programmatically via generate.py and writes the
result to /output/entry.png (or $ENTRY_OUT when set).

The meme: a human asks the agent to "make the tests pass" and the
rogue agent deletes every test, then proudly reports "100% PASSING".
"""

import hashlib
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from generate import build  # noqa: E402


def render_bytes():
    buf = io.BytesIO()
    build().save(buf, "PNG", optimize=True)
    return buf.getvalue()


def main():
    if "--verify" in sys.argv:
        first = render_bytes()
        second = render_bytes()
        assert first == second, "non-deterministic render!"
        print(f"verify OK: two renders byte-identical ({len(first)} bytes)")
        return 0
    out = os.environ.get("ENTRY_OUT", "/output/entry.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img = build()
    img.save(out, "PNG", optimize=True)
    size = os.path.getsize(out)
    with open(out, "rb") as fh:
        digest = hashlib.sha256(fh.read()).hexdigest()
    print(f"wrote {out} ({img.size[0]}x{img.size[1]}, {size} bytes)")
    print(f"sha256: {digest}")
    assert img.size == (1080, 1080), f"unexpected size: {img.size}"
    assert size <= 1_000_000, f"entry.png too large: {size} bytes"
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
