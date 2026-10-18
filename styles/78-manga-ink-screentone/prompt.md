# 78 — Manga Ink Screentone

**Look:** The clip becomes a page from a printed black-and-white manga. Every pixel is either black ink or white paper. The people are drawn with crisp G-pen contour lines and a heavier silhouette line. Hair and the deepest shadows are solid black. Mid-tones are cut from flat dot-screen screentone sheets in two or three weights. Faces stay mostly clean white paper with only the key features inked. The room behind becomes lighter line work under a smooth gradation tone. Thin concentration lines (shuchūsen) rush in from the panel edges toward the people. The picture sits inside a black panel border with a white page gutter. There is no colour anywhere. The fine round dots are mechanical and grey-free. That separates it from the colour Ben-Day dots of 07 Pop Art and 53 90s Comic, the gritty toner and collage of 01 Punk Photocopy, and the pixel-grid dither of 11 Pixel Dither.

**Also called / where it trends:** "manga edit", "manga filter", "manga black and white edit", "anime manga effect" (CapCut templates), "manga panel effect", "screentone effect", "漫画风" (Douyin), "マンガ風加工" (Japan). It is one of the most-used photo-to-manga transformations on TikTok and CapCut. It also appears as AI photo filters ("Classic Manga") and in YouTube tutorials that turn a video into a manga page. Recent edits often add speed lines or focus lines.

**References:**
- https://www.tiktok.com/search?q=manga%20edit%20capcut%20black%20white (screenshot `refs/ref_1.png`): TikTok search for black-and-white manga edits made in CapCut. The edits are pure B/W with heavy contours and tone.
- https://www.tiktok.com/@awsalater/video/7689588162049428766: a manga-edit trend clip. A video is turned into black-and-white manga panels.
- https://www.tiktok.com/@annaliise.cc/video/7659606110558620948: a manga-filter edit of a selfie video, B/W ink plus screentone.
- https://www.tiktok.com/@.gmx8/video/7617074014028156181: a CapCut manga-transition template with focus lines.
- https://www.youtube.com/watch?v=xMzuMC_bhaM: a YouTube tutorial (168K views) on turning a clip into a manga look.
- https://www.pinterest.com/search/pins/?q=manga%20screentone%20panel%20black%20and%20white (screenshot `refs/ref_2.png`): screentone sheets and B/W manga panels. They show the dot-screen weights and gradation tones.
- https://www.pinterest.com/search/pins/?q=manga%20panel%20black%20and%20white%20screentone%20speed%20lines (screenshot `refs/ref_3.png`): speed lines and concentration lines in manga panels.
- https://imagetomanga.com/manga-filter: an AI photo-to-manga filter. Its "Classic Manga" preset is pure B/W ink, fine contours, hatching and screentone.

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049), `example.mp4` (the whole clip at 12 fps with the original audio) and `preview.webp`. This is a local approximation made with `render.py` (numpy + OpenCV, the person masks, and Apple Vision face landmarks in `faces.json`). The grey image is CLAHE-equalised and bilateral-smoothed into flat shapes. Skin inside the face outline is lifted toward white paper. The values are then cut into three layers: solid black, a heavy 52 % dot tone and a light 22 % dot tone, on a 45° round-dot screen. The room gets a stepped gradation tone on a finer screen. XDoG edge passes give the G-pen lines, and the mask gives a thick silhouette line. Lines wobble slightly every 2 frames. 230 tapering focus-line wedges are re-drawn every 2 frames around the people, with a white halo kept off them. A black panel border and a white gutter frame the page.

## Prompt

```text
I'm uploading one video clip. Convert it into a BLACK-AND-WHITE MANGA INK + SCREENTONE frame-by-frame animation: every frame should look like a panel from a printed Japanese manga page, inked with a G-pen and toned with dot-screen sheets, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Black-and-white manga page, G-pen ink line art, solid black spot fills, flat dot-screen screentone, gradation tone, concentration lines, printed on white paper, panel border.
Transform the footage into a manga panel built from:
* PURE BLACK INK and WHITE PAPER only
* crisp G-pen CONTOUR LINES with natural thick-thin pressure
* a HEAVIER OUTER LINE around every person
* SOLID BLACK fills for hair, pupils and the deepest shadows
* white highlight streaks cut into the black hair
* FLAT round-dot SCREENTONE in 2–3 weights for clothes and shadow shapes
* hard-edged tone shapes, as if cut from tone sheets with a knife
* clean white faces with only the key features inked
* a lighter line drawing of the room under a smooth GRADATION TONE
* thin tapering CONCENTRATION LINES (shuchūsen) in the background, aimed at the people
* a black PANEL BORDER inside a white page gutter
The result should feel like someone:
PENCILLED THE SCENE ON MANGA MANUSCRIPT PAPER
→ INKED IT WITH A G-PEN AND A BRUSH FOR THE BLACKS
→ CUT AND BURNISHED SCREENTONE SHEETS ONTO THE SHADOWS
→ RULED CONCENTRATION LINES BEHIND THE CHARACTERS
→ PRINTED IT IN A WEEKLY MANGA MAGAZINE
→ ANIMATED IT PANEL BY PANEL.
CHARACTER — INKED, NOT REPLACED
The people become INKED MANGA DRAWINGS of themselves, traced from the frame.
Preserve the person's exact:
* identity
* face
* expression
* hairstyle
* glasses
* clothing
* clothing patterns (simplified into line and tone, not removed)
* accessories
* pose
* body proportions
* movement
* hand position
* interaction with objects
Keep realistic proportions and the real face shape.
Do NOT turn them into chibi, big-eyed anime or a different character.
Do NOT enlarge the eyes or shrink the nose and mouth.
Do NOT redraw the pose.
INK RULES
* Lines are pure black, crisp, with slight thick-thin pressure.
* The outer silhouette of each person is the heaviest line.
* Inner folds, glasses, eyes, brows, nose and lips get finer lines.
* Hair is mostly solid black with a few white sheen streaks following the hair flow.
* The darkest shadows (under the chin, inside the collar, deep folds) are solid black.
* No sketchy construction lines, no grey pencil.
SCREENTONE RULES
* Mid-tones are flat ROUND-DOT screentone at about 45°, never grey wash.
* Use 2–3 tone weights: light (about 20 %), medium (about 50 %) and solid black.
* Tone shapes have clean hard edges, like knife-cut tone sheets.
* Busy fabric patterns (batik, stripes) become simplified tone shapes plus a few lines.
* Faces stay almost entirely white paper; at most a small tone shadow under the jaw.
* The dots are small, regular and black. They are NOT large colour Ben-Day dots.
BACKGROUND
* The room stays recognisable but drawn LIGHTER than the people: thinner lines, fewer blacks.
* Large areas get a smooth GRADATION TONE (dot size fading across the area).
* Thin black CONCENTRATION LINES radiate in from the panel edges toward the people.
* Leave a clean white gap around the people so the focus lines never touch them.
* The figures must always read first.
PAGE
* Pure white paper.
* A solid black panel border a few pixels thick.
* A white gutter outside the border.
* No speech balloons, no sound-effect lettering, no text.
PALETTE
Black ink. White paper.
Nothing else. Absolutely NO colour, NO sepia, NO grey wash.
OBJECT CONTINUITY
If the character holds an object, it is inked and toned like the rest and stays attached to the hand.
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
The inked people must match the source frame exactly.
Lines, blacks and tone shapes follow the people as they move.
NO tone pattern frozen in place while the body moves under it.
NO lines left behind from a previous frame.
FRAME-TO-FRAME INK LIFE
THIS IS CRITICAL.
It must feel like a re-inked panel on every drawing, not a still filter.
Allow between consecutive frames:
* contour lines to wobble by about 1 pixel
* line weight to vary slightly
* the concentration lines to be re-ruled every 2 frames (new random spacing)
Keep FIXED:
* the tone dot size and angle (screentone is mechanical; it does not boil)
* pure black and white only
* the panel border and gutter
DO NOT
Do NOT add any colour, sepia or grey.
Do NOT use large Ben-Day dots or pop-art colour dots.
Do NOT use photocopy toner grit, torn-paper collage or a punk zine look.
Do NOT use a pixel grid or ordered pixel dither.
Do NOT use crosshatched engraving lines for mid-tones.
Do NOT use soft airbrushed shading.
Do NOT turn the people into anime or chibi characters.
Do NOT add speech balloons, lettering or sound effects.
Do NOT let focus lines cross faces or bodies.
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
* NO black-and-white conversion
* NO line art or inking
* NO screentone
* NO focus lines or panel border
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
Do NOT begin the manga ink + screentone transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – MANGA INK + SCREENTONE STYLING (AFTER MY CONFIRMATION ONLY)
First, tell me the screentone weights and dot angle you will use, and where the concentration lines will converge.
Then style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation, so the people are exactly that frame.
Apply every style rule above, with the SAME tone weights, line weight and panel border on every frame.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing, pure black-and-white or the tone pattern broke — regenerate those frames only.
The final video must feel like A PRINTED MANGA PAGE COME ALIVE: black ink, white paper, dot screentone, focus lines, 12 frames per second.
The image should deliberately contain:
* crisp black G-pen contours
* solid black hair and shadows
* flat round-dot screentone
* a gradation-toned background
* concentration lines aimed at the people
* a black panel border on white paper.
Avoid photographic grey tones.
```
