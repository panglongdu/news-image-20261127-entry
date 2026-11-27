#!/usr/bin/env python3
"""Copy the built news image into the grader's output directory.

The grader runs this program with MAKEFUN_OUTPUT_DIR set; when the
variable is absent the image goes to /output instead. The output
directory is created when it does not exist yet.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")

if not os.path.isfile(SRC):
    raise SystemExit("entry.png is missing; run build_image.py first")

out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
os.makedirs(out_dir, exist_ok=True)
shutil.copyfile(SRC, os.path.join(out_dir, "entry.png"))
print("wrote entry.png to", out_dir)
