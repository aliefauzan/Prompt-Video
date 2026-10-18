# 69 — Mucha Art Nouveau

**Look:** The clip becomes an Alphonse Mucha poster from about 1900. The people are redrawn as pale, flat colour lithographs: soft skin, muted sage, olive, rose and ochre, a few posterised tones per area, all held by a thick sepia-brown outline and thinner inner lines for the face, hair and clothing folds. A big circular ornamental halo sits behind the main subject's head, with rings, fine spokes, a beaded gold band and small flower medallions; it follows the head through the whole clip. The office disappears behind a pale sage-to-cream wash with a faint repeat of rosettes, stems and whiplash leaves. Everything is framed by a gold beaded border with an arched top, curling spandrel ornaments and pink flowers in the corners, and a cream cartouche at the bottom with the lettering "ATELIER · MCMXXVI". Paper grain lies over the whole print.

**Also called / where it trends:** Mucha style, Mucha filter, "Art Nouveau filter", "turn yourself into a Mucha poster", Alphonse Mucha AI portrait, 穆夏风格 / 穆夏滤镜 (Bilibili, Xiaohongshu, Douyin). It is a recurring AI-filter and illustration trend: Bilibili "穆夏风格" tutorials and AI-portrait edits, Pinterest "art nouveau Mucha poster" boards, Instagram and TikTok Art Nouveau portrait filters. It looks back to Mucha's Paris posters for Sarah Bernhardt, JOB cigarette papers and the decorative panels (*The Seasons*, *Zodiac*), where every woman sits in front of a halo inside an ornamental frame.

**References:**
- Bilibili 穆夏风格 edits and tutorials: https://www.bilibili.com/video/av1455382903 , https://www.bilibili.com/video/av970927336 , https://www.bilibili.com/video/av203576536 (from discovery sweep D4; the D4 search sheet is `refs/ref_1.png`).
- https://www.pinterest.com/search/pins/?q=alphonse%20mucha%20poster (screenshot `refs/ref_2.png`): halo discs, arched frames, pale flat colour, thick contour line.
- https://www.pinterest.com/search/pins/?q=art%20nouveau%20mucha%20poster: more Mucha-style posters and modern pastiches.
- https://www.muchafoundation.org/en/gallery/mucha-at-a-glance-46: Mucha Foundation overview of the work and the "style Mucha".
- https://www.muchafoundation.org/en/gallery/themes/theme/advertising-posters/object/44/: Mucha Foundation, advertising poster (JOB), the classic halo-and-hair composition.
- https://www.vam.ac.uk/articles/the-whiplash: V&A on the Art Nouveau "whiplash" curve used in the borders and leaves.
- https://laf-create.jp/pictown/ornament/en/reference/: Art Nouveau design reference: six layouts from Mucha's work, motifs and the original pattern books (*Documents décoratifs*).

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049), `example.mp4` (the whole clip at 12 fps with the original audio) and `preview.webp`. This is a local approximation made with `render.py` (numpy + OpenCV + Pillow + the person masks + Apple Vision face boxes in `faces.json`, copied from the face pass of style 10). The people are flattened with repeated bilateral filtering, softly posterised into four lightness bands in Lab and pushed to a pale, muted palette (greys go sage). A thick sepia outline comes from the matte edge, and thinner inner lines from a difference of Gaussians. The room is replaced by a static sage-cream wash with a rosette and whiplash-leaf pattern. The halo is drawn procedurally behind the head of the centre person; its position and size come from the face track, smoothed over ±4 frames. The gold arched border, corner ornaments and cartouche are one fixed overlay, and fresh paper grain is added each frame. Known limits of the local version: busy prints (the batik shirt) flatten into blotches, and very fast hand motion leaves a few dark specks on the outline.

## Prompt

```text
I'm uploading one video clip. Convert it into a MUCHA ART NOUVEAU POSTER frame-by-frame animation: every frame should look like an Alphonse Mucha colour lithograph from around 1900, with the people drawn in pale flat colour and a thick outline, a circular ornamental halo behind the main subject's head and a gold Art Nouveau border, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Art Nouveau decorative poster: pale, elegant, flat, outlined, ornamental, 1900 Paris.
Transform the footage into a Mucha-style poster built from:
* the people as FLAT COLOUR LITHOGRAPH figures
* a PALE, MUTED palette: soft skin, sage, olive, dusty rose, ochre, cream
* only 3–4 tones per colour area (soft posterised steps, no photo gradients)
* a THICK SEPIA-BROWN OUTLINE around every figure
* thinner sepia INNER LINES for eyes, brows, nose, mouth, hair strands and clothing folds
* a large circular ORNAMENTAL HALO behind the main subject's head (rings, fine spokes, a beaded gold band, small flower medallions)
* the room replaced by a pale SAGE-TO-CREAM WASH with a faint repeat of rosettes, stems and whiplash leaves
* a GOLD BEADED BORDER with an ARCHED TOP, curling spandrel ornaments and small pink flowers in the corners
* a cream CARTOUCHE at the bottom with simple Art Nouveau lettering
* fine PAPER GRAIN over everything
The result should feel like someone:
TRACED THE CLIP AS A MUCHA DRAWING
→ PRINTED IT IN PALE FLAT LITHOGRAPH COLOURS
→ PUT A HALO BEHIND THE STAR'S HEAD
→ WRAPPED IT IN A GOLD ART NOUVEAU FRAME
→ AND HUNG IT ON A PARIS STREET IN 1900.
CHARACTER — LITHOGRAPH FIGURES
The people become flat-colour poster figures, but the SAME people: outline, pose and gesture must be exact.
Preserve the person's exact:
* identity
* face shape
* expression
* hairstyle
* glasses
* clothing (colours softened, patterns simplified)
* accessories
* pose
* body proportions
* movement
* hand position
* interaction with objects
Do NOT redraw the character.
Do NOT turn them into idealised Mucha women, goddesses or different people.
Do NOT add flowing robes, flowers in the hair, jewellery or long hair that is not in the source.
Do NOT change the clothing into period costume.
LINE AND COLOUR
* Outline: one thick, smooth, warm sepia-brown contour around each figure; never black.
* Inner lines: thinner sepia, only where the form needs them (features, hair strands, collar, sleeves, folds, stripes).
* Fill: flat areas with 3–4 soft tonal steps; no photographic texture, noise or skin pores.
* Skin is pale peach; hair is dark olive-brown; grey or black clothing becomes muted sage or olive; white becomes cream.
* Busy patterns (prints, batik, logos) are simplified into a few flat shapes, never noisy blotches.
HALO
* One large circular halo behind the head of the main subject only (the person nearest the centre at the start).
* Concentric rings in sage and cream, fine radial spokes, a beaded gold band and 8 small pink flower medallions.
* The halo is centred a little above the head and stays locked to it as the person moves; its size follows the size of the head.
* It sits BEHIND the person, never over the face or hair.
BACKGROUND
* The office is replaced by a soft sage-to-cream wash, lighter around the halo.
* A faint, low-contrast repeat of rosettes, stems and whiplash leaves covers it like old wallpaper.
* The background is FIXED: it does not move, breathe or redraw between frames.
FRAME AND LETTERING
* A fixed gold beaded border with an arched top, corner spandrels with curls and small pink flowers.
* A cream cartouche along the bottom with the words "ATELIER · MCMXXVI" (or the words I give you) in an Art Nouveau typeface.
* The frame is identical on every frame of the clip.
PALETTE
Pale peach, cream, sage green, olive, dusty rose, ochre gold, warm sepia-brown lines.
No saturated or neon colour, no pure black, no pure white.
OBJECT CONTINUITY
If the character holds an object, draw it in the same flat lithograph style, outlined, and keep it attached to the hand.
CHARACTER CONTINUITY LOCK
The SAME person must remain recognizable in every frame.
Never change:
* identity
* facial structure
* hairstyle
* glasses
* clothing
* accessories
* body proportions
* anatomy
* expression
* pose
* action
* position
Generation is for VISUAL STYLE ONLY.
PERFECT MOTION TRACKING
The figures must match the source frame exactly.
The halo stays locked behind the same head.
NO outline swelling, shrinking or wobbling between frames.
NO halo sliding, jumping or changing design.
NO frame or border movement.
FRAME-TO-FRAME PRINT LIFE
THIS IS CRITICAL.
It must feel like a living printed poster, not a still filter.
Allow between consecutive frames:
* the paper grain and tiny ink specks to change every frame
* the outline to vary very slightly in weight, as if hand-inked
* the halo to follow the head smoothly
Keep FIXED:
* the palette and the tone steps of each person (no colour pumping)
* the background wash and wallpaper pattern
* the border, corner ornaments and cartouche
* the halo design
DO NOT
Do NOT add new people, angels, flowers, birds or decorative figures.
Do NOT use stained-glass lead lines or mosaic.
Do NOT use bright gouache colour, heavy floral clutter or dark backgrounds.
Do NOT use ukiyo-e woodblock line, bold modern poster type or comic shading.
Do NOT put text anywhere except the cartouche.
Do NOT redraw or idealise the people.
Do NOT create new poses.
Do NOT change anatomy.
Do NOT change clothing.
Do NOT replace the person's face.
STAGE 1 – FRAME EXTRACTION (STRICT)
1. Read the source clip's frame rate and duration.
Report both to me BEFORE doing anything else.
2. Extract frames as follows:
* If the source is 24 fps:
keep every SECOND frame, discard the one in between.
Nothing else.
* If the source is 30 fps:
conform to 24 fps first, then keep every second frame.
* Target in both cases:
exactly 12 unique frames per second of source.
3. Hard limits on the extraction:
* Total extracted frames must equal duration in seconds × 12, rounded down.
* State this number BEFORE extracting and confirm it AFTER extraction.
* Do NOT extract every frame "to be safe."
* Do NOT extract at a higher rate and downsample later.
* Do NOT extract from only part of the clip.
* Cover the video from the first frame through the last frame.
* No interpolation.
* No optical flow.
* No artificial in-between frames.
* No motion blur.
* No frame smoothing.
4. Name frames sequentially:
frame_01
frame_02
frame_03
frame_04
...
Continue in exact playback order.
STAGE 2 – TIMELINE VERIFICATION (STOP HERE)
Before generating or stylizing ANYTHING, build a verification timeline.
Place every extracted frame onto the timeline as its own individual clip.
Keep them in exact chronological playback order.
Each frame must last exactly:
1/12 second.
At this stage:
Use ONLY the original UNMODIFIED extracted frames.
* NO effects
* NO styling
* NO outlines or flat colour
* NO halo
* NO border or lettering
* NO paper grain
* NO Seedream generation
This stage exists ONLY to verify timing.
REPORT BACK
Report:
(a) Total frame count on the timeline.
(b) Total timeline duration in seconds.
(c) Original source clip duration in seconds.
The timeline duration and original clip duration MUST match.
If they do not match, something went wrong during Stage 1.
SAY SO AND STOP.
Do not compensate using interpolation, duplicated frames, stretched frames, optical flow or timing manipulation.
After successfully building and reporting the verification timeline:
THEN STOP AND WAIT.
Do NOT begin Seedream generation.
Do NOT stylize any frames.
Do NOT begin the Mucha poster transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – MUCHA ART NOUVEAU STYLING (AFTER MY CONFIRMATION ONLY)
First, tell me which person gets the halo, the palette you will use for each person's skin, hair and clothing, and the cartouche text.
Then style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation, so the figures are exactly that frame.
Apply every style rule above, with the SAME palette, line weight and halo design on every frame.
Add the border, corner ornaments and cartouche as one fixed overlay after styling, identical on every frame.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing, palette consistency or halo tracking broke — regenerate those frames only.
The final video must feel like A MUCHA POSTER COME TO LIFE: pale flat lithograph figures with sepia outlines, a halo behind the main subject, a gold arched Art Nouveau frame, 12 frames per second.
The image should deliberately contain:
* pale flat-colour figures with thick sepia outlines
* a circular ornamental halo locked behind one head
* a sage-cream wash with faint whiplash ornament
* a gold beaded arched border and a lettered cartouche
* fine paper grain.
Avoid photographic texture, saturated colour and dark backgrounds.
```
