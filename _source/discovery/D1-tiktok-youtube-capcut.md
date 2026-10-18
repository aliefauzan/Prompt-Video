# D1 discovery: TikTok, YouTube, CapCut (and Douyin attempt)

Session D1 of the style-discovery sweep. Research only: no style folders, no renders. Compared against the 61 looks in `_source/STYLES_TAKEN.md`.

Totals: 226 queries or page loads (126 YouTube, 49 TikTok searches, 7 TikTok tag pages, 25 Exa queries of which 9 returned text, 18 CapCut pages, 1 Douyin attempt). 39 candidate looks in the table below, 12 marked with a star. 12 screenshots are in `_source/discovery/shots/D1_<slug>.png`.

Access notes:
- TikTok `/discover/...` pages redirect to the home page in the browser and in curl. Their text was only reachable through Exa (`site:tiktok.com/discover`), and Exa's free tier rate-limited after query 9.
- TikTok search and tag pages load without login. Thumbnails only load after a scroll down and back up, so the screenshots are search-result grids taken that way.
- Douyin search is behind a QR/SMS login wall. Nothing usable was visible, so it was skipped.
- CapCut `/template/effects` is mostly slow-motion timing templates. CapCut `/templates/search/...` pages render blank without scripts. CapCut effect names were found through TikTok search instead.

## Keywords tried

The brief's full keyword list was run on YouTube (round 1, including the non-English variants), then a second round of 50 look-specific queries. "Hits" is the number of result rows returned by yt-dlp. TikTok, Exa, CapCut and Douyin queries are listed after the YouTube tables.


### YouTube round 1 (yt-dlp ytsearch25, brief keywords plus slang and non-English)

| # | Query | Hits |
|---|---|---|
| 1 | video style editing | 26 |
| 2 | video editing style | 26 |
| 3 | edit style | 26 |
| 4 | editing styles tutorial | 26 |
| 5 | aesthetic edit | 27 |
| 6 | aesthetic video edit | 26 |
| 7 | trending edit style | 26 |
| 8 | viral edit style | 26 |
| 9 | capcut edit style | 26 |
| 10 | capcut template | 26 |
| 11 | after effects style | 26 |
| 12 | premiere look | 26 |
| 13 | LUT look | 26 |
| 14 | AI video style | 26 |
| 15 | AI video filter | 26 |
| 16 | AI restyle video | 26 |
| 17 | video to video style | 26 |
| 18 | frame by frame edit | 26 |
| 19 | frame by frame animation edit | 26 |
| 20 | rotoscope edit | 26 |
| 21 | mixed media edit | 26 |
| 22 | collage edit | 26 |
| 23 | paper cutout edit | 26 |
| 24 | stop motion edit | 26 |
| 25 | overlay edit | 26 |
| 26 | texture overlay edit | 26 |
| 27 | music video look | 26 |
| 28 | music video edit style | 26 |
| 29 | fashion film edit | 26 |
| 30 | film look | 26 |
| 31 | cinematic look | 26 |
| 32 | retro edit | 26 |
| 33 | vintage edit | 26 |
| 34 | y2k edit | 26 |
| 35 | grunge edit | 26 |
| 36 | dreamcore edit | 26 |
| 37 | weirdcore edit | 26 |
| 38 | liminal edit | 26 |
| 39 | analog horror edit | 26 |
| 40 | found footage look | 26 |
| 41 | lo-fi edit | 26 |
| 42 | indie sleaze edit | 26 |
| 43 | cyber edit | 26 |
| 44 | anime edit | 26 |
| 45 | AMV style | 26 |
| 46 | phonk edit look | 26 |
| 47 | glitch edit | 26 |
| 48 | psychedelic edit | 26 |
| 49 | trippy edit | 26 |
| 50 | experimental video art | 26 |
| 51 | motion design style | 26 |
| 52 | seedream video prompt | 26 |
| 53 | kling style prompt | 26 |
| 54 | runway restyle | 26 |
| 55 | midjourney video style | 26 |
| 56 | higgsfield effect | 26 |
| 57 | pika effect | 26 |
| 58 | AI filter trend | 26 |
| 59 | style transfer video | 26 |
| 60 | tiktok filter trend | 26 |
| 61 | instagram reel effect | 26 |
| 62 | edit inspo | 26 |
| 63 | how to do the edit tutorial | 26 |
| 64 | effect tutorial capcut | 26 |
| 65 | trending capcut effect tutorial | 26 |
| 66 | viral editing style tutorial | 26 |
| 67 | gaya editing video | 26 |
| 68 | efek video viral | 26 |
| 69 | tutorial edit video estetik | 26 |
| 70 | 视频风格 | 26 |
| 71 | 剪辑风格 | 26 |
| 72 | 动画 滤镜 视频 风格 | 26 |
| 73 | 動画 エフェクト 加工 | 26 |
| 74 | 영상 편집 스타일 | 26 |
| 75 | estilo de edición video | 26 |
| 76 | estilo de edição vídeo | 26 |

### YouTube round 2 (yt-dlp ytsearch, targeted tutorial and look-name queries)

| # | Query | Hits |
|---|---|---|
| 1 | how to make your video look like a painting effect tutorial | 16 |
| 2 | how to make your video look like a comic book effect | 16 |
| 3 | how to make your footage look like a video game | 16 |
| 4 | how to make your video look like a dream effect tutorial | 16 |
| 5 | how to make your video look like it was shot on film 2026 | 16 |
| 6 | new capcut effect trend 2026 tutorial | 16 |
| 7 | trending video effect 2026 after effects tutorial | 16 |
| 8 | viral instagram reel effect look 2026 | 16 |
| 9 | tiktok trending filter look 2026 how to | 16 |
| 10 | premiere pro stylized look tutorial effects | 16 |
| 11 | davinci resolve stylized look tutorial | 16 |
| 12 | internet aesthetics explained video editing styles | 16 |
| 13 | cybercore edit tutorial | 16 |
| 14 | dark academia edit tutorial video | 16 |
| 15 | cottagecore edit video look | 16 |
| 16 | frutiger aero edit tutorial | 16 |
| 17 | vaporwave edit tutorial video | 16 |
| 18 | kidcore edit tutorial | 16 |
| 19 | nostalgiacore edit video look | 16 |
| 20 | VHS found footage effect tutorial capcut | 16 |
| 21 | higgsfield effects list new 2026 | 16 |
| 22 | kling ai video restyle effects list | 16 |
| 23 | luma modify video style presets | 16 |
| 24 | runway aleph video style prompts | 16 |
| 25 | seedance 2.5 video to video style prompt | 16 |
| 26 | midjourney video style reference trend | 16 |
| 27 | aestheticcore edit video types list | 16 |
| 28 | edit styles tier list tiktok 2026 | 16 |
| 29 | trending edit look tiktok jedag jedug flash colour invert | 16 |
| 30 | manga edit capcut tutorial | 16 |
| 31 | anime AI filter video trend ghibli alternative | 16 |
| 32 | AI claymation felt plush style video tutorial | 16 |
| 33 | photo to video style trend hypic capcut | 16 |
| 34 | CCD sensor camera look edit tutorial | 16 |
| 35 | Dazz cam digicam filter video | 16 |
| 36 | Wes Anderson style edit capcut | 16 |
| 37 | Euphoria style lighting edit capcut | 16 |
| 38 | korean aesthetic video filter capcut tutorial | 16 |
| 39 | halation glow film look tutorial | 16 |
| 40 | tilt shift miniature effect tutorial | 16 |
| 41 | x-ray effect tutorial | 16 |
| 42 | time warp scan effect tutorial | 16 |
| 43 | depth style edit capcut tutorial | 16 |
| 44 | ice crystal filter ai effect video | 16 |
| 45 | colour splash selective colour video effect | 16 |
| 46 | double vision RGB split chromatic aberration look | 16 |
| 47 | liquid metal chrome effect video tutorial | 16 |
| 48 | VHS bodycam fisheye music video look | 16 |
| 49 | stop motion jitter animation effect on live footage | 16 |
| 50 | boiling line effect video tutorial | 16 |

### TikTok search pages (www.tiktok.com/search?q=..., browser)

| # | Query | Result |
|---|---|---|
| 1 | editing style trend 2026 | tiles reviewed (count not logged) |
| 2 | trending video filter look capcut 2026 | tiles reviewed (count not logged) |
| 3 | new ai video style filter trend | tiles reviewed (count not logged) |
| 4 | edit style frame by frame texture overlay | tiles reviewed (count not logged) |
| 5 | depth style edit capcut | 12+ tiles reviewed, captions and URLs extracted |
| 6 | time warp scan slit scan filter | 12+ tiles reviewed, captions and URLs extracted |
| 7 | weirdcore edit tutorial capcut look | tiles reviewed (count not logged) |
| 8 | x ray filter video effect | 12+ tiles reviewed, captions and URLs extracted |
| 9 | tilt shift miniature effect video | 12+ tiles reviewed, captions and URLs extracted |
| 10 | vaporwave edit capcut effect | tiles reviewed (count not logged) |
| 11 | anaglyph 3d red cyan effect | tiles reviewed (count not logged) |
| 12 | liquid chrome metal effect video edit | tiles reviewed (count not logged) |
| 13 | blacklight uv glow video filter | tiles reviewed (count not logged) |
| 14 | kaleidoscope mirror effect video | tiles reviewed (count not logged) |
| 15 | led screen dot matrix video effect | tiles reviewed (count not logged) |
| 16 | pixar style ai video filter trend | tiles reviewed (count not logged) |
| 17 | ps1 ps2 graphics filter video edit | tiles reviewed (count not logged) |
| 18 | EsDeeKid style edit fisheye flash grain | tiles reviewed (count not logged) |
| 19 | cinestill halation glow film look video | tiles reviewed (count not logged) |
| 20 | hopecore edit aesthetic video | tiles reviewed (count not logged) |
| 21 | wes anderson filter video symmetrical pastel | tiles reviewed (count not logged) |
| 22 | minecraft voxel block filter video ai | tiles reviewed (count not logged) |
| 23 | manga black and white edit filter screentone video | tiles reviewed (count not logged) |
| 24 | chalkboard chalk drawing effect video | 12+ tiles; only AI whiteboard explainer ads, no real look |
| 25 | flip phone camera 2000s low quality filter video | tiles reviewed (count not logged) |
| 26 | papercraft layered paper ai video style | tiles reviewed (count not logged) |
| 27 | kiro mashitala color mixing filter | tiles reviewed (count not logged) |
| 28 | tumblr soft grunge 2014 aesthetic edit | tiles reviewed (count not logged) |
| 29 | weirdcore edit look filter | 12+ tiles reviewed, captions and URLs extracted |
| 30 | halation cinestill red glow filter | 12+ tiles reviewed, captions and URLs extracted |
| 31 | wes anderson filter capcut pastel | 12+ tiles reviewed, captions and URLs extracted |
| 32 | manga panel edit screentone filter | 12+ tiles reviewed, captions and URLs extracted |
| 33 | needle felted wool ai video effect | 12+ tiles reviewed, captions and URLs extracted |
| 34 | phonk edit rgb split chromatic tutorial | 12+ tiles reviewed, captions and URLs extracted |
| 35 | arcane style ai filter video | 12+ tiles reviewed, captions and URLs extracted |
| 36 | kaleidoscope mirror effect video filter | 12+ tiles reviewed, captions and URLs extracted |
| 37 | papercraft paper cut diorama ai video | 12+ tiles reviewed, captions and URLs extracted |
| 38 | backrooms liminal filter video edit | 12+ tiles reviewed, captions and URLs extracted |
| 39 | ps1 graphics filter video effect | 12+ tiles reviewed, captions and URLs extracted |
| 40 | liquid chrome metal effect video ai | 12+ tiles reviewed, captions and URLs extracted |
| 41 | blacklight uv glow filter video | 12+ tiles reviewed, captions and URLs extracted |
| 42 | knitted video trend prompt crochet | 12+ tiles reviewed, captions and URLs extracted |
| 43 | cuphead 1930s rubber hose cartoon filter | 12+ tiles reviewed, captions and URLs extracted |
| 44 | windows 95 desktop popup edit aesthetic | 12+ tiles reviewed, captions and URLs extracted |
| 45 | gta loading screen art style filter | 12+ tiles reviewed, captions and URLs extracted |
| 46 | chalkboard chalk drawing ai video effect | 12+ tiles; only AI whiteboard explainer ads, no real look |
| 47 | tintype 1800s photo filter video | 12+ tiles reviewed, captions and URLs extracted |
| 48 | manga edit capcut black white | 12+ tiles reviewed, captions and URLs extracted |
| 49 | ... | tiles reviewed (count not logged) |

### TikTok tag pages (browser)

| Tag | Result |
|---|---|
| #editingstyle | tiles reviewed (video titles read from anchor attributes) |
| #videostyle | tiles reviewed (video titles read from anchor attributes) |
| #editstyle | tiles reviewed (video titles read from anchor attributes) |
| #weirdcore | tiles reviewed (video titles read from anchor attributes) |
| #dreamcore | tiles reviewed (video titles read from anchor attributes) |
| #analoghorror | tiles reviewed (video titles read from anchor attributes) |
| #mixedmediaedit | tiles reviewed (video titles read from anchor attributes) |

### Exa (mcporter exa.web_search_exa, TikTok Discover pages)

| Query | Result |
|---|---|
| site:tiktok.com/discover capcut edit style trend | text returned (25665 bytes) |
| site:tiktok.com/discover aesthetic video edit style | text returned (25578 bytes) |
| site:tiktok.com/discover viral edit style | text returned (26413 bytes) |
| site:tiktok.com/discover ai video filter trend | text returned (26343 bytes) |
| site:tiktok.com/discover video to video style ai | text returned (25543 bytes) |
| site:tiktok.com/discover frame by frame animation edit | text returned (22523 bytes) |
| site:tiktok.com/discover rotoscope edit | text returned (16414 bytes) |
| site:tiktok.com/discover collage edit | text returned (26255 bytes) |
| site:tiktok.com/discover paper cutout stop motion edit | text returned (23384 bytes) |
| site:tiktok.com/discover overlay texture edit | nothing (rate limited, HTTP 429) |
| site:tiktok.com/discover music video edit style | nothing (rate limited, HTTP 429) |
| site:tiktok.com/discover fashion film edit | nothing (rate limited, HTTP 429) |
| site:tiktok.com/discover film look filter | nothing (rate limited, HTTP 429) |
| site:tiktok.com/discover retro vintage edit | nothing (rate limited, HTTP 429) |
| site:tiktok.com/discover grunge edit | nothing (rate limited, HTTP 429) |
| site:tiktok.com/discover glitch edit | nothing (rate limited, HTTP 429) |
| site:tiktok.com/discover psychedelic trippy edit | nothing (rate limited, HTTP 429) |
| site:tiktok.com/discover experimental video art | nothing (rate limited, HTTP 429) |
| site:tiktok.com/discover higgsfield effect | nothing (rate limited, HTTP 429) |
| site:tiktok.com/discover kling ai style prompt | nothing (rate limited, HTTP 429) |
| site:tiktok.com/discover capcut effects name trending | nothing (rate limited, HTTP 429) |
| site:tiktok.com/discover instagram reel effect trend | nothing (rate limited, HTTP 429) |
| site:tiktok.com/discover edit inspo | nothing (rate limited, HTTP 429) |
| site:tiktok.com/discover anime edit style | nothing (rate limited, HTTP 429) |
| site:tiktok.com/discover phonk edit style look | nothing (rate limited, HTTP 429) |

### CapCut (browser, public pages)

| Page | Result |
|---|---|
| capcut.com/templates | category page, mostly generic templates |
| capcut.com/template/effects | slow-motion and timing templates only |
| capcut.com/template/editors-pick | generic template cards |
| capcut.com/resource/hot-templates | generic cards |
| capcut.com/resource/caption-template | caption templates, no look |
| capcut.com/template/social | generic cards |
| capcut.com/template/others | generic cards |
| capcut.com/template/insights | generic cards |
| capcut.com/templates/search/ai-style | blank page |
| capcut.com/templates/search/vintage-film | blank page |
| other capcut.com category pages (holiday, calendar, anniversary, business, industry, record) | opened and skipped, no style looks |

### Douyin

| Query | Result |
|---|---|
| 视频风格滤镜 (douyin.com search, video tab) | nothing: login wall |


## Candidates

39 distinct looks before filtering. Rows marked ★ are the top 12 and each has a screenshot (a TikTok search-result grid for the keyword shown) in `_source/discovery/shots/`. TikTok links are `https://www.tiktok.com/@user/video/id`, shortened here to `@user/video/id`. YouTube links are `https://youtu.be/id`. "Doable" means a look that can be applied frame by frame to existing footage: yes, or partly (needs a subject matte, depth map, or several frames of context).

| # | Style name | What it looks like | Where seen | Keyword that found it | Doable? | Closest taken style + why it differs |
|---|---|---|---|---|---|---|
| 1 ★ | X-Ray Skeleton Scan | The subject becomes a glowing cyan-white inverted radiograph: bones and organs visible inside a translucent body on a dark ground, often with a flash on the beat. | TikTok @jerrzyo/video/7666624228719987988, @griggen/video/7672078631337823510, @itsnotoriously/video/7543845755027574046; YouTube Qd2FQau3owQ, ZVA2Ek20hAo | x ray filter video effect | yes | 16 Thermal Camera and 39 Lidar Point Cloud. Thermal is false-colour heat and lidar is points; this is a monochrome radiograph with interior anatomy. |
| 2 ★ | Tilt-Shift Miniature | Real footage reads as a toy-scale diorama: a sharp focus band, heavy blur above and below, boosted saturation and contrast, high-angle view. | TikTok @the.dailyshort25/video/7664563122413374753, @antonio_pics_/video/7296333954616003848, @midioin/video/7356953975456861445 (389.9K likes); YouTube vY_0etcrwA0, L5H0vQwYuLw | tilt shift miniature effect video | yes (works best on high-angle shots) | 37 Claymation and 58 Lego Brick Build re-render the material. This keeps real footage and changes only depth of field and colour, so everything looks tiny. |
| 3 ★ | Knit and Needle-Felt Wool World | The scene is rebuilt from crocheted or knitted yarn or fuzzy needle-felted wool, with visible fibres, loops and tiny-diorama lighting. | TikTok @cozywoolvillage/video/7527089596224539934, @space.bananas.agency/video/7575209140985810231 ("knitted video" trend), @eunice_thaddeus/video/7680207562402286868 | needle felted wool ai video effect; knitted video trend prompt crochet | yes | 34 Cross-Stitch Embroidery is a flat thread grid and 37 Claymation is smooth plasticine. Wool is soft fibre volume with knit loops. Another session (D3) has a felt-wool shot, so expect overlap. |
| 4 ★ | Liquid Chrome Flow | Silver liquid-metal ribbons and blobs drift, melt and wrap around the subject and scene, mirroring the surroundings. Viral as a "chrome flow" effect in 2026. | TikTok @meowstardaily/video/7680581615130660126, @finely.ai/video/7510366938736954646, @xbus90971631/video/7681350030183206158 | liquid chrome metal effect video ai | partly (drifting blobs as an overlay are easy; wrapping the subject needs AI) | 15 Y2K Chrome / Frutiger Aero is bubbly chrome type and UI. 45 Marble Statue swaps the subject's material. This is fluid chrome as an animated medium over the whole frame. |
| 5 ★ | Papercraft Layered Diorama | The scene is rebuilt from layered cut card stock with soft shadows between layers, animated at a stop-motion 8 to 12 fps. A large AI "paper-cut" trend. | TikTok @storyboard.co.th/video/7666704828600454408 (3.5K likes), @the_ai_horizon/video/7671247986906631446, @ai.akshu/video/7660905625349524758 | papercraft paper cut diorama ai video | yes | 08 Scrapbook Sticker Collage and 01 Punk Photocopy Collage are messy stuck-on photo scraps. This is a clean, depth-layered paper set in coloured card with cast shadows. |
| 6 ★ | Depth-Style Fog Silhouette | The subject is cut out as a pale grey depth-map silhouette in white fog, slow push-in, sometimes laser-red eyes. The 2026 CapCut "depth style" trend. | TikTok @letsayhey/video/7675064280814783758 (256K likes), @ripedtx_/video/7675956729426873621, @evaned1t/video/7671058197435878677; YouTube ADSs7X1zLQc | depth style edit capcut | partly (needs a subject matte and a depth map per frame) | 39 Lidar Point Cloud is points and 16 Thermal Camera is colour mapped. This is a soft near-white to black depth gradient with fog. |
| 7 ★ | Halation Red-Glow Film | Red-orange bloom bleeds around bright lights and highlights, with soft grain, as on CineStill 800T night street film. | TikTok @zac.freuden/video/7287478187209149703, @vsco/video/7522923782730681655, @peace_gates/video/7237132869800430849; YouTube vbO4nc4UBpU | halation cinestill red glow filter | yes | 03 Super 8 Film Burn is flare and burnt edges, 17 Double Exposure is layered images. This is a highlights-only red halo on a clean modern frame. |
| 8 ★ | Wes Anderson Pastel Symmetry | Flat, centred, symmetrical framing in a pastel palette (mustard, pink, mint, teal), warm flat light, serif title cards. | TikTok @tianchad/video/7225925591248178433 (38.5K likes), @esno.art/video/7225318124696980763 (110K), @wabifathan_/video/7227266297413848346; YouTube l__dnp6e6Ok (613K views) | wes anderson filter capcut pastel | yes for palette and flatness, partly for symmetry (needs reframing) | 54 Teal-Orange Anamorphic is a contrasty cinema grade and 46 1950s Editorial Poster is print. This is a low-contrast pastel palette with deadpan symmetry. |
| 9 ★ | Weirdcore / Dreamcore | Over-bright, nostalgic, low-resolution scene with rainbows, eyes, odd captions and a wrong sense of scale; soft grain. | TikTok @ayitsphotography/video/7687341476929408263 (37.4K likes), @_ilikebugsandmoths_/video/7189624672579882245, @ninanayko/video/7533697244235599112 (232K); YouTube SuaK3EZZUNE | weirdcore edit look filter; #weirdcore and #dreamcore tag pages | yes | 02 VHS Camcorder and 17 Double Exposure Dreamy. This is defined by surreal cues (eyes, rainbows, unsettling captions) on oversaturated pastel, not by tape artefacts. D3 also has a dreamcore shot. |
| 10 ★ | Backrooms Liminal Yellow | A sickly mono-yellow, fluorescent-lit empty office or corridor, damp carpet, wide empty depth, faint hum. | TikTok @awsalater/video/7654750896219376926, @leolikesphotos/video/7106628495865941253 (2.8K likes), @revolve_vr/video/7274690107402145066; YouTube rTLxv_TlzIE | backrooms liminal filter video edit | yes | 38 CCTV Night Vision is green surveillance and 27 Signal Relief Scanlines is a signal look. This is a yellow-olive wash with fluorescent ceiling light, smooth wide-angle and no surveillance framing. |
| 11 ★ | Arcane Painterly 3D | Hand-painted brush texture on faces and clothes, gritty ink lines, strong teal and magenta rim light. A CapCut Arcane filter has over 270K likes. | TikTok @jackvsai/video/7669765802563849475, @aimirror.official/video/7441804356124527902, CapCut filter tile "Filter Arcane" (153.6K likes) in the search grid | arcane style ai filter video | yes | 51 Ghibli Painted Anime is soft pastoral watercolour and 30 Spider-Verse Comic Offset is halftone and print offset. This is painted-3D grit with coloured rim light. |
| 12 ★ | Manga Ink Black-and-White | Black ink on white paper, fine screentone gradients, speed lines, panel splits, no colour. Many CapCut tutorials. | TikTok @awsalater/video/7689588162049428766 (25.3K likes), @annaliise.cc/video/7659606110558620948 (11.4K), @.gmx8/video/7617074014028156181; YouTube xMzuMC_bhaM (168K views) | manga edit capcut black white | yes | 07 Pop-Art Comic Halftone and 53 90s Comic Book are colour Ben-Day print, 31 Sin City Noir Red is noir with red. This is Japanese manga page ink with screentone, black and white only. |
| 13 | Phonk RGB-Split | Red and cyan channel offsets ghost around a high-contrast, grainy, shaky subject. | TikTok @fredpelle.tv/video/7421593745025502469, @miracampschool/video/7492166552389733654 | phonk edit rgb split chromatic tutorial | yes | 05 Datamosh Glitch is codec smear. This is a pure channel offset (chromatic aberration), closer to a lens artefact. Borderline near-duplicate. |
| 14 | Time-Warp Scan | A scan line sweeps down the frame; the part above it shows a later moment than the part below, so faces stretch. | TikTok @mr.alexaa/video/6879344833576602881, @hicksphc0lg/video/7696883510325349646; YouTube HJvIfcbk3lA | time warp scan slit scan filter | partly (needs several frames of context) | 26 Slow Shutter Smear is a continuous blur. This is a hard scan boundary between two moments. Mostly a timing trick. |
| 15 | Kaleidoscope Mirror | The footage is mirrored into 6 or 8 radial segments, mandala-like. | TikTok @jonsimo/video/7190839394457095429, @kfconcept/video/7564643516916256022 | kaleidoscope mirror effect video filter | yes | 44 Broken Mirror Shards has irregular shards. This is radial symmetry. D3 also has a kaleidoscope shot. |
| 16 | Retro OS Desktop Overlay | Grey bevelled Windows 95 windows, error popups, a cursor and a teal desktop layered over the footage. | TikTok @s1lax.art/video/7598465499810237717, @odditylooms/video/7625183082550676758, @adxyxn_g59/video/7170185052045806854 | windows 95 desktop popup edit aesthetic | partly (overlay) | 12 ASCII Terminal Phosphor is a text terminal and 15 Y2K Chrome is glossy. This is grey Win9x interface chrome. |
| 17 | PS1 Low-Poly Warp | Vertex wobble, warped affine textures, 240p dither and distance fog, like early PlayStation. | TikTok @dan.esberg/video/7349281640935394603, @decaying_sun/video/7675591094083620118, @ember.lite/video/7624261224116604167 (483.8K likes); YouTube nJfZ9D6rcVw | ps1 graphics filter video effect | yes | 40 Low-Poly 3D is clean facets and 11 16-Bit Pixel Art Dither is sprites. This is jittering vertices and warped low-res textures. |
| 18 | GTA Loading-Screen Art | Bold-outline, flat-shaded illustration with sunset gradients and saturated palette, like game loading screens. Viral for GTA VI. | TikTok @anne102333/video/7688553544248577310, @ngcnguynkithng3/video/7688630801646325012, @kitrp16/video/7638949974004288788 | gta loading screen art style filter | yes | 53 90s Comic Book is the nearest. Likely a near-duplicate unless the airbrushed vector-poster finish is kept. |
| 19 | Cuphead 1930s Rubber-Hose | Rubber-hose limbs, pie eyes, watercolour backgrounds, film scratches and flicker. | TikTok @xbus2604103358/video/7667576183491448094, @remycoup/video/7360735006718774570 | cuphead 1930s rubber hose cartoon filter | yes (AI) | 52 Retro 90s Cartoon and 28 Hand-Cranked Silent Film. This is 1930s inkblot cartoon. D3 also has a rubber-hose shot. |
| 20 | Pixar 3D Render | Glossy, soft 3D characters with subsurface skin and big eyes. | YouTube OajM9WMAbDc (47.7K views) | pixar style ai video filter trend | yes (AI) | 59 3D Kawaii Chibi. Near-duplicate: Pixar proportions are only a step from chibi. |
| 21 | Blacklight UV Glow | Fluorescent paint and objects glow in violet darkness. | TikTok @artsyfeet/video/6900856994085752069 | blacklight uv glow filter video | yes | 13 Neon Scribble Outline and 55 Cyberpunk Neon City. This is UV purple dark with glowing pigment. Thin evidence: one real hit. |
| 22 | Euphoria Glitter-Gel Lighting | Blue, pink and purple gel light on faces, glitter makeup sparkle, shallow focus. | YouTube 7sVFUjkyyRA (151K views) | Euphoria style lighting edit capcut | yes | 55 Cyberpunk Neon City and 32 Synthwave are city and landscape neon. This is portrait lighting. |
| 23 | Wong Kar-wai Step-Printed Dream Glow | Smeared step-printed motion, saturated green and red, soft glow. | YouTube K1cO7mHwj3Q (350K views) | halation glow film look tutorial | partly (step-printing is temporal) | 26 Slow Shutter Smear and 56 Prismatic Dreamscape. This adds stutter step-printing and a specific green-red palette. |
| 24 | Dark Academia Warm Library | Desaturated brown and green, candlelit, serif quotes. | YouTube k1u4qOfF_D0 (135K views), fItjbLNJU2Y | dark academia edit tutorial video | yes | 28 Hand-Cranked Silent Film is monochrome. This is a warm colour grade. |
| 25 | Cottagecore Soft Pastel | Hazy, warm, pastel greens and creams. | YouTube v_wdzLhsQxk, plus 12 cottagecore preset videos | cottagecore edit video look | yes | 60 Floral Maximalism Gouache is painted. Grade-level look, near-duplicate of Korean soft tone. |
| 26 | Korean Soft Tone / K-drama | Milky lifted highlights, cool-pink tint. | YouTube Q94Eszq6Mnc, Mf0S9rzPEuU | korean aesthetic video filter capcut tutorial | yes | 20 Polaroid Photo Dump is framing and print. Grade-level look. |
| 27 | Kidcore / Indie Kid | Primary colours, rainbows, 90s toy stickers, VHS. | YouTube QLteHd1uwSM, SuaK3EZZUNE | kidcore edit tutorial | partly | 08 Scrapbook Sticker Collage and 02 VHS Camcorder. Near-duplicate. |
| 28 | Vaporwave / Simpsonswave | Pink, purple and teal, grids, marble busts, 90s cartoon VHS. | YouTube DskSPS9wKE0 (56K views), 3ZUPJbgDk38 | vaporwave edit tutorial video | yes | 32 Synthwave Outrun. Near-duplicate. |
| 29 | Analog Horror | Degraded broadcast tape, red warning text, dread. | YouTube Jv5nCegZ4EM (89K views); #analoghorror tag page | analog horror edit; VHS found footage effect | yes | 02 VHS Camcorder and 38 CCTV Night Vision. Near-duplicate with horror overlay text. |
| 30 | Fisheye Bodycam / VX1000 | Barrel-distorted wide lens, overexposed, handheld bodycam realism. | YouTube E-cyiYFywGs (110K views), bz0ipJJlxxA | VHS bodycam fisheye music video look | yes | 04 Y2K Digicam Flash and 38 CCTV Night Vision. This is lens distortion plus bodycam framing. |
| 31 | Line-Boil Hand-Drawn Jitter | Outlines wobble at 8 to 12 fps over flat colour fills. | YouTube it3PGEcaobk (53K views), Iq5VnJ2c-eY (102K) | boiling line effect video tutorial | yes | 18 Pencil Sketch Rotoscope, 25 Red Pencil Mixed Media. The distinguishing part is the boil jitter on cel fills. |
| 32 | Collage Cut-Out Stop-Motion | Jerky paper cut-outs animated frame by frame. | YouTube XAm4i1X7L_Y (471K views), _gttJPivVyM | collage edit; stop motion edit | yes | 08 and 01. Near-duplicate; see Papercraft for the cleaner variant. |
| 33 | Bleach Bypass | Desaturated, high-contrast silver look, war-film grade. | YouTube xP8SGuOGMBw | davinci resolve stylized look tutorial | yes | 54 Teal-Orange Anamorphic. A desaturating grade rather than split-tone. |
| 34 | Tintype / Wet-Plate | Silver-grey plate tone, vignette, soft focus, plate scratches. | TikTok @mikaylastephens3/video/7682577693828861197 (17.8K likes), @merrickhanna/video/7477321000473120046 | tintype 1800s photo filter video | yes (AI) | 28 Hand-Cranked Silent Film is moving silent film. This is a still plate look. |
| 35 | Chalkboard Chalk Drawing | White chalk lines on a dark board. | TikTok chalk search returned only AI whiteboard promos | chalkboard chalk drawing ai video effect | yes | 09 Cyanotype Sun Print and 18 Pencil Sketch Rotoscope. Weak evidence: no real example found. |
| 36 | Premiere Grunge | Torn paper, scribbles, fast shutter. | YouTube "the GRUNGE Effect Masterclass" (48.8K views) | premiere pro stylized look tutorial effects | yes | 01 Punk Photocopy Collage and 49 Chaotic Red Ink. Near-duplicate. |
| 37 | Cybercore / Y2K Cyber | Black and blue chrome, cyber glyph overlays. | YouTube PNWvG5R4dTU (4.4K views), jzbHJ61E3b8 | cybercore edit tutorial | yes | 15 Y2K Chrome and 55 Cyberpunk Neon City. Near-duplicate. |
| 38 | Colour Splash | Black and white with one colour kept. | YouTube bDzSWXJbAyQ, jDod-n-3Udk | colour splash selective colour video effect | yes | 31 Sin City Noir Red. Near-duplicate. |
| 39 | Hyperpop Chaos | Glitter, stickers, acid colours, chaotic cuts. | YouTube "CREATE CRAZY CHAOTIC HYPERPOP EDITS" (3.8K views) | cybercore / hyperpop edit tutorial | yes | 05, 08 and 15 together. Near-duplicate. |

### Top 12 (★)

1. X-Ray Skeleton Scan
2. Tilt-Shift Miniature
3. Knit and Needle-Felt Wool World
4. Liquid Chrome Flow
5. Papercraft Layered Diorama
6. Depth-Style Fog Silhouette
7. Halation Red-Glow Film
8. Wes Anderson Pastel Symmetry
9. Weirdcore / Dreamcore
10. Backrooms Liminal Yellow
11. Arcane Painterly 3D
12. Manga Ink Black-and-White

Screenshots: `D1_xray-skeleton-scan.png`, `D1_tiltshift-miniature.png`, `D1_knit-felt-wool-world.png`, `D1_liquid-chrome-flow.png`, `D1_papercraft-diorama.png`, `D1_depth-fog-silhouette.png`, `D1_halation-red-glow.png`, `D1_wes-anderson-pastel.png`, `D1_weirdcore-dreamcore.png`, `D1_backrooms-liminal-yellow.png`, `D1_arcane-painterly.png`, `D1_manga-ink-bw.png`.

Ranking rationale: strongest demand (view or like counts, many tutorials) combined with a look that is clearly not in the taken list and can be applied per frame. The weakest stars on that test are Depth-Style Fog Silhouette (needs mattes) and Liquid Chrome Flow (subject wrap needs AI); they are in because they are the biggest 2026 trends found.

### Seen but dropped as already taken

Frutiger Metro Aero (15), Dazz Cam / CCD digicam (04), 16-bit game look (11), AI anime and Ghibli filters (10, 51), claymation and AI plush (37, 59), VHS CapCut tutorials (02), halftone comic tutorials (07, 53), Spider-Verse look (30), stained-glass and mosaic (21).

### Looks searched with no usable result

Anaglyph 3D red/cyan, LED dot-matrix screen, Minecraft voxel, flip-phone camera, hopecore, tumblr soft grunge, EsDeeKid-style flash grain, "kiro mashitala colour mixing" filter. The pages loaded but no distinct frame-by-frame look came out of them beyond what is already in the table. Tattoo flash, technicolor and pixel sort returned nothing in the YouTube results; D3 has a pixel-sort shot.
