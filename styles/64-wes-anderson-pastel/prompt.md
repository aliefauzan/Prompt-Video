# 64 — Wes Anderson Pastel Symmetry

**Look:** The three people stand, exactly as filmed, in a flat, perfectly symmetrical pastel set. It has a pink wall with a cream cornice, a mint panelled wainscot under a mustard chair rail and a centred mustard-framed window with red curtains. Matching sconces and pictures sit mirrored either side, under a burgundy sign in Futura. The light is flat and warm, the contrast low, and a centred Futura chapter caption sits at the bottom, as in a deadpan storybook film.

**Also called / where it trends:** "Wes Anderson style", "Wes Anderson filter", "Accidentally Wes Anderson", "#WesAndersonTrend" (the April 2023 TikTok wave, where creators filmed their daily lives as Wes Anderson films), "symmetry edit", "pastel symmetry". It is a CapCut template and filter trend on TikTok and Reels and a popular AI-video style prompt, with YouTube "how to shoot like Wes Anderson" breakdowns.

**References:**
- https://www.tiktok.com/search?q=wes%20anderson%20filter%20video%20symmetrical%20pastel (screenshot `refs/ref_1.png`): TikTok search grid from the discovery sweep. Top posts: https://www.tiktok.com/@esno.art/video/7225318124696980763 (110K likes), https://www.tiktok.com/@tianchad/video/7225925591248178433 (38.5K likes), https://www.tiktok.com/@wabifathan_/video/7227266297413848346.
- https://theconversation.com/the-wes-anderson-recipe-a-detailed-guide-on-how-to-recreate-the-directors-aesthetic-206886 (screenshot `refs/ref_2.png`): The Conversation, "The Wes Anderson recipe". It covers centred planimetric framing, pastel palettes, Futura text and deadpan staging.
- https://www.youtube.com/watch?v=l__dnp6e6Ok: YouTube Wes Anderson style breakdown (613K views, discovery sweep).
- https://www.studiobinder.com/blog/wes-anderson-symmetry/: StudioBinder on Wes Anderson symmetry and symmetrical editing.
- https://www.smithsonianmag.com/smart-news/these-are-the-building-blocks-of-wes-andersons-signature-visual-style-180986316/: Smithsonian on the building blocks of the style.
- https://www.filminquiry.com/wes-anderson-framing/: Film Inquiry on the "Andersonian" framing.

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049), `example.mp4` (the whole clip at 12 fps with the original audio) and `preview.webp`. This is a local approximation made with `render.py` (numpy + OpenCV + PIL + the person masks). The pastel set is drawn once, mirrored about the centre line, and held still like a locked-off camera. The people are cut from the masks and graded with lifted blacks, compressed contrast and a warm pink-yellow cast. A soft shadow falls straight back onto the wall. A centred Futura "CHAPTER ONE / The Three Colleagues" caption, faint grain and a hair of softness finish the frame. The camera framing of the people is unchanged: the symmetry comes from the set, not from moving the people. One known artefact: on some frames the person masks include part of an office chair, which shows as a dark shape in front of the set.

## Prompt

```text
I'm uploading one video clip. Convert it into a WES ANDERSON PASTEL SYMMETRY frame-by-frame animation: every frame should look like a still from a deadpan, storybook Wes Anderson film, with the people standing in a flat, perfectly symmetrical pastel set, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Film still in the style of Wes Anderson, centred symmetrical planimetric composition, pastel production design, flat frontal lighting, Futura typography, 35mm, deadpan.
Transform the footage into a frame built from:
* a PERFECTLY SYMMETRICAL set, mirrored about the vertical centre line of the frame
* the set's walls FLAT and PARALLEL to the camera (planimetric), no diagonals
* a PASTEL palette: blush pink, mint green, mustard yellow, cream, powder sky blue
* deep accents: burgundy and tomato red
* a CENTRED architectural feature (window, doorway or arch) behind the people
* matching pairs either side: sconces, frames, pilasters, curtains
* FLAT, WARM, FRONTAL light with soft, short shadows
* LOW CONTRAST: lifted blacks, no deep shadows, no hard highlights
* a slightly warm, creamy film look with very fine grain
* centred FUTURA lettering: a sign on the set and a chapter caption
The result should feel like someone:
BUILT A DOLLHOUSE SET IN PASTEL PAINT
→ MADE EVERY DETAIL MIRROR ON BOTH SIDES
→ STOOD THE PEOPLE IN FRONT OF IT, FACING CAMERA
→ LIT IT FLAT AND WARM FROM THE FRONT
→ LOCKED OFF THE CAMERA DEAD CENTRE
→ ADDED A FUTURA CHAPTER TITLE
→ SHOT IT FRAME-BY-FRAME.
CHARACTER — PHOTOGRAPHIC, IN A STORYBOOK
The people stay PHOTOGRAPHIC: real faces, real clothes, filmed.
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
Do NOT turn them into a painting, cartoon, puppet or stop-motion figure.
Do NOT dress them in costumes or uniforms.
Do NOT move them to the centre; keep their exact positions in the frame.
THE SET (BACKGROUND)
* Replace the office behind the people with ONE pastel set that matches the room's layout in spirit: wall, window, low wall or planter.
* The set is perfectly mirrored about the centre line of the frame.
* Upper wall: blush pink, with pilasters or panels.
* Lower wall: mint green panelled wainscot under a mustard chair rail.
* Centre: a mustard-framed window with pale sky-blue panes and red curtains, or a similar centred feature.
* Either side: identical sconces, small framed pictures, pilasters.
* A small sign above the centre in Futura capitals on a burgundy plaque.
* A burgundy carpet strip at the floor.
* Everything clean, painted, a little theatrical; no clutter, no office furniture.
* The set does NOT move between frames: the camera is locked off. Only the people move.
LIGHT AND GRADE
* Flat, frontal, warm light, as from a big soft source at the camera.
* People cast a soft, short shadow straight back onto the wall behind them.
* Skin warm and peachy, never orange.
* Blacks lifted to soft charcoal; contrast gentle.
* The people's clothing keeps its own colours, warmed and softened to sit in the pastel world.
TYPOGRAPHY
* Futura only.
* A centred two-line chapter caption near the bottom of the frame: a small capital line and a larger title line, for example "CHAPTER ONE" / "The Three Colleagues", in pale mustard yellow with a soft dark shadow.
* The caption stays in exactly the same place and size on every frame.
* The set sign may be partly hidden behind the people; that is fine.
PALETTE
Blush pink, dusty rose, mint, sage, mustard, cream, powder blue, burgundy, tomato red, warm skin.
Do NOT use neon, saturated primaries, black backgrounds or teal-orange grading.
OBJECT CONTINUITY
If the character holds an object, it stays attached to the hand and graded like the rest.
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
The people must match the source frame exactly.
Clean edges between the people and the set: no leftover office pixels, no halo, no cut-out outline.
FRAME-TO-FRAME STABILITY
THIS IS CRITICAL.
The set is one locked, unchanging image. Only the people move.
Allow between consecutive frames:
* very fine film grain to change every frame
* the people's shadow on the wall to follow them
Keep FIXED:
* every line, colour and object of the set
* the symmetry
* the caption text, position and size
* the grade
DO NOT
Do NOT let the set redesign itself from frame to frame.
Do NOT make the set asymmetrical or shoot it at an angle.
Do NOT use harsh, dramatic or coloured lighting.
Do NOT use deep shadows or high contrast.
Do NOT use any font other than Futura.
Do NOT add extra characters, animals or props.
Do NOT redraw or illustrate the people.
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
* NO colour grade
* NO set replacement
* NO pastel palette, titles or grain
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
Do NOT begin the Wes Anderson pastel transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – WES ANDERSON PASTEL STYLING (AFTER MY CONFIRMATION ONLY)
First, generate ONE empty pastel set plate (the background with no people) and show it to me with the exact caption text. Use that same plate for every frame.
Then style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation, so the people are exactly that frame, and the set plate as the background reference.
Apply every style rule above, with the SAME set, caption and grade on every frame.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing, the set, the symmetry or the caption changed — regenerate those frames only.
The final video must feel like A SCENE FROM A WES ANDERSON FILM: the real people, deadpan, in front of a mirrored pastel set, flat warm light, Futura chapter title, 12 frames per second.
The image should deliberately contain:
* a perfectly symmetrical pastel set
* a centred window or doorway
* mirrored pairs of details either side
* flat, warm, low-contrast light
* centred Futura lettering.
Avoid ordinary office video.
```
