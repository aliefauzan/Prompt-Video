# 14 — Magazine Cover Typography

**Look:** every frame becomes a glossy editorial magazine cover: a giant serif or condensed MASTHEAD across the top that sits BEHIND the subjects' heads (depth via the person matte), stacked cover lines down both sides in heavy condensed caps + Didot italics, a single accent colour, a red "NEW ISSUE" sticker, barcode + price, editorial colour grade or B&W, fine print grain. Type drops and types on at each new "cover", then tracks open slowly — kinetic, not static.

**Also called / where it trends:** "magazine cover edit", "text behind person", "text behind subject / depth effect", "Vogue cover edit", "kinetic typography edit", "editorial cover trend" — CapCut text-behind-person templates and tutorials on TikTok, IG Reels, YouTube Shorts; Pinterest magazine-cover edits; LinkedIn creator-tips posts (2026).

**References:**
- https://www.pinterest.com/search/pins/?q=magazine%20cover%20edit%20text%20behind%20person — screenshot `refs/ref_1.png`: FOCUS / MOTION / VISUAL / create covers, heads overlapping mastheads, side cover lines, barcodes, accent colours
- https://www.capcut.com/resource/how-to-put-text-behind-a-person-in-capcut — "The Viral Depth Effect" (Sept 2026): text layer between background and auto-cut-out subject
- https://www.linkedin.com/posts/bizcrown-media_bizcrownmedia-capcutedit-videoeditingtips-activity-7412689154511400960-buFe — 'Want that professional "magazine cover" look for your videos?' (Jan 2026)
- https://www.capcut.com/explore/text-behind-person — CapCut text-behind-person template gallery
- https://www.tiktok.com/@byrvm_contentcreation/video/7463064484005809430 — TikTok tutorial: text behind AND in front effect
- https://www.tiktok.com/@roydmedia/video/7525781552307997959 — TikTok CapCut kinetic typography tutorial
- https://www.youtube.com/watch?v=HLbrOPRbXhU — "How to Create a Magazine Cover Effect in CapCut"
- https://gizzmotion.com/templates/studio/magazine-cover/ — motion template "Magazine Cover: Editorial"

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049). Local approximation rendered with `render.py` (numpy + OpenCV + Pillow fonts + person masks); 17 frames in `frames/`.

## Prompt

```text
I'm uploading one video clip. Convert it into a bold EDITORIAL MAGAZINE COVER / KINETIC TYPOGRAPHY frame-by-frame animation matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Transform the footage into a sequence of high-fashion magazine covers built from:
* the ORIGINAL photographic frame, editorially colour-graded
* a GIANT MASTHEAD word across the top of the frame
* the masthead placed BEHIND the people's heads (depth effect)
* stacked COVER LINES down the left and right edges
* heavy condensed sans-serif caps mixed with elegant serif italics
* ONE strong accent colour per cover
* a round sticker / badge
* a barcode block with price and issue number
* a thin kicker line above the masthead (issue name, number, month)
* fine print grain and subtle glossy-paper finish
* type that ANIMATES: drops in, types on, tracks open
* occasional studio-backdrop covers (seamless paper) and B&W covers with one spot colour
The result should feel like someone:
SHOT A COVER STORY
→ PICKED THE BEST FRAME
→ CUT THE PEOPLE OUT
→ SET A HUGE MASTHEAD BEHIND THEIR HEADS
→ LAID OUT THE COVER LINES
→ ADDED THE BARCODE AND STICKER
→ PRINTED IT ON GLOSSY STOCK
→ ANIMATED EVERY ISSUE FRAME-BY-FRAME.
CHARACTER — COVER STAR
The MAIN HUMAN SUBJECT(S) stay fully PHOTOGRAPHIC: they are the cover stars.
Preserve the person's exact:
* identity
* face
* expression
* hairstyle
* clothing
* accessories
* pose
* body proportions
* movement
* hand position
* interaction with objects
Do NOT redraw the character.
Do NOT turn them into a cartoon or illustration.
Do NOT beautify, slim, reshape or retouch faces beyond normal editorial colour grading.
EDITORIAL PHOTO GRADE
Grade the photograph like a printed fashion cover:
* clean editorial contrast (rich but not crushed blacks)
* gently lifted, creamy highlights
* WARM grade on some covers, COOL grade on others
* full B&W grade on selected covers (black-and-white photo + one spot-colour masthead or cover lines)
* skin tones natural and flattering
* no heavy filters, no HDR, no oversaturation
MASTHEAD — THE HERO TYPE
Every cover has ONE giant masthead word across the top.
Example words (choose short, 4–6 letters): MOTION, TRIO, FOCUS, OFFICE, VISUAL.
The masthead should be:
* huge (about the top third of the frame, edge to edge)
* in a classic high-contrast Didone serif (Didot / Bodoni style) OR a heavy condensed grotesk (Helvetica Condensed Black style)
* tightly tracked
* one flat colour: RED, BLACK, WHITE, LIME or YELLOW
* perfectly spelled, crisp, print-quality letterforms
DEPTH — MASTHEAD BEHIND THE HEADS
THIS IS THE SIGNATURE OF THE STYLE.
The masthead sits BEHIND the people:
heads, hair and shoulders overlap and hide parts of the letters,
exactly like a real magazine cover where the cover star's head covers the logo.
The letters must stay readable even when partly hidden.
The overlap edge must follow the hair and head silhouette exactly (clean, natural hair edge, no halo, no box).
Optionally, on some covers, a second big word or a cover line passes IN FRONT of the lower body
(text behind the head, in front of the torso: "woven" depth).
NEVER put type over a face.
COVER LINES
Down the left and right edges, stack 3–5 short cover lines:
* a small light/medium caps line ("THE NEW", "STAY IN")
* one or two heavy condensed caps lines ("OFFICE CREW", "LATE NIGHTS"), one of them in the accent colour
* one serif italic line in lower case ("3 friends, 1 desk", "the 9-to-5 reset")
Also add:
* a kicker line centred above the masthead: "THE WORKPLACE ISSUE · No. 14 · OCTOBER 2026"
* a thin accent-coloured rule above the left cover lines
* a bottom line: "INSIDE: THE STRIPE THAT STARTED IT ALL / P. 42"
All words must be real, correctly spelled English.
Keep cover lines short and punchy.
Keep them on the margins, never across faces.
STICKER, BARCODE, PRICE
* a round RED sticker with white type ("NEW / ISSUE"), lower right
* a white barcode block with digits, the price ("$9.99") and issue number, bottom right corner
* these stay in the same positions on every cover
BACKGROUND OPTIONS
ORIGINAL ENVIRONMENT COVERS:
keep the real room exactly as shot, editorially graded.
STUDIO COVERS (for selected sections):
replace the room with a seamless studio paper backdrop:
* warm CREAM paper with soft falloff, or
* saturated RED paper with soft falloff
with a soft contact shadow behind the people.
The people stay exactly where they are in the original frame.
PALETTE RULES
Each cover uses:
the photograph
+ ONE masthead colour
+ ONE accent colour (repeated in one cover line, the rule and the kicker)
+ white / black for the remaining type.
Accent colours to rotate between covers:
RED, LIME GREEN, YELLOW.
Do NOT use more than two type colours on one cover.
Do NOT use gradients, outlines, bevels or glow on the type.
KINETIC TYPOGRAPHY
The covers are ANIMATED, not static.
Divide the clip into about 6 cover sections (about every 2–3 seconds, ideally on natural pauses).
At the start of each section:
* the masthead letters DROP IN from above one after another (staggered, ease-out, about 6 frames)
* cover lines TYPE ON character by character, line by line (about 3–5 frames each)
* the sticker POPS in (scale up from 60% to 100%)
During a section:
* the masthead tracking opens very slowly (letters drift apart by a fraction of a pixel per frame)
* everything else holds still, like a printed page
Between sections:
* hard cut to the next cover design (new masthead word, new accent, new grade or backdrop)
LAYER ORDER
A typical cover reads:
BACKGROUND (original room OR studio paper)
↓
MASTHEAD
↓
PHOTOGRAPHIC PEOPLE (heads overlapping the masthead)
↓
OPTIONAL WORD IN FRONT OF THE TORSOS
↓
COVER LINES, RULE, KICKER
↓
STICKER, BARCODE, PRICE
↓
FINE PRINT GRAIN + SOFT VIGNETTE.
OBJECT CONTINUITY
IMPORTANT:
If the character is interacting with an object, preserve that object inside the photographic layer.
Examples:
* phone
* cup
* chair
* bag
* microphone
* headphones
If the object is essential to the person's action, keep it in front of the masthead together with the person.
Do NOT accidentally cut it out or hide it behind type.
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
The TYPE animates.
The HUMAN MOTION does NOT change.
If the head moves:
the masthead occlusion follows the head exactly.
If the hand moves:
the hand stays in front of all type.
If the body turns or leans into the masthead:
the overlap updates in that same frame.
If the character interacts with an object:
the object moves exactly with the original action.
NO lagging cut-out edges.
NO head silhouettes from previous frames.
NO type flickering on or off at random.
TYPE CONSISTENCY
THIS IS CRITICAL.
Within one cover section, the layout is LOCKED:
* same masthead word, font, size, colour, position
* same cover lines, same fonts, same positions
* same sticker, barcode, price
Only the planned kinetic animation (drop-in, type-on, slow tracking) changes between frames.
Allow, every frame:
* fine print grain to change
* very slight paper sheen variation
* the masthead tracking to open by a fraction of a pixel
Do NOT let the letters change shape, spelling or font between frames.
Do NOT let new random words appear.
DO NOT
Do NOT misspell any word.
Do NOT generate pseudo-text, gibberish or melted letters.
Do NOT put type over faces.
Do NOT let the masthead float in front of the heads.
Do NOT cut the people out with a hard halo or white outline.
Do NOT turn the photo into an illustration, painting or cartoon.
Do NOT beautify or replace faces.
Do NOT create new poses.
Do NOT change anatomy.
Do NOT change clothing.
Do NOT use real magazine brand names or logos (no VOGUE, ELLE, TIME, etc.).
Do NOT use more than two type colours per cover.
Do NOT add glow, bevel, chrome or 3D effects to the type.
Do NOT add grunge, collage, torn paper or photocopy texture.
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
* NO masthead
* NO cover lines
* NO typography
* NO cut-outs
* NO colour grading
* NO studio backdrop
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
Do NOT begin the magazine-cover transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – MAGAZINE COVER STYLING (AFTER MY CONFIRMATION ONLY)
Style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation.
Apply every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT restyle a whole shot from one keyframe.
Plan the cover sections first and list them to me (frame range, masthead word, font style, masthead colour, accent colour, grade, background) before generating.
Generate the TYPE as part of each frame, but keep every word, font and position identical within a section; if Seedream cannot keep type perfectly consistent, generate the photo/grade/backdrop frames with Seedream and set the type as a locked text layer on top, with the masthead layer masked behind the people's heads.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose or the style rules broke — regenerate those frames only.
The final video must feel like FLIPPING THROUGH ANIMATED MAGAZINE COVERS: crisp type, real depth behind the heads, clean editorial photo, glossy print.
The image should deliberately contain:
* razor-sharp, correctly spelled typography
* exact hair-edge occlusion of the masthead
* restrained two-colour type palette
* fine print grain
* subtle glossy-paper finish
* a slight vignette.
Avoid clutter: one masthead, a few cover lines, one sticker, one barcode.
```
