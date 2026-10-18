"""Build the example video and animated preview for one style folder.

usage: python -I make_video.py <styled_frames_dir> <out_dir> [audio_file]

<styled_frames_dir> must hold every frame, frame_001.png .. frame_NNN.png with
no gaps, rendered in the style (12 fps, same numbering as _source/frames).
audio_file defaults to _source/source_audio.m4a. Writes into <out_dir>:
  example.mp4   full clip, 12 fps, H.264, with the original audio
  preview.webp  animated loop, 400 px wide, for the README
The frames dir can be a temp folder: nothing in it is kept.
"""
import subprocess
import sys
from pathlib import Path

from PIL import Image

SOURCE = Path(__file__).resolve().parent.parent
AUDIO = SOURCE / "source_audio.m4a"
PREVIEW_W = 400


def main():
    frames, out = Path(sys.argv[1]), Path(sys.argv[2])
    audio = Path(sys.argv[3]) if len(sys.argv) > 3 else AUDIO
    count = len(list(frames.glob("frame_*.png")))
    missing = [n for n in range(1, count + 1) if not (frames / f"frame_{n:03d}.png").exists()]
    if not count or missing:
        sys.exit(f"frames must be frame_001.png .. frame_NNN.png with no gaps ({count} found)")
    out.mkdir(parents=True, exist_ok=True)

    subprocess.run([
        "ffmpeg", "-y", "-v", "error",
        "-framerate", "12", "-i", str(frames / "frame_%03d.png"),
        "-i", str(audio),
        "-map", "0:v", "-map", "1:a", "-shortest",
        "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2",
        "-c:v", "libx264", "-preset", "slow", "-crf", "24", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart",
        str(out / "example.mp4"),
    ], check=True)

    seq = []
    for n in range(1, count + 1):
        im = Image.open(frames / f"frame_{n:03d}.png").convert("RGB")
        seq.append(im.resize((PREVIEW_W, round(im.height * PREVIEW_W / im.width)), Image.LANCZOS))
    seq[0].save(out / "preview.webp", save_all=True, append_images=seq[1:],
                duration=round(1000 / 12), loop=0, quality=40, method=4)
    for f in ("example.mp4", "preview.webp"):
        print(out / f, f"{(out / f).stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
