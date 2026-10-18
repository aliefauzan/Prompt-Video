# 12 — ASCII Terminal Phosphor

**Look:** the clip rebuilt entirely from monospace text characters on a fixed character grid, glowing green on a black CRT terminal: character density follows brightness (`@#%&` in the faces and shirts, `.:'` in the dim room), silhouettes traced with direction glyphs (`- / | \`), phosphor bloom, scanlines, a slow rolling band, slight barrel curvature and vignette, a shell prompt line on top and a status bar at the bottom. A few characters re-roll every frame, so the image "boils" like live terminal output. Optional mode: amber P3 phosphor (used here for 00:08–00:11).

**Also called / where it trends:** "ASCII art filter", "ASCII video effect", "text-mode / matrix effect", "terminal edit", "hacker green CRT", "turn video into ASCII" (TikTok, YouTube Shorts, Instagram Reels; After Effects / DaVinci / TouchDesigner ASCII tutorials; browser ASCII generators).

**References:**
- https://www.youtube.com/shorts/fRERcwO01D0 — "hajime ASCII art" Short: white glyph figures on black, density by luminance (refs/ref_2.png)
- https://www.youtube.com/shorts/ozQ3QqyxzZg — green CRT terminal ASCII edit with "ACCESS GRANTED" chrome (refs/ref_3.png)
- https://www.youtube.com/results?search_query=ascii+art+video+effect — Shorts grid of the ASCII trend (refs/ref_1.png)
- https://www.youtube.com/shorts/IXF69XQs9Vo — "Free After Effects Plugin - ASCII Generator"
- https://www.youtube.com/shorts/danD7Kw1XQY — ASCII video-effect short from the same search
- https://asciigen.art/ , https://krkart.cc/effects/asciikit.html , https://modulate.to/effects/ascii — browser ASCII video generators (cell size, ramp, colour)
- https://github.com/xianfengting/ascii-video-converter , https://github.com/ideoshi/glyphloop — open-source video-to-ASCII converters

**Example:** `example.png` (6 frames of the test clip), `before_after.png`. Local approximation in `render.py`: 12×20 px cells (135×54 characters), Menlo glyph atlas sorted by ink coverage, people contrast-stretched and bright, room sparse and dim, edge glyphs from the mask/image gradient, 2.5% glyph flicker per frame, green phosphor bloom + 4-px scanlines + rolling band + barrel + vignette, prompt and status lines; amber on frames 97–132. All 179 frames are in `frames/`.

## Prompt

```text
I'm uploading one video clip. Convert it into an ASCII-ART CRT TERMINAL frame-by-frame animation matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.

TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.

CORE VISUAL STYLE
Transform the footage into live ASCII output on an old monochrome CRT terminal, built from:
* ONLY monospace text characters on a fixed character grid (about 135 columns × 54 rows for a 3:2 frame)
* every cell the same size, perfectly aligned in rows and columns
* character DENSITY = brightness: dense glyphs (@ # % & M W 8 B) for bright areas, light glyphs (. : ' ` , -) for dark areas, empty cells for black
* direction glyphs ( - / | \ _ ) tracing silhouettes and strong edges
* glowing green P1 phosphor on near-black glass
* soft phosphor bloom around bright characters
* fine horizontal scanlines
* a slow bright rolling band moving down the screen
* slight barrel curvature and a dark vignette at the corners
* a shell prompt line at the top and a status bar at the bottom
The result should feel like someone:
PRINTED THE VIDEO FRAME
→ SAMPLED IT ON A CHARACTER GRID
→ REPLACED EVERY CELL WITH THE CHARACTER OF MATCHING INK DENSITY
→ TRACED THE SILHOUETTES WITH SLASHES AND PIPES
→ PIPED THE TEXT TO A GREEN-PHOSPHOR TERMINAL
→ FILMED THE GLOWING CRT
→ ANIMATED IT FRAME-BY-FRAME.

CHARACTER — ASCII FIGURES
Every person is rebuilt from text characters ON TOP OF their exact footage pose.
Preserve each person's exact:
* identity (readable face layout: hairline, eyes, nose shadow, mouth, jaw)
* face shape
* expression
* hairstyle silhouette
* clothing shapes and big patterns (stripes become rows of dense/light glyphs)
* glasses (as visible rings of glyphs)
* pose
* body proportions
* movement
* hand position
* interaction with objects
People must be the BRIGHTEST, DENSEST text in the frame.
Use local contrast inside each person so eyes, mouth, hair and folds stay readable.
Do NOT invent a new character.
Do NOT change pose, age, gender or body type.

CHARACTER SET AND GRID
* One monospace font for everything (Menlo / Courier / IBM VGA style).
* A density ramp of about 40–70 printable ASCII characters, ordered by ink coverage, for example:
  " .'`,:;-~_^!i|lI1+=r*/\)(?7tfjxcvzunoJCLYT{}[]s35a2eSkhdbqpGwmZO0Q8&%#B@M$W"
* ONLY printable ASCII. No emoji, no box-drawing blocks, no Unicode shading blocks.
* The grid is FIXED: same columns, same rows, same cell size in every frame.
* Edges of people use direction glyphs that follow the edge angle:
  - horizontal edge, / rising edge, | vertical edge, \ falling edge.

BACKGROUND — DIM TEXT ROOM
The room stays in the same place but is printed much DIMMER and SPARSER than the people:
* mostly dots, colons, commas and empty cells
* only the strongest shapes of the room (window frame, screen, chair, plants, wall panels) as faint glyphs
* bright windows become fields of medium-density characters, not solid blocks
* large dark areas stay EMPTY (pure black glass)
The people must separate clearly from the background.

TERMINAL CHROME
* top line: a shell prompt, for example
  user@crt:~$ ./ascii --live --fps 12 clip.mov   [frame 013]_
  with a blinking cursor block or underscore
* bottom line: a status bar, for example
  -- 135x54 -- luma ramp 41 -- P1 GREEN -- 00:01.00
  with a running timecode
* the chrome is the same font and the same phosphor colour, slightly dimmer
* the chrome never covers a face

PHOSPHOR AND CRT
* phosphor colour: green (#66ff4d family) on near-black green-tinted glass
* bright characters bloom softly into neighbouring cells
* thin dark scanlines across the whole screen
* a faint bright band rolls slowly from top to bottom
* slight brightness flicker between frames
* slight barrel curvature and vignette
* faint glass noise
Do NOT use other colours in green mode.

OPTIONAL MODE — AMBER PHOSPHOR
For a short section (or the whole clip, if requested), switch the phosphor to amber P3 (#ffb81a family):
* the same grid, the same characters, the same chrome text with "P3 AMBER"
* the same bloom, scanlines and curvature
Switch on a cut or a beat, never mid-motion.

LAYER ORDER
BLACK GLASS
↓
DIM SPARSE BACKGROUND TEXT
↓
BRIGHT DENSE PEOPLE TEXT
↓
EDGE GLYPHS ON SILHOUETTES
↓
PROMPT LINE + STATUS BAR
↓
PHOSPHOR BLOOM, SCANLINES, ROLLING BAND, CURVATURE, VIGNETTE.

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
Print the object in text characters, in the same place, moving exactly with the original action.
Do NOT drop objects while converting the character into ASCII.

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
the text face follows.
If the hand moves:
the hand glyphs follow.
If the body turns:
the edge glyphs follow.
NO floating text figures.
NO previous-frame silhouette.
NO delayed edges.

TEXT BOIL (FRAME-TO-FRAME)
ASCII output is re-printed every frame. Between consecutive frames:
* the grid never moves, never scales, never rotates
* about 2–3% of the characters re-roll to a different glyph of similar density (live-output flicker)
* characters on moving people change with the motion
* static background characters stay mostly the same
* the cursor blinks, the timecode advances, the rolling band moves down
Do NOT let the whole frame re-randomize.
Do NOT let the character set, font or phosphor colour drift.

DO NOT
Do NOT make it photographic.
Do NOT show any photo pixels or gradients under the text.
Do NOT use a halftone, dot or pixel-mosaic filter instead of real characters.
Do NOT use proportional fonts, bold/italic mixes or random font sizes.
Do NOT use emoji, Unicode blocks or box-drawing characters.
Do NOT use full-colour text (one phosphor colour only).
Do NOT make "Matrix" falling-code rain over the people.
Do NOT replace the person's face or change identity.
Do NOT create new poses.
Do NOT change anatomy.
Do NOT change clothing.
Do NOT add text other than the prompt line and the status bar.
It must feel like REAL ASCII TEXT OUTPUT GLOWING ON A CRT TERMINAL.

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
* NO ASCII conversion
* NO character grid
* NO phosphor colour
* NO scanlines or CRT effects
* NO terminal chrome
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
Do NOT begin the ASCII transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.

STAGE 3 – ASCII EVERY FRAME (ONLY AFTER MY CONFIRMATION)
1. Restyle EVERY extracted frame individually with Seedream 5.0 Pro, using that exact original frame as the image reference.
2. Keep each output at the source resolution and framing. No crop, no zoom, no reframing.
3. Keep the SAME character grid (columns × rows), the SAME font, the SAME density ramp and the SAME phosphor colour in every frame. If the model drifts, rebuild the frame from the original with a deterministic ASCII pass (sample luminance per cell, pick the glyph by ink coverage) and use the Seedream output only as the look reference.
4. Replace each clip on the timeline IN PLACE with its ASCII version. Same order. Same 1/12 second duration.
5. Lock the style sheet before generating: the same people brightness, background sparsity, edge-glyph rule and chrome text layout in EVERY frame. Re-use the same wording for every frame prompt.
6. Update only the frame number and timecode in the chrome per frame.
7. If the amber mode is used, apply it to a continuous run of frames that starts on a cut or a beat.
8. Check every 12th frame against the original: same pose, same expression, same position. Regenerate any frame that is off-pose or unreadable.
9. Export at the original duration with the original audio.
```
