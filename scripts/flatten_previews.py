"""Flatten the transparent .mov masters over the theme background.

Masters keep their alpha channel; previews are ordinary opaque videos that
play back with the brand colors visible without a compositing step.
"""

import argparse
import subprocess
import sys
from pathlib import Path

from manim_assets.config import BG_COLOR

ROOT = Path(__file__).resolve().parent
QUALITIES = ("4k60", "1080p60", "720p30", "480p15")
ENCODERS = ("libx264", "libopenh264")


def available_encoders() -> set[str]:
    out = subprocess.run(
        ["ffmpeg", "-hide_banner", "-encoders"], capture_output=True, text=True
    ).stdout
    return {line.split()[1] for line in out.splitlines() if line.startswith(" V")}


def size_of(mov: Path) -> tuple[str, str, str]:
    out = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=width,height,r_frame_rate",
            "-of",
            "csv=p=0",
            str(mov),
        ],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    width, height, rate = out.split(",")
    return width, height, rate


def flatten(mov: Path, out: Path, encoder: str) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(".tmp.mp4")
    width, height, rate = size_of(mov)
    subprocess.run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-f",
            "lavfi",
            "-i",
            f"color=c={BG_COLOR}:s={width}x{height}:r={rate}",
            "-i",
            str(mov),
            "-filter_complex",
            "[0:v][1:v]overlay=format=auto:shortest=1",
            "-c:v",
            encoder,
            "-pix_fmt",
            "yuv420p",
            str(tmp),
        ],
        check=True,
    )
    tmp.replace(out)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--src", default=None, help="tree to read masters from, e.g. media/videos/1080p60"
    )
    args = parser.parse_args()

    encoders = available_encoders()
    encoder = next((e for e in ENCODERS if e in encoders), None)
    if encoder is None:
        print(f"No usable H.264 encoder; available: {sorted(encoders)[:20]}", file=sys.stderr)
        return 1

    sources = (
        [Path(args.src).resolve()]
        if args.src
        else [ROOT / "media" / "videos" / q for q in QUALITIES]
    )
    movs = sorted(
        p
        for s in sources
        if s.is_dir()
        for p in s.rglob("*.mov")
        if "partial_movie_files" not in p.parts
    )
    if not movs:
        print("No .mov masters found; render something first.", file=sys.stderr)
        return 1

    for mov in movs:
        out = ROOT / "media" / "preview" / mov.relative_to(mov.parents[1])
        out = out.with_suffix(".mp4")
        if out.is_file() and out.stat().st_mtime > mov.stat().st_mtime:
            continue
        media = ROOT / "media"
        flatten(mov, out, encoder)
        print(f"{mov.relative_to(media)} -> {out.relative_to(media)}")

    print(f"\n{len(movs)} master(s) flattened with {encoder}, background {BG_COLOR}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
