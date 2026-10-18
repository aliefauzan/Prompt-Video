# D4 — Asia platforms, GitHub, design blogs

Researcher: side session D4. Scope: Xiaohongshu, Bilibili, Douyin/Weibo, Japanese and Korean sources, Indonesian slang, GitHub, and trend reports from design and editing blogs. Research only. No style folders were created and nothing was rendered.

## Coverage notes (read first)

- **OpenCLI was disconnected.** Xiaohongshu therefore had no direct search backend. I reached it only through Exa `site:xiaohongshu.com` queries. Those returned mostly profile pages and trend roundups, not individual notes. Xiaohongshu coverage is thin and should not be treated as exhausted.
- **Exa hit its free rate limit (HTTP 429)** partway through, shared with sibling sessions. After that I used WebSearch, WebFetch and the jina reader. The late Exa queries for named looks (港风, 中式梦核, ato, プリクラ, 写ルンです, 平成レトロ, ゆめかわ, 인생네컷, 디카) all came back with 0 hits, which reflects the rate limit and not a lack of content. They are worth re-running once the quota resets.
- **Bilibili worked well** through its public search API (cookie jar plus Referer header, because the `bili` CLI was not installed). Hit counts below are Bilibili's own "total results" figure. I looked at the top 20 by play count for each.
- **GitHub** was read only through `~/.agent-reach/gh-burner.sh` (burner account). Long multi-word queries often return 0 repos on GitHub search, so several of those zeros are query-shape problems, not missing content.
- I did **not** run the roughly 90 English keywords from the brief verbatim on every platform. The English keyword space is covered by sibling sessions. I ran the Chinese, Japanese, Korean and Indonesian equivalents plus the look-specific names I discovered along the way (see the list below).
- Candidates are judged on whether the look can be applied frame by frame to footage, as the brief asks. Screenshots for ★ rows are contact sheets of Bilibili cover frames (search results sorted by plays) or the ditherer gallery preview, because Bilibili video pages show a black player when not signed in.

## Keywords tried

Total: 132 logged queries (60 Bilibili, 33 Exa, 39 GitHub) plus about 15 WebSearch/WebFetch queries on trend reports and blogs that were not itemised in my log. Counts after the tab are hit counts. For Bilibili the count is total results (top 20 reviewed); for GitHub it is repos returned; for Exa it is results returned.

### Bilibili (60)

| Query | Hits |
|---|---|
| 视频风格 | 1000+ |
| 剪辑风格 | 1000+ |
| 视频转绘 | 1000+ |
| AI视频风格转换 | 112 |
| 剪辑风格 教程 | 1000+ |
| 视频调色风格 氛围感 | 22 |
| 氛围感视频 剪辑 风格 | 135 |
| AE 特效 风格 教程 逐帧 | 10 |
| 逐帧动画 剪辑 | 1000+ |
| 定格动画 剪辑 风格 | 577 |
| 拼贴 剪辑 风格 | 141 |
| 纸片 剪辑 视频 风格 | 19 |
| 复古 剪辑 风格 视频 | 406 |
| 怪核 梦核 剪辑 | 1000+ |
| 故障艺术 剪辑 | 791 |
| 赛博朋克 剪辑 风格 | 1000+ |
| AI视频滤镜 风格 | 63 |
| 视频转视频 风格 可灵 | 10 |
| 即梦 视频 风格 提示词 | 54 |
| 剪映 风格 模板 爆款 | 13 |
| 剪映 特效 教程 氛围 | 37 |
| MV风格 剪辑 | 497 |
| 音乐MV 画面风格 | 17 |
| AMV 风格 剪辑 | 630 |
| 卡点 风格 视频 特效 | 59 |
| 转绘 风格 动画 AI 视频 | 83 |
| 手绘风格 视频 特效 | 191 |
| 水墨风 视频 特效 | 1000+ |
| 漫画风 视频 特效 | 189 |
| 素描风 视频 | 669 |
| 油画风 视频 AI | 156 |
| 冲击帧 动画 特效 逐帧 | 9 |
| anime impact frame 剪辑 | 292 |
| 手绘特效 叠加 实拍 视频 | 40 |
| PS1 风格 画面 复古 3D | 19 |
| 低多边形 视频 风格 转换 | 10 |
| 旋转 镜像 万花筒 视频 特效 | 8 |
| 时间切片 狭缝扫描 视频 | 982 |
| 红蓝3D 视频 特效 | 74 |
| 雕版 版画 风格 视频 | 11 |
| 凹版印刷 钞票 雕刻 风格 视频 | 19 |
| 传真机 热敏 打印 风格 视频 | 1000+ |
| 毛毡 羊毛毡 定格 风格 AI | 9 |
| 针织 毛线 风格 AI 视频 | 4 |
| 折纸 风格 视频 AI 转换 | 13 |
| 剪纸 风格 视频 特效 | 92 |
| 皮影 风格 视频 AI | 9 |
| 国风 敦煌 壁画 AI视频 风格 | 20 |
| 新中式 国潮 AI 视频 风格 提示词 | 9 |
| 蒸汽波 视频 剪辑 | 1000+ |
| 液态玻璃 视频 风格 AI | 9 |
| 果冻 黏土 3D 风格 AI视频 | 15 |
| 融化 特效 AI视频 变形 | 15 |
| 像素风 转绘 视频 | 15 |
| 水彩 转绘 视频 AI 风格 丝滑 | 8 |
| 老港片 滤镜 视频 AI 风格 | 30 |
| 千禧 DV 画质 视频 滤镜 CCD | 37 |
| 手机壳 贴纸 风格 视频 特效 描边 | 9 |
| 漫画分镜 风格 视频 转绘 | 10 |
| 涂鸦 手绘 线条 视频 特效 AE | 68 |
| 胶片 划痕 灰尘 叠加 视频 剪辑 | 45 |

### Exa — Xiaohongshu, Douyin, Weibo, Japanese, Korean, Indonesian (33)

| Query | Hits |
|---|---|
| site:xiaohongshu.com 视频风格 剪辑 特效 教程 | 6 (profiles and roundups, no usable notes) |
| site:xiaohongshu.com AI视频 风格转绘 玩法 爆款 | 6 (same) |
| site:xiaohongshu.com 氛围感 视频 剪辑 风格 合集 | 6 (same) |
| site:xiaohongshu.com 剪映 特效 风格 模板 最近很火 | 6 (same) |
| site:xiaohongshu.com 逐帧 拼贴 剪辑 风格 | 6 (same) |
| 小红书 视频 滤镜 风格 trend 2026 爆火 | 6 |
| site:douyin.com 视频 风格 特效 滤镜 爆火 | 6 (mostly profile pages) |
| 抖音 AI 特效 风格 变身 爆火 玩法 2026 | 6 |
| 微博 视频 剪辑 风格 新玩法 特效 | 6 |
| 動画 加工 エフェクト 流行り スタイル | 7 |
| 動画編集 スタイル 流行 エモい 加工 2026 | 7 |
| site:note.com 動画 加工 エフェクト 風 スタイル AE | 7 |
| ato風 エフェクト 動画編集 とは | 7 |
| odd edit 動画 スタイル 特徴 | 7 |
| 動画 レトロ 加工 トレンド 映像 質感 エフェクト | 7 |
| AI 動画 スタイル変換 動画 風 プロンプト Kling Seedance | 7 |
| Pixiv モーショングラフィックス 風 映像 エフェクト 新しい | 7 |
| 영상 편집 스타일 유행 필터 감성 | 7 |
| site:blog.naver.com 영상 편집 스타일 유행 효과 템플릿 캡컷 | 7 |
| 인스타 릴스 영상 효과 유행 AI 스타일 변환 | 7 |
| gaya editing video viral tren capcut estetik | 7 |
| style edit video tiktok indonesia lagi viral template capcut efek | 7 |
| tren edit video instagram reels efek AI 2026 indonesia | 7 |
| efek video estetik jadul vintage edit slang edit style tutorial | 7 |
| 港风 复古 视频 风格 抽帧 拖影 滤镜 是什么 | nothing (rate limit) |
| 中式梦核 视频 风格 特征 | nothing (rate limit) |
| ato风格 odd风格 剪辑 数码特效 是什么 | nothing (rate limit) |
| newjeans 风格 视频 剪辑 DV 复古 数码 | nothing (rate limit) |
| プリクラ風 動画 加工 シール風 エフェクト | nothing (rate limit) |
| 写ルンジャス 風 動画 エフェクト フィルムカメラ風 流行り | nothing (rate limit) |
| 平成レトロ 動画 加工 ガラケー風 エフェクト | nothing (rate limit) |
| ゆめかわ メンヘラ 加工 動画 風 スタイル | nothing (rate limit) |
| 인생네컷 캠코더 감성 영상 필터 유행 싸이월드 감성 | nothing (rate limit) |
| 디카 감성 영상 편집 요즘 유행 효과 이름 | nothing (rate limit) |

In addition, I ran a number of follow-up Bilibili searches to build the contact sheets for the ★ rows (for example 移轴摄影 微缩 视频, 穆夏风格, 梦核 做旧画面 教程, 频闪 多重曝光 残影 视频特效, 时间切片 特效 PR教程, 手绘逐帧 特效 街头美漫 VFX). These were not logged one by one and are not included in the 132 count.

### GitHub via burner wrapper (39)

| Query | Repos |
|---|---|
| video style transfer | 8 |
| awesome video effects | nothing |
| video filter shader collection | nothing |
| comfyui video style workflow | nothing |
| ffmpeg filter gallery effects | nothing |
| shadertoy video effects post processing | nothing |
| retro video filter ffmpeg | nothing |
| glsl video filters | 1 |
| video stylization | 8 |
| cartoonize video | 8 |
| AI video restyle | nothing |
| video to anime | 8 |
| art style video effects opengl | nothing |
| lut collection film emulation | nothing |
| rotoscope | 8 |
| video aesthetic effects python opencv | nothing |
| slang-shaders | 7 |
| reshade shaders | 7 |
| awesome-video-effects | 7 |
| awesome shaders | 7 |
| awesome video editing | 4 |
| video effects glsl-transitions | nothing |
| ComfyUI video style lora | nothing |
| wan video lora styles | nothing |
| kling effects prompts | nothing |
| higgsfield effects | nothing |
| seedance prompts | 7 |
| ai video effect prompt library | nothing |
| video lora style collection | nothing |
| DreamStyle video stylization | nothing |
| aesthetic video filter | nothing |
| vhs filter | 7 |
| film grain halftone shader | nothing |
| ffmpeg effects | 7 |
| lut | 7 |
| post-processing shaders | 7 |
| retro shaders | 7 |

The most productive GitHub find was `gyng/ditherer`, a browser image and video filter app with a gallery of 120+ presets and filters with preview images. It was the evidence source for several candidates. Other useful repos: `DaveFace/UnrealRetroShaders` (PS1 look), `GarrettGunnell` ink shader, `libretro/slang-shaders` (handheld LCD, NTSC, cel, film, VHS), and `renoise-ai/awesome-seedance-prompts` (about 290 prompts, a prompt vault and not a look source by itself).

### WebSearch / WebFetch on trend reports and blogs (about 15, not itemised)

Sources read: Canva 2026 design trends, Envato video trends, Videobolt motion-design trends, Clipchamp aesthetic roundups, CapCut and Adobe trend posts, Vidguru AI effect roundups, VIDEO SALON (Japan) 2026-02 retro and film-look feature, realsound (昭和レトロ), coart.co.jp (平成レトロ video camera), ditoday (Korean 디토 감성), huxiu, sixthtone and whatsonweibo pieces on Chinese dreamcore. I did not get usable content from Motion Array, PremiumBeat or Shutterstock trend reports, so those three are effectively not covered.

## Candidates

★ marks the top 12. Screenshot files for ★ rows are in `_source/discovery/shots/` with the prefix `D4_`. "Bilibili avNNN" means `https://www.bilibili.com/video/avNNN`. "ditherer" means `https://github.com/gyng/ditherer` and its preset gallery.

| Style name | What it looks like (1 line) | Where seen (platform + 1–3 URLs) | Keyword that found it | Frame-by-frame doable? | Closest taken style + why it's different |
|---|---|---|---|---|---|
| ★ Slit-scan time-slice (时间切片) `D4_time-slice.png` | Frame is cut into diagonal or vertical bands, each band showing a different moment, so one image holds a time sweep | Bilibili av857120801, av1253209917, av772306622; ditherer "Time Slice" and "Stargate" | 时间切片 狭缝扫描 视频 | partly (each output frame samples neighbouring source frames) | 26 slow-shutter smear blends time into blur; this keeps each band crisp and sharp-edged. 29 hyperspace burst is radial motion, not temporal slicing |
| ★ Marey chronophotography strobe (频闪 残影) `D4_chronophoto.png` | Subject repeated as several crisp frozen copies along its path on a dark ground | Bilibili av1003686133, av1403624324, av841422349; ditherer "Ghost Dance" | 频闪 多重曝光 残影 视频特效 | partly (needs a few past frames per output frame) | 17 double exposure is a dreamy blend of two images; this is many sharp stepped copies. 26 smears them instead |
| ★ Banknote engraving `D4_banknote-engraving.png` | Single-ink fine line hatching with wavy guilloche modulation, like currency or an etched portrait | ditherer "Currency Engraving" and "Etching"; Bilibili 凹版印刷 search (19 results) gave no usable example | 凹版印刷 钞票 雕刻 风格 视频 | yes | 35 ukiyoe woodblock is flat colour with bold outline; 48 charcoal is soft tonal. This is dense parallel linework whose line width carries the tone |
| ★ Red-cyan anaglyph 3D `D4_anaglyph.png` | Red and cyan channel pair offset by depth, as if viewed through paper 3D glasses | Bilibili av10386725, av884424989, av43370835; ditherer "Retro 3D" | 红蓝3D 视频 特效 | partly (a depth estimate improves it; a flat offset works as a cheap version) | 30 Spider-Verse offset misregisters CMYK ink; anaglyph shifts only red versus cyan, scaled by depth. Moderate overlap risk with 30 |
| ★ Tilt-shift miniature `D4_tilt-shift.png` | Blur above and below a sharp horizontal band plus boosted saturation, so real places read as toy models | Bilibili av116938671916661, av1750216414, av1134010449274844 (cover frames) | 移轴摄影 微缩 视频 | yes | Nothing close in the taken list. It is optical, not a texture or medium |
| ★ Hand-drawn frame-by-frame FX over footage (手绘逐帧特效) `D4_handdrawn-fx.png` | Painted fire, smoke, lightning and slash shapes drawn frame by frame and laid on live action | Bilibili av116018609456464, av708819741, av342965495 | 手绘逐帧 特效 街头美漫 VFX | yes | 13 neon scribble outline and 23 boogley doodles are line doodles. This is shaded, cel-painted elemental FX with squash and fade. Moderate overlap with 13 |
| ★ Needle-felt wool (羊毛毡) `D4_felt-wool.png` | Fuzzy fibre surface with soft edges and visible wool lumps, as if everything were handmade felt | Bilibili av114754530056606, av115944470876451, av117117382825527 | 毛毡 羊毛毡 定格 风格 AI | partly (texture and edge fuzz are easy; stepped stop-motion cadence is optional) | 37 claymation is smooth plasticine; 34 cross-stitch is a thread grid. Felt has random fibre fuzz and no grid |
| ★ Shadow puppet (皮影) `D4_shadow-puppet.png` | Back-lit translucent leather figures with jointed limbs, coloured cut-out holes and a paper-screen glow | Bilibili av115846861100593, av115851374107335, av1455315280 | 皮影 风格 视频 AI | partly (silhouette plus cut-out texture is doable; joint-rig motion is not) | 43 dark stage spotlight is lighting only; 35 ukiyoe is print. This is flat translucent colour with punched pattern detail |
| ★ Mucha art nouveau (穆夏风格) `D4_mucha-nouveau.png` | Pale muted palette, flowing outlines, circular halo behind the subject and ornamental floral border | Bilibili av1455382903, av970927336, av203576536 | 穆夏风格 / 穆夏 filter | yes | 60 floral maximalism gouache is dense and saturated; 46 editorial poster is 1950s; 21 stained glass uses lead lines. Mucha is pale, outlined, haloed. Overlap risk with 60 |
| ★ Chinese millennium dreamcore (中式梦核) `D4_cn-dreamcore.png` | Low-resolution, hazy, washed-teal 2000s Chinese interiors, school hallways and apartment blocks with nostalgic emptiness | Bilibili av1801274686, av822461061, av1703595960; huxiu 4780809; sixthtone 1018582 | 怪核 梦核 剪辑 / 中式梦核 | partly (the look is a soft low-res haze with a green-teal cast; the emptiness comes from the footage chosen) | 02 VHS camcorder has tape defects and date stamps; 38 CCTV is night vision. This is soft-focus haze and tonal cast with no tape artefacts |
| ★ Thermal / fax receipt print `D4_thermal-fax.png` | One-bit black on white with stochastic dot noise and horizontal head-banding, like a thermal printer or fax | ditherer "Thermal Printer", "Fax Machine", "Receipt Printer" | 传真机 热敏 打印 风格 视频 | yes | 16 thermal camera is a false-colour heat map and shares only a word. 01 punk photocopy and 11 pixel dither are the nearest by look; this is paper-feed banding with a printer-head streak. Moderate overlap risk |
| ★ PS1 low-poly retro 3D (PS1风格) `D4_ps1-retro.png` | 240p texture warp, vertex jitter, dither and fog, like early PlayStation games | Bilibili av579370715, av113747729322810, av835651974; DaveFace/UnrealRetroShaders | PS1 风格 画面 复古 3D | partly (low-res, dither, affine wobble and fog can be faked in 2D; true vertex jitter needs geometry) | 40 low-poly-3d is clean faceted geometry; 11 pixel dither is 2D sprites. PS1 is wobbling textures in 3D plus fog. Moderate overlap risk with 40 |
| Anime impact frame (冲击帧) | Hard black-white inverted flash frames with radiating speed lines and ink splashes | Bilibili search 冲击帧 动画 特效 逐帧 and anime impact frame 剪辑 (292 results) | anime impact frame 剪辑 | yes | 07 pop-art halftone and 30 Spider-Verse are print looks; this is a one-to-three-frame inverted ink burst. Not a sustained look, so weaker |
| Wong Kar-wai step-printed smear (王家卫抽帧) | Dropped frames plus trailing ghosting and saturated red-green neon grade | Bilibili av680513388, av92568106, av1705420943 | 老港片 滤镜 视频 AI 风格 | partly | 26 slow-shutter smear is the same effect. Near-duplicate, listed for completeness |
| Depth-map layered edit (深度图风格剪辑) | Foreground, midground and background split by depth and treated separately (fog, scale, colour) | Bilibili av117119714859186 | 剪辑风格 | partly (needs a depth model per frame) | 22 glass invisibility cloak is a refraction effect; nothing taken uses depth layering |
| Torn-paper news shredding (撕纸拼贴复古) | Footage torn into ragged paper strips with newsprint texture and visible fibre edges | Bilibili av267770989; Videobolt "torn paper" trend | 拼贴 剪辑 风格 | yes | 01 punk photocopy and 08 scrapbook sticker collage are the same family. Near-duplicate |
| Gothic dark AI filter (哥特暗黑滤镜) | Desaturated crushed blacks, cold highlights and heavy vignette with gothic grain | Bilibili av115163525029458 | AI视频滤镜 风格 | yes | 43 dark stage spotlight and 48 charcoal expressionism cover most of this. Near-duplicate |
| Corrupted-video look (视频损坏) | Frozen blocks, colour banding and stuck-pixel streaks as if the file were damaged | Bilibili av789468250, av739429626 | 故障艺术 剪辑 | yes | 05 datamosh glitch is the same family. Near-duplicate |
| Backrooms / liminal (后室) | Empty fluorescent-lit corridors and yellow carpet, flat light and eerie low-res | Bilibili av594183358, av707275138 | 怪核 梦核 剪辑 | partly | Overlaps with the Chinese dreamcore row above and with 02. Treat as one family |
| Evangelion title-card edit (庵野秀明) | Black cards with huge white serif type, hard flash cuts and Matisse font | Bilibili av383518330 | 剪辑风格 | partly (look is typographic cards, not footage grade) | 14 magazine cover typography is layout-led; this is black-card flash typography. Weak as a footage look |
| Tyndall god rays (丁达尔光线) | Volumetric light shafts through haze, warm highlights | Bilibili av383981359 | 氛围感视频 剪辑 风格 | yes | 29 hyperspace burst is radial streaking from a centre. God rays are soft and angled from a light source. Nothing taken matches |
| Selective colour reveal (黑白渐变彩色) | Black and white that floods to colour along a wipe or object | Bilibili av209823189 | 氛围感视频 剪辑 风格 | partly (more of a transition than a look) | 31 Sin City keeps one red accent; this reveals all colour over time |
| Paper puppet (纸偶) | Cut-paper figures on thin joints with visible paper grain and shadow | Bilibili av116883323884999 | 纸片 剪辑 视频 风格 | partly | 01 and 08 are collage. Near-duplicate |
| ato / odd digital-FX style (ato风格) | Plane-tracked digital overlays: HUD boxes, scanning rectangles, glitchy graphic callouts over footage | Bilibili av116287715941088; Japanese "ato風" and "odd edit" explanation pages (Exa) | ato風 エフェクト 動画編集 とは | partly (tracking needed for the best version) | 39 lidar point cloud and 42 blob tracking are the nearest. Overlap risk |
| Daguerreotype plate | Silvery mirror-like monochrome with tarnished edges, soft focus and long-exposure ghosting | ditherer "Daguerreotype" and "Mavica" presets | GitHub: gyng/ditherer gallery | yes | 03 Super 8 and 28 silent film are film stock looks. A daguerreotype is a polished-metal plate with its own tarnish and vignette |
| Kaleidoscope mirror | Image folded into a radially symmetrical mirror pattern | ditherer "Kaleidoscope"; Bilibili search 旋转 镜像 万花筒 (8 results) | 旋转 镜像 万花筒 视频 特效 | yes | 44 broken mirror shards is irregular fragments; kaleidoscope is symmetric repetition |
| Matrix rain | Green falling glyphs over a dark image | ditherer "Matrix rain" | GitHub: gyng/ditherer gallery | yes | 12 ASCII terminal phosphor covers it. Near-duplicate |
| Mode-7 floor / F-Zero plane | Image mapped to a tilted receding floor plane with horizon scaling | ditherer "F-Zero floor" | GitHub: gyng/ditherer gallery | partly | 32 synthwave outrun has a grid floor; this maps the whole frame as the floor texture |
| Dream Sequence vaseline | Smeared halo-soft highlights, vaseline-on-lens bloom and pastel haze | ditherer "Dream Sequence"; Japanese ゆめかわ pages | GitHub: gyng/ditherer gallery | yes | 17 double exposure dreamy covers the mood. Near-duplicate |
| Heat shimmer / CRT degauss | Wavering refraction ripple, or magnetic colour ripple on a CRT | ditherer "Heat shimmer", "Degauss CRT" | GitHub: gyng/ditherer gallery | yes | 27 signal relief scanlines covers CRT. Near-duplicate |
| Red coat / solarize | Selective red boost and solarised tonal inversion | ditherer "Red Coat", "Solarized" | GitHub: gyng/ditherer gallery | yes | 31 Sin City noir red is the same idea. Near-duplicate |
| Handheld LCD grid (Game Boy style) | Four-green LCD with visible pixel grid and ghosting | libretro/slang-shaders (handheld) | GitHub: slang-shaders | yes | 11 pixel art dither and 24 cobalt pixel halftone. Near-duplicate |
| Inktober ink shader | Rim-lit ink lines with cross-hatch shading | GarrettGunnell Inktober shader (GitHub) | GitHub: post-processing shaders | yes | 18 pencil sketch rotoscope and 48 charcoal are close. Moderate overlap |
| Canva "Reality Warp" | Distorted, stretched real-world imagery treated as surreal | Canva 2026 trends report | WebSearch: Canva 2026 design trends | partly | 57 surrealist Dalí/Magritte is nearby but is about composition. Weak evidence of an actual look |
| Canva "Texture Check" (glossy / waxy / glass) | Objects and surfaces rendered as glossy, waxy or glass-like | Canva 2026 trends report; Videobolt "dispersions and glass shapes" | WebSearch: Canva 2026 design trends | partly | 22 glass invisibility cloak and 15 Y2K chrome. Overlap risk |
| Canva "Prompt Playground" early-internet UI | Browser chrome, chat windows and 1990s-2000s web widgets framing the footage | Canva 2026 trends report | WebSearch: Canva 2026 design trends | yes (overlay) | 15 Y2K chrome / Frutiger Aero is glossy. This is OS-window framing. Partly new |
| Canva "Notes App Chic" | Plain notes-app text overlays in default fonts on photos | Canva 2026 trends report | WebSearch: Canva 2026 design trends | yes (overlay) | 14 magazine cover typography is polished layout; this is deliberately plain. Weak as a look |
| Canva "Drama Club" mockumentary spotlight | Hard single-spot lighting with confessional framing | Canva 2026 trends report | WebSearch: Canva 2026 design trends | partly | 43 dark stage spotlight is the same. Near-duplicate |
| Canva "Zinegeist" | Cut-and-paste zine layout with photocopied textures | Canva 2026 trends report | WebSearch: Canva 2026 design trends | yes | 01 punk photocopy collage is the same. Near-duplicate |
| Envato neon lights +200% | Heavily boosted neon saturation and glow | Envato video trends | WebSearch: Envato video trends 2026 | yes | 55 cyberpunk neon city and 13 neon scribble outline. Near-duplicate |
| AI object transforms (cakeify / squish / inflate / melt) | Objects cut like cake, squished, inflated or melted by a hand or knife | Vidguru AI effect roundup; Bilibili 融化 特效 AI视频 变形 (15 results) | AI视频滤镜 风格 / 融化 特效 | partly (needs AI; not a per-frame filter) | Nothing taken. It is an object-level transform, not a surface look |
| 昭和レトロ / 平成レトロ video camera | Showa-era print and film cast, or Heisei-era camcorder and flip-phone grain | VIDEO SALON 2026-02 retro and film-look feature; realsound; coart.co.jp/blog/ai/637 | 動画 レトロ 加工 トレンド | yes | 02 VHS, 03 Super 8, 04 Y2K digicam. Near-duplicate family |
| Korean 디토 감성 low-quality analog mood | Deliberately low-quality, soft, warm digital-camera mood | ditoday blog 114680 (Naver) | 디카 감성 영상 편집 | yes | 04 Y2K digicam flash. Near-duplicate |
| Seedance / Kling prompt vault styles | Hundreds of AI prompt recipes covering many looks | renoise-ai/awesome-seedance-prompts (GitHub) | seedance prompts | n/a (source list, not a look) | Source for prompts only; no single new look extracted |

Candidate count: 44 rows. Of those, 12 are marked ★ as new looks that can be applied frame by frame. About 20 are near-duplicates or families of taken styles (listed so the main session does not re-discover them). The rest are weaker, overlay-only, or AI-only effects.

## Notes for the main session

- Strongest genuinely new looks, in order of how little they overlap taken styles: tilt-shift miniature, slit-scan time-slice, banknote engraving, Marey chronophotography, needle-felt wool, shadow puppet, Daguerreotype plate (not starred only because ditherer's preview image was too small to screenshot well).
- Highest overlap risk among the ★ rows: PS1 retro (40 low-poly-3d), Mucha (60 floral gouache), hand-drawn FX (13 and 23), thermal/fax (01 and 11), anaglyph (30). If any of those is built, make the difference explicit in the prompt: affine texture wobble and fog for PS1; pale outlined halo and ornamental border for Mucha; shaded elemental FX with squash for hand-drawn; stochastic one-bit with head-banding for fax; red-cyan parallax split for anaglyph.
- Xiaohongshu remains the main gap. Re-run Exa `site:xiaohongshu.com` queries once the quota resets, or connect OpenCLI to a controlled Chrome session.
