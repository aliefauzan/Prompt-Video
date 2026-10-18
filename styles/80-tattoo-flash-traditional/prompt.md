# 80 — American Traditional Tattoo Flash

**Look:** The clip becomes a sheet of American Traditional tattoo flash, the hand-painted designs that hang on a tattoo-shop wall. The people are outlined in very bold, even black lines and filled with a few flat, saturated tattoo colours: red, mustard yellow, kelly green, teal, brown, skin tone and cream. Shading is black "whip" stippling that fades out from the outlines. There are no gradients and no photo texture. Faces get bold brows, outlined eyes and filled lips. Hair is solid black. Classic flash motifs fill the empty wall around the people and stay fixed on the sheet: swallows, roses, a heart, stars, sparkle dots and a ribbon banner reading "TRUE TO LIFE". All of it sits on aged, stained cream paper. The look is made of colour, heavy line and stipple. That separates it from the halftone dots of 07 Pop Art and 53 90s Comic, the B/W toner of 01 Punk Photocopy, and the pixel dither of 11 Pixel Dither.

**Also called / where it trends:** "American traditional", "old school tattoo", "Sailor Jerry style", "tattoo flash", "flash sheet", "traditional tattoo filter", "photo to tattoo flash", "turn yourself into a tattoo". The #americantraditional tag on Instagram is huge (3.2M+ reels). AI photo-to-tattoo-flash converters have made "me as a flash sheet" posts a trend, and tattoo animation is a common Behance and Reels format.

**References:**
- https://www.pinterest.com/search/pins/?q=american%20traditional%20tattoo%20flash (screenshot `refs/ref_1.png`): American Traditional flash sheets. They show the bold outlines, the limited red/yellow/green palette, whip shading, swallows, roses, banners and aged paper.
- https://artstyles.com/photo-filter-converter/tattoo-flash-art-style (screenshot `refs/ref_2.png`): a photo-to-tattoo-flash converter with a before/after. The after shows a red-beret portrait with a swallow, a "STAY GOLD" banner, an anchor and roses.
- https://www.instagram.com/popular/american-traditional-tattoo/: Instagram American Traditional tattoo reels (3.2M+).
- https://www.behance.net/search/projects?search=tattoo%20flash%20animation: Behance tattoo-flash animation projects.
- https://flashvellum.com/photo-to-tattoo: an AI photo-to-tattoo-flash tool.
- https://www.nyhistory.org/blogs/a-short-incomplete-history-of-american-traditional-tattooing: New-York Historical Society on the history of American Traditional tattooing and flash.
- https://www.lighthousetattoo.com.au/american-traditional-flash/: what defines American Traditional flash (bold lines, limited palette, classic motifs).
- https://www.designstylebook.com/tattoo/american-traditional: American Traditional style notes (outlines, solid colour, whip shading, iconography).

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049), `example.mp4` (the whole clip at 12 fps with the original audio) and `preview.webp`. This is a local approximation made with `render.py` (numpy + OpenCV + PIL, the person masks, and Apple Vision face landmarks in `faces.json`). The people are mean-shift smoothed and each region is classified by hue and value into the flash palette. Skin is found with YCrCb rules plus the face and neck areas. Dark areas around each face become solid black hair. The labels are smoothed into clean shapes. Black whip-shading stipple is added from each region's shadow and tapers away from the edges. A heavy outer line, inner region lines and XDoG detail lines wobble slightly every frame. Brows, eyes, pupils, lips and the nose are drawn from the face landmarks. The swallows, roses, heart, stars, dots and "TRUE TO LIFE" banner are drawn once and stay fixed. Everything sits on aged cream paper with stains and a faint sepia trace of the room.

## Prompt

```text
I'm uploading one video clip. Convert it into an AMERICAN TRADITIONAL TATTOO FLASH frame-by-frame animation: every frame should look like a hand-painted flash sheet hanging on a tattoo-shop wall, with the people painted as bold old-school tattoo designs, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
American Traditional tattoo flash, old school Sailor Jerry style, bold black outlines, flat saturated tattoo colours, black whip shading, swallows, roses, banners, stars, hand-painted on aged paper.
Transform the footage into a flash sheet built from:
* VERY BOLD, even BLACK OUTLINES around every shape
* a heavier outline around each person
* FLAT, SATURATED TATTOO COLOURS: red, mustard yellow, kelly green, teal, brown, skin tone, cream
* SOLID BLACK hair and deepest shadows
* black WHIP SHADING: stippled dots that fade out from the outlines
* NO gradients, NO airbrush, NO photo texture
* simple bold faces: strong brows, outlined eyes with black pupils, filled red lips
* classic flash MOTIFS around the people: swallows, roses, a heart, stars, sparkle dots
* a ribbon BANNER reading "TRUE TO LIFE"
* AGED CREAM PAPER with tea stains, foxing and darker edges
The result should feel like someone:
TRACED THE SCENE ONTO TATTOO STENCIL PAPER
→ LINED IT WITH A HEAVY BLACK LINER NEEDLE
→ PACKED IN FLAT TRADITIONAL COLOURS
→ WHIP-SHADED THE SHADOWS IN BLACK
→ HUNG IT ON THE SHOP WALL WITH THE OTHER FLASH
→ ANIMATED THE SHEET FRAME BY FRAME.
CHARACTER — FLASH-PAINTED, NOT REPLACED
The people become FLASH DESIGNS of themselves, traced from the frame.
Preserve the person's exact:
* identity
* face
* expression
* hairstyle
* glasses
* clothing
* clothing patterns (simplified into flat colour shapes, not removed)
* accessories
* pose
* body proportions
* movement
* hand position
* interaction with objects
Keep realistic proportions and the real face shape.
Do NOT turn them into sailors, pin-ups, skulls or other flash characters.
Do NOT add tattoos to their skin.
Do NOT give them new hats, clothes or props.
Do NOT redraw the pose.
LINE RULES
* Outlines are pure black, bold and even, like a single heavy liner pass.
* The outer silhouette of each person is the heaviest line.
* Every colour region is closed by a black line.
* Faces get bold, simple lines: brows, eye outlines with black pupils, a nose line, outlined lips.
COLOUR RULES
* Each region is filled with ONE flat colour from the palette.
* Skin is a warm flat skin tone.
* Hair is solid black.
* Light clothes become cream or yellow; dark clothes become teal or green; red and orange things become tattoo red; brown things stay brown.
* Busy fabric patterns become simplified flat colour shapes outlined in black.
* No colour blends inside a region.
SHADING RULES
* Shading is BLACK WHIP SHADING only: stippled dots and short flicks.
* It is densest next to the outlines and fades out into the colour.
* Use it only in shadow areas.
* Faces get only a light touch of whip shading.
BACKGROUND
* The wall around the people becomes the flash sheet: aged cream paper.
* The room may show as a very faint sepia pencil trace, never as photo detail.
* Place classic motifs in the empty space: two swallows, two roses, a heart, stars, sparkle dots, and a ribbon banner reading "TRUE TO LIFE" across the top.
* The motifs are painted in the same bold outline and flat colour style.
* The motifs NEVER cover the people.
* The motifs stay in the SAME place on every frame. They are part of the sheet.
PALETTE
Black. Tattoo red. Mustard yellow. Kelly green. Teal. Brown. Warm skin tone. Cream paper.
Do NOT add pastel, neon, purple or gradient colours.
OBJECT CONTINUITY
If the character holds an object, it is outlined and flat-coloured like the rest and stays attached to the hand.
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
The flash-painted people must match the source frame exactly.
Outlines, colour shapes and shading follow the people as they move.
NO colour region frozen in place while the body moves under it.
NO lines left behind from a previous frame.
FRAME-TO-FRAME PAINT LIFE
THIS IS CRITICAL.
It must feel like the sheet was hand-painted for every frame, not a still filter.
Allow between consecutive frames:
* outlines to wobble by about 1 pixel
* the stipple dots of the whip shading to change position
* colour edges to shift very slightly
Keep FIXED:
* the palette (each region keeps its colour from frame to frame)
* the motifs, banner and their positions
* the paper, stains and edge darkening
DO NOT
Do NOT use halftone dots, Ben-Day dots or pop-art colour dots.
Do NOT use photocopy toner, grit or collage.
Do NOT use pixel dither or a pixel grid.
Do NOT use gradients, airbrush, realistic or neo-traditional shading.
Do NOT use thin, sketchy or variable-width ink lines.
Do NOT use photo texture inside the colour regions.
Do NOT let motifs move, jump or cover the people.
Do NOT add any text other than "TRUE TO LIFE".
Do NOT turn the people into skulls, sailors or pin-ups.
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
* NO whip shading
* NO flash motifs or banner
* NO paper texture
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
Do NOT begin the tattoo flash transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – TATTOO FLASH STYLING (AFTER MY CONFIRMATION ONLY)
First, tell me which palette colour you will give each main region (skin, hair, each person's clothes), and where each motif and the banner will sit on the sheet.
Then style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation, so the people are exactly that frame.
Apply every style rule above, with the SAME palette assignment, motifs and paper on every frame.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing, the palette or a motif position broke — regenerate those frames only.
The final video must feel like A TATTOO FLASH SHEET COME ALIVE: bold black lines, flat red-yellow-green colour, whip shading, swallows and roses, 12 frames per second.
The image should deliberately contain:
* very bold black outlines
* flat saturated tattoo colours
* black whip-shading stipple
* solid black hair
* swallows, roses, a heart, stars and a "TRUE TO LIFE" banner
* aged cream flash paper.
Avoid photographic texture.
```
