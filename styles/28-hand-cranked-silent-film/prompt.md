# 28 — Hand-Cranked Silent Film

**Look:** Every frame looks like a print from a 1910s–20s hand-cranked reel. The tones are orthochromatic with sepia toning, a soft hazy lens with halation, a hot centre and burnt edges, and a rounded projector gate. There are coarse grain, exposure flicker, gate weave, drifting scratches, dust and hairs, and an iris closes on the main subject at the end.

**Also called / where it trends:** "Hand-Cranked Camera" (Ashok Reddy S's label), "silent film effect", "old film look", "1920s film filter", "vintage film overlay", "handcrank". It trends in AI-restyle reels on Instagram and as old-film presets and tutorials (Prolost Handcrank, AE / Premiere old-film packs) on YouTube and TikTok.

**References:**
- https://www.instagram.com/p/Deme5ygBN_5/ (screenshots `refs/ref_1.png` the look; `refs/ref_2.png` split view; `refs/ref_3.png` post page with caption): Ashok Reddy S (@ashokreddyai), one clip run through a Figma Weave workflow into ten looks. This one is labelled **Hand-Cranked Camera**, at about 2.8–3.6 s: sepia, cream hot centre, scratch line. Credit: Ashok Reddy S.
- https://www.instagram.com/ashokreddyai/: creator page.
- https://dukedenverfilm.dk/silent-movie-effect: what makes the silent-movie look (flicker, sepia, vignette, frame rate).
- https://chrismoran.link/product/exposure-flicker-gate-weave: exposure flicker and gate weave as separate film artefacts.
- https://www.dehancer.com/learn/articles/film-breath-gate-weave: film breath and gate weave explained.
- https://proloststore.com/use-handcrank: Prolost Handcrank, a hand-cranked camera look tool.
- https://darkskiesfilm.com/how-to-make-video-look-like-old-film-after-effects/: old-film look in After Effects (grain, scratches, dust, flicker).

**Example:** `example.png` (six frames of the test clip) and `before_after.png` (frame 049). This is a local approximation made with `render.py` (numpy + OpenCV). It uses an orthochromatic channel mix, soft blur, a milky-black contrast curve, ±10% flicker, halation, a hot-centre vignette, an iris from frame 157, coarse two-scale grain, persistent drifting scratches per section, dust and hairs, a sepia tone map, gate weave and a rounded gate.

## Prompt

```text
I'm uploading one video clip. Convert it into a HAND-CRANKED SILENT FILM (1910s–1920s) frame-by-frame animation, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Every frame becomes a print from a 100-year-old nitrate reel:
* monochrome with warm SEPIA toning
* orthochromatic tones: reds and lips go dark, skies and blues go pale
* soft period lens, highlights bleeding (halation)
* HOT bright centre, BURNT dark edges
* rounded projector-gate corners
* coarse clumpy film grain
* uneven exposure FLICKER from hand cranking
* gate weave: the picture jitters a few pixels and a hair of rotation
* vertical scratches, dust specks and the odd hair in the gate
* a soft IRIS closing in on the main subject in the final section
The result should feel like someone:
FILMED THE SCENE ON A HAND-CRANKED CAMERA
→ DEVELOPED IT ON ORTHOCHROMATIC STOCK
→ TONED THE PRINT SEPIA
→ STORED THE REEL FOR A CENTURY
→ RAN IT THROUGH A WORN PROJECTOR
→ ANIMATED IT FRAME-BY-FRAME.
CHARACTER — PHOTOGRAPHIC, PERIOD STOCK
The people stay PHOTOGRAPHIC.
Preserve the person's exact:
* identity
* face
* expression
* hairstyle
* glasses
* clothing
* accessories
* pose
* body proportions
* movement
* hand position
* interaction with objects
Do NOT redraw the character.
Do NOT add period costumes, make-up or moustaches.
Only the FILM changes, not the people.
ORTHOCHROMATIC TONE
* skin reads a little darker and more textured than modern film
* red and brown fabrics go deep, almost black
* blue and white areas go pale and creamy
* blacks are milky, never pure digital black
* highlights roll off softly with a halo
SEPIA PALETTE
Use only warm brown-to-cream tones:
* deep umber shadows
* warm brown mid-tones
* pale cream / paper highlights
Do NOT use colour, blue tints or neon.
LENS AND VIGNETTE
* soft focus, slightly hazy
* bright hot centre
* edges burnt dark, uneven, a little denser on one side
* rounded projector gate with dark corners
FILM DAMAGE
* coarse grain that changes every frame
* 1–3 thin vertical scratches that persist and drift within a reel section
* dust specks: white and black, different every frame
* an occasional hair caught in the gate
* small density changes from side to side
IRIS
In the final section, close a soft circular IRIS onto the main subject's face over about two seconds.
Outside the iris goes to near black.
OBJECT CONTINUITY
If the character holds an object, keep it in the frame and moving exactly with the hand.
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
The people move exactly as in the source footage.
The FILM jitters.
The HUMAN MOTION does NOT.
Gate weave moves the whole picture together; it never moves one person separately.
Do NOT speed up or slow down the action.
Do NOT drop or repeat frames to fake undercranking.
FRAME-BY-FRAME FLICKER
THIS IS CRITICAL.
Every frame must look like a separate, slightly different film frame.
Allow between consecutive frames:
* exposure to flicker by about ±10%
* gate weave of a few pixels and a fraction of a degree
* grain, dust and hairs to change
* scratches to drift a little sideways
Keep FIXED within a section:
* sepia tone
* scratch positions (drifting slowly)
* vignette shape
DO NOT
Do NOT use a modern black-and-white filter.
Do NOT keep any colour.
Do NOT make it sharp or clean.
Do NOT add intertitles or text cards unless I ask.
Do NOT change the timing or speed of the action.
Do NOT add period costumes, props or make-up.
Do NOT redraw or illustrate the people.
Do NOT create new poses.
Do NOT change anatomy.
Do NOT change clothing.
Do NOT replace the person's face.
Do NOT freeze grain, flicker and dust across frames.
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
* NO sepia or monochrome
* NO grain, scratches or dust
* NO vignette, gate or iris
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
Do NOT begin the silent film transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – SILENT FILM STYLING (AFTER MY CONFIRMATION ONLY)
First, plan the reel sections and list them for me: frame range, scratch positions, and the frame where the iris starts closing.
Then style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation, so the moment on film is exactly that frame.
Apply every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing or the style rules broke — regenerate those frames only.
The final video must feel like A HAND-CRANKED SILENT FILM REEL: sepia, flickering, scratched and weaving in the gate, 12 frames per second.
The image should deliberately contain:
* sepia orthochromatic tones
* halation
* a hot centre and burnt edges
* a rounded projector gate
* coarse grain
* exposure flicker
* gate weave
* scratches, dust and hairs.
Avoid polished digital perfection.
```
