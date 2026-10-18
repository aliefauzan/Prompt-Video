# Style discovery brief (research only — no rendering)

Goal: find video editing / restyle LOOKS we do not have yet. The list of taken styles is
`_source/STYLES_TAKEN.md` — skip those and near-duplicates (same look under another name).

A good candidate is a visual look that can be applied frame by frame to existing footage
(texture, palette, medium, overlay, compositing treatment). Pure timing tricks (velocity
ramps, beat cuts, transitions only) do not count unless they come with a distinct look.

## Keywords — try ALL of these, then expand

Search each on every platform you own, plus the variants you discover along the way
(hashtags, creator slang, names in comments, "related searches", tag pages):

video style editing · video editing style · edit style · editing styles tutorial ·
aesthetic edit · aesthetic video edit · trending edit style · viral edit style ·
capcut edit style · capcut template · after effects style · premiere look · LUT look ·
AI video style · AI video filter · AI restyle video · video to video style ·
frame by frame edit · frame by frame animation edit · rotoscope edit · mixed media edit ·
collage edit · paper cutout edit · stop motion edit · overlay edit · texture overlay edit ·
music video look · music video edit style · fashion film edit · film look · cinematic look ·
retro edit · vintage edit · y2k edit · grunge edit · dreamcore · weirdcore · liminal edit ·
analog horror edit · found footage look · lo-fi edit · indie sleaze edit · cyber edit ·
anime edit · AMV style · phonk edit look · glitch edit · psychedelic edit · trippy edit ·
experimental video art · motion design style · seedream video prompt · kling style prompt ·
runway restyle · midjourney video style · higgsfield effect · pika effect · AI filter trend ·
"style transfer" video · tiktok filter trend · instagram reel effect · edit inspo ·
plus the same ideas in Indonesian, Chinese, Japanese, Korean, Spanish, Portuguese
(e.g. 视频风格, 剪辑风格, 動画 エフェクト 加工, 영상 편집 스타일, estilo de edición).

## Tools

- agent-reach skill (read its SKILL.md and references/*.md for exact commands). Run
  `agent-reach doctor --json` first. OpenCLI-backed platforms (X, Reddit, Instagram,
  Facebook, Xiaohongshu) may be disconnected — try once, and if a command hangs or fails,
  fall back. Burner accounts only; GitHub via `~/.agent-reach/gh-burner.sh`, never bare `gh`.
- Exa: `mcporter call exa.web_search_exa query="..." numResults=10` — use `site:` filters
  (site:tiktok.com, site:instagram.com, site:pinterest.com, site:reddit.com, site:x.com, ...).
- YouTube: `yt-dlp "ytsearch25:QUERY" --flat-playlist --print "%(title)s | %(url)s"`.
- Bilibili: `bili search "QUERY" --type video -n 20`.
- Jina reader: `curl -s "https://r.jina.ai/URL"`.
- Built-in browser (`mcp__Claude_Browser__*`) for public pages: TikTok tag/search pages,
  Pinterest, Instagram, CapCut template pages. Never sign in; decline cookie banners;
  if a login wall blocks, use what is visible and move on.

## Output — `_source/discovery/<your-file>.md`

1. `## Keywords tried` — every query with platform and a hit count / "nothing".
2. `## Candidates` — a table, one row per distinct look:
   | Style name | What it looks like (1 line) | Where seen (platform + 1–3 URLs) | Keyword that found it | Frame-by-frame doable? (yes/partly) | Closest taken style + why it's different |
3. Aim for 30+ candidates before filtering, then mark your top 12 with ★.
4. Save 1 screenshot per ★ candidate to `_source/discovery/shots/<your-prefix>_<slug>.png`.

Only write your own discovery file and your own screenshots. Do not create style folders.
Final report: number of keywords tried, number of candidates, your ★ top 12 names.
