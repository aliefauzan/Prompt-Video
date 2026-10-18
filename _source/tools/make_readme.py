"""Rebuild the gallery README.md at the repo root from styles/*/.

Also writes styles/*/preview.jpg, a small copy of example.png for the README.

usage: python -I _source/tools/make_readme.py

Each style folder needs example.png and a prompt.md whose first line is
"# NN — Style Name". Folders missing either are skipped.
"""
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
COLS = 3
THUMB_W = 960

HOW_TO = [
    "## How to use",
    "",
    "Every example here was made on a Mac with [Claude Code](https://claude.com/claude-code) and plain Python.",
    "No image AI was used. To restyle your own video the same way:",
    "",
    "1. Install [Claude Code](https://claude.com/claude-code), `ffmpeg` and Python 3 on a Mac.",
    "2. Clone this repo and open the folder in Claude Code:",
    "   ```bash",
    "   git clone https://github.com/aliefauzan/Prompt-Video.git",
    "   cd Prompt-Video",
    "   claude",
    "   ```",
    "3. Pick a style from the gallery below and note its number.",
    "4. Tell Claude Code, replacing the path and the number:",
    "   ```text",
    "   Restyle /path/to/my-video.mov in style 62. Extract frames at 12 fps into my/frames,",
    "   make person masks with _source/tools/segment, adapt styles/62-*/render.py to my frames,",
    "   then build the video with _source/tools/make_video.py into my/.",
    "   ```",
    "5. Open `my/example.mp4` when it finishes.",
    "6. To change the look, tell Claude what to change, for example \"more blur\" or \"less grain\".",
]


def styles():
    for d in sorted((ROOT / "styles").iterdir()):
        prompt, example = d / "prompt.md", d / "example.png"
        if not (d.is_dir() and prompt.exists() and example.exists()):
            continue
        title = prompt.read_text(encoding="utf-8").splitlines()[0].lstrip("# ").strip()
        num, _, name = title.partition("—")
        yield num.strip(), name.strip() or title, d.name


def thumb(folder):
    """Write a light preview.jpg next to example.png so the README stays fast."""
    d = ROOT / "styles" / folder
    src, dst = d / "example.png", d / "preview.jpg"
    if not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime:
        im = Image.open(src).convert("RGB")
        im = im.resize((THUMB_W, round(im.height * THUMB_W / im.width)), Image.LANCZOS)
        im.save(dst, quality=82, optimize=True)


def cell(num, name, folder):
    d = ROOT / "styles" / folder
    # Animated preview + video once make_video.py has run, still image until then.
    img = "preview.webp" if (d / "preview.webp").exists() else "preview.jpg"
    has_video = (d / "example.mp4").exists()
    target = "example.mp4" if has_video else "prompt.md"
    video = f' · <a href="styles/{folder}/example.mp4">▶ video</a>' if has_video else ""
    return (f'<td width="33%" valign="top">'
            f'<a href="styles/{folder}/{target}"><img src="styles/{folder}/{img}" alt="{name}" width="100%"></a>'
            f'<br><b>{num}. <a href="styles/{folder}/prompt.md">{name}</a></b>{video}</td>')


def main():
    items = list(styles())
    for s in items:
        thumb(s[2])
    rows = []
    for i in range(0, len(items), COLS):
        rows.append("<tr>" + "".join(cell(*s) for s in items[i:i + COLS]) + "</tr>")
    text = "\n".join([
        "# Video Style Prompts",
        "",
        f"{len(items)} frame-by-frame video restyle prompts, each shown on the same test clip.",
        "Click a preview to play the video, or a name to open its prompt.",
        "",
        *HOW_TO,
        "",
        "## Styles",
        "",
        "<table>",
        *rows,
        "</table>",
        "",
    ])
    (ROOT / "README.md").write_text(text, encoding="utf-8")
    print(f"README.md: {len(items)} styles")


if __name__ == "__main__":
    main()
