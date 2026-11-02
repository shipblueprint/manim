"""Render a single manim scene with proper environment setup."""
import sys
import os
import shutil

from manim import config
config.transparent = True

import importlib

mod_name = sys.argv[1]
cls_name = sys.argv[2]
category = sys.argv[3] if len(sys.argv) > 3 else None

mod = importlib.import_module(mod_name)
cls = getattr(mod, cls_name)
scene = cls()
scene.render()

# Move output to category subfolder if specified
if category:
    # Find the rendered video file (Manim puts it in media/videos/<quality>/)
    media_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "media", "videos")
    src_file = None
    if os.path.isdir(media_dir):
        for quality_dir in os.listdir(media_dir):
            candidate = os.path.join(media_dir, quality_dir, f"{cls_name}.mov")
            if os.path.exists(candidate):
                src_file = candidate
                break

    if src_file:
        quality_dir = os.path.dirname(src_file)
        dst_dir = os.path.join(quality_dir, category)
        os.makedirs(dst_dir, exist_ok=True)
        dst_file = os.path.join(dst_dir, f"{cls_name}.mov")
        shutil.move(src_file, dst_file)
        print(f"Moved to: {dst_file}")
    else:
        print(f"Warning: could not find output file for {cls_name}")
