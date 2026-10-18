# 35 — Ukiyo-e Woodblock Print

**Look:** every frame is a hand-printed Japanese ukiyo-e woodblock print (Edo period, nishiki-e colour print). Dark sumi key-block lines are carved with a knife, so they swell and taper. Inside them sit flat areas of water-based pigment: gofun white-pink skin, sumi-black hair, indigo, vermilion, ochre and pale green garments, each with a darker printed pattern on top. The sky has a Prussian-blue bokashi gradient and the floor a soft beni-red glow. Everything sits on cream washi paper with visible fibres, baren mottling and a slight misregistration between the colour blocks. A vertical title cartouche (浮世三人図), a red artist seal and kentō registration marks finish the sheet. Each frame is "re-printed": the key line, the ink density, the mottling and the registration shift a little.

**Also called / where it trends:** "ukiyo-e style", "ukiyo-e filter", "Japanese woodblock print effect", "Hokusai style", "Hiroshige style", "nishiki-e", "Edo print AI video", "woodblock print AI". Ukiyo-e portrait and "you as an Edo woodblock print" filters keep trending on TikTok / Reels / Pinterest. It is a stock preset in AI video-style generators (Seedance / Kling style libraries, Hypernatural, ShortFast, HitPaw, Morphic).

**References:**
- https://www.pinterest.com/search/pins/?q=ukiyo-e%20woodblock%20print%20portrait%20modern (screenshot `refs/ref_1.png`): modern portraits redone as ukiyo-e prints. Note the flat colour, carved outlines, patterned garments, bokashi skies and cartouches.
- https://drama.so/seedance-2-5-prompts/lemomo-ukiyoe: a Seedance 2.5 ukiyo-e style prompt. It asks for a firm keyblock line, flat colour, bokashi gradients, Prussian blue, paper white and a vermilion seal (Lemomo, CC BY 4.0).
- https://github.com/lemomo-ai/lemo-opuscar/blob/main/styles/ukiyoe/STYLE.md: the source style sheet for that prompt (palette, line, gradient and composition rules for video).
- https://www.shortfast.com/styles/ukiyo-e-video-generator: an ukiyo-e video-style generator preset.
- https://app.hypernatural.ai/video-styles/ukiyo-e: Hypernatural's ukiyo-e video style.
- https://www.hitpaw.com/ai-video/how-to-turn-videos-into-ukiyo-e-art-style.html: a how-to on turning live footage into ukiyo-e style video.
- https://morphic.com/resources/images/ukiyo-e-ai: an ukiyo-e AI image style guide with example prompts.

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049), `example.mp4` (the whole clip, 12 fps, with audio) and `preview.webp`. This is a local approximation made with `render.py` (numpy + OpenCV + person masks):
- mean-shift flattening, then quantizing to a fixed 16-pigment Edo palette (Lab, chroma weighted), with median-cleaned colour areas
- gofun skin found by YCrCb, sumi hair only near faces, and flat garment colours with a darker printed pattern
- carved key lines with swelling and tapering width
- a Prussian-blue bokashi on the top and a beni glow on the floor
- washi fibres, baren mottling and a per-frame colour-block misregistration
- a 浮世三人図 cartouche, a 写画 seal, kentō marks and the paper margin

## Prompt

```text
I'm uploading one video clip. Convert it into a hand-printed Japanese UKIYO-E WOODBLOCK PRINT frame-by-frame animation, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Transform the footage into an Edo-period nishiki-e colour woodblock print, built from:
* a carved SUMI KEY-BLOCK line around every shape: dark, firm, swelling and tapering like a knife cut
* FLAT areas of water-based pigment, one block per colour, with no shading inside an area
* gofun white-pink skin with only the key line to describe the face
* solid sumi-black hair with fine carved strands at the hairline
* garments in indigo, vermilion, ochre, pale green and lilac, each with a darker PRINTED PATTERN
* BOKASHI: a Prussian-blue gradient wiped across the top of the sheet, and a soft beni-red glow at the floor
* cream WASHI paper with visible fibres and paper texture showing through the ink
* baren rubbing marks and slight mottling in large ink areas
* slight MISREGISTRATION: colour blocks shifted a hair from the key line
* a vertical title CARTOUCHE, a red artist SEAL and KENTŌ registration marks in the paper margin
The result should feel like someone:
PRINTED THE VIDEO FRAME
→ TRACED IT AS AN UKIYO-E DESIGN
→ CARVED THE KEY BLOCK IN CHERRY WOOD
→ CARVED ONE COLOUR BLOCK PER PIGMENT
→ PRINTED THE BLOCKS ONE BY ONE ON DAMP WASHI WITH A BAREN
→ WIPED A BOKASHI GRADIENT ON THE SKY BLOCK
→ STAMPED THE CARTOUCHE AND SEAL
→ PHOTOGRAPHED THE SHEET
→ CARVED AND PRINTED IT AGAIN FOR THE NEXT FRAME
→ ANIMATED IT FRAME-BY-FRAME.
CHARACTER — PRINTED, NOT REDRAWN
The MAIN HUMAN SUBJECT becomes an ukiyo-e figure, traced directly from the real frame.
Preserve the person's exact:
* identity
* face
* expression
* hairstyle
* glasses
* clothing and clothing pattern (stripes, prints, batik)
* accessories
* pose
* body proportions
* movement
* hand position
* interaction with objects
Keep modern clothing modern: do NOT change it into a kimono.
Do NOT turn the person into a samurai, a geisha or a kabuki actor.
Do NOT give them an Edo hairstyle.
Do NOT make them anime or manga.
The likeness comes from the real photo, printed in flat Edo colour.
KEY-BLOCK LINE
* one dark sumi line around every figure, face, hand, garment edge and object
* the line swells and tapers as if carved, thicker on the shadow side
* thin carved lines for eyes, brows, nose, mouth and glasses
* a few carved lines for garment folds
* the line never shades or blurs
FLAT COLOUR BLOCKS
* each area is one flat pigment, laid with slightly uneven density
* skin: gofun white-pink, very pale, almost no tone
* hair: solid sumi black
* garments: their real colour shifted to the nearest Edo pigment
* garment patterns (stripes, prints) printed as a second, darker block
* no photographic shading, no airbrush, no soft gradients inside a figure
BOKASHI AND BACKGROUND
* the room is simplified into flat printed planes: wall, door, floor, furniture
* the top of the sheet has a Prussian-blue bokashi that fades into paper white
* the floor has a soft beni / vermilion glow that fades upward
* light background areas stay bare washi paper
* no perspective blur, no depth of field
PAPER AND PRINTING
* cream washi with long fibres and faint wood-grain transfer
* baren mottling in large ink areas
* ink sitting slightly unevenly: a little darker at the edges of a block
* each colour block shifted a hair (1–3 px) from the key line
* a narrow paper margin around the image
CARTOUCHE, SEAL AND MARKS
* a vertical rectangular title cartouche with a short Japanese title in calligraphic script, in a quiet corner of the sheet
* a small red artist seal near it
* kentō registration marks at a corner of the margin
* never over a face or a hand
PALETTE RULES
Use a limited Edo pigment palette:
* sumi black
* Prussian blue (bero-ai) and indigo
* vermilion / beni red
* ochre / yellow
* pale green
* lilac / pale purple
* gofun white-pink
* washi cream
About 12–16 colours in total.
Do NOT use neon, gradients inside figures or photographic colour.
LAYER ORDER
A typical frame reads:
WASHI PAPER
↓
BOKASHI SKY + FLOOR GLOW
↓
FLAT COLOUR BLOCKS
↓
PRINTED GARMENT PATTERNS
↓
SUMI KEY-BLOCK LINE
↓
CARTOUCHE + SEAL + KENTŌ MARKS
↓
PAPER FIBRES + BAREN MOTTLING.
OBJECT CONTINUITY
IMPORTANT:
If the character is interacting with an object, preserve that object and print it.
Examples:
* phone
* glasses
* chair
* bag
* microphone
* clothing accessory
If an object is essential to the action, print it with its own key line and colour block.
Do NOT let it dissolve into the background.
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
The underlying character movement must remain exactly faithful to the source footage.
The PRINT boils.
The HUMAN MOTION does NOT.
If the head moves:
the printed head and its key line move with it.
If the hand moves:
the printed hand follows.
If the body turns:
the colour blocks and garment pattern follow.
If the character interacts with an object:
the object moves exactly with the original action.
NO key line lagging behind the body.
NO colour blocks from the previous frame.
NO cartouche or seal drifting around the sheet.
FRAME-BY-FRAME BOILING EFFECT
THIS IS CRITICAL.
Every frame must look like it was CARVED AND PRINTED AGAIN.
Allow:
* the key line to swell and taper slightly differently
* small carving nicks along the line
* ink density and baren mottling to change
* the colour-block registration to shift by a pixel or two
* paper fibres to change
* the edge of the bokashi to move a little
This creates a gentle, hand-printed BOILING animation.
CONTROLLED BOIL
The boil must stay SMALL.
The pigment of each element (skin, hair, each garment, wall, sky) stays the SAME across frames.
The cartouche, seal and kentō marks stay in the same place.
Faces keep the same carved features.
Do NOT let colours swap between frames.
Do NOT let the bokashi jump.
DO NOT
Do NOT make it a posterize or cel-shade filter.
Do NOT make it anime, manga or a modern vector illustration.
Do NOT use photographic shading or soft airbrush gradients on the figures.
Do NOT change modern clothing into kimono.
Do NOT add Mount Fuji, waves or cherry blossoms that are not in the footage.
Do NOT put text or the seal over faces.
Do NOT create new poses.
Do NOT change anatomy.
Do NOT change clothing.
Do NOT replace the person's face.
Do NOT freeze the same print across all frames.
Do NOT smooth the motion.
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
* NO key lines
* NO flat colour
* NO paper texture
* NO cartouche or seal
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
Do NOT begin the ukiyo-e transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – UKIYO-E STYLING (AFTER MY CONFIRMATION ONLY)
Style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation, so the print sits exactly on the real pose.
Apply every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT restyle a whole shot from one keyframe: the boil only works if every frame is printed separately.
Lock the look first: generate frame_01 and show it to me with the pigment of each element (skin, hair, each garment, wall, floor), the bokashi colours, the key-line weight, and the cartouche text, seal and position. Keep those choices for every frame.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, palette, cartouche position or the style rules broke — regenerate those frames only.
The final video must feel like AN EDO WOODBLOCK PRINT THAT CAME ALIVE: real people, carved and printed in flat pigment on washi, re-printed 12 times per second.
The image should deliberately contain:
* a carved, swelling sumi key line
* flat pigment areas with printed patterns
* bokashi gradients
* washi fibres and baren mottling
* slight colour-block misregistration
* a cartouche, a red seal and kentō marks
* slight print-to-print irregularity.
Avoid polished digital perfection.
```
