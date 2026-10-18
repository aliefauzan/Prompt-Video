# D3 — X/Twitter, Reddit, prompt-sharing sites, AI-tool style libraries

Group D3 discovery sweep. Research only. No style folders, no rendering.
Compared against `_source/STYLES_TAKEN.md` (61 styles). Screenshots: `_source/discovery/shots/D3_<slug>.png`.

## Platform access — read first (honest coverage notes)

- **X/Twitter**: OpenCLI extension not connected, twitter-cli returned 404. Fell back to Exa (`site:x.com`) and WebSearch with `allowed_domains: x.com`, plus unrollnow/twiscan mirrors. Coverage = search-snippet level, no timelines or hashtag pages.
- **Reddit**: blocked everywhere (curl, Jina, api.reddit.com, built-in browser; pullpush rate-limited). Exa `site:reddit.com` hit its free-tier 429 limit on 10 of 11 queries. Reddit evidence below is limited to ~10 threads that surfaced in Exa snippets. **Reddit is under-covered. Treat "nothing found" there as "could not look", not "no signal".**
- **Exa free MCP**: shared quota with sibling sessions; 429s throughout. Added retry/sleep, then moved to WebSearch, the Civitai public REST API, Jina reader and the built-in browser.
- **Not reachable**: Higgsfield via Jina (abuse block; used built-in browser instead), Krea (login-gated), unrollnow via Jina (403), TikTok/YouTube (covered by sibling groups).
- Hit counts below are approximate where I did not tally per query. "~8" = a page of results of which most were relevant.

## Keywords tried

Totals: ~56 Exa queries, 13 WebSearch queries, ~40 Civitai API search phrases, 1 full Morphic sitemap scan (1,036 aesthetic/resource slugs), ~20 tool-library/prompt-site page fetches. **≈110 query runs.**

### X / Twitter (Exa `site:x.com` and WebSearch `allowed_domains: x.com`)

| Query | Platform | Hits |
|---|---|---|
| AI video style prompt restyle | X (Exa) | ~8, useful |
| video to video style transfer prompt | X (Exa) | ~8, useful (ProperPrompter Seedance 2.0 v2v) |
| Kling restyle prompt style | X (Exa) | ~8 |
| Seedance style prompt aesthetic | X (Exa) | ~8 (rom1trs mini-DV vlog) |
| Higgsfield effect new style | X (Exa) | ~8 |
| Runway Aleph restyle prompt / "turn this video into" | X (Exa) | ~8 (Ror_Fly Restyle posts) |
| video style editing viral edit style | X (Exa) | ~8, mostly generic |
| AI video filter trend "video to video" | X (Exa) | ~8 |
| aesthetic video edit prompt thread | X (Exa) | ~8 |
| capcut edit style trending | X (Exa) | ~8 |
| after effects look breakdown / texture overlay | X (Exa) | ~8 |
| Kling O1 O3 restyle claymation paper cutout | X (Exa) | ~8 |
| paper cutout stop motion AI video restyle | X (Exa) | ~8, strong (OriSilver, insMind, techhalla) |
| mixed media collage edit AI video | X (Exa) | ~8 |
| rotoscope AI video prompt | X (Exa) | 8 |
| dreamcore weirdcore liminal AI video | X (Exa) | 8 |
| analog horror found footage look | X (Exa) | 8 |
| indie sleaze edit AI video | X (Exa) | 8 |
| glitch phonk edit look | X (Exa) | 8 |
| psychedelic trippy AI video restyle | X (Exa) | 8 |
| anime edit AMV AI restyle | X (Exa) | 9 |
| fashion film edit style | X (Exa) | nothing (empty) |
| music video look | X (Exa) | ~8 |
| midjourney video style sref | X (Exa) | ~8, strong (Artedeingenio, promptsref srefs) |
| higgsfield effects list / pika effects list | X (Exa) | ~16 |
| tiktok AI filter trend / instagram reel AI effect trend | X (Exa) | ~16 |
| "AI video style trend viral restyle prompt thread" | X (WebSearch) | ~8 |
| "Yung Lean music video viral AI prompt" | X (WebSearch) | trend found (GENER8ION "Storm" remake) |
| "aura farming edit Higgsfield Katana" | X (WebSearch) | ~8 |
| "PixVerse effects templates list" / "Kling AI effects templates list" / "Hailuo effects templates list" / "Runway Aleph restyle styles list" | X (WebSearch) | ~8 each |

### Reddit (Exa `site:reddit.com`; direct access blocked)

| Query | Platform | Hits |
|---|---|---|
| r/aivideo video to video style transfer new look | Reddit | 429, nothing |
| r/VideoEditing aesthetic edit style how to get this look | Reddit | 429, nothing |
| r/AfterEffects how to recreate this style effect look texture | Reddit | 429, nothing |
| r/editors film look LUT style recreate | Reddit | 429, nothing |
| r/vfx rotoscope stylized look mixed media | Reddit | 429, nothing |
| r/StableDiffusion video style LoRA Wan restyle video to video | Reddit | 429, nothing (threads from earlier runs) |
| r/midjourney video style sref prompt animation look | Reddit | 429, nothing |
| r/premiere how to get this edit style look | Reddit | 429, nothing |
| r/capcut edit style trending template look | Reddit | 429, nothing |
| what is this editing style called video aesthetic | Reddit | 429, nothing |
| name of this video effect style glitch texture overlay edit | Reddit | 1 partial |
| (earlier runs) Kling restyle, EditAnything, anime restyle, kpop edits | Reddit | ~10 threads surfaced (see Evidence) |

### Prompt-sharing sites / model hubs

| Query / page | Platform | Hits |
|---|---|---|
| Civitai API: wan style, video style, wan 2.2 style, ltx style, ltx 2.3 style, ltx style lora, hunyuan video style, wan cartoon, wan filter effect | Civitai | ~100+ models skimmed |
| Civitai API: felt, knit plush, miniature, crayon, sketch, oil painting, watercolor, 3D render toy | Civitai | felt/plush hits good; knit weak |
| Civitai API: vaporwave, retro, film grain, 8mm, vintage, comic, manga, pixel, paper, stop motion, puppet | Civitai | mixed |
| Civitai API: tarot, woodcut, engraving, silhouette, anaglyph, neon, glitch, cyber, fashion, photo | Civitai | silhouette strong, rest mostly taken |
| Morphic resource sitemap (1,036 slugs: aesthetics/effects/animation types) | Morphic | ~60 relevant slugs |
| PromptHero / Lexica / PromptBase / shared Google Docs | web | nothing usable (image-first, no video-look taxonomy) |
| apimodels.app MiniMax H3 animation prompts, GitHub awesome-minimax-h3-prompts | web | ~6 looks (felt, voxel, ink) |
| opus.pro "17 Viral AI Video Styles of 2026", "11 Editing Aesthetics" | web | ~10 |
| Picsart "27 AI video editing prompts", vid2vid.io recipes | web | ~8 |
| Seedance libraries (Shoty, vflow, seedancelib, Renoise, dev.to 400 prompts) | web | prompt-level, no new looks |

### AI-tool style / effect libraries

| Tool | Hits |
|---|---|
| PixVerse Restyle (eachlabs) | 8 curated styles: Felted Art, Origami, Ukiyo-e, Cyberpunk, Clay, Baroque, Van Gogh, Animal World |
| Magic Hour / OpenArt | LEGO, marble, Minecraft, Rick & Morty, Ghibli, Pixar, claymation |
| Wink restyle | Dopamine, Pixe, Nightcap, Horror Anime, Graffiti, Idol, Clay, Hand-drawn, Oil Painting, Sim Life, Comic |
| Captions AI Edit styles (40+) | Chalk, Kai (soft aura), Rebel (grungy), Zine, Vinyl II, Analog, Film, Y2K, Neon, Sketch, Paper II |
| Kling creative effects / Kling 3.0 style list | Crochet Diary, Wes Anderson, others |
| Higgsfield /effects (built-in browser), /video-to-video, SOUL presets | Scrapbook Collage, Comic, Canvas, LSD, Cutout (mostly motion VFX); SOUL: CCTV, Fairycore, 90's Editorial, Double Exposure |
| Runway Aleph / Krea Video Restyle / Pika / Hailuo / Leonardo / Seedance presets | list pages login-gated or generic; mostly prompt-driven, no fixed preset names |
| Meta Restyle (Instagram Edits) / Reface Restyle | 50+ and 36 presets; comic, anime-film, game-world, Van Gogh, vintage |
| Decart Lucy Restyle, Wan wan2.7-videoedit (Alibaba) | prompt-driven "convert scene to claymation" |

### Multilingual (WebSearch)

| Query | Language | Hits |
|---|---|---|
| gaya edit video estetik tren CapCut AI restyle video filter viral | Indonesian | ~9, CapCut generic (Y2K, cozy, clean girl), nothing new |
| 视频风格 AI视频风格转换 剪辑风格 爆款 可灵 即梦 提示词 | Chinese | ~9, tool pages only |
| 動画 エフェクト 加工 AI 動画スタイル変換 流行り 編集 風 | Japanese | ~9, tool pages only |
| 영상 편집 스타일 AI 영상 스타일 변환 유행 감성 편집 | Korean | ~9, tool pages only |
| estilo de edición de video tendencia estética AI video restyle efecto viral | Spanish | ~9, Meta Restyle, "clumsy AI" parody trend |
| estilo de edição de vídeo estética tendência efeito IA restyle vídeo viral | Portuguese | ~9, Meta Restyle |

Multilingual added no new looks. Results were product pages restating the same preset set (anime, clay, oil, watercolor, cyberpunk, vintage film). Only new signal: Meta/Instagram Restyle ships 50+ presets.

## Candidates

★ = top 12. "Frame-by-frame doable" = can be applied to existing footage as a texture/palette/medium/overlay treatment.

| Style name | What it looks like (1 line) | Where seen (platform + URLs) | Keyword that found it | Frame-by-frame doable? | Closest taken style + why different |
|---|---|---|---|---|---|
| ★ Felt / wool needle-felt fiber world | Subjects rebuilt from stitched felt cutouts with fuzzy fibres, visible seams and soft shadows, 8–12 fps stop-motion jitter | Civitai https://civitai.com/models/2525862 ; PixVerse "Felted Art" (eachlabs restyle page) ; Aisma wool material | "felt", "wan style", PixVerse restyle | yes (fibre-noise displacement + fuzz edge + stepped timing) | 37 claymation / 34 cross-stitch — matte fibrous fuzz and stitched seams, no plasticine sheen, not flat thread |
| ★ Shadow silhouette / Bad Apple 1-bit | Subject as flat pure-white mask on black, zero shading, motion carries the image | Civitai https://civitai.com/models/1732430 ; Morphic silhouette-animation | "silhouette", Civitai API | yes (threshold + matte) | 31 Sin City noir red / 47 two-tone screen print — no grey, no red spot, no print texture; pure mask. Partial overlap with 31 |
| ★ Retro 80s–90s OVA anime (grain + halation) | Hand-painted cel look with matte painted backgrounds, film grain, soft halation, 4:3 feel | Civitai https://civitai.com/models/1671285 (9k dl), https://civitai.com/models/1833906 ; X @Artedeingenio MJ sref 2726004757 | "retro anime", "midjourney video style sref" | yes | 10 anime cel shade / 52 retro 90s cartoon — painted-bg film-print texture, not clean digital cel or western cartoon |
| ★ Painterly 3D (Arcane / Dispatch) | 3D-lit characters with brushstroke albedo, harsh rim light, hand-painted texture over geometry | Civitai https://civitai.com/models/2197303 , https://civitai.com/models/2332126 | "wan style", "3D render" | partly (painterly texture pass + rim light; true re-lighting is heavier) | 51 Ghibli / 59 3D kawaii — painterly-on-3D with dramatic lighting, not soft pastel |
| ★ Drawing time-lapse reveal | Frame builds from sketch lines to flat colour to final render, as if drawn live | Civitai https://civitai.com/models/1389992 , https://civitai.com/models/1397074 (DrawUndo) ; Morphic digital-art-timelapse | "drawing time-lapse" | yes (stroke-order mask + progressive fill per frame) | 18 pencil sketch rotoscope — a build-up reveal with colour fill, not a static pencil look |
| ★ PS1 / N64 lo-fi 3D | Warped affine textures, vertex wobble, blurry nearest textures, distance fog, 15 fps | Civitai https://civitai.com/models/1643552 | "retro", "3D", Civitai API | yes | 40 low-poly 3D — texture swim, blur and fog, not clean flat facets |
| ★ Kaleidoscope / mirror symmetry | Whole frame folded into radial mirrored petals that rotate | Morphic https://morphic.com/resources/videos/kaleidoscope-effect-videos | "psychedelic", Morphic slugs | yes (polar mirror remap) | 44 broken mirror shards — clean radial symmetry of the full frame, not fractured pieces |
| ★ Pixel-sort streaks | Brightness-threshold bands smeared into long sorted pixel ribbons | Morphic https://morphic.com/resources/videos/pixel-sort-effect-videos | "glitch", Morphic slugs | yes (threshold row/column sort) | 05 datamosh — sorted colour streaks keep the image readable; no codec smear |
| ★ Dreamcore / liminal haze | Overexposed empty rooms, pastel bloom, soft focus, uncanny nostalgic emptiness | Morphic https://morphic.com/resources/videos/dreamcore-videos ; Hailuo dreamcore guide ; EmpirioLabs liminal template ; TikTok liminal-land-ai | "dreamcore", "weirdcore", "liminal edit" | yes (bloom + haze + desaturated pastel grade) | 17 double exposure / 02 VHS — hazy pastel bloom on clean frames, no ghost layer or tape noise |
| ★ Sand animation on lightbox | Subject drawn in glowing amber sand grains, warm backlit translucent look | Morphic https://morphic.com/resources/videos/sand-animation-videos | "sand animation", Morphic slugs | partly (grain-field + glow ok; the "morphing" is motion) | 48 charcoal / 19 watercolor — translucent granular amber light, no pigment or charcoal |
| ★ Giallo gel lighting | 70s Italian horror: magenta/blue gels, rain-slick streets, black-gloved menace | Morphic https://morphic.com/resources/videos/giallo-style-videos | "giallo", Morphic slugs | yes (split gel colour grade + contrast + grain) | 31 Sin City noir red / 43 dark stage spotlight — saturated magenta-cyan gel palette, not B/W+red, not a single spot |
| ★ Rubber-hose 1930s cartoon | B/W pie-eyed noodle-limbed cartoon with squash-stretch, scratches, grain | Morphic https://morphic.com/resources/videos/rubber-hose-animation-videos | "rubber hose", Morphic slugs | partly (line+B/W film treatment yes; limb noodling needs warp) | 52 retro 90s cartoon / 28 silent film — inkblot line style with rubbery limbs; 28 only covers flicker |
| Crochet / knit amigurumi yarn | Everything built from crocheted yarn loops, plush and cute | Kling Creative Effects "Crochet Diary" ; Civitai knit/plush searches | "knit plush", Kling effects | partly | 34 cross-stitch — 3D looped yarn volume vs flat thread grid |
| Origami folded paper | Faceted folded-paper figures with crisp creases | PixVerse Restyle "Origami" (eachlabs) ; vid2vid.io | "paper cutout", PixVerse restyle | partly | 40 low-poly / 08 scrapbook — fold lines and paper sheen |
| Layered hinged paper-cut diorama | Stacked cardstock layers with cast shadows between layers, torn edges | Civitai https://civitai.com/models/2528213 ; X https://x.com/insmind_com/status/2077030549571727778 , https://x.com/OriSilver/article/2078103099986657470 | "paper cutout stop motion" | partly | 08 scrapbook sticker collage — depth-stacked single-material paper, not ephemera/stickers. Overlap risk |
| Interpolated colour rotoscope (Waking Life) | Wobbling flat colour fills with loose line boil over live footage | Morphic https://morphic.com/resources/videos/rotoscope-animation-videos ; ACM paper on generative rotoscoping | "rotoscope edit" | yes | 18 pencil sketch rotoscope — colour wash fills vs graphite |
| Ink-brush cinematic 3D | Brush-stroke ink edges on 3D-lit scenes | X @aimikoda "Visual Preset #01" https://www.unrollnow.com/status/2072816831367176466 | "AI video style" | partly | 19 watercolor ink wash — dense black brush edges on volumetric scene |
| Vaporwave | Pastel pink-teal, grids, Greek bust, glitch sunsets | Morphic vaporwave | "aesthetic video edit" | yes | 32 synthwave / 45 marble — close; weak candidate |
| Voxel / Minecraft blocks | Scene rebuilt as untextured or pixel-textured cubes | Civitai (H3 voxel) ; Magic Hour Minecraft ; Morphic voxel-art | "restyle", Magic Hour | partly | 58 lego — grid cubes with no studs/gloss. Near-dup risk |
| PC-98 16-colour | Japanese 90s PC dithered palette | Civitai https://civitai.com/models/1619014 | "pixel" | yes | 11 pixel art dither — **near-dup**, skip |
| Chromatic aberration / RGB split / anaglyph | Colour channels offset with fringing, red-cyan 3D | Morphic chromatic-aberration ; Civitai anaglyph | "glitch edit" | yes | 05 datamosh / 27 signal relief — channel offset only. Thin on its own |
| Analog horror broadcast | EAS-style broadcast, wrong tape, text cards | Morphic found-footage-horror ; media.io analog-horror ; alici.ai | "analog horror" | yes | 02 VHS / 38 CCTV — **near-dup** |
| Indie sleaze flash party | Late-2000s harsh flash, blur, sweat, nightclub | Morphic indie-sleaze ; DomoAI ; promptkin | "indie sleaze" | yes | 04 Y2K digicam flash — **near-dup** |
| Newspaper / newsprint animation | Halftone grey newsprint with headline cut-ins | Morphic newspaper-animation | "collage edit" | yes | 01 / 07 — **near-dup** |
| Art Nouveau (Mucha) | Ornamental whiplash borders, muted gold-sage palette | Morphic art-nouveau | Morphic slugs | yes | 35 ukiyo-e / 60 floral gouache — decorative curved frame and flat tones |
| Art Deco gold geometry | Sunbursts, gold on black, symmetry | Morphic art-deco | Morphic slugs | yes | 46 1950s poster — metallic geometric ornament |
| Bauhaus / Soviet constructivist | Primary colours, diagonals, photomontage | Morphic bauhaus, soviet-animation | Morphic slugs | yes | 47 two-tone screen print — three-colour geometry vs two-tone |
| 1950s Technicolor three-strip | Saturated primaries, soft studio glow | Morphic 1950s-technicolor | Morphic slugs | yes | 54 teal-orange — different grade; mostly a LUT |
| Grindhouse film damage | Scratches, reel burns, missing frames | Morphic grindhouse | Morphic slugs | yes | 03 Super 8 / 28 silent film — **near-dup** |
| Tintype / sepia daguerreotype | Long-exposure plate, soft edges, sepia | Morphic sepia-vintage | Morphic slugs | yes | 28 silent film / 20 polaroid — still-plate look; weak |
| Aura-farming glow edit | Soft halo around subject, slow-mo, dark vignette, heroic | Captions "Kai" ; Higgsfield Katana https://x.com/EugenioFierro3/status/2109758438792180148 ; CapCut aura-farming template | "aura farming edit" | partly (glow yes; the slow-mo is timing) | 17 double exposure / 43 spotlight — soft halo grade, not an overlay |
| Dot-matrix / LED panel | Display matrix of lit dots | Morphic dot-matrix-animation | Morphic slugs | yes | 12 ASCII / 24 cobalt pixel halftone — **near-dup** |
| Chalk-on-blackboard | White chalk dust lines on slate | Captions "Chalk" | "AI Edit styles" | yes | 48 charcoal — white-on-slate chalk, not black-on-paper |
| Medieval manuscript / tapestry | Flat gold-leaf figures, no perspective | X https://x.com/davincisdigital/status/1906070835149832405 ; Morphic medieval-aesthetic | "midjourney video style" | yes | 35 ukiyo-e — gold leaf, flattened perspective |
| Ligne claire / Franco-Belgian | Uniform ink line, flat colour, no hatching | X @Artedeingenio sref 2793737906 | "midjourney sref" | yes | 53 90s comic / 07 pop-art — no halftone, no hatching |
| GTA loading-screen art | Thick outlines, airbrushed shading, poster composition | Civitai https://civitai.com/models/2031050 | "wan style" | yes | 53 90s comic book — airbrushed vector poster shading |
| Live2D parallax | Anime layers in 2.5D parallax | Civitai https://civitai.com/models/2144951 | "anime" | partly | 10 anime cel — depth-layered motion; needs layer split |
| Fairycore / angelcore soft glow | Dreamy diffusion, pastel lace | Morphic angelcore/fairycore ; Higgsfield SOUL Fairycore | "aesthetic edit" | yes | 17 double exposure — grade + bloom only. Overlaps dreamcore |
| Wes Anderson pastel symmetry | Centred framing, pastel palette | Kling 3.0 style list (Medium, Travis Nicholson) | "kling style prompt" | partly | 46 1950s poster — grade + composition; weak |
| Spaghetti Western | Dust, extreme close-ups, warm sepia | Civitai https://civitai.com/models/1326567 | "wan style" | yes | 03 / 28 — **near-dup** risk |
| Mid-century UPA flat animation | Angular flat shapes, textured paper | low evidence (Morphic art-era slugs) | Morphic slugs | yes | 46 / 52 — low evidence |

41 rows. 12 ★. About 9 are near-dups of taken styles and are flagged as such.

## Evidence notes (Reddit leads, for follow-up when Reddit is reachable)

- r/KLING "Kling Restyle Catalogue - 100+ options": https://www.reddit.com/r/KLING/comments/1mv3lyi/kling_restyle_catalogue_100_options/ (OP wanted the style list; ~20 on the image restyler).
- r/Kling_A_I KOLORS v2 restyle: https://www.reddit.com/r/Kling_A_I/comments/1k754v3/kling_kolors_v2_restyle_feature_image_reference/
- r/AfterEffects "Help me edit like this??" (kpop twitter edits): https://www.reddit.com/r/AfterEffects/comments/kltymi/help_me_edit_like_this/ ; BTS social edit https://www.reddit.com/r/AfterEffects/comments/1fxm507/bts_social_media_edit_from_latest_project/
- r/VideoEditingRequests X-style motion video: https://www.reddit.com/r/VideoEditingRequests/comments/1qdej3f/need_a_video_editor_for_this_exact_xstyle_motion/
- r/StableDiffusion: https://www.reddit.com/r/StableDiffusion/comments/1qp1vps/best_models_to_restyle_anime_scenes/ , https://www.reddit.com/r/StableDiffusion/comments/1sp03jq/editanything_iclora_ltx23/ , https://www.reddit.com/r/StableDiffusion/comments/1jalber/anime_with_wan_i2v_comparison_of_prompt_formats/

Late Reddit batch (background Exa run finished after the table was written: 24 queries, 13 hit 429, 11 returned threads). Leads only, not mined into candidates; all are mixed-media / painterly / era-transition how-to threads that map onto already-listed looks (collage, painterly 3D, rotoscope):
- https://www.reddit.com/r/AIVideoTrends/comments/1q687bt/how_to_create_era_transition_tiktok_trending_ai/
- https://www.reddit.com/r/AI_UGC_Marketing/comments/1vzkqgo/guide_to_making_ai_anime_videos_that_trend_on/
- https://www.reddit.com/r/AfterEffects/comments/1kapn0x/emulating_mixed_media_look_advice/
- https://www.reddit.com/r/AfterEffects/comments/12b2p2o/quick_mixed_media_loop_using_procreate_photoshop/
- https://www.reddit.com/r/AfterEffects/comments/15hj9bd/is_this_collage_animation/
- https://www.reddit.com/r/AfterEffects/comments/18gv11a/does_anyone_know_how_to_achieve_this_look_on/
- https://www.reddit.com/r/AfterEffects/comments/1u15qe6/looking_for_a_painterly_plugin_for_thesis_film/
- https://www.reddit.com/r/AfterEffects/comments/5xtg3q/name_for_the_technique_for_these_types_of/

## Observations

- AI-tool preset libraries converge on one core set (anime, clay, Lego, oil, watercolor, cyberpunk, vintage film, comic, pixel). Most of that is already taken. The 61-style library covers the mainstream.
- The new signal is in **Civitai video LoRAs** (felt, silhouette, OVA anime, drawing time-lapse, PS1/N64) and the **Morphic aesthetic taxonomy** (giallo, sand, rubber hose, kaleidoscope, pixel sort, dreamcore).
- X yields mostly recipes and sref codes for known looks, not new ones. Paper-cut and felt stop-motion recipes on X are the strongest cross-platform trend (OriSilver, vladdubchak_x, insMind, techhalla).
- Morphic pages are SEO landing pages, not a popularity measure. Civitai download counts (9k for retro OVA, 1.4k for felt) are the best demand signal I found.
