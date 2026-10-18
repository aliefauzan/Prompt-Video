# Style pack brief (shared by every session)

Goal: a library of video-restyle prompts in the same shape as
`reference_prompt_punk_collage.txt` (the "Punk Photocopy Collage" prompt), each
for a DIFFERENT editing style, each with an example made from the same test clip.

## Inputs (read-only, do not modify)

- `_source/original.mov` — the test clip (symlink), 1620x1080, ~14.9 s, three people in an office.
- `_source/frames/frame_001..179.png` — the clip at 12 fps (Stage-1 extraction from the reference prompt).
- `_source/masks/frame_NNN.png` — matching person masks (Apple Vision, white = person).
- `_source/reference_prompt_punk_collage.txt` — the reference prompt. Copy its STRUCTURE:
  intro + "STYLE ONLY should change", TOOL LOCK, CORE VISUAL STYLE bullets, the
  "someone printed → cut → ... → animated" process chain, palette rules, per-element
  rules, background rules, "boil"/frame-to-frame rules, NEGATIVE list, then the
  STAGE 1 (12 fps extraction) / STAGE 2 (verification timeline, stop) / STAGE 3
  (style every frame, consistency rules) workflow. Keep Stages 1–2 identical in
  meaning; rewrite everything style-specific.
- `_source/tools/punk.py` — how style 01 was rendered locally (numpy + OpenCV + masks). Use as a pattern.
- `_source/tools/make_sheet.py` — builds the standard example images.
- Python: `_source/.venv/bin/python -I` (numpy, Pillow, opencv-python-headless 5.0). `pip install` more into that venv if needed.
- ffmpeg / ffprobe are on PATH.

## Research

Find real references for each style (what creators call it, how it looks, signature details):
- agent-reach skill: Exa search (`mcporter call exa.web_search_exa query="..." numResults=8`),
  Jina reader (`curl -s "https://r.jina.ai/URL"`), Twitter/Reddit/Instagram via OpenCLI
  (the OpenCLI browser extension may be disconnected — if a command hangs or fails, skip it),
  GitHub via `~/.agent-reach/gh-burner.sh` only (never bare `gh` for scraping).
- Built-in browser (`mcp__Claude_Browser__*`) for TikTok, Pinterest, Instagram, YouTube pages: read
  public pages, take screenshots. Never sign in, never accept anything beyond declining cookie banners.
- Save 1–3 reference screenshots per style as `refs/ref_N.png` (screenshot of the public page/post),
  and list every URL used in the prompt file's "References" section.

## Deliverable per style — `styles/NN-slug/`

1. `prompt.md`:
   - `# NN — Style Name`
   - **Look:** 1–2 sentence summary
   - **Also called / where it trends:** names creators use, platforms
   - **References:** bullet list of URLs (with one-line note each)
   - **Example:** pointer to `example.png`, `before_after.png`
   - `## Prompt` then the FULL prompt in a ```text block, written for an AI video agent
     (default TOOL LOCK model: Seedream 5.0 Pro, like the reference — change it only if the
     style clearly needs a video model, and say why).
2. `frames/frame_NNN.png` — the test clip restyled locally for at least frames
   013 049 085 109 145 178 (render more if cheap). Use the masks so subject identity/pose stay
   exact, and vary texture per frame so it "boils" where the style calls for it.
   It is an approximation made with code — make it as close to the style as you can.
3. `example.png` + `before_after.png` — run:
   `_source/.venv/bin/python -I _source/tools/make_sheet.py styles/NN-slug/frames styles/NN-slug "Style Name"`
   Then LOOK at example.png and iterate on the render until it clearly reads as the style.
4. `example.mp4` + `preview.webp` — the whole test clip in the style:
   render ALL 179 frames (frame_001..179) into a temp folder outside the project, e.g.
   `/tmp/prompt-video-render/NN-slug/`, then run:
   `_source/.venv/bin/python -I _source/tools/make_video.py /tmp/prompt-video-render/NN-slug styles/NN-slug`
   It writes a 12 fps H.264 mp4 with the original audio and a 400 px animated WebP loop.
   Watch a few seconds of motion (or check consecutive frames) so the boil/jitter feels
   right at 12 fps and nothing flickers that should hold still. Afterwards keep only the 6
   sheet frames in `styles/NN-slug/frames/` and delete the temp folder, to save disk.
5. `refs/ref_N.png` — the reference screenshots.
6. Put render scripts in `styles/NN-slug/render.py` (not in `_source`).

## Rules

- Only write inside your own assigned `styles/NN-*` folders. Do not touch `_source/` or other styles.
- Not a git repo: no git commands.
- Each style must be clearly different from punk collage and from the other assigned styles.
- When done, report: the folder names, style names, and one line on render quality per style.
