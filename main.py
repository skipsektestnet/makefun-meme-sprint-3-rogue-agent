"""Meme Sprint 3: AI Agent Goes Rogue: writes the meme image to /output/entry.png.

Why this meme: the agent is asked to fix one bug and deletes the whole
codebase, then calls it fixed.
"""

import os
import shutil

SOURCE = os.path.join(os.path.dirname(__file__), "entry.png")
OUT = "/output/entry.png"


def main():
    # Guard: never copy a missing meme image to the sealed gate.
    assert os.path.exists(SOURCE), "entry.png missing"
    os.makedirs("/output", exist_ok=True)
    shutil.copyfile(SOURCE, OUT)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
