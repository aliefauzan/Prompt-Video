# 85 — Drawing Time-Lapse Reveal

**Look:** The clip is "drawn" over its own length, like a sped-up digital-painting time-lapse, while the people keep moving exactly as in the source. It starts as blank paper. Loose blue construction lines appear, then clean dark line art is inked over them from the heads down. Flat colours drop in one colour region at a time, then shading is brushed on. The background is painted in loose washes after the figures, and the last seconds add highlights and polish while the blue sketch fades away. A round brush cursor moves along the edge being drawn.

**Also called / where it trends:** "drawing time-lapse", "speedpaint", "Procreate time-lapse", "sketch to colour", "drawing process reveal", "art process video", "line art to colour transition", "DrawUndo" (the reversed version). It trends as Wan 2.1 video LoRAs on Civitai (Drawing Time-Lapse, DrawUndo), as Morphic's "digital art timelapse" generator, and as the endless "sketch → final" art reels on TikTok and Instagram, which AI edits now copy using real footage.

**References:**
- https://civitai.com/models/1389992 (screenshot `refs/ref_1.png`): "Drawing Time-Lapse — Wan 2.1 T2V 14B LoRA", trained on time-lapse recordings of the author's own drawings. Its tips: trigger words "time lapse, drawing, 2d, illustration, static camera, brushstrokes, coloring". It also works with First-and-Last-Frame-to-Video by putting a white frame first and the finished image last.
- https://civitai.com/models/1397074 (screenshot `refs/ref_2.png`): "DrawUndo — Wan 2.1 I2V 720p LoRA", the reverse effect (a finished picture un-draws back to sketch).
- https://morphic.com/resources/videos/digital-art-timelapse-videos: Morphic's digital-art time-lapse video generator page (from D3).

How it differs from the styles already in the library: **18 Pencil Sketch Rotoscope** is a static graphite look on every frame. **61 Colored Marker Sketch** is a fixed marker rendering. This style is a PROGRESSION. The stage of the drawing changes over the clip (paper → sketch → ink → flat colour → shading → final), so every second of the video looks different, while the drawn people still track the footage.

**Example:** `example.png` (six frames of the test clip, so you see the build-up stages at 1, 4, 7, 9, 12 and 14.8 s), `before_after.png` (frame 049, mid line-art), `example.mp4` (the whole clip at 12 fps with the original audio) and `preview.webp`. This is a local approximation made with `render.py` (numpy + OpenCV + the person masks). For each frame it builds every layer of the finished drawing for that pose: an XDoG blue sketch drawn in three jittered passes, XDoG line art plus the silhouette, flat fills from a fixed k-means palette, painted shading from local value, and a posterised wash background. It then shows each layer only where its "order map" is below the stage progress. The order maps are stroke-shaped noise with a top-down bias for the lines, the colour region's turn for the fills (one paint at a time), and smeared noise for the shading and the background. A cursor ring is drawn on the active edge.

## Prompt

```text
I'm uploading one video clip. Convert it into a DRAWING TIME-LAPSE REVEAL frame-by-frame animation: over the length of the clip, the picture should be drawn from a blank page to a finished digital illustration, like a sped-up speedpaint recording, while the people keep moving exactly as in the footage, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
(This style needs a different drawing stage on every frame, so each frame gets its own generation with its own stage instruction from the schedule below.)
CORE VISUAL STYLE
Drawing time-lapse, speedpaint, digital illustration being drawn live, blue construction sketch, clean line art, flat colour fills, brushed shading, white paper background, static camera.
Transform the footage into a drawing that builds up over time:
* BLANK PAPER at the very start (warm white, faint paper grain)
* a LOOSE BLUE CONSTRUCTION SKETCH: light, overlapping, searching lines
* CLEAN DARK LINE ART inked over the sketch, heads first, then downwards
* FLAT COLOUR FILLS dropped in one colour region at a time (all skin, then hair, then each garment)
* SHADING brushed in with visible stroke-shaped passes
* the BACKGROUND painted after the figures, in loose washes
* final HIGHLIGHTS and polish; the blue sketch fades away
* a round BRUSH CURSOR on the edge being drawn
The result should feel like someone:
OPENED A BLANK CANVAS
→ ROUGHED IN THE POSE WITH A BLUE PENCIL
→ INKED CLEAN LINES ON TOP
→ BUCKET-FILLED THE FLAT COLOURS
→ BRUSHED IN THE SHADING
→ PAINTED THE ROOM BEHIND THEM
→ POLISHED THE HIGHLIGHTS
→ AND RECORDED THE WHOLE THING AS A SPED-UP TIME-LAPSE.
STAGE SCHEDULE (progress p = frame index / last frame index, 0 → 1)
* p 0.00-0.04: blank paper only.
* p 0.04-0.24: the blue construction sketch appears stroke by stroke, top of the frame first.
* p 0.22-0.42: clean dark line art is inked over the sketch, heads first, then bodies.
* p 0.40-0.62: flat colours fill in, one colour region at a time (skin, then hair, then each garment).
* p 0.58-0.82: shading is brushed onto the flat colours in stroke-shaped passes.
* p 0.55-0.90: the background is painted in loose washes, figures first, room after.
* p 0.82-1.00: highlights, soft glow and final polish; the blue sketch fades out; the last frames are the finished illustration.
Each frame shows EXACTLY its stage: everything finished in earlier stages stays, the current stage is partly done, later stages are not started.
The amount drawn grows steadily from frame to frame; it never goes backwards.
CHARACTER — DRAWN, NOT PHOTOGRAPHED
Draw each person as a clean digital illustration, but keep them unmistakably the SAME person at every stage.
Preserve the person's exact:
* identity
* face shape and features
* expression
* hairstyle
* glasses
* clothing and its pattern (stripes stay stripes, the batik pattern is drawn)
* accessories
* pose
* body proportions
* movement
* hand position
* interaction with objects
The drawing on each frame follows THAT frame's pose: the people keep moving while they are being drawn.
Do NOT freeze the pose while drawing.
Do NOT turn the people into anime characters with different faces.
LINES AND PAINT
* Blue sketch: light cyan-blue, thin, loose, overlapping, with a few construction marks.
* Line art: dark warm grey-brown, clean, confident, slightly varied weight.
* Flat colours: clean, slightly brighter than the footage, one flat value per region.
* Shading: soft brushed value steps on top of the flats, never photographic.
* Final polish: small highlights, a gentle glow, a slight contrast lift.
BACKGROUND
* Keep the SAME room layout: window, plant box, cupboards, screen, chair, perspective.
* Before p 0.55 the room is blank paper with at most faint grey pencil guide lines.
* From p 0.55 the room is painted in loose posterised washes, sweeping across the frame.
CURSOR
* A small round brush-cursor ring (dark ring with a thin white outline) sits on the edge currently being drawn.
* It jumps along with the work like a real time-lapse cursor; it never covers a face.
PALETTE
Warm white paper, light cyan-blue sketch, dark grey-brown ink.
Clean illustration colours based on the footage.
Do NOT use neon or heavy filters.
OBJECT CONTINUITY
If the character holds an object, it is drawn at the same stage as the hand holding it.
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
The drawn people must match the source frame exactly: same silhouette, pose and position.
NO drawn part left behind where a person was on a previous frame.
NO stage that jumps backwards.
FRAME-TO-FRAME DRAWING LIFE
THIS IS CRITICAL.
It must feel like a real drawing recording, not a slow fade.
Allow between consecutive frames:
* new strokes, fills and brush passes to appear in chunks
* the blue sketch lines to be re-drawn slightly every few frames
* the cursor to jump along the active edge
Keep FIXED:
* the stage schedule
* each region's flat colour once it is filled
* the paper colour and grain
DO NOT
Do NOT cross-fade from the photo to the drawing.
Do NOT show the original photo at any stage.
Do NOT keep a static pencil-sketch look for the whole clip.
Do NOT reveal everything at once.
Do NOT add hands, styluses, app interfaces or watermarks.
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
* NO sketch, line art or colour
* NO paper, cursor or reveal
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
Do NOT begin the drawing time-lapse transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – DRAWING TIME-LAPSE STYLING (AFTER MY CONFIRMATION ONLY)
First, give me the stage table: for every frame number, its progress p and which stages are done, in progress (with % done) and not started. Also list the flat colour for each region and the order the regions are filled.
Then style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation, so the people are exactly that frame, and give each generation its row of the stage table.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing, the stage schedule or a filled colour broke (or the drawing went backwards) — regenerate those frames only.
The final video must feel like A SPEEDPAINT OF THE SCENE BEING DRAWN LIVE: blank page, blue sketch, ink, flat colours, shading, background, polish, the people moving the whole time, 12 frames per second.
The image should deliberately contain, at the right stage:
* warm white paper
* a light-blue construction sketch
* clean dark line art
* flat colour regions filled one at a time
* brushed shading
* a loosely painted background
* a brush cursor on the active edge.
Avoid a cross-fade.
```
