# 09 — Cyanotype Sun Print

**Look:** every frame is a hand-coated cyanotype (blueprint / sun print). The image is monochrome Prussian blue, from deep indigo shadows to paper-white highlights. It sits inside a hand-brushed patch of emulsion on cold-press watercolour paper, with ragged dry-brush edges, streaky uneven coating and a bare paper margin. White botanical photogram shadows of ferns and leaves, with visible veins, lie where plants touched the paper during exposure. A small pencil note sits in the margin. Coating streaks, brush edge, paper grain and the leaves shift slightly every frame, as if each frame was printed by hand in the sun.

**Also called / where it trends:** "cyanotype effect", "blueprint effect", "sun print edit", "cyanotype filter", "Prussian blue edit", "botanical cyanotype". Seen in TikTok cyanotype-effect edits and CapCut templates, in Photoshop / BeFunky cyanotype-effect tutorials, and on Pinterest cyanotype portrait boards. Real cyanotype sun printing (plant photograms, Anna Atkins' algae books) is a big crafts trend on TikTok and Pinterest.

**References:**
- https://www.pinterest.com/search/pins/?q=cyanotype%20portrait%20photography — Pinterest search, screenshot `refs/ref_1.png`: brushed emulsion edges, white leaf photograms over portraits
- https://www.tiktok.com/search/video?q=cyanotype%20effect%20edit — TikTok search, screenshot `refs/ref_2.png`: cyanotype effect edits
- https://www.tiktok.com/@staseradigital/video/7672514512653798678 — TikTok cyanotype effect edit
- https://www.tiktok.com/@capcut.ed1t5/video/7682175097049779463 — CapCut cyanotype-style edit
- https://www.tiktok.com/@alexrojoo/video/7559351577991990541 — cyanotype sun-print process video
- https://www.befunky.com/learn/cyanotype-effect/ — how to fake the cyanotype effect: blue monochrome, paper, brushed edges
- https://effect.app/effects/cyanotype — cyanotype video effect preset
- https://digital-photography-school.com/digital-cyanotype-using-photoshop/ — digital cyanotype in Photoshop
- https://www.youtube.com/watch?v=3OWgI-ZI-Bw — cyanotype process / look tutorial
- https://www.nybg.org/planttalk/the-art-and-science-of-cyanotype-making-sun-prints-with-plants/ — sun prints with plants: brush-coated paper, UV exposure, white plant shadows
- https://www.vam.ac.uk/blog/caring-for-our-collections/a-blueprint-for-the-future-cyanotypes-by-anna-atkins — Anna Atkins' cyanotypes (V&A)
- https://old-digitalcollections.nypl.org/collections/photographs-of-british-algae-cyanotype-impressions — Atkins, "Photographs of British Algae: Cyanotype Impressions" (NYPL scans)

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049). Local approximation rendered with `render.py` (numpy + OpenCV + Pillow + person masks).

## Prompt

```text
FULL PROMPT FOR CYANOTYPE SUN PRINT EDIT:

I'm uploading one video clip. Convert it into a handmade CYANOTYPE / SUN PRINT frame-by-frame animation: monochrome Prussian blue on hand-brushed watercolour paper, with white botanical photograms.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.

TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.

CORE VISUAL STYLE
Transform the footage into a 19th-century-style cyanotype print built from:
* ONE colour only: PRUSSIAN BLUE, from deep indigo to pale cyan
* paper white as the only highlight
* a hand-brushed patch of light-sensitive emulsion
* ragged dry-brush edges with bristle streaks
* uneven, streaky coating density
* cold-press watercolour paper with visible tooth
* a bare paper margin around the print
* soft contact-print sharpness (no crisp digital detail)
* WHITE BOTANICAL PHOTOGRAMS: ferns, leaves, fronds, grasses
* small chemistry flaws: pinholes, specks, faint tide lines
* a small handwritten pencil note in the margin
* botanical / alternative-process photography aesthetics
The result should feel like someone:
PRINTED THE VIDEO FRAME AS A NEGATIVE
→ BRUSHED CYANOTYPE EMULSION ONTO WATERCOLOUR PAPER
→ LAID THE NEGATIVE AND A FEW FERNS AND LEAVES ON IT
→ EXPOSED IT IN THE SUN
→ WASHED IT IN WATER UNTIL THE BLUE CAME UP
→ DRIED IT AND WROTE A NOTE IN PENCIL
→ SCANNED THE PRINT
→ ANIMATED IT FRAME-BY-FRAME.

TONE MAPPING — PRUSSIAN BLUE MONOCHROME
Map the image brightness to a single blue ramp:
* highlights → paper white / very pale blue-white
* light tones → pale cyan-blue
* mid-tones → medium cyan / cerulean blue
* shadows → deep Prussian blue
* the darkest shadows → near-indigo, never black
Approximate colours:
* paper #F6F1E8
* light #AACDDE
* mid #3C6EAA
* deep #123A6E
* darkest #0A2046
Remove ALL other colour.
Do NOT leave any skin tones, greens, browns or neutrals.
Do NOT use pure black or grey.

CHARACTER — PRINTED IN BLUE
The people remain PHOTOGRAPHIC, just printed as a cyanotype.
Preserve each person's exact:
* identity
* face
* expression
* hairstyle
* clothing and its patterns
* accessories (e.g. glasses)
* pose
* body proportions
* movement
* hand position
* interaction with objects
Do NOT redraw the people.
Do NOT turn them into a sketch or illustration.
Faces must stay readable: keep eyes, brows, nostrils and mouth.
The image is slightly soft, like a contact print, but faces must not blur away.

BRUSHED EMULSION PATCH
The image only exists where the emulsion was brushed on.
* a roughly rectangular patch with a bare paper margin of a few percent
* top and bottom edges wavy and uneven, following the brush strokes
* left and right ends feathered into DRY-BRUSH bristle streaks of varying length
* thin gaps and lighter streaks inside the patch along the brush direction
* slightly denser blue where the coating pooled
* a faint darker tide line along the edge of the coating
Do NOT use a clean rectangular crop or a digital vignette.

WATERCOLOUR PAPER
* warm off-white cold-press paper
* fine, even embossed tooth visible across the whole sheet, including the blue areas
* soft fibre clouds
* a slightly uneven paper tone
The texture must stay FINE. Do NOT use a coarse, wormy emboss filter.

BOTANICAL PHOTOGRAMS
Plants lying on the paper blocked the sun, so they print as WHITE / pale-blue silhouettes.
* fern fronds with many small leaflets
* single leaves with visible central veins and side veins (thin blue lines where the leaf let some light through)
* small leaves and fronds entering from the corners and edges
* edges slightly soft where a leaf lifted off the paper
* placed in the background and the empty space around the people
* NEVER over a face
* where a plant crosses a body, it may print faintly over the clothing only

BACKGROUND OPTIONS
Switch between these treatments in sections of a few seconds:
1. FULL PRINT — the original office printed as a cyanotype together with the people, with 1–2 plants near the corners.
2. PHOTOGRAM FIELD — the room is fully exposed to a deep, even Prussian blue. Only the people print as a photograph. More ferns and leaves are scattered as white photograms around them.
Keep the original composition in both.

PENCIL NOTE
* a small graphite note in the lower margin, e.g. "no. 1 — office, morning", "no. 4 — sun print"
* thin, grey, slightly broken where the pencil skipped on the paper tooth
* the same note for the whole section
* correctly spelled

OBJECT CONTINUITY
IMPORTANT:
If a person is interacting with an object, keep that object.
Examples:
* phone
* chair
* bag
* glasses
* clothing accessory
Print it in blue like everything else.
Do NOT accidentally remove it.

DO NOT
Do NOT use any colour other than Prussian blue and paper white.
Do NOT use black, grey or sepia.
Do NOT use a flat digital blue tint or a duotone gradient map.
Do NOT make it sharp, glossy or clean digital.
Do NOT use a perfect rectangular border or digital vignette.
Do NOT use a technical blueprint grid with white CAD lines.
Do NOT put plants over faces.
Do NOT use a coarse, wormy paper emboss.
Do NOT turn the people into drawings.
Do NOT create new poses.
Do NOT change anatomy.
Do NOT change clothing.
Do NOT replace anyone's face.
It must feel SUN-PRINTED, BRUSHED BY HAND and PHYSICAL.

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
* NO blue toning
* NO brushed edges
* NO paper texture
* NO plant photograms
* NO pencil notes
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
Do NOT begin the cyanotype transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.

STAGE 3 – CYANOTYPE STYLING (AFTER MY CONFIRMATION ONLY)
Style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation.
Apply every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT restyle a whole shot from one keyframe.
Plan the sections first and list them to me (frame range, background option, plant types and their positions, pencil note) before generating.
Within a section keep the same brushed-patch shape, the same plants in the same places and the same pencil note.
If Seedream cannot keep the plants consistent, generate the blue print per frame and lay the plant photograms as a locked white layer on top.

CHARACTER CONTINUITY LOCK
The SAME people must remain recognizable in every frame.
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
The STYLE jitters.
The HUMAN MOTION does NOT.
The underlying movement must remain exactly faithful to the source footage.
If a head moves, the print follows.
If a hand moves, the print follows.
In the photogram field, the people's printed area follows them exactly.
NO delayed silhouette.
NO previous-frame ghost.

FRAME-BY-FRAME BOILING EFFECT
THIS IS CRITICAL.
Every frame should feel separately coated, exposed and washed.
Allow between consecutive frames:
* coating streaks and density to shift
* the dry-brush edge and bristle streaks to change slightly
* the paper margin to wobble
* plant photograms to shift by 1–2 px and a tiny rotation, as if re-laid on the paper
* specks and pinholes to appear and disappear
* the pencil note to wobble slightly
Do NOT make the wobble so large that the image swims.
The result must feel like a STACK OF HAND-MADE SUN PRINTS flipped one after another.

The image should deliberately contain:
* deep Prussian blue
* clean paper whites
* brushed, streaky emulsion
* ragged dry-brush edges
* fine watercolour paper tooth
* white fern and leaf photograms with veins
* soft contact-print focus
* tiny chemistry flaws.
Avoid clean digital perfection.
```
