# 02 — VHS Camcorder Home Video

**Look:** the clip becomes a 1990s camcorder tape played back on a VCR: soft low-resolution picture, milky lifted blacks, smeared colour that bleeds to the right of every edge, edge-enhancement halos, wobbling lines, a rolling tracking band of white snow streaks, torn head-switching noise along the bottom, and a burned-in camcorder display (blinking red ● REC, battery, tape counter, "OCT.18 1997 / 10:24:07 AM" date stamp).

**Also called / where it trends:** "VHS filter", "vintage camcorder effect", "90s home video", "camcorder aesthetic", "VHS edit", "Handycam look", "found footage look" — TikTok's built-in *Vintage Camcorder* effect trend (the "Watermelon Sugar" look-into-the-past trend), CapCut VHS templates, YouTube Shorts tutorials, ntsc-rs / Prequel / camcorder apps; real Sony Handycam revival on TikTok.

**References:**
- https://www.tiktok.com/discover/how-to-make-videos-look-like-90s-vhs — screenshot `refs/ref_1.png`: TikTok "How to Make Videos Look Like 90s VHS": PLAY ▶ / date stamp OSD, washed colour, soft picture
- https://www.youtube.com/results?search_query=90s+vhs+camcorder+effect+home+video — screenshot `refs/ref_2.png`: "Efek VHS asli GRATIS", "TV VHS Combo", "Footage captured with a vintage…", raw 1991 camcorder home-video playlist
- https://github.com/ntsc-rs/ntsc-rs — screenshot `refs/ref_3.png`: open-source NTSC/VHS emulator (chroma low-pass and delay, head switching, tracking noise, edge wave, snow) — the signal model used for `render.py`
- https://www.dexerto.com/entertainment/how-to-do-tiktok-viral-vhs-filter-trend-1646026/ — the TikTok "Vintage Camcorder" VHS filter trend explained
- https://www.olddry.com/how-to-do-the-retro-vhs-effect-on-tiktok/ — how creators fake the retro VHS effect on TikTok
- https://www.capcut.com/explore/vhs-effect — CapCut VHS effect template gallery
- https://www.tiktok.com/@pvresilk/video/7286214255588691233 — real Sony Handycam footage for the 90s vibe

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049). Local approximation made with `render.py` (numpy + OpenCV YIQ signal emulation + Pillow OSD); 6 frames in `frames/` (`render.py ... all` renders all 179).

## Prompt

```text
I'm uploading one video clip. Convert it into an authentic 1990s VHS CAMCORDER HOME VIDEO, styled frame by frame, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Transform the footage into a worn analog home-video tape built from:
* soft, low-resolution standard-definition picture (about 240 lines of real detail)
* milky, lifted blacks and soft-clipped, blooming whites
* colour that is smeared sideways and bleeds to the RIGHT of edges (chroma bleed / chroma delay)
* thin bright and dark halos along hard edges (edge-enhancement ringing)
* slightly wobbling horizontal lines (time-base jitter)
* a rolling TRACKING BAND of white horizontal snow streaks
* HEAD-SWITCHING NOISE: the bottom few lines torn sideways with static
* horizontally stretched tape noise and colour streaks
* faint interlace scanlines
* a camcorder ON-SCREEN DISPLAY burned into the picture
* the colour of a 1990s consumer CCD under office fluorescent light
* a slight dark vignette and a dark blanking edge on the left side
The result should feel like someone:
FILMED THE SCENE ON A 1997 HANDYCAM
→ WITH THE DATE STAMP SWITCHED ON
→ RECORDED IT ON SP TAPE
→ LEFT THE TAPE IN A DRAWER FOR 25 YEARS
→ PLAYED IT BACK ON A TIRED VCR
→ CAPTURED THE PLAYBACK FRAME BY FRAME.
CHARACTER — UNCHANGED PEOPLE, DEGRADED SIGNAL
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
Do NOT turn anyone into a cartoon or illustration.
Do NOT beautify, smooth or retouch faces.
The VHS look is a SIGNAL DEGRADATION applied on top of the real picture, not a repaint.
Faces must stay recognizable through the softness and noise.
RESOLUTION AND SOFTNESS
Make the picture look like 480i standard definition blown up to the full frame.
* fine textures (hair strands, fabric weave, small print) melt into soft blur
* horizontal detail is softer than vertical detail
* edges get a thin light halo on one side and a dark halo on the other (sharpening ringing)
It should NOT look like a modern 4K image with a filter on top.
It should NOT look like a gaussian blur either: detail is lost sideways, with ringing.
COLOUR — CHROMA BLEED
The colour channel has much lower resolution than the brightness.
* colours spill 5–10 pixels to the RIGHT of their objects
* red, orange and brown areas smear and fringe the most
* skin keeps a natural but slightly warm, slightly over-red camcorder tone
* overall palette: warm, slightly green fluorescent office cast, gently faded
* blacks are lifted to a milky dark gray, never pure black
* bright windows and white walls clip softly and bloom
Do NOT use teal-and-orange cinema grading.
Do NOT use neon or vaporwave colours.
TAPE ARTIFACTS
Every frame carries real VHS playback damage:
* TRACKING BAND: a horizontal band 20–60 px tall where lines shift sideways and short white snow streaks appear; it rolls slowly up or down the frame over consecutive frames and comes and goes
* HEAD-SWITCHING NOISE: the bottom 8–14 lines of the frame are torn sideways to the right with static, every frame
* TIME-BASE JITTER: vertical edges wobble by 1–3 px from line to line
* DROPOUTS: occasional single bright horizontal streaks
* TAPE NOISE: fine horizontal luma grain and faint colour streaks across the whole picture
* a dark 4–8 px blanking edge on the left side of the frame
Keep artifacts mostly away from the centre of faces, but do not avoid faces completely; the tracking band may cross a face for a few frames.
ON-SCREEN DISPLAY (OSD)
Burn a classic camcorder display into the picture, in a chunky white monospace pixel font with a hard 2 px black drop shadow:
* top-left: a red ● dot + "REC" (dot blinks about twice per second) — or "PLAY ▶" in playback sections
* under it: a tape counter "0:00:07" that advances in real time
* top-right: a battery icon with three bars — or "SP" in playback sections
* bottom-right: date stamp "OCT.18 1997"
* under the date: time "10:24:07 AM" whose seconds advance in real time
The OSD is part of the recorded signal: it is slightly soft, it carries the same chroma bleed and it wobbles with the line jitter.
Keep the OSD text identical in size, font and position across all frames; only the counters, the blinking dot and the section labels change.
Spell every OSD word exactly as written above.
SECTIONS
Plan the clip in sections, for example:
* first 5 seconds: "● REC" + battery (camera recording)
* middle 5 seconds: "PLAY ▶" + "SP" (VCR playback)
* last 5 seconds: "● REC" + battery again
The tape damage, colour and softness stay the same in every section.
FRAME-BY-FRAME TAPE BOIL
THIS IS CRITICAL.
Every frame must look like a different moment of a moving tape.
Allow, every frame:
* tape noise pattern to change completely
* the tracking band to move to a new height
* line jitter to change
* head-switching tear to change length
* dropout streaks to appear and disappear
* slight brightness flicker
Do NOT freeze the noise.
Do NOT copy the same noise pattern between frames.
PERFECT MOTION TRACKING
The underlying character movement must remain exactly faithful to the source footage.
The SIGNAL jitters.
The HUMAN MOTION does NOT.
If the head moves:
the picture follows exactly.
If the hand moves toward the camera:
it moves exactly as in the source, only softer and noisier.
If the character interacts with an object:
the object moves exactly with the original action.
NO ghosting from previous frames beyond the slight soft smear of the tape.
NO added camera shake.
NO zoom, crop or reframing.
OBJECT CONTINUITY
Keep every object the people hold or touch (phone, chair, bag, cup, glasses).
Do NOT remove or invent objects.
COMPOSITION
Keep the full original framing, aspect ratio and camera position.
Do NOT add black bars, a TV set, a monitor bezel or a VHS cassette graphic.
The picture itself IS the tape.
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
Do NOT use a generic "retro" Instagram filter (no simple sepia, no film grain, no light leaks).
Do NOT use film scratches, sprocket holes or film burns — this is VIDEO TAPE, not film.
Do NOT add CRT curvature, RGB phosphor masks or TV frames.
Do NOT add glitch-art datamosh or pixel sorting.
Do NOT use neon, vaporwave pink/purple or rainbow colours.
Do NOT misspell or change the OSD text.
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
* NO VHS noise
* NO tracking band
* NO chroma bleed
* NO on-screen display
* NO date stamp
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
Do NOT begin the VHS transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – VHS CAMCORDER STYLING (AFTER MY CONFIRMATION ONLY)
Style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation.
Apply every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT restyle a whole shot from one keyframe.
Plan the sections first and list them to me (frame range, OSD labels, tracking-band behaviour) before generating.
Keep the colour grade identical in every frame.
If Seedream cannot keep the OSD text perfectly consistent, generate the degraded picture with Seedream and add the OSD as a locked text layer on top, then apply the same softness, chroma bleed and jitter to that layer so it sits inside the signal.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose or the style rules broke — regenerate those frames only.
The final video must feel like a REAL HOME-VIDEO TAPE FROM 1997: soft, warm, smeared, noisy, alive.
The image should deliberately contain:
* low-resolution softness with edge ringing
* chroma bleed to the right
* milky blacks and blooming whites
* line jitter
* a rolling tracking band
* head-switching noise at the bottom
* tape noise that changes every frame
* the burned-in camcorder OSD and date stamp.
Avoid digital perfection.
```
