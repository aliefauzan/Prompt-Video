"""Build the standard example images for one style folder.

usage: python -I make_sheet.py <styled_frames_dir> <style_dir> "<Style Name>"

<styled_frames_dir> holds frame_NNN.png files rendered in the style (at least
the SHEET_FRAMES below). Writes into <style_dir>:
  example.png       3x2 grid of styled frames with timecodes
  before_after.png  original frame vs styled frame, side by side
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SRC = Path(__file__).resolve().parent.parent / "frames"
SHEET_FRAMES = [13, 49, 85, 109, 145, 178]   # ~1s, 4s, 7s, 9s, 12s, 14.8s at 12 fps
HERO = 49
CELL = (540, 360)


def font(size):
    for p in ("/System/Library/Fonts/Supplemental/Arial Bold.ttf",
              "/System/Library/Fonts/Helvetica.ttc"):
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            pass
    return ImageFont.load_default()


def tc(n):
    s = (n - 1) / 12
    return f"{int(s // 60):02d}:{s % 60:05.2f}"


def main():
    styled, out, name = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
    out.mkdir(parents=True, exist_ok=True)
    head = 56
    sheet = Image.new("RGB", (CELL[0] * 3, CELL[1] * 2 + head), (16, 16, 16))
    d = ImageDraw.Draw(sheet)
    d.text((18, 12), name, font=font(30), fill=(240, 240, 240))
    for i, n in enumerate(SHEET_FRAMES):
        im = Image.open(styled / f"frame_{n:03d}.png").convert("RGB").resize(CELL, Image.LANCZOS)
        x, y = (i % 3) * CELL[0], head + (i // 3) * CELL[1]
        sheet.paste(im, (x, y))
        d.rectangle((x + 8, y + CELL[1] - 34, x + 120, y + CELL[1] - 8), fill=(0, 0, 0))
        d.text((x + 14, y + CELL[1] - 32), tc(n), font=font(20), fill=(255, 255, 255))
    sheet.save(out / "example.png")

    a = Image.open(SRC / f"frame_{HERO:03d}.png").convert("RGB").resize((810, 540), Image.LANCZOS)
    b = Image.open(styled / f"frame_{HERO:03d}.png").convert("RGB").resize((810, 540), Image.LANCZOS)
    ba = Image.new("RGB", (1620 + 12, 540 + head), (16, 16, 16))
    ba.paste(a, (0, head))
    ba.paste(b, (822, head))
    d = ImageDraw.Draw(ba)
    d.text((18, 12), "ORIGINAL", font=font(26), fill=(200, 200, 200))
    d.text((840, 12), name.upper(), font=font(26), fill=(240, 240, 240))
    ba.save(out / "before_after.png")
    print(out / "example.png")


if __name__ == "__main__":
    main()
