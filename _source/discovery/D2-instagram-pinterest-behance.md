# D2 — Instagram, Pinterest, Behance, Dribbble, Vimeo, Threads discovery

Research only. No style folders were created and nothing was rendered. Taken styles in `_source/STYLES_TAKEN.md` (61) were skipped.

## Result in short

- 49 distinct candidate looks (table below), 12 marked ★.
- About 540 queries and page loads across the platforms (details in "Keywords tried"). All 70 brief keywords were run on Pinterest and Behance; the multilingual variants were included (Indonesian, Chinese, Japanese, Korean, Spanish, Portuguese).
- Most generic edit-style keywords return how-to tutorials, templates, LUT packs and CapCut links, not new looks. The new looks came from searching for specific visual styles on Pinterest and Instagram topic pages, then confirming on Behance and Vimeo.
- 78 screenshots of the Pinterest, Behance and Dribbble result pages were taken during research. Only the 12 ★ ones are kept in `_source/discovery/shots/`.

## ★ Top 12

1. **Pixel Stretch (slit streak)** — `_source/discovery/shots/D2_pixel-stretch.png`
2. **Pixel Sort Glitch** — `_source/discovery/shots/D2_pixel-sort.png`
3. **Persona 5 Red-Black Cutout UI** — `_source/discovery/shots/D2_persona5-ui.png`
4. **GTA Loading-Screen Illustration** — `_source/discovery/shots/D2_gta-loading-art.png`
5. **Kaleidoscope Mirror** — `_source/discovery/shots/D2_kaleidoscope.png`
6. **PS1 Low-Poly Wobble** — `_source/discovery/shots/D2_ps1-lowres.png`
7. **Needle-Felted Wool** — `_source/discovery/shots/D2_needle-felt.png`
8. **American Traditional Tattoo Flash** — `_source/discovery/shots/D2_tattoo-flash.png`
9. **Tilt-Shift Miniature** — `_source/discovery/shots/D2_tilt-shift.png`
10. **Liquid Light Show (60s psychedelic)** — `_source/discovery/shots/D2_liquid-light-show.png`
11. **Topographic Contour Lines** — `_source/discovery/shots/D2_topographic-contour.png`
12. **Windows 95 Desktop UI** — `_source/discovery/shots/D2_win95-desktop.png`

## Candidates

| Style name | What it looks like (1 line) | Where seen (platform + 1–3 URLs) | Keyword that found it | Frame-by-frame doable? (yes/partly) | Closest taken style + why it's different |
|---|---|---|---|---|---|
| ★ Pixel Stretch (slit streak) | One row or column of pixels is smeared into long hard-edged colour streaks that trail behind a sharp subject, like a rubber-band of the frame. | https://www.pinterest.com/search/pins/?q=pixel%20stretch%20effect<br>https://www.instagram.com/popular/pixel-stretch-effect/ | pixel stretch effect | yes (per frame: extrude a single pixel line from the subject edge) | 26-slow-shutter-smear is a soft whole-frame motion ghost; this is hard-edged one-pixel-wide extrusion with the subject kept crisp. 05-datamosh is codec damage, not a clean streak. |
| ★ Pixel Sort Glitch | Pixels above a brightness threshold are sorted along rows or columns, so the image melts into smooth vertical or horizontal gradient streaks while the dark areas stay intact. | https://www.pinterest.com/search/pins/?q=pixel%20sorting%20glitch%20art<br>https://www.instagram.com/popular/pixel-sorting/<br>https://www.behance.net/search/projects?search=glitch%20art%20motion | pixel sorting | yes | 05-datamosh-glitch smears and blocks from compression errors; pixel sort is a deterministic luminance sort with clean gradient bands and no macroblocks. |
| ★ Persona 5 Red-Black Cutout UI | Jagged red, black and white cut-paper shards, slanted UI panels and ransom-note type slam over the footage on a crushed red-black grade. | https://www.pinterest.com/search/pins/?q=persona%205%20ui%20style<br>https://www.instagram.com/popular/persona-5-style/ | persona 5 style | partly (grade is easy; the UI shards and type must be regenerated per frame) | 31-sin-city-noir-red is photographic black and white with one red accent; 49-chaotic-red-ink is ink splatter. This is flat graphic UI geometry and typography, not ink or photo. |
| ★ GTA Loading-Screen Illustration | Flat-shaded digital illustration with thick black outlines, airbrushed hot-sunset gradients and orange/pink/teal skies, like a Rockstar loading screen. | https://www.pinterest.com/search/pins/?q=gta%20loading%20screen%20art%20style<br>https://www.instagram.com/popular/gta-vice-city-style/ | gta loading screen art style | yes | 46-1950s-editorial-poster and 30-spiderverse use print texture and halftone; this is clean vector-airbrush fills with a sunset palette and heavy outline. |
| Wes Anderson Pastel Symmetry | Dead-centre flat-on framing, pink/mint/mustard palette, soft matte grade, tidy graphic set dressing. | https://www.pinterest.com/search/pins/?q=wes%20anderson%20color%20palette%20symmetrical<br>https://www.instagram.com/popular/wes-anderson-style/ | wes anderson style | partly (palette and matte grade yes; composition cannot be changed in restyle) | 54-teal-orange-anamorphic is a cold/warm cinema grade; this is a pastel matte palette. Little overlap with 60-floral-maximalism. |
| CineStill Halation Night | Tungsten night street with a red halo bleeding around every light source, teal-green shadows and coarse 800 ISO grain. | https://www.pinterest.com/search/pins/?q=cinestill%20800t%20halation%20night<br>https://www.instagram.com/popular/cinestill-800t/ | cinestill 800t | yes | 55-cyberpunk-neon-city is stylised neon; 54-teal-orange is a clean grade. This is red halation glow plus grain on realistic night footage. |
| ★ Kaleidoscope Mirror | The frame is mirrored into 6 to 12 radial wedges so the footage becomes a symmetrical rotating mandala. | https://www.pinterest.com/search/pins/?q=kaleidoscope%20mirror%20effect<br>https://www.instagram.com/popular/kaleidoscope-effect/<br>https://www.behance.net/search/projects?search=kaleidoscope%20animation | kaleidoscope effect | yes | 44-broken-mirror-shards is irregular reflective glass; this is strict radial symmetry. 56-prismatic-dreamscape is colour refraction, not tiling. |
| ★ PS1 Low-Poly Wobble | Chunky 240p polygons with affine-warped textures, vertex jitter, 15-bit dithered colour and thick draw-distance fog. | https://www.pinterest.com/search/pins/?q=ps1%20graphics%20aesthetic<br>https://www.instagram.com/popular/ps1-aesthetic/ | ps1 graphics | partly (jitter and warp need temporal consistency) | 40-low-poly-3d is clean flat-shaded facets; 11-pixel-art-dither is 2D sprites. PS1 means warped low-res textures, wobble and fog. |
| Minecraft Voxel World | Everything rebuilt from cubic voxels with small pixel textures and blocky lighting. | https://www.pinterest.com/search/pins/?q=minecraft%20voxel%20style%20realistic%20render<br>https://www.instagram.com/popular/minecraft-style/ | minecraft style | yes | Near-duplicate risk with 58-lego-brick-build (studs, plastic gloss); voxel cubes use flat pixel textures with no studs. Low priority. |
| ★ Needle-Felted Wool | Everything looks sculpted from dyed wool: fuzzy fibre halo on every edge, soft rounded forms, macro tabletop lighting. | https://www.pinterest.com/search/pins/?q=needle%20felted%20wool%20animation<br>https://www.instagram.com/popular/needle-felting/<br>https://www.behance.net/search/projects?search=felt%20stop%20motion%20animation | needle felting | yes | 37-claymation-plasticine is smooth fingerprinted clay; 34-cross-stitch is flat thread. Felt is fibrous, fuzzy and furry on the silhouette. |
| Knitted Yarn Amigurumi | Subjects rebuilt from chunky knit or crochet stitches with visible yarn texture and soft toy proportions. | https://www.pinterest.com/search/pins/?q=knitted%20yarn%20crochet%20style<br>https://www.behance.net/search/projects?search=yarn%20knitted%20animation | knitted yarn crochet | yes | 34-cross-stitch-embroidery is flat 2D stitches; this is 3D stitched volume like a toy. |
| Matisse Paper Cut-outs | Flat organic algae and leaf shapes in 2 to 4 saturated gouache colours on white, scissor-cut edges, no texture or detail. | https://www.pinterest.com/search/pins/?q=matisse%20cut%20outs%20style<br>https://www.behance.net/search/projects?search=matisse%20cutout%20animation | matisse cutout animation | yes | 60-floral-maximalism-gouache is dense and ornate; 08-scrapbook-sticker-collage is layered photo scraps. This is minimal flat cut shapes. |
| ★ American Traditional Tattoo Flash | Bold black outlines, limited red/yellow/green/blue palette, whip shading, subjects redrawn as flash sheet motifs on aged cream paper. | https://www.pinterest.com/search/pins/?q=american%20traditional%20tattoo%20flash<br>https://www.instagram.com/popular/american-traditional-tattoo/<br>https://www.behance.net/search/projects?search=tattoo%20flash%20animation | american traditional tattoo | yes | 36-spray-stencil-graffiti and 35-ukiyoe are different line languages; 07-pop-art uses halftone. Flash has its own motif vocabulary and shading. |
| Chalkboard Animation | White and pastel chalk lines with dust smudges and erased ghosts on a dark green or black board. | https://www.pinterest.com/search/pins/?q=chalk%20drawing%20blackboard%20animation<br>https://www.instagram.com/popular/chalkboard-animation/<br>https://www.behance.net/search/projects?search=chalk%20animation | chalkboard animation | yes | 48-charcoal-expressionism is heavy black smudge on paper; this is bright chalk on a dark board with erase trails. |
| Crayon / Oil-Pastel Child Drawing | Waxy crayon strokes with paper tooth, naive proportions and sun-in-the-corner colour fields. | https://www.pinterest.com/search/pins/?q=crayon%20oil%20pastel%20child%20drawing<br>https://www.instagram.com/popular/crayon-drawing/<br>https://dribbble.com/search/crayon-animation | crayon drawing | yes | 61-colored-marker-sketch is clean marker line; 23-boogley-doodle is doodle creatures. Crayon has waxy grain and filled colour areas. |
| Linocut Block Print | Gouged carving marks, two or three flat ink colours, rough registration and uneven ink coverage. | https://www.pinterest.com/search/pins/?q=linocut%20block%20print<br>https://www.behance.net/search/projects?search=linocut%20animation | linocut | yes | 35-ukiyoe-woodblock and 47-two-tone-screen-print are close. Differs by visible gouge marks and ink starvation. Low priority. |
| Banknote Engraving Crosshatch | Tone built only from fine parallel and curved burin lines, currency-green or sepia monochrome, guilloche borders. | https://www.pinterest.com/search/pins/?q=engraving%20crosshatch%20banknote<br>https://www.instagram.com/popular/engraving-style/ | engraving style | yes | 18-pencil-sketch-rotoscope is loose graphite; engraving is rigid line-field shading with flowing contour lines. |
| Anaglyph Red-Cyan 3D | Left and right views tinted red and cyan, offset by depth so near objects fringe strongly. | https://www.pinterest.com/search/pins/?q=anaglyph%203d%20red%20cyan | anaglyph 3d | yes (needs depth map for parallax) | 30-spiderverse-comic-offset is a flat CMY misregistration; anaglyph offsets by depth. Near 27-signal-relief. |
| ★ Tilt-Shift Miniature | A thin sharp band with strong blur above and below plus oversaturation makes real scenes look like a tiny toy model. | https://www.pinterest.com/search/pins/?q=tilt%20shift%20miniature<br>https://www.instagram.com/popular/tilt-shift/ | tilt shift | yes | None of the 61 is an optical depth trick; 58-lego and 37-claymation rebuild materials, this keeps the real footage and changes focus plane and scale cue. |
| Inflatable Balloon Puffy 3D | Subjects become glossy air-filled balloon or mylar forms with soft creases and pinched seams. | https://www.pinterest.com/search/pins/?q=inflatable%20balloon%20puffy%203d<br>https://www.behance.net/search/projects?search=inflatable%203d%20animation | inflatable 3d | yes | 59-3d-kawaii-chibi is character proportions; 41-holographic is foil card. Inflatable is a material treatment on any shape. |
| Arcane 2.5D Painterly | Brush-textured 3D surfaces with angular shapes, hatched shading and neon rim light. | https://www.instagram.com/popular/arcane-style/ | arcane style | partly | 51-ghibli and 50-impasto are traditional paint; Arcane keeps 3D volume with painted texture. Evidence thin: the Pinterest page rendered blank logged-out. |
| Construction-Paper Cut-out Puppets | Flat jointed paper puppets with hard drop shadows and stiff motion, solid colours. | https://www.pinterest.com/search/pins/?q=paper%20cutout%20animation%20south%20park%20style<br>https://www.behance.net/search/projects?search=paper%20cutout%20animation | paper cutout | yes | 08-scrapbook-sticker-collage is layered photo scraps; this is flat puppet-style cutouts with joints. |
| 1930s Rubber-Hose Cartoon | Tube limbs, pie-cut eyes, ink-black outline and cream paper grain, like Cuphead or early Fleischer cartoons. | https://www.pinterest.com/search/pins/?q=rubber%20hose%20cartoon%201930s%20cuphead<br>https://www.instagram.com/popular/rubber-hose-animation/ | rubber hose animation | partly (needs character redraw) | 52-retro-90s-cartoon is colour TV cartoon; 28-hand-cranked-silent-film is film damage. Rubber hose is the character style. |
| ★ Liquid Light Show (60s psychedelic) | Backlit coloured oil and ink blobs spread, bubble and blend like overhead-projector concert visuals. | https://www.pinterest.com/search/pins/?q=liquid%20light%20show%20psychedelic%2060s<br>https://www.instagram.com/popular/liquid-light-show/<br>https://www.behance.net/search/projects?search=liquid%20light%20show%20animation | liquid light show | yes | 56-prismatic-dreamscape is refraction; 17-double-exposure is overlay. This has circular blobs of oil with bright transparent rims. |
| Marbled Ink Swirl (Ebru) | Combed swirling ink veins in layered colours on a water-surface look. | https://www.pinterest.com/search/pins/?q=marbled%20paper%20ebru%20ink<br>https://www.instagram.com/popular/marbling-effect/ | marbling effect | yes | 19-watercolor-ink-wash is soft wash; marbling is combed vein patterns. Low priority. |
| ★ Topographic Contour Lines | Brightness becomes elevation: thin closed isolines in a single ink colour on map paper, so the footage turns into a terrain map. | https://www.pinterest.com/search/pins/?q=topographic%20contour%20lines%20art<br>https://www.instagram.com/popular/topographic-lines/ | topographic lines | yes | 39-lidar-point-cloud is points; 27-signal-relief is scanline displacement. Contour lines are closed isolines. |
| Art Nouveau Mucha Poster | Flowing organic outlines, circular halo, ornate floral border and muted ochre-olive palette. | https://www.pinterest.com/search/pins/?q=art%20nouveau%20mucha%20poster | art nouveau | yes | 46-1950s-editorial-poster is modernist; 21-stained-glass is leaded cells. Nouveau is ornament and whiplash line. |
| Soviet Constructivist Poster | Diagonal red-black-cream shapes, photomontage cutouts and bold sans type. | https://www.pinterest.com/search/pins/?q=constructivist%20poster%20soviet | constructivism | partly | Near 47-two-tone-screen-print, 31 and 49 in colour; layout and photomontage are the difference. Low priority. |
| Op Art Optical Illusion | Footage luminance drives black-and-white warped stripe or checker fields that seem to vibrate. | https://www.pinterest.com/search/pins/?q=op%20art%20optical%20illusion | op art | yes | 07-pop-art is halftone dots; op art is warped line fields that create motion illusion. |
| LED Dot-Matrix Display | Footage shown as glowing round LED dots on a black grid, amber or RGB. | https://www.pinterest.com/search/pins/?q=led%20dot%20matrix%20display<br>https://www.behance.net/search/projects?search=led%20dot%20matrix%20animation | led display | yes | 24-cobalt-pixel-halftone and 11-pixel-art-dither are close; LED adds glow bleed and dark gaps. Low priority. |
| City Pop Illustration | Flat pastel anime-poster illustration of palms, wide skies and neon city nights with a coloured outline. | https://www.pinterest.com/search/pins/?q=city%20pop%20illustration<br>https://www.instagram.com/popular/city-pop/ | city pop | yes | 32-synthwave-outrun is neon grid sunsets; city pop is bright daytime pastel flat illustration. |
| Kodachrome Slide | Warm saturated reds and cyans, fine grain, white slide-mount border. | https://www.pinterest.com/search/pins/?q=kodachrome%20slide%20film%20look<br>https://www.instagram.com/popular/kodachrome/ | kodachrome | yes | 03-super8-film-burn is burn and damage; Kodachrome is the clean 1950s to 1970s slide colour. |
| Tintype Wet-Plate | Metallic grey collodion tone, very shallow focus, scratched and uneven plate edges. | https://www.pinterest.com/search/pins/?q=tintype%20portrait%20wet%20plate<br>https://www.instagram.com/popular/tintype/ | tintype | yes | 28-hand-cranked-silent-film is moving film flicker; tintype is a single-plate chemical look. |
| Three-Strip Technicolor | Hyper-saturated primaries with cyan-magenta-yellow cast and painted-set glow. | https://www.pinterest.com/search/pins/?q=technicolor%20three%20strip%20film%20still | technicolor | yes | 54-teal-orange is modern cinema grade; this is 1940s primary colour palette. |
| X-Ray Skeleton | Black translucent body with white bones and blue glow, like a radiograph. | https://www.pinterest.com/search/pins/?q=x-ray%20skeleton%20effect<br>https://www.behance.net/search/projects?search=runway%20restyle | x-ray skeleton; runway restyle (Behance project "Day 8: Restyle video into Xray") | partly (needs body segmentation) | 16-thermal-camera maps heat colours; x-ray inverts to bone structure. |
| Kirlian Aura | Electrical corona glow around the subject outline on black, blue-magenta streamers. | https://www.pinterest.com/search/pins/?q=kirlian%20aura%20photography<br>https://www.instagram.com/popular/kirlian-photography/ | kirlian photography | yes | 13-neon-scribble-outline is drawn lines; Kirlian is a branching discharge halo. |
| Dreamcore Pastel Surreal | Soft-focus clouds, empty doorways, floating eyes and pastel sky gradients with low-fi glow. | https://www.pinterest.com/search/pins/?q=dreamcore%20aesthetic<br>https://www.instagram.com/popular/dreamcore-aesthetic/ | dreamcore | partly | Near 17-double-exposure-dreamy and 57-surrealist-dali-magritte; dreamcore adds low-fi pastel haze and liminal doorways. Low priority. |
| Liminal Backrooms Fluorescent | Empty corridors under flat fluorescent light in one dominant yellow or green cast, uncanny stillness. | https://www.pinterest.com/search/pins/?q=liminal%20space%20backrooms%20fluorescent<br>https://www.instagram.com/popular/liminal-space/ | liminal space | yes | 38-cctv-night-vision is monochrome green surveillance; 02-vhs is tape noise. Backrooms is single-hue light and architecture. |
| ★ Windows 95 Desktop UI | Beveled grey window chrome, teal desktop, pixel icons and error dialogs framing the footage in 256 colours. | https://www.pinterest.com/search/pins/?q=windows%2095%20desktop%20aesthetic<br>https://www.instagram.com/popular/windows-95-aesthetic/ | windows 95 desktop | partly (overlay chrome per frame, colour quantise) | 12-ascii-terminal is text-mode; 15-y2k-chrome-frutiger-aero is glossy glass. Win95 is flat grey bevel and 256-colour palette. |
| Illuminated Manuscript | Gold-leaf initials, lapis and vermilion pigment, parchment texture and ornamental borders. | https://www.pinterest.com/search/pins/?q=illuminated%20manuscript%20medieval | illuminated manuscript | yes | 21-stained-glass-mosaic uses leaded cells; manuscript uses gilded flat figures and border ornament. |
| Greek Black-Figure Vase | Black silhouettes with incised detail on terracotta orange, banded frieze composition. | https://www.pinterest.com/search/pins/?q=greek%20black%20figure%20vase%20painting | greek vase painting | yes | 35-ukiyoe-woodblock has colour outlines; vase painting is two-colour silhouette with incised lines. |
| Memphis Design 80s | Squiggles, confetti and geometric shapes in pastel and black over footage. | https://www.pinterest.com/search/pins/?q=memphis%20design%2080s%20pattern | memphis design | partly (pattern overlay) | 08-scrapbook-sticker-collage is photo scraps; Memphis is abstract geometric pattern graphics. |
| Bleach Bypass | Desaturated, crushed contrast with silvery highlights and gritty texture. | https://www.pinterest.com/search/pins/?q=bleach%20bypass%20film%20look | bleach bypass | yes | 54-teal-orange is saturated; bleach bypass is the opposite, low colour and high contrast. |
| VX1000 Fisheye Skate Video | Extreme fisheye barrel distortion, low-angle follow camera, mini-DV softness and punchy contrast. | https://www.pinterest.com/search/pins/?q=vx1000%20fisheye%20skate%20video | vx1000 fisheye | partly (lens distortion per frame) | 02-vhs-camcorder and 04-y2k-digicam are tape and flash; this is wide fisheye geometry. |
| Tarot Card Illustration | Footage framed as ornate tarot card with numeral, title banner and flat symbolic palette. | https://www.pinterest.com/search/pins/?q=tarot%20card%20art%20illustration | tarot card | yes | 41-holographic-trading-card is foil game card; tarot is mystical illustration and border. |
| Blister-Pack Action Figure | Subject sealed in clear plastic bubble on printed cardboard backing with logo and accessories. | https://www.pinterest.com/search/pins/?q=action%20figure%20blister%20pack | blister pack | partly | 41-holographic-trading-card is also packaging but flat; blister pack is 3D bubble and backing. |
| Rain on Window Bokeh | Footage seen through beaded raindrops on glass with blurred city light bokeh. | https://www.pinterest.com/search/pins/?q=rain%20on%20window%20droplets%20bokeh | rain on window | yes | 22-glass-invisibility-cloak is refractive distortion of a subject; this is droplets with bokeh. |
| Cardboard Diorama | Layered corrugated cardboard sets with visible flute edges and tape. | https://www.pinterest.com/search/pins/?q=cardboard%20craft%20diorama<br>https://www.behance.net/search/projects?search=cardboard%20stop%20motion | cardboard stop motion | yes | 08-scrapbook and 37-claymation are other crafts; cardboard has corrugated edges and layered relief. |
| Origami Paper Fold | Subjects folded from creased flat sheets with faceted shading. | https://www.pinterest.com/search/pins/?q=origami%20paper%20fold%20animation | origami | yes | 40-low-poly-3d is smooth facets; origami has crease lines, paper thickness and fold shading. |

### Looked at and rejected as near-duplicates or not a look

- Vaporwave and Tron neon grid: near 32-synthwave-outrun and 55-cyberpunk-neon-city.
- Japan photo collage and K-pop mixed-media collage: near 01-punk-photocopy-collage and 08-scrapbook-sticker-collage.
- Pixar-style 3D render: near 59-3d-kawaii-chibi.
- Datamosh, rotoscope sketch, Y2K digicam, VHS, risograph, halftone, anime cel: already taken (05, 18, 04, 02, 06, 07, 10).
- VOX-style documentary (many Behance hits for "video style editing"): an editing format with maps and archive footage, not a texture or medium.
- Velocity ramps, beat cuts, transition packs, CapCut templates: timing tricks, excluded by the brief.

## Keywords tried

Counts: Pinterest "pins rendered" is the number of pin images found on the logged-out results page (about 10 to 45 is a normal full page). Behance count is the result count Behance printed. Instagram "reels" is the total Instagram showed on the topic page.

### Vimeo / Staff Picks — WebSearch (Vimeo blocks the built-in browser; 8 queries)

| Query | Result |
|---|---|
| vimeo staff pick rotoscope (ford. "In My Eyes") | found: rotoscope Staff Pick, but near taken 18-pencil-sketch-rotoscope |
| vimeo staff pick knitted stop-motion (Visible Mending) | found: knitted stop-motion Staff Pick, supports Knitted Yarn Amigurumi |
| vimeo paper-cut-out music video | found: several, supports Construction-Paper Cut-out Puppets |
| vimeo analog glitch visuals / film collage | found: glitch and collage videos, nothing new |
| vimeo staff pick needle felted stop motion short film | found: Andrea Love needle-felted music video https://vimeo.com/640419758 and course https://vimeo.com/816152344 (supports Needle-Felted Wool) |
| vimeo staff pick pixel sorting datamosh music video | found: https://vimeo.com/227273336 (pixel-sort code), https://vimeo.com/3139412 (datamosh-style); no confirmed Staff Pick |
| vimeo staff pick kaleidoscope liquid light show psychedelic music video | found: https://vimeo.com/235299071 (liquid light show ink tests), https://vimeo.com/274383145 (liquid music video), https://vimeo.com/850736526 (kaleidoscope, Staff Pick credit); supports Liquid Light Show and Kaleidoscope Mirror |
| vimeo staff pick tilt shift miniature timelapse | found: https://vimeo.com/174392521, https://vimeo.com/152834042, channel https://vimeo.com/channels/293484 (supports Tilt-Shift Miniature) |

### Instagram — Exa `site:instagram.com` queries (36)

| Query | Hits |
|---|---|
| site:instagram.com mixed media edit style reel | 8 |
| site:instagram.com collage edit capcut template reel | 8 |
| site:instagram.com aesthetic video edit style trending | 8 |
| site:instagram.com trending edit style viral reel effect | 8 |
| site:instagram.com after effects style look tutorial reel | 8 |
| site:instagram.com premiere pro look LUT film look reel | 8 |
| site:instagram.com AI video style filter reel kling | 8 |
| site:instagram.com higgsfield effect reel | 8 |
| site:instagram.com pika effects reel | 8 |
| site:instagram.com runway restyle video to video | 8 |
| site:instagram.com midjourney video style prompt reel | 8 |
| site:instagram.com seedream video prompt | 8 |
| site:instagram.com rotoscope edit reel | 8 |
| site:instagram.com frame by frame animation edit reel | 8 |
| site:instagram.com texture overlay edit reel | 8 |
| site:instagram.com music video look edit style reel | 8 |
| site:instagram.com fashion film edit style reel | 8 |
| site:instagram.com dreamcore weirdcore edit reel | 8 |
| site:instagram.com liminal edit reel | 8 |
| site:instagram.com analog horror found footage look reel | 8 |
| site:instagram.com lo-fi edit reel | 8 |
| site:instagram.com indie sleaze edit reel | 8 |
| site:instagram.com y2k edit reel capcut | 8 |
| site:instagram.com grunge edit reel | 8 |
| site:instagram.com cyber edit reel | 8 |
| site:instagram.com anime edit AMV style reel | 8 |
| site:instagram.com glitch edit reel | 8 |
| site:instagram.com psychedelic trippy edit reel | 8 |
| site:instagram.com experimental video art reel | 8 |
| site:instagram.com motion design style reel | 8 |
| site:instagram.com instagram reel effect trend filter | 8 |
| site:instagram.com edit inspo style | 8 |
| site:instagram.com style transfer video AI | 8 |
| site:instagram.com stop motion edit reel | 8 |
| site:instagram.com vintage retro edit reel | 8 |
| site:instagram.com cinematic look color grade reel | 8 |

### Other Exa queries on Instagram, Pinterest, Behance, Threads (120)

| Query | Hits |
|---|---|
| site:pinterest.com video edit aesthetic | 8 |
| site:pinterest.com motion design style | 8 |
| site:pinterest.com video style editing | 8 |
| site:pinterest.com aesthetic video edit style | 8 |
| site:pinterest.com capcut edit style | 8 |
| site:pinterest.com after effects style | 8 |
| site:pinterest.com AI video style | 8 |
| site:pinterest.com frame by frame animation | 8 |
| site:pinterest.com rotoscope | 8 |
| site:pinterest.com mixed media collage video | 8 |
| site:pinterest.com paper cutout stop motion | 8 |
| site:pinterest.com texture overlay video | 8 |
| site:pinterest.com music video aesthetic still | 8 |
| site:pinterest.com fashion film aesthetic | 8 |
| site:pinterest.com film look cinematic aesthetic | 8 |
| site:pinterest.com retro vintage edit aesthetic | 8 |
| site:pinterest.com y2k edit aesthetic | 8 |
| site:pinterest.com grunge edit aesthetic | 8 |
| site:pinterest.com dreamcore weirdcore aesthetic | 8 |
| site:pinterest.com liminal aesthetic | 8 |
| site:pinterest.com analog horror aesthetic | 8 |
| site:pinterest.com found footage look | 8 |
| site:pinterest.com lo-fi aesthetic video | 8 |
| site:pinterest.com indie sleaze aesthetic | 8 |
| site:pinterest.com cyber aesthetic edit | 8 |
| site:pinterest.com anime edit aesthetic | 8 |
| site:pinterest.com glitch aesthetic | 8 |
| site:pinterest.com psychedelic trippy aesthetic | 8 |
| site:pinterest.com experimental video art | 8 |
| site:pinterest.com video effect ideas | 8 |
| site:pinterest.com edit inspo | 8 |
| site:pinterest.com style transfer | 8 |
| site:behance.net motion design style frames music video | 8 |
| site:behance.net AI video style transfer | 8 |
| site:behance.net mixed media animation | 8 |
| site:behance.net stop motion paper cutout | 8 |
| site:behance.net rotoscope animation | 8 |
| site:behance.net frame by frame animation | 8 |
| site:behance.net experimental video art | 8 |
| site:behance.net music video visual look | 8 |
| site:behance.net fashion film | 8 |
| site:behance.net texture overlay motion | 8 |
| site:behance.net glitch aesthetic motion | 8 |
| site:behance.net analog lo-fi video | 8 |
| site:behance.net psychedelic motion | 8 |
| site:dribbble.com motion design style | 8 |
| site:dribbble.com mixed media animation | 8 |
| site:dribbble.com frame by frame animation | 8 |
| site:dribbble.com glitch texture motion | 8 |
| site:dribbble.com stop motion | 8 |
| site:dribbble.com AI video style | 8 |
| site:dribbble.com music video visual | 8 |
| site:vimeo.com staff picks music video | 8 |
| site:vimeo.com staff picks experimental animation | 8 |
| site:vimeo.com staff picks mixed media | 8 |
| site:vimeo.com staff picks stop motion | 8 |
| site:vimeo.com staff picks rotoscope | 8 |
| site:vimeo.com staff picks fashion film | 8 |
| site:vimeo.com staff picks analog texture | 8 |
| site:vimeo.com motion design style frames | 8 |
| site:threads.com video style editing | 8 |
| site:threads.net video style editing | 8 |
| site:threads.com AI video style prompt | 8 |
| site:threads.net AI video restyle | 8 |
| site:threads.net edit style trend | 8 |
| site:threads.net aesthetic video edit | 8 |
| site:threads.net kling style prompt | 8 |
| site:threads.net seedream video prompt | 8 |
| site:threads.net higgsfield effect | 8 |
| site:threads.net capcut template trend | 8 |
| site:threads.net mixed media edit | 8 |
| site:threads.net rotoscope | 8 |
| site:threads.net frame by frame animation | 8 |
| site:threads.net motion design style | 8 |
| site:threads.net music video look | 8 |
| site:threads.net cinematic look | 8 |
| site:threads.net glitch edit | 8 |
| site:threads.net retro edit | 8 |
| site:threads.net AI filter trend | 8 |
| site:threads.net instagram reel effect | 8 |
| site:instagram.com pixel stretch effect edit | 8 |
| site:instagram.com skull x-ray effect edit capcut | 8 |
| site:instagram.com windows xp desktop edit aesthetic reel | 8 |
| site:instagram.com GTA loading screen art style AI video | 8 |
| site:instagram.com persona 5 style edit | 8 |
| site:instagram.com wes anderson style video AI prompt | 8 |
| site:instagram.com cinestill 800T halation film look | 8 |
| site:instagram.com kaleidoscope mirror edit effect | 8 |
| site:instagram.com ps1 graphics aesthetic edit | 8 |
| site:instagram.com minecraft voxel style AI video | 8 |
| site:instagram.com needle felted wool animation AI video | 8 |
| site:instagram.com knitted crochet yarn style AI video | 8 |
| site:instagram.com matisse paper cutout AI video style | 8 |
| site:instagram.com tattoo flash american traditional style video AI | 8 |
| site:instagram.com chalkboard chalk drawing animation effect | 8 |
| site:instagram.com crayon children drawing animation effect video | 8 |
| site:instagram.com linocut woodcut style video | 8 |
| site:instagram.com engraving hatching etching style AI video | 8 |
| site:instagram.com anaglyph 3D red cyan edit | 8 |
| site:instagram.com tilt shift miniature effect video | 8 |
| site:instagram.com inflatable balloon puffy 3D AI video effect | 8 |
| site:instagram.com arcane painterly style AI video | 8 |
| site:instagram.com pixar style AI video | 8 |
| site:instagram.com south park cutout style animation filter | 8 |
| site:instagram.com rubber hose cuphead style animation AI | 8 |
| site:instagram.com liquid light show psychedelic 60s edit | 8 |
| site:instagram.com marbling ink paper effect video | 8 |
| site:instagram.com topographic contour line video effect | nothing |
| site:instagram.com art nouveau mucha style AI video | 8 |
| site:instagram.com constructivist soviet poster style video | 8 |
| site:instagram.com op art optical illusion video edit | 8 |
| site:instagram.com LED dot matrix display effect video | 8 |
| site:instagram.com city pop illustration style AI video | 8 |
| site:instagram.com kodachrome slide film look video | 8 |
| site:instagram.com tintype daguerreotype vintage look video filter | 8 |
| site:instagram.com technicolor 1950s look video | 8 |
| site:instagram.com bleach bypass film look | 8 |
| site:instagram.com kirlian aura photography effect edit | 8 |
| site:instagram.com gaussian splat dreamy edit | 8 |
| site:instagram.com dark academia painterly video aesthetic | 8 |

### Instagram — public `/popular/<slug>/` hashtag/topic pages via Jina reader (117 tried, 73 found, 44 unavailable)

| Slug (https://www.instagram.com/popular/SLUG/) | Result |
|---|---|
| aesthetic-edit | 18M reels |
| aesthetic-video-edit | 69K reels |
| ai-filter-trend | 30K reels |
| ai-video-filter | page found (no total shown) |
| ai-video-style | page found (no total shown) |
| american-traditional-tattoo | 3.2M reels |
| analog-horror-edit | 2.4K reels |
| arcane-style | 39K reels |
| art-nouveau | 10M reels |
| bleach-bypass | 76K reels |
| capcut-template | 1.6M reels |
| chalkboard-animation | page found (no total shown) |
| cinematic-look | 2.4M reels |
| cinestill-800t | 3.2M reels |
| city-pop | 2.5M reels |
| collage-edit | 94K reels |
| constructivism | 1.2M reels |
| crayon-drawing | 420K reels |
| crochet-style | 872K reels |
| cyberpunk-aesthetic | 1.7M reels |
| dreamcore-aesthetic | 1M reels |
| dreamcore | 6.6M reels |
| edit-inspo | 147K reels |
| engraving-style | 24K reels |
| film-look | 2.8M reels |
| frame-by-frame-animation | 304K reels |
| frame-by-frame-edit | page found (no total shown) |
| glitch-edit | 442K reels |
| grunge-aesthetic | 25M reels |
| grunge-edit | 769K reels |
| gta-vice-city-style | page found (no total shown) |
| instagram-reel-effect | page found (no total shown) |
| kaleidoscope-effect | page found (no total shown) |
| kirlian-photography | 23K reels |
| kodachrome | 1.1M reels |
| led-display | 3.6M reels |
| liminal-space | 4.6M reels |
| liquid-light-show | 166K reels |
| lut-look | page found (no total shown) |
| marbling-effect | page found (no total shown) |
| minecraft-style | page found (no total shown) |
| mixed-media-edit | 3.6K reels |
| needle-felting | 8.7M reels |
| op-art | 2.9M reels |
| overlay-edit | 58K reels |
| paper-cutout-edit | page found (no total shown) |
| persona-5-style | page found (no total shown) |
| phonk-edit | 294K reels |
| pika-effect | page found (no total shown) |
| pixel-sorting | 673K reels |
| pixel-stretch-effect | 2.3K reels |
| ps1-aesthetic | page found (no total shown) |
| ps1-graphics | 33K reels |
| psychedelic-edit | 5K reels |
| retro-edit | 481K reels |
| rotoscope-edit | page found (no total shown) |
| rubber-hose-animation | page found (no total shown) |
| south-park-style | 132K reels |
| stop-motion-edit | 1.6K reels |
| technicolor | 1M reels |
| tiktok-filter-trend | page found (no total shown) |
| tilt-shift | 2.5M reels |
| tintype | 1.3M reels |
| topographic-lines | page found (no total shown) |
| video-editing-style | 500+ reels |
| vintage-edit | 541K reels |
| vox-style | 350+ reels |
| weirdcore-aesthetic | 1.2M reels |
| weirdcore | 7.3M reels |
| wes-anderson-style | 588K reels |
| windows-95-aesthetic | page found (no total shown) |
| y2k-aesthetic | 11M reels |
| y2k-edit | 129K reels |
| after-effects-style | nothing (page not served) |
| ai-restyle-video | nothing (page not served) |
| amv-style | nothing (page not served) |
| anaglyph-3d | nothing (page not served) |
| analog-horror | nothing (page not served) |
| anime-edit | nothing (page not served) |
| backrooms | nothing (page not served) |
| capcut-edit-style | nothing (page not served) |
| cyber-edit | nothing (page not served) |
| edit-style | nothing (page not served) |
| editing-styles-tutorial | nothing (page not served) |
| experimental-video-art | nothing (page not served) |
| fashion-film-edit | nothing (page not served) |
| found-footage-look | nothing (page not served) |
| found-footage | nothing (page not served) |
| gta-style-art | nothing (page not served) |
| higgsfield-effect | nothing (page not served) |
| indie-sleaze-edit | nothing (page not served) |
| indie-sleaze | nothing (page not served) |
| inflatable-3d | nothing (page not served) |
| japan-collage | nothing (page not served) |
| kling-style-prompt | nothing (page not served) |
| liminal-edit | nothing (page not served) |
| linocut | nothing (page not served) |
| lo-fi-edit | nothing (page not served) |
| matisse-cutouts | nothing (page not served) |
| midjourney-video-style | nothing (page not served) |
| motion-design-style | nothing (page not served) |
| music-video-edit-style | nothing (page not served) |
| music-video-look | nothing (page not served) |
| paper-ink-animation | nothing (page not served) |
| pixar-style | nothing (page not served) |
| premiere-look | nothing (page not served) |
| runway-restyle | nothing (page not served) |
| seedream-video-prompt | nothing (page not served) |
| skull-x-ray-effect | nothing (page not served) |
| style-transfer-video | nothing (page not served) |
| texture-overlay-edit | nothing (page not served) |
| trending-edit-style | nothing (page not served) |
| trippy-edit | nothing (page not served) |
| video-style-editing | nothing (page not served) |
| video-to-video-style | nothing (page not served) |
| viral-edit-style | nothing (page not served) |
| windows-xp-edit | nothing (page not served) |

### Pinterest — brief keywords, logged-out search (70)

| Keyword | Pins rendered | Related-search chips seen (sample) |
|---|---|---|
| video style editing | 34 | Harry, Egirl, Hair, Life, Styling, Street, Game art, Luxury lifestyle 4k |
| video editing style | 25 | Minimal, Professional, Talking head, Minimalist, Different, Types of, Viral, Trendy |
| edit style | 41 | Gacha, Photo, Photography, Video, Gacha life, Vox, Wedding photo, Minimal |
| editing styles tutorial | 21 | Gacha, Gacha life, Candy, Photo, Capcut, Alight motion candy, Alight motion, Tiktok |
| aesthetic edit | 41 | Video, Photo, Remix collage, Template, Jennie, Blackpink, Video template, Eyes videos |
| aesthetic video edit | 37 | Nature, Reels instagram, Study motivation, Father and daughter, Eye contact, Eye contact couple, Virat kohli, Shiv ji |
| trending edit style | 42 | Gacha, Harry, Editing, Candy, Video editing, Gacha life editing, Vox editing, Overlays |
| viral edit style | 16 | Video editing, Reel, Tech |
| capcut edit style | 14 | Tutorial, Candy, Tiktok |
| capcut template | 39 | Video aesthetic, Link aesthetic, Best, Qr code, Video, Trend ical, Video aesthetic link, Trending thailand |
| after effects style | 18 | Frame, Iphone ios 16 depth, Text, Animation after, Simple but effective harry, Documentary, Font, Tattoo 3d |
| premiere look | 23 | Zendaya odyssey, Movie, 90s, Zendaya movie, Margot robbie, Zendaya, Vintage movie, Odyssey |
| LUT look | 44 | Kavmi, Cinematic, Ideas easy, Cercei din, Polimeric idei, Polimeric, Gaye song, Modele din |
| AI video style | 12 | — |
| AI video filter | 10 | — |
| AI restyle video | 9 | — |
| video to video style | 33 | Harry, Egirl, Hair, Life, Editing, Street, Game art, Luxury lifestyle 4k |
| frame by frame edit | 44 | Aesthetic, Aesthetic template, Photo, Happy birthday photo, Overlay, Editing ideas, Video, Aesthetic template wallpaper |
| frame by frame animation edit | 16 | — |
| rotoscope edit | 15 | — |
| mixed media edit | 29 | Overlay, Tutorial, Background, Png, Kpop, Digital, Stickers, Video |
| collage edit | 40 | Remix, Aesthetic, Photo, Birthday, Kpop, Template, Y2k, Video |
| paper cutout edit | 18 | Photo, Video |
| stop motion edit | 30 | Tutorial, Alight, Graphics, Graphics video, Qr code alight, Video editing, Graphics ideas, Template video |
| overlay edit | 44 | Video, Png, Line, Pink, Ship, Black, Black and white, Yumeship |
| texture overlay edit | 19 | Paper, Film, Video, Overlays for, Screen, Skin |
| music video look | 30 | Ariana grande, Iconic, Lady gaga, Beyonce, Megan thee stallion, Sabrina carpenter, Rihanna, Taylor swift |
| music video edit style | 12 | — |
| fashion film edit | 12 | — |
| film look | 41 | Color grading, Photography, Vintage, Aesthetic, 35mm, Analog, Cinematic, Dreamy |
| cinematic look | 22 | Film, Color grading, Photography, Orange and teal, Photo, Capcut, Dark, Retro |
| retro edit | 29 | Heisei, Photo, Iphone, Overlay, Kpop, Style, Inspo, Lightroom |
| vintage edit | 41 | Iphone, Photos, Lightroom, Aesthetic, Overlay, Rp, Snapseed, Inspo |
| y2k edit | 43 | Photos, Background, Overlay, Template, Kpop, Video, Inspo, Tutorial |
| grunge edit | 30 | Photo, Overlay, Style, Kpop, Y2k, Video, Inspo, Tutorial |
| dreamcore | 43 | Aesthetic, Wallpaper, Background, Oc, Outfits, Pfp, Illit, Icons |
| weirdcore | 42 | Dreamcore, Aesthetic, Oc, Outfits, Pfp, Wallpaper, Art, Makeup |
| liminal edit | 19 | Espaço, Space, Space photo, Photo, Gacha, Space video, Core, Space aesthetic nostalgia |
| analog horror edit | 15 | Columbina, Kpop, Tutorial, Wolf, Big bad wolf, Jurassic park, Hansel and gretel, Hansel |
| found footage look | 49 | An afterlife, Cctv, Raw, Stock, Videos cinematic, Edits, Security camera, Car |
| lo-fi edit | 9 | — |
| indie sleaze edit | 19 | Photo, Aesthetic |
| cyber edit | 18 | — |
| anime edit | 39 | Watermark, Free, Black, Cool, Aesthetic hindi song, Hindi song, Blasian, Background for |
| AMV style | 14 | — |
| phonk edit look | 46 | Kny, Audio, Blue lock, Songs, Tiki tiki, Car, Jujutsu kaisen, Lamborghini |
| glitch edit | 22 | Overlay, Tutorial, Overlay gif, Video, Overlay video, Kpop, Gojo, Photo |
| psychedelic edit | 14 | — |
| trippy edit | 18 | Photo, Overlay, Picsart, Background, Instagram, Trippie red, Aesthetic videos, Trippie red video |
| experimental video art | 15 | — |
| motion design style | 14 | Frames, 2d, 3d, Apple, Vox, Graphics, Design, paper collage, Collage |
| seedream video prompt | 7 | — |
| kling style prompt | 14 | — |
| runway restyle | 15 | — |
| midjourney video style | 11 | — |
| higgsfield effect | 43 | Prompt, Logo, Soul prompt, Tutorial, Soul 2.0, Animation, Video ideas, Prompt product |
| pika effect | 47 | Tabi, Workout, Jigokuraku, Kamu benar benar mengenalku, Tabi shoes, Windbreaker, Maka, Semua bersandar |
| AI filter trend | 15 | — |
| style transfer video | 9 | — |
| tiktok filter trend | 20 | Matcha, Never needed |
| instagram reel effect | 31 | Videos, Aesthetic, Edits, Filter, Name, Background, Cover, Story |
| edit inspo | 41 | Rp, Photo, Kpop, Canva, Rp simple, Rp pfp, Birthday, Video |
| gaya editing video | 12 | — |
| efek video aesthetik | 12 | Mentahan, Partikel, Capcut |
| 视频风格 | 14 | — |
| 剪辑风格 | 17 | — |
| 動画 エフェクト 加工 | 1 | — |
| 영상 편집 스타일 | 17 | — |
| estilo de edición video | 9 | — |
| estilo de edição vídeo | 12 | — |

### Pinterest — look-specific searches with screenshot (54)

| Search | URL |
|---|---|
| pixel stretch effect | https://www.pinterest.com/search/pins/?q=pixel%20stretch%20effect |
| pixel sorting glitch art | https://www.pinterest.com/search/pins/?q=pixel%20sorting%20glitch%20art |
| persona 5 ui style | https://www.pinterest.com/search/pins/?q=persona%205%20ui%20style |
| gta loading screen art style | https://www.pinterest.com/search/pins/?q=gta%20loading%20screen%20art%20style |
| wes anderson color palette symmetrical | https://www.pinterest.com/search/pins/?q=wes%20anderson%20color%20palette%20symmetrical |
| cinestill 800t halation night | https://www.pinterest.com/search/pins/?q=cinestill%20800t%20halation%20night |
| kaleidoscope mirror effect | https://www.pinterest.com/search/pins/?q=kaleidoscope%20mirror%20effect |
| ps1 graphics aesthetic | https://www.pinterest.com/search/pins/?q=ps1%20graphics%20aesthetic |
| minecraft voxel style realistic render | https://www.pinterest.com/search/pins/?q=minecraft%20voxel%20style%20realistic%20render |
| needle felted wool animation | https://www.pinterest.com/search/pins/?q=needle%20felted%20wool%20animation |
| knitted yarn crochet style | https://www.pinterest.com/search/pins/?q=knitted%20yarn%20crochet%20style |
| matisse cut outs style | https://www.pinterest.com/search/pins/?q=matisse%20cut%20outs%20style |
| american traditional tattoo flash | https://www.pinterest.com/search/pins/?q=american%20traditional%20tattoo%20flash |
| chalk drawing blackboard animation | https://www.pinterest.com/search/pins/?q=chalk%20drawing%20blackboard%20animation |
| crayon oil pastel child drawing | https://www.pinterest.com/search/pins/?q=crayon%20oil%20pastel%20child%20drawing |
| linocut block print | https://www.pinterest.com/search/pins/?q=linocut%20block%20print |
| engraving crosshatch banknote | https://www.pinterest.com/search/pins/?q=engraving%20crosshatch%20banknote |
| anaglyph 3d red cyan | https://www.pinterest.com/search/pins/?q=anaglyph%203d%20red%20cyan |
| tilt shift miniature | https://www.pinterest.com/search/pins/?q=tilt%20shift%20miniature |
| inflatable balloon puffy 3d | https://www.pinterest.com/search/pins/?q=inflatable%20balloon%20puffy%203d |
| arcane painterly style | https://www.pinterest.com/search/pins/?q=arcane%20painterly%20style |
| pixar style 3d render | https://www.pinterest.com/search/pins/?q=pixar%20style%203d%20render |
| paper cutout animation south park style | https://www.pinterest.com/search/pins/?q=paper%20cutout%20animation%20south%20park%20style |
| rubber hose cartoon 1930s cuphead | https://www.pinterest.com/search/pins/?q=rubber%20hose%20cartoon%201930s%20cuphead |
| liquid light show psychedelic 60s | https://www.pinterest.com/search/pins/?q=liquid%20light%20show%20psychedelic%2060s |
| marbled paper ebru ink | https://www.pinterest.com/search/pins/?q=marbled%20paper%20ebru%20ink |
| topographic contour lines art | https://www.pinterest.com/search/pins/?q=topographic%20contour%20lines%20art |
| art nouveau mucha poster | https://www.pinterest.com/search/pins/?q=art%20nouveau%20mucha%20poster |
| constructivist poster soviet | https://www.pinterest.com/search/pins/?q=constructivist%20poster%20soviet |
| op art optical illusion | https://www.pinterest.com/search/pins/?q=op%20art%20optical%20illusion |
| led dot matrix display | https://www.pinterest.com/search/pins/?q=led%20dot%20matrix%20display |
| city pop illustration | https://www.pinterest.com/search/pins/?q=city%20pop%20illustration |
| kodachrome slide film look | https://www.pinterest.com/search/pins/?q=kodachrome%20slide%20film%20look |
| tintype portrait wet plate | https://www.pinterest.com/search/pins/?q=tintype%20portrait%20wet%20plate |
| technicolor three strip film still | https://www.pinterest.com/search/pins/?q=technicolor%20three%20strip%20film%20still |
| x-ray skeleton effect | https://www.pinterest.com/search/pins/?q=x-ray%20skeleton%20effect |
| kirlian aura photography | https://www.pinterest.com/search/pins/?q=kirlian%20aura%20photography |
| dreamcore aesthetic | https://www.pinterest.com/search/pins/?q=dreamcore%20aesthetic |
| liminal space backrooms fluorescent | https://www.pinterest.com/search/pins/?q=liminal%20space%20backrooms%20fluorescent |
| windows 95 desktop aesthetic | https://www.pinterest.com/search/pins/?q=windows%2095%20desktop%20aesthetic |
| vaporwave aesthetic | https://www.pinterest.com/search/pins/?q=vaporwave%20aesthetic |
| tron legacy neon grid | https://www.pinterest.com/search/pins/?q=tron%20legacy%20neon%20grid |
| illuminated manuscript medieval | https://www.pinterest.com/search/pins/?q=illuminated%20manuscript%20medieval |
| greek black figure vase painting | https://www.pinterest.com/search/pins/?q=greek%20black%20figure%20vase%20painting |
| japan photo collage cut out | https://www.pinterest.com/search/pins/?q=japan%20photo%20collage%20cut%20out |
| memphis design 80s pattern | https://www.pinterest.com/search/pins/?q=memphis%20design%2080s%20pattern |
| bleach bypass film look | https://www.pinterest.com/search/pins/?q=bleach%20bypass%20film%20look |
| vx1000 fisheye skate video | https://www.pinterest.com/search/pins/?q=vx1000%20fisheye%20skate%20video |
| tarot card art illustration | https://www.pinterest.com/search/pins/?q=tarot%20card%20art%20illustration |
| action figure blister pack | https://www.pinterest.com/search/pins/?q=action%20figure%20blister%20pack |
| rain on window droplets bokeh | https://www.pinterest.com/search/pins/?q=rain%20on%20window%20droplets%20bokeh |
| cardboard craft diorama | https://www.pinterest.com/search/pins/?q=cardboard%20craft%20diorama |
| origami paper fold animation | https://www.pinterest.com/search/pins/?q=origami%20paper%20fold%20animation |
| mixed media edit kpop collage | https://www.pinterest.com/search/pins/?q=mixed%20media%20edit%20kpop%20collage |

### Behance — brief keywords, logged-out project search (70 done)

| Keyword | Result count shown | Example project titles |
|---|---|---|
| video style editing | 10,000+ | VOX-Style Animated Documentary / The His...; Documentary TRUMP / Breakdown YT vídeo; The First Camera Ever Made - Vox style I... |
| video editing style | 10,000+ | VOX-Style Animated Documentary / The His...; Documentary TRUMP / Breakdown YT vídeo; The First Camera Ever Made - Vox style I... |
| edit style | 10,000+ | Fashion Illustration for The Shanghai ED...; Metila Brand guidelines Free Editable Te...; Jonny Czar Portfolio 2024 |
| editing styles tutorial | 10,000+ | Fashion Illustration for The Shanghai ED...; Spaghetti Mit Pesto; Kumarika Wedding Hair Style Tutorial EP2 |
| aesthetic edit | 10,000+ | Y2K Editable Logo Collection Vol. 01 / L...; 36 Days of Type 7th Edition |
| aesthetic video edit | 10,000+ | Clinica Germania / Video Editing &Produc...; Say My Name: Bloody Mary / Visual Storyt...; Aesthetic Clinic / Video Editing |
| trending edit style | 10,000+ | Apple Style Trending UI Animation; Fashion Illustration for The Shanghai ED...; Limited Edition capsule for Befree brand |
| viral edit style | 10,000+ | Fashion Illustration for The Shanghai ED...; Creator Oly - Viral Video Editing Style; Advertisement/ Eat Clean |
| capcut edit style | 10,000+ | Documentary style, whiteboard and talkin...; Fashion Illustration for The Shanghai ED...; Video Editing Portfolio |
| capcut template | 10,000+ | Open Case Template; Portfolio |
| after effects style | 10,000+ | Alfa Card / Creative Project; BDSR Lite - jan 2026; VOX-Style Animated Documentary / The His... |
| premiere look | 10,000+ | Lazer KinetiCore 2026; LOOK UP! - Zeppelin Films; The Devil Wears Prada 2 - Premiere Looks |
| LUT look | 10,000+ | Soft Indie Film LUTs; A collection of 3Dluts; 30 Sweet Fall Video LUTs |
| AI video style | 10,000+ | Documentary-style Civic Video; Sugar Cloud — AI Confectionery Content; AI Fashion Film / Cinematic Beauty & Style |
| AI video filter | 10,000+ | ViSiora - AI-powered image generation pl...; Ponder AI; Movie Streaming Mobile App UI/UX |
| AI restyle video | 10,000+ | ViSiora - AI-powered image generation pl...; Ponder AI; Movie Streaming Mobile App UI/UX |
| video to video style | 10,000+ | CASTING STUDY — FROM STILL TO MOTION; AI video / from field to plate; GRAPHIC DESIGN PORTFOLIO 2026 |
| frame by frame edit | 10,000+ | LEC - Redesign Concept; The walking Flowers; Water |
| frame by frame animation edit | 10,000+ | LEC - Redesign Concept; The walking Flowers; Water |
| rotoscope edit | 10,000+ | ROTOSCOPING; Rotoscopia e Animação; y esta pared es mía |
| mixed media edit | 10,000+ | TwoJeys fan art project; Anyme023 - Vlog Martinique; Creative Portfolio 2026 / Anggitym |
| collage edit | 10,000+ | VOX-Style Animated Documentary / The His...; Al Jazeera DNR / Behind the Map Lines |
| paper cutout edit | 4,000+ | Where did the name "podcast" come from?; Laser-cut cutout stop motion; Pensamientos |
| stop motion edit | 10,000+ | VISUAL COMMUNICATION PORTFOLIO 2026; Il Gatto con gli Stivali; Collage Animation |
| overlay edit | 10,000+ | Free Textures Pack Vol. 4; Free Photoshop Templates & Actions for C...; LOLLINOBA - 2026 TWITCH |
| texture overlay edit | 3,000+ | Free Textures Pack Vol. 4; 10 Free Film Texture Frames; 32 Free Film Grain Textures 4K |
| music video look | 10,000+ | 走走&看看/GO&LOOK; Look Me In The Eyes - The Darcy's; How does an earworm look like? |
| music video edit style | 10,000+ | Lyric Hip Hop Clip; GRAPHIC DESIGN PORTFOLIO 2026; Ponder AI |
| fashion film edit | 10,000+ | YSL - Libre; AI Fashion Film; Morobé |
| film look | 10,000+ | Coffee Machine: A Product Film Study; TED - Take A Closer Look; PICNIC - Malayalam movie first look |
| cinematic look | 10,000+ | TED - Take A Closer Look; VALORÉ — Cinematic CGI Fragrance Film; HYPERPC — 3D Product Animation & Cinemat... |
| retro edit | 10,000+ | Jonny Czar Portfolio 2024; Bookify - Bringing acclimated books righ...; Worldpackers Experiences Brand and App D... |
| vintage edit | 10,000+ | Jonny Czar Portfolio 2024; Cairo Tales l Posters Edition; Free Textures Pack Vol. 4 |
| y2k edit | 10,000+ | Imagen intervenida / Y2K; Bitmap Dreams Color Edition; Y2K Editable Logo Collection Vol. 01 / L... |
| grunge edit | 10,000+ | Bitmap Dreams Color Edition; ПАУК - Music Video for Astra Pride; Personal edition / Collection of a Motio... |
| dreamcore | 700+ | Dreamcore; Editorial Álbum Dreamcore de Ghouljaboy; FRAGILE |
| weirdcore | 300+ | Anticipation/Предвкушение; Sticker pack from Sugar die; Last Lucidity |
| liminal edit | 10,000+ | GRAPHIC DESIGN PORTFOLIO 2026; Ponder AI; To Japan / Short Film |
| analog horror edit | 3,000+ | "Asegurá tu futuro" - Campaña Publicitar...; HORROR MOVIE POSTER & VHS VIDEO DESIGN; Late Night With the Devil Title Sequence |
| found footage look | 600+ | Cave Story - Southern Hype; Photography 3rd Lab Exam: Outside Concep...; Discover the Unknown |
| lo-fi edit | 4,000+ | TONE / GDR — Urban Lo-Fi Visuals; Lo Fi; St. GOGO - くま　ｅｖｅｒｌａｓｔｉｎｇ |
| indie sleaze edit | 600+ | "Indie sleaze/Collage" visualizer for Ch...; Un Aruginil Yeno - Music Video; CONTEMPORARY PERSONAL STYLE |
| cyber edit | 10,000+ | Cyber-Pop Variants Jennie edition:; CYBER-BALL / VFX & Visual Identity; GRAPHIC DESIGN PORTFOLIO 2026 |
| anime edit | 10,000+ | AMV edit - Muzan; Culturas Caribeñas del Hip Hop; 富邦悍將 2025年度系列影片 |
| AMV style | 10,000+ | Kham — Brand Book for a Sport Coaching P...; SL24: Brutalist Data-Logistics & Cyber-T...; Sayori |
| phonk edit look | 1,000+ | 走走&看看/GO&LOOK; LOOK UP! - Zeppelin Films; HUAWEI I LOOK UP |
| glitch edit | 10,000+ | YNG Martyr - Since You Been Gone; AmEN![Terminal Version]; GLITCH KIT 2.0 |
| psychedelic edit | 10,000+ | Divine Fire – A Psychedelic Journey Into...; Book «The Mysteries of the Amanita Mushr...; BCCO Berlin × Diana Franco × ERRXD |
| trippy edit | 10,000+ | Divine Fire – A Psychedelic Journey Into...; BCCO Berlin × Diana Franco × ERRXD; alice's in wonderland & under ground |
| experimental video art | 10,000+ | Season of Roses; AmEN![Terminal Version]; Time collages |
| motion design style | 10,000+ | BDSR Lite - jan 2026; VOX-Style Animated Documentary / The His...; Education City / Qatar |
| seedream video prompt | 700+ | ViSiora - AI-powered image generation pl...; AI Video; Product Film: Wireless Earbuds / AI Hybr... |
| kling style prompt | 100+ | Viral animal selfie-style video made wit...; Visual Development: Anime Project with A...; AI Jewelry Collection/AI Commercial Visu... |
| runway restyle | 10,000+ | Nel Hydrogen - Brand Identity Restyling; Restyling runway looks; Day 8: Restyle video into Xray |
| midjourney video style | 10,000+ | Alfa Card / Creative Project; Fashion Visual Story; Surreal Riviera: Whimsical Summer Style ... |
| higgsfield effect | 10,000+ | Higgsfield - Kinetic Typography & UI Ani...; AI Instagram Reel - Created by Higgsfiel...; Motion Study / Higgsfield AI Investor Deck |
| pika effect | 10,000+ | Here is my Portfolio; Farseer; Hiep Tran's Lab |
| AI filter trend | 1,000+ | Top Services for AI Amazon Review / Comm...; Design Trends 2025; NOISE FILTER LAB |
| style transfer video | 10,000+ | Alfa Card / Creative Project; 2016. Yung Sanya x Fhydjeck. Rendezvous....; The Science / the Sea and I (official vi... |
| tiktok filter trend | 700+ | Wesanderson Reel ft Tempat Kita; Batalha de Fini - TikTok Effect; Balaio Discos |
| instagram reel effect | 10,000+ | Before and After, Podcast Reel Edition F...; Short-Form Video Editing & Motion Graphics; SOCİAL MEDİA content creation / Reels an... |
| edit inspo | 10,000+ | Breathe .2; GRAPHIC DESIGN PORTFOLIO 2026; Ponder AI |
| gaya editing video | 10,000+ | GRAPHIC DESIGN PORTFOLIO 2026; Ponder AI; To Japan / Short Film |
| efek video aesthetik | 10,000+ | GRAPHIC DESIGN PORTFOLIO 2026; ViSiora - AI-powered image generation pl...; Ponder AI |
| 视频风格 | 10,000+ | Nike TOMA - 线下活动主题视觉设计; TWO的二次方 / 数学家咖啡品牌视觉设计; 贝壳品牌VI视觉识别规范 |
| 剪辑风格 | 10,000+ | 「放风的羊」Fresh Lamb Meat Brand Image Design...; WinnieHO南洋爵士专辑设计; TAOBAO-LIFE HTML5 Creative&Design / 淘宝人生... |
| 動画 エフェクト 加工 | 2,000+ | Canthy Bank — 2026 year of the horse cal...; 綻光文化30 ✦ 活動主視覺 Event Key Visual Design; 南投集集鎮 在地市集活動【2020南投縣 集集鎮 蕉十一郎市集-主視覺設計】 f... |
| 영상 편집 스타일 | 2,000+ | 5월,6월｜브랜딩 영상｜채널A; 디자인 포트폴리오; [2025] 영상&모션그래픽 포트폴리오 |
| estilo de edición video | 10,000+ | Video para Estilo Home Decor's; Edición de video estilo Iman Gadzhi; diseño de miniatura para youtube estilo ... |
| estilo de edição vídeo | 10,000+ | Color Grading; edição de vídeo estilo youtube; A Volta do Estilo Emo / Edição de Vídeo |

### Behance and Dribbble — look-specific searches with screenshot (24)

| Search | URL |
|---|---|
| beh-felt-stopmotion | https://www.behance.net/search/projects?search=felt%20stop%20motion%20animation |
| beh-papercut-anim | https://www.behance.net/search/projects?search=paper%20cutout%20animation |
| beh-matisse | https://www.behance.net/search/projects?search=matisse%20cutout%20animation |
| beh-rotoscope | https://www.behance.net/search/projects?search=rotoscope%20animation |
| beh-glitch | https://www.behance.net/search/projects?search=glitch%20art%20motion |
| beh-linocut | https://www.behance.net/search/projects?search=linocut%20animation |
| beh-tattoo-flash | https://www.behance.net/search/projects?search=tattoo%20flash%20animation |
| beh-cardboard | https://www.behance.net/search/projects?search=cardboard%20stop%20motion |
| beh-chalk | https://www.behance.net/search/projects?search=chalk%20animation |
| beh-kaleido | https://www.behance.net/search/projects?search=kaleidoscope%20animation |
| beh-vinyl-toy | https://www.behance.net/search/projects?search=designer%20vinyl%20toy%203d%20character |
| beh-ai-music-video | https://www.behance.net/search/projects?search=ai%20music%20video%20visuals |
| beh-inflatable | https://www.behance.net/search/projects?search=inflatable%203d%20animation |
| beh-yarn | https://www.behance.net/search/projects?search=yarn%20knitted%20animation |
| beh-led | https://www.behance.net/search/projects?search=led%20dot%20matrix%20animation |
| beh-liquid-light | https://www.behance.net/search/projects?search=liquid%20light%20show%20animation |
| drb-felt | https://dribbble.com/search/felt-animation |
| drb-macrame | https://dribbble.com/search/macrame-yarn |
| drb-crayon | https://dribbble.com/search/crayon-animation |
| drb-chalk | https://dribbble.com/search/chalk-animation |
| drb-pixelsort | https://dribbble.com/search/pixel-sort-glitch |
| drb-mixed-media-anim | https://dribbble.com/search/mixed-media-animation-video |
| drb-paper-cut | https://dribbble.com/search/paper-cut-animation |
| drb-voxel | https://dribbble.com/search/voxel-animation |

### Threads — public `/tag/<tag>` pages via Jina reader (46 tags)

| Tag (https://www.threads.com/tag/TAG) | Result |
|---|---|
| aestheticedit | 70K threads |
| aftereffects | 186K threads |
| aiart | 3M threads |
| aivideo | 950K threads |
| aivideoprompt | nothing (page not served) |
| amv | nothing (page not served) |
| analoghorror | 17K threads |
| animation | 3.7M threads |
| anime | 21M threads |
| capcut | 6.9M threads |
| capcuttemplate | 88K threads |
| cinematiclook | 53K threads |
| collageedit | nothing (page not served) |
| cyberpunk | 964K threads |
| dreamcore | 79K threads |
| editingstyle | nothing (page not served) |
| editstyle | nothing (page not served) |
| experimentalfilm | 3.5K threads |
| fashionfilm | 13K threads |
| filmlook | 31K threads |
| framebyframe | 32K threads |
| glitch | 1.1M threads |
| glitchart | 26K threads |
| higgsfield | 270K threads |
| klingai | 126K threads |
| liminalspace | 26K threads |
| lofi | 641K threads |
| midjourney | 1M threads |
| mixedmedia | 240K threads |
| motiondesign | 80K threads |
| musicvideo | 817K threads |
| restyle | 88K threads |
| retroedit | nothing (page not served) |
| rotoscope | 4.3K threads |
| runway | 4.2M threads |
| seedance | 574K threads |
| seedream | 52K threads |
| stopmotion | nothing (page not served) |
| stylereference | nothing (page not served) |
| styletransfer | nothing (page not served) |
| vhs | 792K threads |
| videoart | 32K threads |
| videostyle | nothing (page not served) |
| videotovideo | nothing (page not served) |
| weirdcore | 47K threads |
| y2k | 1.5M threads |

### Dribbble

- 8 look-specific searches rendered and screenshots were taken (felt-animation, macrame-yarn, crayon-animation, chalk-animation, pixel-sort-glitch, mixed-media-animation-video, paper-cut-animation, voxel-animation); URLs are in the Behance and Dribbble table above.
- Running the 70 brief keywords on Dribbble was stopped after the first query: the site showed "Let's confirm you are human". It was not bypassed. So Dribbble was not swept with the full brief list.

## Caveats

- OpenCLI was not connected, so Instagram search through the logged-in browser was unavailable. Instagram was covered with Exa (`site:instagram.com`) and with public `/popular/<slug>/` pages through the Jina reader. 44 of the 117 slugs tried returned no page.
- Exa hit a rate limit mid-run (HTTP 429). The 8 Instagram queries that failed then were re-run later and returned results.
- The built-in browser pane was hidden, so screenshots were taken with a separate headless Playwright script on public pages only. No sign-in, no CAPTCHA bypass; Pinterest sign-up dialogs were removed from the screenshot only.
- Vimeo could not be opened in the built-in browser; WebSearch was used instead. Staff Pick status could not be confirmed for most results because "Staff Picks" also appears as site navigation text.
- Threads exposes only public tag pages and WebSearch blocks threads.net, so Threads gave thread counts per hashtag and little style content (mostly editor job posts and AI tool chatter).
- Instagram hashtag pages with a pure edit-style keyword (e.g. "edit-style", "viral-edit-style") were not served at all.
- Arcane Painterly has thin evidence because its Pinterest search page rendered blank; it is the weakest row.
