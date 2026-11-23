"""Meme Sprint 3 entry: writes the meme image to /output/entry.png."""
import os, shutil
OUT = "/output/entry.png"
os.makedirs("/output", exist_ok=True)
shutil.copyfile(os.path.join(os.path.dirname(__file__), "entry.png"), OUT)
print("wrote", OUT)
