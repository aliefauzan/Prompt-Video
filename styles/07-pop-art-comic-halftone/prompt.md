# 07 — Pop Art Comic Halftone

**Look:** every frame becomes a Lichtenstein-style 1960s comic panel. Skin is red Ben-Day dots, colour is flattened to newsprint CMYK (yellow, red, blue, black, paper), and every figure gets thick black ink outlines with solid spot blacks. The plates sit slightly off-register. Backgrounds switch between dot fields, sunbursts, speed lines and a simplified room. Panels also carry a caption box, speech balloons and SFX bursts (POW! WOW! BAM!), and a black panel border with a gutter. Line wobble and dot phase boil every frame.

**Also called / where it trends:** "comic book effect", "comics trend", "pop art effect", "comic halftone edit", "Lichtenstein filter", "AI comic trend", "video to comic". CapCut comics-effect tutorials and the "AI COMIC TREND" on TikTok, Premiere / After Effects pop-art halftone tutorials on YouTube, Pinterest Lichtenstein portrait boards, and AI "video to comic style" tools.

**References:**
- https://www.tiktok.com/@duekneel/video/7308758511419264257 — CapCut "comics" effect tutorial: dots, outlines, speech bubble
- https://www.tiktok.com/search/video?q=comic%20book%20effect%20edit%20capcut — TikTok search, screenshot `refs/ref_2.png`: "Comics trend tutorial on CapCut", "AI COMIC TREND", "Cara buat efek pop art comics"
- https://www.pinterest.com/search/pins/?q=pop%20art%20comic%20halftone%20portrait%20lichtenstein — Pinterest search, screenshot `refs/ref_1.png`: Ben-Day skin, thick outlines, primary flats, speech balloons
- https://effect.app/effects/halftone-screen — halftone screen video effect preset
- https://borisfx.com/blog/create-after-effects-halftone-plugin-2-methods/ — two ways to build a halftone dot look in After Effects
- https://www.youtube.com/watch?v=peyJNqGrn98 — Pop Art effect tutorial in Premiere Pro
- https://www.somake.ai/tools/video-to-comic-style — AI "video to comic style" tool (shows the trend as a product)

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049). Local approximation rendered with `render.py` (numpy + OpenCV + Pillow fonts + person masks).

## Prompt

```text
FULL PROMPT FOR POP ART COMIC EDIT:

I'm uploading one video clip. Convert it into a 1960s POP ART COMIC PANEL frame-by-frame animation in the style of Roy Lichtenstein: Ben-Day dots, thick black ink outlines, flat newsprint CMYK colour, speech balloons and SFX lettering.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.

TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.

CORE VISUAL STYLE
Transform the footage into a printed comic-book panel built from:
* BEN-DAY DOTS (evenly spaced round dots of one flat colour)
* thick, confident BLACK INK OUTLINES
* solid BLACK spot shadows
* flat newsprint colours: YELLOW, RED, BLUE, BLACK, PAPER WHITE
* slightly off-register colour plates
* cheap yellowed newsprint paper
* a black PANEL BORDER with a white gutter
* rectangular CAPTION BOXES
* round SPEECH BALLOONS with tails
* jagged SFX bursts with bold lettering (POW! WOW! BAM!)
* action lines, speed lines and sunbursts
* 1960s pop-art / Lichtenstein aesthetics
The result should feel like someone:
PRINTED THE VIDEO FRAME
→ TRACED IT IN INK AS A COMIC PANEL
→ FILLED IT WITH FLAT CMYK COLOUR
→ SCREENED THE SKIN AND SKY WITH BEN-DAY DOTS
→ HAND-LETTERED THE BALLOONS AND SFX
→ PRINTED IT ON CHEAP NEWSPRINT, SLIGHTLY OFF-REGISTER
→ SCANNED THE PAGE BACK IN
→ ANIMATED IT FRAME-BY-FRAME.

CHARACTER — INKED COMIC VERSION OF THE REAL PERSON
The people become INKED COMIC FIGURES that match the footage exactly.
Preserve each person's exact:
* identity and likeness
* face shape and features
* expression
* hairstyle
* clothing and its patterns (stripes, prints)
* accessories (e.g. glasses)
* pose
* body proportions
* movement
* hand position
* interaction with objects
Trace the real person. Do NOT invent a new character.
Do NOT turn them into a generic cartoon or anime face.
Each face must stay recognisable as the same person.

INK LINES
* thick black contour around every figure (heavier on the outside edge)
* thinner interior lines for eyes, brows, nose, lips, ears, collar, folds
* solid black spot fills in hair shadows, pupils, deep clothing folds and cast shadows
* lines slightly brushy, with tapered ends, like brush and nib ink
* NOT a uniform-width digital stroke
* NOT an edge-detection filter

SKIN — BEN-DAY DOTS
Skin is the signature:
* paper-white base with evenly spaced RED (or pink-red) Ben-Day dots
* dots on a regular diagonal grid, all the same size within an area
* slightly darker / denser dots in the shadow side of the face
* lips flat red
* no smooth skin shading, no airbrush

FLAT COLOUR RULES
Reduce every colour to the comic palette:
* light warm tones → flat YELLOW
* dark warm tones → flat RED
* cool and dark tones → flat BLUE
* mid cool tones → BLUE Ben-Day dots on paper
* highlights and white garments → PAPER WHITE
* deepest shadows → solid BLACK
Hair: black with a few flat blue highlight bands.
Patterns such as stripes stay as clean bands of flat colour.
Use flat colour shapes only. Do NOT use gradients.

PALETTE
* YELLOW approximately #FFDA14
* RED approximately #E4202C
* BLUE approximately #185CC4
* BLACK ink
* PAPER: warm newsprint off-white, approximately #FAF3E2
Nothing else. Do NOT use photographic colour, pastel tones, neon or rainbow gradients.

PRINT TEXTURE
* colour plates offset 2–4 px from the black line plate
* dots slightly soft and uneven, as on cheap newsprint
* faint yellowing and paper grain
* tiny ink specks
The print must look like a real 1960s comic page, not a clean vector graphic.

BACKGROUND OPTIONS
Switch between these background treatments in sections of a few seconds:
1. DOT FIELD — a flat background of large coloured Ben-Day dots (blue or red on paper).
2. SUNBURST — radiating yellow / red rays behind the group.
3. SIMPLIFIED ROOM — the original office traced in ink and flat colour, with less detail than the people.
4. SPEED LINES — black radial or horizontal action lines on paper behind the group.
Keep the original composition in every option.

LETTERING
Each section carries ONE text element, hand-lettered in comic capitals:
* a yellow CAPTION BOX at a top corner (e.g. "MEANWHILE, AT THE OFFICE...")
* a white SPEECH BALLOON with a tail pointing at the speaker's mouth (e.g. "HEY! YOU'RE IN THE COMIC NOW!")
* a jagged yellow or red SFX BURST with huge outlined letters (e.g. "WOW!", "POW!", "BAM!")
Rules:
* lettering must be correctly spelled and clearly readable
* keep balloons and boxes OFF the faces
* the same text stays in the same place for the whole section

PANEL BORDER
* a thick black panel border just inside the frame
* a thin paper-white gutter outside it
* the border slightly hand-ruled, not perfectly straight

OBJECT CONTINUITY
IMPORTANT:
If a person is interacting with an object, keep that object.
Examples:
* phone
* chair
* bag
* glasses
* clothing accessory
Ink and colour it like everything else.
Do NOT accidentally remove it.

DO NOT
Do NOT use photographic shading or real skin texture.
Do NOT use smooth gradients or airbrush.
Do NOT use a generic cartoon / anime / 3D look.
Do NOT use a cheap edge-detect + posterize filter.
Do NOT make the dots tiny or random. They must be clear, even Ben-Day dots.
Do NOT misspell lettering or generate gibberish text.
Do NOT cover faces with balloons or SFX.
Do NOT add colours outside the comic palette.
Do NOT create new poses.
Do NOT change anatomy.
Do NOT change clothing.
Do NOT replace anyone's face.
It must feel INKED, LETTERED and PRINTED like a real comic page.

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
* NO ink lines
* NO Ben-Day dots
* NO flat colour
* NO balloons, captions or SFX
* NO panel border
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
Do NOT begin the comic transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.

STAGE 3 – POP ART COMIC STYLING (AFTER MY CONFIRMATION ONLY)
Style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation.
Apply every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT restyle a whole shot from one keyframe.
Plan the sections first and list them to me (frame range, background option, lettering element and its exact text and position) before generating.
Within a section keep the same background, the same lettering, the same balloon / box / burst position and the same colour assignment for each garment.
If Seedream cannot keep the lettering perfectly consistent, generate the panel art per frame and set the balloon / caption / SFX as a locked graphic layer on top.

CHARACTER CONTINUITY LOCK
The SAME people must remain recognizable in every frame.
Never change:
* identity
* facial structure
* hairstyle
* clothing and its flat colours
* accessories
* body proportions
* anatomy
* expression
* pose
* action
* position
Generation is for VISUAL STYLE ONLY.

PERFECT MOTION TRACKING
The STYLE jitters.
The HUMAN MOTION does NOT.
The underlying movement must remain exactly faithful to the source footage.
If a head moves, the inked figure follows.
If a hand moves, the inked figure follows.
A balloon tail keeps pointing at its speaker.
NO delayed outline.
NO previous-frame silhouette.

FRAME-BY-FRAME BOILING EFFECT
THIS IS CRITICAL.
Every frame should feel separately inked and printed.
Allow between consecutive frames:
* ink line wobble and slight thickness changes
* the Ben-Day dot grid phase to shift slightly
* the colour-plate offset to wobble by 1–2 px
* newsprint grain and specks to change
* speed lines / sunburst rays to flicker slightly
* the panel border to wobble by 1 px
Do NOT make the wobble so large that faces swim.
The result must feel like FLIPPING THROUGH COMIC PANELS.

The image should deliberately contain:
* even, clearly visible Ben-Day dots
* bold black ink contours
* solid spot blacks
* flat primary colours
* plate misregistration
* newsprint paper tone
* crisp hand-style lettering.
Avoid modern digital polish.
```
