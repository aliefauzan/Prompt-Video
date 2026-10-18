# 11 — 16-Bit Pixel Art Dither

**Look:** the clip rebuilt as a 16-bit (SNES / Mega Drive era) video-game screen: a coarse visible pixel grid (about 270×180 art pixels), every pixel snapped to one fixed 32-colour palette, 4×4 ordered (Bayer) dithering for every gradient, people as sprites with a 1-pixel dark outline, the bright window turned into a banded pixel sky with blocky clouds, and a tiny game HUD (1P, hearts, SCORE). Optional mode: the 4-shade Game Boy green palette (used here for 00:08–00:11).

**Also called / where it trends:** "8-bit / 16-bit retro game filter", "put me in a retro video game", "pixel art video", "dithering effect", "dither filter", "Game Boy camera look" (TikTok, YouTube Shorts, Instagram Reels; CapCut / After Effects / TouchDesigner dither tutorials; AI "retro pixel" video templates).

**References:**
- https://www.youtube.com/shorts/ztoEWg9KDC4 — "Put me in a classic 8-bit retro pixel art video game" AI trend example (refs/ref_2.png)
- https://www.youtube.com/results?search_query=dithering+effect+video+pixel+art — Shorts grid of the dither trend: ordered dither, 1-bit, Game Boy palettes (refs/ref_1.png)
- https://www.youtube.com/shorts/k0T9bxCdf4g — "After Effects Dither Effect in 10 Seconds"; https://www.youtube.com/shorts/mIJUH1pnAYQ — another dither-effect short from the same search
- https://www.youtube.com/watch?v=sk2sIj_ga04 — "VFX Side Quest: Creating a 16-Bit Retro Video Game Look"
- https://www.youtube.com/watch?v=lh-bI-a3u2Y — "Super Easy PIXEL ART Effect in DaVinci Resolve"
- https://wunkolo.itch.io/pixdither — Pixdither, palette + ordered-dither video tool
- https://www.maxon.net/en/red-giant/universe — Universe "Pixel Dither" effect used in many edits
- https://collidingscopes.github.io/video-to-pixel-art/ — browser video-to-pixel-art tool (grid size, palette)
- https://github.com/gyng/ditherer , https://github.com/niccolofanton/dithering-shader — open-source dithering for images/video

**Example:** `example.png` (6 frames of the test clip), `before_after.png`. Local approximation in `render.py`: 6×6 screen px per art pixel, Endesga 32 palette, 4×4 Bayer dither, nearest colour in Lab, 1-px sprite outline + inner sel-out from the person masks, banded dithered sky in the window, HUD, Game Boy palette on frames 97–132. All 179 frames are in `frames/`.

## Prompt

```text
I'm uploading one video clip. Convert it into a 16-BIT PIXEL-ART VIDEO-GAME frame-by-frame animation matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.

TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.

CORE VISUAL STYLE
Transform the footage into a screenshot of a 16-bit console game (SNES / Mega Drive era) built from:
* a coarse, clearly visible square pixel grid (about 270 × 180 art pixels for a 3:2 frame)
* every art pixel the same size, perfectly square, perfectly aligned to the grid
* ONE fixed limited palette of about 32 colours for the whole video
* ordered (Bayer 4×4) dithering for every gradient, shadow and skin transition
* checkerboard and cross-hatch dither patterns instead of smooth blends
* characters as game SPRITES with a 1-pixel dark outline
* selective inner outline (darker palette colour along the inside of the outline)
* hard pixel edges everywhere: no anti-aliasing, no blur, no sub-pixel detail
* a banded pixel-art sky with blocky white clouds where the window is
* a tiny pixel-font game HUD
* a very faint pixel / LCD grid when viewed full size
The result should feel like someone:
PRINTED THE VIDEO FRAME
→ SHRANK IT TO A CONSOLE RESOLUTION
→ REPAINTED EVERY PIXEL BY HAND FROM ONE GAME PALETTE
→ DITHERED EVERY GRADIENT WITH A BAYER PATTERN
→ OUTLINED EVERY PERSON AS A SPRITE
→ DROPPED THEM INTO A GAME LEVEL
→ SCALED IT UP WITH NEAREST-NEIGHBOUR
→ ANIMATED IT FRAME-BY-FRAME.

CHARACTER — PIXEL SPRITE
Every person becomes a pixel-art sprite placed ON TOP OF their exact footage pose.
Preserve each person's exact:
* identity
* face shape
* expression (eyes, smile and mouth as 1–3 pixel marks)
* hairstyle and hair silhouette
* clothing colours and clothing pattern (stripes become pixel stripes, batik becomes a dithered pattern)
* glasses and accessories (1-pixel frames)
* skin tone (nearest palette skin ramp, same family as the footage)
* pose
* body proportions
* movement
* hand position
* interaction with objects
Do NOT invent a new character.
Do NOT change age, gender or body type.
Do NOT turn people into chibi / super-deformed game mascots.
Keep REALISTIC proportions, as in a 16-bit adventure game with large character art.

PALETTE (LOCKED)
Use ONE palette for the whole video, chosen once, for example the 32-colour Endesga 32 set:
* 3–4 skin tones (light peach → warm brown → dark rose-brown)
* 3 hair darks (deep plum, near-black, dark brown)
* greens, teals, blues, purples for room and clothes
* warm wood oranges and browns
* one pure white, one near-black ink colour
NO colours outside the palette.
NO gradients made by blending: every in-between tone is a DITHER of two palette colours.
The palette must NOT drift between frames.

DITHERING
* Use ordered (Bayer 4×4) dithering, aligned to the art-pixel grid and FIXED in screen space.
* Dither on: skin shading, hair sheen, clothing folds, walls, wood, plants, shadows, sky bands.
* Large flat areas (wall, sky bands, screen) stay mostly solid colour with dither only at transitions.
* Do NOT use random noise dithering.
* Do NOT use error diffusion "worms" that crawl from frame to frame.

SPRITE OUTLINE
* 1 art-pixel outline around every person in the darkest palette colour.
* Inside the outline, a selective outline: the outer row of sprite pixels shifted one palette shade darker.
* Inner detail lines (jaw, collar, arms, fingers) as single pixels only.
* NO thick vector outlines. NO soft edges.

BACKGROUND — GAME LEVEL
The room stays in the same place but is repainted as a 16-bit game background:
* the same walls, wood panels, plants, screen, chair and furniture, in palette colours
* simplified shapes, tile-like repetition is welcome on panels and walls
* slightly darker / less saturated than the sprites, so the characters pop as in a game
BRIGHT WINDOWS / OVEREXPOSED AREAS → PIXEL SKY
Replace blown-out windows with a game sky:
* horizontal colour bands from deep blue at the top to pale cyan near the horizon
* dither only on the band edges
* blocky white pixel clouds (stacked rectangles, 1 shadow row underneath)
* clouds step 1 art pixel every few frames (slow parallax drift)
Keep window frames, blinds and the screen in place.

GAME HUD
Add a small, unobtrusive HUD in a pixel font with a 1-pixel drop shadow:
* top-left: "1P" and three pixel hearts
* top-right: "SCORE" with a 6-digit counter that ticks up slowly
* the third heart may blink
Keep the HUD tiny and in the corners. It must NEVER cover a face.

OPTIONAL MODE — GAME BOY PALETTE
For a short section (or the whole clip, if requested), switch to the 4-shade Game Boy palette:
* darkest #0f380f, dark #306230, light #8bac0f, lightest #9bbc0f
* the same grid, the same Bayer dither, the same outlines, the same HUD in green
* people slightly brighter than the background
Switch on a cut or a beat, never mid-motion.

LAYER ORDER
PIXEL SKY
↓
GAME-LEVEL BACKGROUND (palette + dither)
↓
CHARACTER SPRITES (palette + dither)
↓
SPRITE OUTLINE + SELECTIVE INNER OUTLINE
↓
HUD
↓
FAINT PIXEL GRID.

OBJECT CONTINUITY
IMPORTANT:
If a character is interacting with an object, preserve that object.
Examples:
* glasses
* phone
* chair
* bag
* lanyard / badge
* clothing accessory
Draw the object as pixel art in the same place, with the same palette, moving exactly with the original action.
Do NOT drop objects while converting the character into a sprite.

CHARACTER CONTINUITY LOCK
The SAME person must remain recognizable in every frame.
Never change:
* identity
* facial structure
* hairstyle
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
The underlying character movement must remain exactly faithful to the source footage.
If the head moves:
the sprite follows.
If the hand moves:
the hand pixels follow.
If the body turns:
the outline follows.
NO floating sprites.
NO previous-frame silhouette.
NO delayed outline.

FRAME-TO-FRAME PIXEL STABILITY
Pixel art is crisp and stable. Between consecutive frames:
* the grid never moves, never scales, never rotates
* the palette never changes (except at the optional Game Boy switch)
* static background pixels stay EXACTLY the same
* only pixels on moving people change
* dither patterns stay locked to the screen grid (no swimming dither)
Allow only:
* sprite pixels to re-quantize as the person moves (natural sprite animation feel)
* clouds to step slowly
* the score to tick, the heart to blink

DO NOT
Do NOT make it photographic.
Do NOT use a mosaic / blur pixelation filter with soft colours.
Do NOT use more colours than the palette.
Do NOT use anti-aliasing, soft edges or bilinear upscaling.
Do NOT make non-square or uneven pixels.
Do NOT use random noise or swimming dither.
Do NOT make 3D, voxel or modern HD-2D lighting.
Do NOT make chibi or exaggerated proportions.
Do NOT replace the person's face or change identity.
Do NOT create new poses.
Do NOT change anatomy.
Do NOT change clothing.
Do NOT add big text, logos or subtitles beyond the tiny HUD.
Do NOT add glitch, VHS or CRT curvature.
It must feel like a REAL 16-BIT GAME SCREEN, hand-pixelled frame by frame.

STAGE 1 – FRAME EXTRACTION (STRICT)
1. Read the source clip's frame rate and duration.
Report both to me BEFORE doing anything else.
2. Extract frames as follows:
* If the source is 24 fps:
keep every SECOND frame, discard the one in between.
* If the source is 30 fps:
conform to 24 fps first, then keep every second frame.
* Target in both cases:
exactly 12 unique frames per second of source.
Nothing else.
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
Use ONLY the original UNMODIFIED extracted frames.
At this stage:
* NO Seedream generation
* NO pixel-art conversion
* NO palette reduction
* NO dithering
* NO sprite outlines
* NO sky replacement
* NO HUD
* NO effects
* NO styling
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
THEN STOP AND WAIT
After successfully building and reporting the verification timeline:
STOP.
Do NOT begin Seedream generation.
Do NOT stylize any frames.
Do NOT begin the pixel-art transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.

STAGE 3 – PIXEL-ART EVERY FRAME (ONLY AFTER MY CONFIRMATION)
1. Restyle EVERY extracted frame individually with Seedream 5.0 Pro, using that exact original frame as the image reference.
2. Keep each output at the source resolution and framing. No crop, no zoom, no reframing.
3. After generation, snap every frame to the SAME art-pixel grid (nearest-neighbour down to ~270 × 180, then nearest-neighbour back up) and to the SAME locked palette, so the grid and colours match exactly across frames.
4. Replace each clip on the timeline IN PLACE with its pixel-art version. Same order. Same 1/12 second duration.
5. Lock the style sheet before generating: the same palette, the same sprite colours per person, the same outline colour, the same HUD position, in EVERY frame. Re-use the same wording for every frame prompt.
6. Lock the background: the same game-level room and the same sky; only the clouds step slowly.
7. If the Game Boy mode is used, apply it to a continuous run of frames that starts on a cut or a beat.
8. Check every 12th frame against the original: same pose, same expression, same position. Regenerate any frame that is off-model or off-pose.
9. Export at the original duration with the original audio.
```
