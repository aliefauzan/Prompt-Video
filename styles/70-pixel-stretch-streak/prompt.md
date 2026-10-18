# 70 — Pixel Stretch Slit Streak

**Look:** The people stay sharp photographs, but a one-pixel slit is cut through each of them just inside their trailing edge. That single line of pixels is pulled sideways into long, hard-edged ribbons of their own colours: hair, skin, batik brown, beige-and-white shirt stripes. The ribbons run until they hit the next person or the frame edge. Everyone looks like they are tearing out of a band of stretched colour, while the room above them stays real.

**Also called / where it trends:** "pixel stretch", "pixel stretch effect", "pixel drag", "slit streak", "colour trail", "stretched pixels" — a Photoshop poster technique (single-row/single-column marquee → Free Transform stretch) that moved to Instagram Reels and TikTok edits (#pixelstretcheffect, about 2.3K reels) and to sports, car and fashion posters on Pinterest and Behance. In video it is done in After Effects with "Slit Scan" / "Stretch" plugins or by tracking a 1 px slice of the subject.

**References:**
- https://www.pinterest.com/search/pins/?q=pixel%20stretch%20effect (screenshot `refs/ref_1.png`, from the discovery sweep D2): skater, basketball player, walking man and cars, each with straight or curved hard-edged ribbons coming out of the subject.
- https://www.instagram.com/popular/pixel-stretch-effect/: Instagram tag page for the effect (Reels edits).
- https://phlearn.com/tutorial/how-to-create-a-pixel-stretch-effect-in-photoshop/ (screenshot `refs/ref_2.png`): PHLEARN tutorial; the runner's back half becomes long smeared ribbons while her face and front stay sharp.
- https://design.tutsplus.com/tutorials/how-to-create-a-pixel-stretch-in-photoshop--cms-39408: Envato Tuts+ step-by-step (1 px column selection → stretch → mask).
- https://www.matiash.com/blog/ps-pixel-stretching-tutorial: Matt Kloskowski on pixel stretching, with examples where the slit goes through the subject.
- https://www.youtube.com/watch?v=mJQC797OyXQ: YouTube tutorial "How to Create a Pixel Stretch Effect in Photoshop".
- https://www.skillshare.com/en/classes/easily-make-this-colour-trail-using-pixel-stretch-effect-from-a-photo-in-adobe-photoshop/1657440118: Skillshare class on the colour-trail version.

How it differs from taken styles: **26 Slow Shutter Smear** is a soft time-based ghost of earlier frames. This is one frame only, a hard-edged one-pixel extrusion with the subject crisp. **05 Datamosh** is codec damage with macroblocks and colour blooms; there are no blocks or broken frames here, only clean straight streaks.

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049), `example.mp4` (the whole clip at 12 fps with the original audio) and `preview.webp`. This is a local approximation made with `render.py` (numpy + OpenCV + the person masks). On every pixel row it finds each person's left edge and samples a short slit a little inside it (the depth scales with the silhouette width, so small faces are not cut). It then extrudes that colour leftwards as a hard 1 px streak, up to the next person or the frame edge. The thin strip of the person behind the slit is swallowed, so people seem to tear out of the ribbons. The ribbons get a slight saturation push, a sheen that fades with distance and 1 px row contrast. The streaks follow the people's real edges, so they change with the motion and do not flicker on their own.

## Prompt

```text
I'm uploading one video clip. Convert it into a PIXEL STRETCH / SLIT STREAK frame-by-frame animation: in every frame the people stay sharp photographs, and a single line of pixels cut through each person is pulled sideways into long, hard-edged colour ribbons, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Transform the footage into a pixel-stretch edit built from:
* SHARP, untouched photographic people
* a ONE-PIXEL SLIT cut vertically through each person, just inside their trailing (left) edge
* that slit's pixels EXTRUDED sideways into long straight STREAKS
* streaks that are exactly 1 pixel tall per row, perfectly horizontal and HARD-EDGED
* ribbon colours taken ONLY from the person at the slit: hair black-brown, skin tan, batik brown, beige-and-white shirt stripes, charcoal grey
* ribbons that run until they meet the next person or the frame edge
* a subtle glossy sheen on the ribbons, slightly darker further from the person
* a slight colour push on the ribbons (richer, a touch more contrast than the photo)
* the REAL room still visible above the heads and wherever no person trails
The result should feel like someone:
SHOT A CLEAN PHOTO OF EVERY FRAME
→ SELECTED A ONE-PIXEL COLUMN THROUGH EACH PERSON
→ STRETCHED THAT COLUMN ACROSS THE FRAME
→ MASKED THE PERSON BACK ON TOP
→ LET THE PEOPLE TEAR OUT OF THEIR OWN COLOUR TRAILS
→ PLAYED IT BACK FRAME-BY-FRAME.
CHARACTER — PHOTOGRAPHIC, CRISP
The people stay PHOTOGRAPHIC and SHARP in front of the slit.
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
Do NOT blur, smear or motion-blur the people.
Do NOT beautify or re-sculpt faces.
THE SLIT AND THE STREAKS
* The slit sits a little inside each person's LEFT edge, on every row: in the hair, the shoulder, the sleeve, the arm, the trouser leg.
* The slit is shallow: about one twelfth of the person's width on that row, never deeper than about 35 px at 1620 px frame width.
* NEVER put the slit through a face. If a face is at the left edge of a person, the slit goes through the hair or the background side of the head instead.
* Everything to the left of the slit, up to the next person or the frame edge, is replaced by that row's slit colour repeated: one solid colour per pixel row.
* Rows where the slit crosses the woman's striped shirt become alternating beige and cream ribbons. Rows through hair become near-black ribbons. Rows through skin become warm tan ribbons. Rows through the batik shirt become deep brown and rust ribbons.
* Streaks are perfectly HORIZONTAL and STRAIGHT. No curves, no waves.
* Streak ends are HARD where they meet a person: no feathering, no glow.
* Rows above the heads and below the people that have no person in them keep the real room.
RIBBON FINISH
* A thin brighter sheen right next to the slit, as if the stretched pixels catch the light.
* The ribbons darken by about 25% towards the far end.
* Saturation +30%, contrast slightly up, on the ribbons only.
* Fine 1 px row-to-row tone differences so the stretched rows read as pixels, not as a smooth gradient.
DIRECTION
* All streaks run to the LEFT, as if the people are moving right at high speed.
* Keep that direction for the whole clip.
BACKGROUND
* The office stays a normal sharp photo wherever no ribbon covers it.
* Do not grade, blur or restyle the room.
PALETTE
The people's own colours only, stretched: black-brown hair, warm tan skin, batik brown and rust, beige and cream stripes, charcoal grey.
Do NOT add neon, rainbow or colours that are not on the people.
OBJECT CONTINUITY
If a hand or arm reaches out, it is part of the person: it gets its own slit and its own short streak, and stays sharp in front of it.
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
The slit follows each person's real edge in every frame, so the ribbons change colour as the person moves (a lowered head turns a band of rows from hair to skin, a raised hand adds a short tan streak).
NO ribbon pattern frozen from a previous frame.
NO streak that stays on screen after the person who made it has moved.
FRAME-TO-FRAME BEHAVIOUR
Allow between consecutive frames:
* ribbon colours to shift only where the person at the slit moved
* the sheen to shimmer very slightly
Keep FIXED:
* the streak direction (left)
* the slit depth rules
* the room where no ribbon covers it
* the people's sharpness
DO NOT
Do NOT motion-blur or smear the whole frame.
Do NOT make soft directional blur instead of hard 1 px streaks.
Do NOT add macroblocks, datamosh smears or RGB split.
Do NOT add ghost copies of earlier frames.
Do NOT curve or wave the ribbons.
Do NOT cut through any face.
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
* NO slit or pixel streaks
* NO colour push
* NO sheen
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
Do NOT begin the pixel stretch transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – PIXEL STRETCH STYLING (AFTER MY CONFIRMATION ONLY)
First, tell me the streak direction and the slit depth rule you will use, and name any frame where a face sits at a person's left edge (and where the slit will go instead).
Then style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation, so the people are exactly that frame and the ribbon colours come from that frame's own pixels.
Apply every style rule above, with the SAME direction and finish on every frame.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing, a cut face or a soft (blurred) streak broke the style — regenerate those frames only.
The final video must feel like THE PEOPLE ARE TEARING OUT OF THEIR OWN STRETCHED PIXELS: sharp photographic people, hard one-pixel colour ribbons trailing to the left, the real room above, 12 frames per second.
The image should deliberately contain:
* sharp untouched people
* a one-pixel slit just inside each person's trailing edge
* long straight hard-edged ribbons in the person's own colours
* striped ribbons from the striped shirt
* a glossy sheen fading along each ribbon.
Avoid soft motion blur.
```
