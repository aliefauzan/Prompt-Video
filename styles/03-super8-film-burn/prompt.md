# 03 — Super 8 Film Burn

**Look:** the clip becomes a scanned Super 8 home-movie reel: warm amber, faded reversal-film colour with brown lifted blacks and creamy highlights, soft 8 mm optics, heavy moving grain, exposure flicker, strong lamp vignette, red-orange halation, dark dust specks, hairs and thin scratches, orange light leaks bleeding in from the edges, and white-hot FILM BURNS that eat through the frame at the end of a shot — all seen as a weaving film strip with a rounded gate, frame lines, slivers of the neighbouring frames and a glowing sprocket hole.

**Also called / where it trends:** "Super 8 effect", "8mm film look", "film burn transition", "light leak edit", "vintage film filter", "home movie aesthetic", "Kodak film look" — Super 8 emulation reels and film-burn overlay packs on TikTok, YouTube Shorts ("Film burn effect overlay" 1.3 M views), Instagram travel/wedding edits, Splice / CapCut / Dazz / 8mm apps; real Super 8 scans posted by film shooters.

**References:**
- https://www.youtube.com/results?search_query=super+8+film+look+light+leaks+film+burn — screenshot `refs/ref_1.png`: film burn overlay Shorts (white-hot centre, orange edge, sprocket edge), film-burn/light-leak overlay packs
- https://www.youtube.com/results?search_query=super+8+home+movie+film+scan+sprocket+holes — screenshot `refs/ref_2.png`: "Spain captured on super 8 film", "Super 8mm vs Digital Emulation", "A Wedding Film shot on Super 8", real Super 8 scans
- https://www.tiktok.com/discover/super-8-film-effect — TikTok "Super 8 Film Effect" (Jason's Film "Here's how I emulate Super 8", Splice "Ready to give your phone…", clipster "Super8 Film Overlays")
- https://filmlooks.com/free-film-burn-overlays-super-8mm-light-leaks/ — free Super 8 film-burn / light-leak overlays (real burns shot on film)
- https://filtergrade.com/product/super-8-film-burns/ — Super 8 film burn overlay pack
- https://kurosu.co/editing-assets/p/film-burns — 4K Kodak film burn transitions
- https://nofilmschool.com/creating-super-8-look-adobe-premiere-pro — recipe for the Super 8 look (softness, grain, gate weave, vignette, flicker)
- https://www.blackout-fx.com/store/overlays/8mm-film-overlays/ — 8 mm gate/sprocket/dust overlays

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049). Local approximation made with `render.py` (numpy + OpenCV: film grade, grain, halation, dust, leak and burn fields, weaving strip with sprocket); 6 frames in `frames/` (`render.py ... all` renders all 179).

## Prompt

```text
I'm uploading one video clip. Convert it into an authentic SUPER 8 HOME-MOVIE FILM with LIGHT LEAKS and FILM BURNS, styled frame by frame, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Transform the footage into a scanned reel of 1970s Super 8 reversal film built from:
* warm, amber, slightly faded film colour
* brown, lifted, never-pure blacks
* creamy yellow-white highlights
* soft 8 mm lens sharpness
* heavy, moving, organic film grain
* frame-to-frame exposure flicker
* strong uneven projector-lamp vignette
* red-orange halation glow around bright areas
* dark dust specks, hairs and thin vertical scratches
* orange / red / yellow LIGHT LEAKS bleeding in from the frame edges
* white-hot FILM BURNS eating through the frame at section ends
* gate weave: the picture drifts a few pixels every frame
* a visible Super 8 FILM STRIP: rounded-corner gate, black frame lines, slivers of the previous and next frames, a glowing sprocket hole on the left
The result should feel like someone:
SHOT THE SCENE ON A SUPER 8 CAMERA
→ ON KODACHROME / EKTACHROME REVERSAL FILM
→ HAD IT DEVELOPED
→ LEFT THE REEL IN A WARM ATTIC FOR 50 YEARS
→ RAN IT THROUGH A HOT PROJECTOR UNTIL IT BURNED
→ SCANNED THE WHOLE STRIP EDGE TO EDGE, FRAME BY FRAME.
CHARACTER — UNCHANGED PEOPLE, FILMED ON SUPER 8
The people stay PHOTOGRAPHIC and exactly as in the source.
Preserve each person's exact:
* identity
* face
* expression
* hairstyle
* clothing and clothing patterns
* accessories (glasses, watches)
* pose
* body proportions
* movement
* hand position
* interaction with objects
Do NOT redraw anyone.
Do NOT turn anyone into a painting, cartoon or illustration.
Do NOT beautify, smooth or retouch faces.
The film look is chemistry, optics and damage applied to the real picture, not a repaint.
Faces must stay recognizable through the grain, softness and leaks.
FILM COLOUR
Grade every frame like faded reversal film:
* overall warm amber / honey tone
* reds and skin tones rich and warm
* greens slightly olive, blues muted and pushed toward teal-gray
* blacks lifted to a warm dark brown
* highlights soft, creamy, slightly yellow, rolling off gently
* gentle S-curve contrast in the mid-tones
Do NOT use modern teal-and-orange grading.
Do NOT desaturate to sepia or black-and-white (that is a different style).
FILM TEXTURE
* GRAIN: coarse, clumpy, colour-and-luminance film grain, strongest in the mid-tones, completely new every frame
* SOFTNESS: Super 8 optics — no crisp micro-detail, slightly soft edges, no digital sharpening
* HALATION: a thin red-orange glow bleeding around windows, white walls and other bright areas
* FLICKER: overall exposure pulses slightly up and down from frame to frame
* VIGNETTE: darker, warmer corners and edges, brighter hot centre
FILM DAMAGE
* 10–40 small DARK dust specks per frame, different every frame
* occasional dark curly HAIRS caught in the gate (0–2 per frame)
* 1–2 thin vertical SCRATCHES that stay near the same horizontal position for a whole section and flicker in and out
* never so much dirt that faces are hidden
LIGHT LEAKS
In most sections, a soft LIGHT LEAK enters from one edge of the frame (left, top, right or bottom — one edge per section):
* colours: deep red → orange → warm yellow, with a brighter core
* blended like light (screen / additive), never like flat paint
* it drifts slowly along its edge and breathes brighter and dimmer over consecutive frames
* it may wash across part of a person, but it must not erase a face
Some sections have no leak at all (clean film) for contrast.
FILM BURNS
At the end of selected sections (for example around 9 seconds and in the final second), the film BURNS:
* a white-hot hole opens from one edge of the frame
* the hole is ringed by bright yellow → orange → red melted emulsion
* just outside the ring there is a thin charred dark-brown edge
* the edge is organic, bubbly and irregular, never a perfect circle
* the burn GROWS over consecutive frames, following the same shape, and is largest on the last frame of the section
* outside the burn the picture glows warm orange
The burn must look like real melting film, not like a digital fire overlay.
SUPER 8 FILM STRIP (FRAME EDGES)
Show the frame as a scanned piece of film strip:
* the picture sits in a gate with ROUNDED corners and soft, slightly rough edges
* above and below it, a black FRAME LINE, then a thin sliver of the previous / next frame of the same footage
* on the LEFT, outside the picture, a rounded-rectangle SPROCKET HOLE glowing bright warm white, aligned with the frame line
* a dark warm-black film base around the picture
* keep the picture large: it fills about 88% of the width and height, so the original composition is fully preserved
GATE WEAVE
The whole strip (picture, frame lines and sprocket hole together) drifts 2–5 px horizontally and vertically every frame, with a tiny rotation, like film moving through a projector gate.
Do NOT add big camera shake.
FRAME-BY-FRAME FILM BOIL
THIS IS CRITICAL.
Every frame must feel like a separate physical film frame.
Allow, every frame:
* the grain pattern to change completely
* dust and hairs to change
* scratches to flicker
* exposure to flicker
* light leaks to drift and pulse
* burns to grow
* the strip to weave slightly
Do NOT freeze the grain.
Do NOT copy the same dust between frames.
PERFECT MOTION TRACKING
The underlying character movement must remain exactly faithful to the source footage.
The FILM jitters.
The HUMAN MOTION does NOT.
If the head moves:
the picture follows exactly.
If the hand moves toward the camera:
it moves exactly as in the source.
If the character interacts with an object:
the object moves exactly with the original action.
NO motion blur trails that are not in the source.
NO zoom, crop or reframing beyond the film-strip border.
OBJECT CONTINUITY
Keep every object the people hold or touch (phone, chair, bag, cup, glasses).
Do NOT remove or invent objects.
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
DO NOT
Do NOT make it clean, sharp or HD.
Do NOT use VHS artifacts (no tracking lines, no chroma bleed, no date stamp, no REC display) — this is FILM, not video tape.
Do NOT use a sepia / black-and-white silent-movie look.
Do NOT use digital glitch, pixel sorting or datamosh.
Do NOT use cartoon fire, flames or sparks for the burns.
Do NOT use neon or rainbow colours.
Do NOT add a cinema-screen, projector or TV-set graphic around the strip.
Do NOT create new poses.
Do NOT change anatomy.
Do NOT change clothing.
Do NOT replace or beautify faces.
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
* NO film grain
* NO light leaks
* NO film burns
* NO dust or scratches
* NO film-strip border
* NO colour grading
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
Do NOT begin the Super 8 transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – SUPER 8 FILM STYLING (AFTER MY CONFIRMATION ONLY)
Style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation.
Apply every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT restyle a whole shot from one keyframe.
Plan the sections first and list them to me (frame range, light-leak edge and colour or "clean", film burn yes/no and from which edge) before generating.
Keep the colour grade identical in every frame.
If Seedream cannot keep the film-strip border, sprocket hole and burn shapes consistent, generate the graded, grainy picture with Seedream and composite the strip border, light leaks and burns as locked layers on top (leaks and burns in screen/add mode), keeping the frame-by-frame weave and growth described above.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose or the style rules broke — regenerate those frames only.
The final video must feel like a REAL SUPER 8 REEL burning in the projector: warm, soft, grainy, flickering, weaving, alive.
The image should deliberately contain:
* warm faded reversal-film colour
* coarse grain that changes every frame
* flicker and vignette
* halation
* dust, hairs and scratches
* drifting light leaks
* growing film burns
* the rounded gate, frame lines and sprocket hole of the strip.
Avoid digital perfection.
```
