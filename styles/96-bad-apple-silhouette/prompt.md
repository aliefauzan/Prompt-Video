# 96 — Bad Apple 1-Bit Silhouette

**Look:** The clip becomes pure two-colour shadow art, like the Touhou "Bad Apple!!" PV. Every pixel is either black or white: no grey, no texture, no outline drawing, no face detail. The people are flat solid silhouettes, cut out cleanly. Their hair, glasses, sleeves and hands read only from the shape of the outline. The room is gone: the figures stand on a blank ground. Where one person overlaps another, a thin gap in the ground colour keeps them apart. On hard beats the polarity flips: black figures on white become white figures on black. The last section is the PV's split screen, where the figures change colour as they cross a drifting dividing line.

**Also called / where it trends:** "Bad Apple style", "Bad Apple!! shadow art", "Bad Apple PV", "1-bit silhouette animation", "shadow PV", "影絵" (kage-e, shadow-picture) and "影絵PV" (Niconico / Bilibili). The 2009 Touhou fan PV (by Anira / あにら) is one of the most re-made clips on the internet. People have played it on oscilloscopes, calculators, in CSS, in Minecraft, and on almost anything with two colours. It is also an AI-video trend: a Wan 2.1/2.2 LoRA on Civitai ("bad apple style") turns any clip into it, and Morphic sells a "silhouette animation" preset.

**References:**
- https://civitai.com/models/1732430: "Bad Apple Style" LoRA for Wan 2.2 / 2.1 video, trigger `bad apple style`. It was trained on the black-and-white silhouette PV and gives the two-colour look with no post-processing (screenshot `refs/ref_1.png`, from discovery D3).
- https://www.youtube.com/watch?v=UkgK8eUdpAo: "[HD] Touhou - Bad Apple!! PV [Shadow Art]", the original PV (thumbnail contact sheet of the YouTube results: `refs/ref_2.png`).
- https://www.youtube.com/watch?v=p5CFu5rOvGs: another upload of the PV.
- https://www.youtube.com/watch?v=6QY4ekac1_Q: "Bad Apple Explained", the history and why it is re-made on everything.
- https://www.youtube.com/watch?v=MQbjW2VfaHs: "Bad Apple!!" in pure CSS (shows how strictly 1-bit the source is).
- https://archive.org/details/dagobah_Bad_Apple_HQ: archived HQ copy of the PV.
- https://morphic.com (silhouette-animation preset, noted in discovery D3) and https://mereja.com/index/650600 (re-upload with commentary).

How it differs from taken styles: **31 Sin City** is high-contrast black and white *photography*: it keeps grey ramps, faces, texture and a red accent. Here nothing survives but the cut-out shape, there is no grey, and there is no accent colour. **47 two-tone screen print** has ink texture, halftone and paper. Here the edges are vector-clean and the ground is flat. **16 Thermal** and **39 Lidar** are sensor looks with gradients. Bad Apple's signature moves are also its own: whole-frame polarity flips on the beat, and a split screen whose figure colour inverts across the line.

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049), `example.mp4` (the whole clip at 12 fps with the original audio) and `preview.webp`. This is a local approximation made with `render.py` (numpy + OpenCV). People come from the source mattes, smoothed so the outline is one clean cut. Broken mattes (023, 068) are repaired from their neighbours, and stray chair bits are dropped. Thin ground-colour gaps are cut where two people overlap. They come from Apple Vision person-instance masks (`instances.swift`) and are kept only where the gap holds still for ±2 frames, so label swaps never flicker. The room is removed. Polarity is black-on-white for 0–5 s, then white-on-black for 5–10 s. From 10 s the frame splits along a slowly drifting line, with figures XOR-inverted across it. Every output pixel is pure #000 or #FFF.

## Prompt

```text
I'm uploading one video clip. Convert it into a BAD APPLE!! STYLE 1-BIT SHADOW-ART frame-by-frame animation: every frame should look like a frame from the Touhou "Bad Apple!!" shadow-art PV, pure black and pure white silhouettes, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Bad Apple!! shadow art, 1-bit two-colour silhouette animation, pure black and pure white only, clean vector-cut outlines, blank ground.
Transform the footage into shadow art built from:
* EXACTLY TWO COLOURS: pure black #000000 and pure white #FFFFFF
* every person as ONE FLAT SOLID SILHOUETTE, no inner detail
* clean, smooth, confident outlines, as if cut from paper with a sharp blade
* identity carried ONLY by the outline: hairstyle, glasses frames sticking out past the face, sleeves, collar, hands and fingers
* a BLANK GROUND: the room, wall, window and furniture removed
* a THIN GAP in the ground colour wherever one person overlaps another, so the figures stay separate
* POLARITY FLIPS on hard beats: black figures on white, then white figures on black
* a final SPLIT-SCREEN section: the frame divided by a slowly drifting vertical line, with the ground colour swapping across it and each figure inverting where it crosses
The result should feel like someone:
FILMED THE PEOPLE AGAINST A LIGHT BOX
→ TRACED EVERY FRAME AS A SOLID SHADOW
→ CUT IT OUT CLEAN
→ THREW AWAY EVERY GREY
→ FLIPPED BLACK AND WHITE ON THE BEAT
→ PLAYED IT FRAME-BY-FRAME.
CHARACTER — SILHOUETTE ONLY
The people become solid shadows. Their shape stays exact.
Preserve the person's exact:
* outline and identity read from the outline
* head shape
* hairstyle silhouette
* glasses (where they stick out past the face)
* clothing silhouette (sleeves, collar, hem)
* accessories that change the outline
* pose
* body proportions
* movement
* hand position and finger shapes
* interaction with objects
Do NOT draw eyes, mouth, nose, stripes, prints or folds inside the silhouette.
Do NOT simplify the outline into a generic mannequin.
Do NOT add anime features or change the person into a Touhou character.
SILHOUETTE RULES (WHAT MAKES IT BAD APPLE)
* Decide for every pixel: is it a person or not? Person = figure colour, everything else = ground colour.
* Hands, phones and anything the people hold are part of the figure.
* Furniture, screens, plants, walls and windows are NOT figures: remove them completely. Do NOT leave half-tracked furniture shapes.
* Outlines are smooth and continuous, without jagged pixel stair-steps, halos, anti-aliased grey edges or feathering.
* A hand in front of the lens becomes a huge silhouette that can fill most of the frame. That is correct.
* Overlapping people get a clean gap about 0.3–0.5% of the frame width along the edge of the nearer person. The gap must be stable, never wandering or appearing for a single frame.
POLARITY AND SPLIT SCREEN
* First section (about the first half of the first 10 seconds): black figures on white.
* At a hard beat (about 5 s): hard cut to white figures on black, no fade.
* At the next beat (about 10 s): split screen. The left side has a black ground with white figures, the right side a white ground with black figures. The dividing line drifts slowly left and right, and figures invert exactly where they cross it.
* Flips are hard cuts on a single frame. Never cross-fade.
PALETTE
#000000 and #FFFFFF only.
Do NOT use grey, sepia, blue-black, off-white, paper texture, noise or grain.
OBJECT CONTINUITY
If the character holds an object, it stays merged with the hand's silhouette in the same colour.
CHARACTER CONTINUITY LOCK
The SAME person must remain recognizable in every frame from the outline alone.
Never change:
* identity (outline)
* head shape
* hairstyle silhouette
* glasses
* clothing silhouette
* accessories
* body proportions
* anatomy
* pose
* action
* position
Generation is for VISUAL STYLE ONLY.
PERFECT MOTION TRACKING
The silhouettes must match the source frame exactly.
Every outline follows the person's real edge in that frame.
NO frozen silhouette from a previous frame.
NO silhouette that swells, shrinks or wobbles without the person moving.
FRAME-TO-FRAME SHADOW LIFE
THIS IS CRITICAL.
It must feel like the Bad Apple PV: crisp, flat, rhythmic.
Allow between consecutive frames:
* the outline to change ONLY where the person moved
* polarity to flip ONLY on the chosen beats
Keep FIXED:
* the two colours
* the outline smoothness
* the gap width between overlapping people
* the blank ground
DO NOT
Do NOT use any grey or gradient.
Do NOT keep photographic faces, skin, clothing patterns or room detail.
Do NOT draw line-art outlines instead of solid shapes.
Do NOT add halftone, dither, paper texture, film grain, glow or blur.
Do NOT add a red or any colour accent.
Do NOT leave furniture, screens or plants as silhouettes.
Do NOT let separation gaps flicker or wander.
Do NOT create new poses.
Do NOT change anatomy.
Do NOT change clothing.
Do NOT replace the person's face shape.
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
* NO colour change
* NO thresholding or silhouettes
* NO polarity flips
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
Do NOT begin the shadow-art transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – BAD APPLE SHADOW-ART STYLING (AFTER MY CONFIRMATION ONLY)
First, tell me which frames you will flip polarity on, when the split screen starts, and what counts as a figure (people, held objects) and what is removed.
Then style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation, so every silhouette is exactly that frame's outline.
Apply every style rule above, with the SAME two colours, outline smoothness and gap width on every frame.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing, a grey pixel, a leftover background object or a flickering gap appears — regenerate those frames only.
The final video must feel like THE BAD APPLE!! PV: crisp black-and-white shadows, flipping on the beat, 12 frames per second.
The image should deliberately contain:
* only pure black and pure white
* solid silhouettes recognizable from the outline alone
* thin clean gaps between overlapping people
* hard polarity flips and a split screen with inverting figures.
Avoid grey, texture and any leftover room detail.
```
