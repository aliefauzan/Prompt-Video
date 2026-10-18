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
    "1. **Pick a style.** Click its preview to watch the example clip, then click its name to open `prompt.md`.",
    "2. **Copy the prompt.** Copy everything inside the `text` block under **Prompt**.",
    "3. **Open an AI video agent** that can extract frames from a video and generate images, for example the",
    "   invideo AI agent or any agent with Seedream 5.0 Pro. The prompt's TOOL LOCK names the model to use.",
    "   A few styles (such as 72 Slit-Scan and 73 Chronophotography) need a video model or several frames at once, and their prompts say so.",
    "4. **Upload your clip and paste the prompt.** Short clips work best: the agent makes one image per frame,",
    "   so a 15 s clip at 12 fps means about 180 images.",
    "5. **Stage 1, frame extraction.** The agent extracts frames at 12 fps and reports the count.",
    "   Check that it equals the clip length in seconds × 12.",
    "6. **Stage 2, verification timeline.** The agent rebuilds the clip from the raw frames and stops.",
    "   Play it and check the timing matches the original, then reply that it is confirmed. If it is off, say what is wrong instead.",
    "7. **Stage 3, styling.** The agent restyles every frame and assembles the video.",
    "   Ask it to redo any frames where faces, poses or colours drift or flicker.",
    "8. **Export** the finished video.",
    "",
    "To change a style, edit the CORE VISUAL STYLE, palette and NEGATIVE parts of the prompt, and leave",
    "Stages 1–3 as they are. Each folder's `example.*` files are local approximations rendered with code",
    "(`render.py`), and you don't need them to use the prompt.",
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
