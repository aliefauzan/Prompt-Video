# 20 — Polaroid Photo Dump

**Look:** every frame of the clip is a real instant-film print. It uses a landscape Instax Wide card, so the full composition survives. The print has faded, warm instant-film colour, soft lifted blacks and a slightly blown highlight. A handwritten Sharpie caption sits on the thick bottom border. Each print lies on a table, corkboard or linen bed on top of a pile of earlier prints, with washi tape or push pins and a soft lamp shadow. The print shifts a little in angle and position every frame, like a flipbook of photos dropped on the pile, while the people inside it move exactly as in the video.

**Also called / where it trends:** "polaroid photo dump", "polaroid trend", "polaroid memories template", "Polaroid Camera Shutter template", "photos hold memories", "recent polaroids #photodump", "instax aesthetic", "photo dump slideshow". It trends hard on TikTok and CapCut templates in 2025–26 and on Pinterest "polaroid wall / instax corkboard" boards.

**References:**
- https://www.pinterest.com/search/pins/?q=polaroid%20photo%20dump%20table%20aesthetic (screenshot `refs/ref_1.png`): instant prints scattered and overlapping on wood and linen. Note the faded warm colour, the thick white borders and the handwritten captions.
- https://www.tiktok.com/@capcutniiyaa/video/7561266657209978168 (screenshot `refs/ref_2.png`): "Polaroid Camera Shutter | Polaroid Photos Template" by @capcutniiyaa, about 12K likes and 14K saves. A shutter flash turns each clip into an instant print.
- https://www.pinterest.com/search/pins/?q=instax%20polaroid%20handwritten%20caption%20corkboard (screenshot `refs/ref_3.png`): Instax prints pinned to cork with handwritten dates and captions.
- https://www.tiktok.com/@chocholvte/video/7552310182533942539: "polaroid memories trend template #CapCut".
- https://www.tiktok.com/@sau5894/video/7556296662050688264: "photos hold memories | polaroid photo dump template".
- https://www.trypostbase.com/resources/how-to-do-polaroid-trend-tiktok: a how-to for the TikTok polaroid trend (frame, caption, beat-synced shuffle).
- https://www.nemovideo.com/templates/polaroid-frame-tiktok-template: polaroid-frame video template.
- https://www.freevisuals.net/post/why-photo-dump-capcut-templates-are-so-popular: why photo-dump CapCut templates took off (nostalgia, casual, unpolished).
- https://www.flexclip.com/learn/photo-dump-video.html: how to build a photo-dump video.

**Example:** `example.png` (six frames of the test clip) and `before_after.png` (frame 049). This is a local approximation made with `render.py` (numpy + OpenCV). It uses five sections across the clip: wood "office crew", cork "tues 4pm :)", linen "the trio", wood "say hi!!" in red ink, and cork "core memory". Each frame gets an instant-film grade on the photo, an Instax Wide card with a Sharpie caption, perspective, a drop shadow and gloss, a fixed pile of earlier prints, tape or pins, lamp falloff, and a small per-frame angle and position shuffle.

## Prompt

```text
I'm uploading one video clip. Convert it into a POLAROID / INSTANT-FILM PHOTO DUMP frame-by-frame animation, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Transform the footage into a tactile instant-film photo dump built from:
* every frame shown as ONE physical instant-film print
* landscape Instax Wide format (thick white border, thicker at the bottom)
* faded, warm, slightly washed-out instant-film colour
* lifted milky blacks and soft, slightly blown highlights
* gentle teal-green shadows and creamy-yellow highlights
* uneven chemical development at the edges of the image
* a handwritten Sharpie caption on the bottom border
* the print lying on a real surface (wood table / corkboard / linen)
* a messy pile of earlier prints underneath
* washi tape or push pins
* a soft drop shadow and a gloss reflection on the print
* warm lamp light falling off toward the corners
* the print shifting slightly every frame like a flipbook
The result should feel like someone:
SHOT EVERY FRAME ON INSTANT FILM
→ WAITED FOR IT TO DEVELOP
→ WROTE A CAPTION ON THE BORDER IN MARKER
→ DROPPED THE PRINT ON THE PILE
→ PHOTOGRAPHED IT FROM ABOVE UNDER A LAMP
→ PICKED IT UP AND SHOT THE NEXT ONE
→ ANIMATED THE PRINTS FRAME-BY-FRAME.
THE PRINT
Use a LANDSCAPE INSTAX WIDE print so the WHOLE original composition fits.
Rules:
* image area roughly 99 × 62 mm inside a 108 × 86 mm card (wide aspect, about 1.6:1)
* off-white, slightly warm card border — NOT pure digital white
* border wider at the bottom, where the caption goes
* the video frame fills the image area with ALL people and the main action inside it
* do NOT crop heads, hands or key objects out of the print
* the print fills most of the output frame (about 75–85% of the width) so faces stay readable
* the print is slightly tilted (about 1–3°) and seen with a tiny perspective keystone, like a real photo shot from above
INSTANT-FILM LOOK (INSIDE THE PRINT ONLY)
The image inside the print should look like real instant film:
* reduced saturation, warm cast
* lifted, milky blacks — no deep black
* soft contrast, gentle highlight bloom
* teal-green in the shadows, cream-yellow in the highlights
* slight vignette and soft focus toward the image edges
* faint roller marks / uneven development along one edge
* small chemical stains or a slightly darker corner
* fine film grain
It should NOT look like a sharp phone photo with a white frame added.
HANDWRITTEN CAPTION
Write a short, casual caption on the bottom border in black (or occasionally red) Sharpie marker.
Rules:
* real handwriting: slightly uneven baseline, imperfect letters, small slant
* lowercase, casual, photo-dump style — e.g. "office crew", "tues 4pm :)", "the trio", "say hi!!", "core memory"
* can include a tiny doodle (heart, star, smiley) and a date like "10.18"
* ONE caption per section of the video; it stays the SAME for every frame in that section
* the ink sits ON the card, with a slight marker bleed
Do NOT use a typed font.
Do NOT write on the photo itself.
THE TABLE — SURFACE + PILE
Each section of the video gets ONE surface, kept the same for the whole section:
* warm wood table with visible grain
* cork board with pores and pin holes
* creamy linen / bedsheet with soft folds
Underneath the hero print, show a PILE of 3–5 EARLIER prints from the same video (other moments of the clip):
* overlapping at different angles, partly hidden
* same instant-film look and white borders
* their captions partly visible or cut off
* the pile stays the same through a section; it only grows/changes when the section changes
Props:
* strips of washi tape on wood/linen, or push pins on cork, holding the hero print
* optional small extras at the edge: a flower, a ticket stub, a film box — kept small, never covering people
LIGHT ON THE TABLE
* one warm lamp light from above-left
* soft drop shadow under each print
* a faint gloss sheen band across the hero print
* corners of the frame falling into darker warm shadow
PEOPLE INSIDE THE PRINT
The people in the print are the REAL people from the video, photographed, not drawn.
Preserve their exact:
* identity
* face
* expression
* hairstyle
* glasses
* clothing and clothing pattern
* accessories
* pose
* body proportions
* movement
* hand position
* interaction with objects
Do NOT redraw them.
Do NOT beautify, retouch or replace faces.
Only the instant-film colour and grain change.
SECTION PLAN
Split the video into 4–6 sections at natural beats or cuts (about 2–4 seconds each).
For each section choose:
* the surface (wood / cork / linen)
* the caption text and ink colour
* the base tilt of the hero print (alternate left/right, e.g. −2.5°, +2°, −1°, +3°)
* the pile of earlier prints underneath
Keep these FIXED within a section.
On a section change the print "lands" on the new surface — a new tilt, a new caption, a new pile.
PALETTE RULES
Use the warm, faded instant-film palette:
INSTANT-FILM CREAM / WARM WHITE (borders)
FADED WARM SKIN TONES
SOFT TEAL-GREEN SHADOWS
CREAMY YELLOW HIGHLIGHTS
HONEY WOOD / TAN CORK / OAT LINEN (surfaces)
BLACK OR RED MARKER INK.
Do NOT use neon, high-contrast or HDR colour.
Do NOT make borders bright digital white.
LAYER ORDER
A typical frame reads:
SURFACE (WOOD / CORK / LINEN)
↓
PILE OF EARLIER PRINTS + THEIR SHADOWS
↓
HERO PRINT DROP SHADOW
↓
HERO PRINT CARD + INSTANT-FILM IMAGE
↓
HANDWRITTEN CAPTION
↓
TAPE / PINS
↓
GLOSS SHEEN + LAMP FALLOFF.
OBJECT CONTINUITY
IMPORTANT:
If the character is interacting with an object, preserve that object inside the print.
Examples:
* phone
* glasses
* chair
* bag
* microphone
* clothing accessory
If an object is essential to the action, keep it inside the image area.
Do NOT crop it off the print.
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
The PRINT shuffles.
The HUMAN MOTION inside the print does NOT.
If the head moves:
it moves inside the print exactly as in the video.
If the hand moves:
it moves inside the print.
If the character interacts with an object:
the object moves exactly with the original action.
NO frozen photo while the video moves.
NO motion copied from the previous frame.
FRAME-BY-FRAME SHUFFLE EFFECT
THIS IS CRITICAL.
Every frame must look like a NEW instant print, freshly developed and re-dropped.
Allow between consecutive frames:
* the hero print to rotate by about ±0.5–1°
* the hero print to shift by a few pixels
* film grain, development marks and small stains to change
* the gloss sheen to move slightly
* the caption to stay the same text but with tiny handwriting variation
Keep FIXED within a section:
* surface
* caption text
* pile of earlier prints
* tape / pins position (moves with the print)
This creates a tactile, handheld PHOTO-DUMP flipbook.
CONTROLLED SHUFFLE
The shuffle must stay SMALL.
The print must NOT jump around the table.
The image inside must stay sharp enough to read faces.
Do NOT flicker the colour grade between frames.
DO NOT
Do NOT just add a white frame around the video.
Do NOT make the photo sharp, saturated phone-camera quality.
Do NOT use a typed font for the caption.
Do NOT use square or portrait prints that crop the people out.
Do NOT crop heads, hands or key objects.
Do NOT let the pile or props cover the people in the hero print.
Do NOT change the surface or caption mid-section.
Do NOT redraw or illustrate the people.
Do NOT create new poses.
Do NOT change anatomy.
Do NOT change clothing.
Do NOT replace the person's face.
Do NOT freeze grain and print position across frames.
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
* NO print frames or borders
* NO captions
* NO table or props
* NO film grading
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
Do NOT begin the photo-dump transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – POLAROID PHOTO DUMP STYLING (AFTER MY CONFIRMATION ONLY)
First, plan the sections and list them for me: frame range, surface, caption text and ink colour, base tilt, and which earlier frames go in the pile.
Then style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation, so the moment inside the print is exactly that frame.
Apply every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT use one still print for a whole section: every frame is a new print of its own moment.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, cropping, caption or the style rules broke — regenerate those frames only.
The final video must feel like A PILE OF INSTANT PHOTOS THAT PLAYS LIKE A VIDEO: every moment developed on instant film, captioned by hand and dropped on the table, 12 prints per second.
The image should deliberately contain:
* visible film grain
* faded instant-film colour
* uneven development marks
* real handwriting
* overlapping earlier prints
* tape or pins
* soft shadows and gloss
* small print-to-print shifts.
Avoid polished digital perfection.
```
