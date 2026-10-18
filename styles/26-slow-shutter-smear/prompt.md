# 26 — Slow Shutter Smear

**Look:** A 12 fps fake long exposure. Every frame keeps a sharp lead exposure of the person, with discrete stepped ghost copies of earlier moments trailing behind. Each copy streaks along its own motion path, and a slight camera drag makes the trails read. Static areas stay sharp and the colour grade is untouched. This is the Wong Kar-wai step-printing look.

**Also called / where it trends:** "slow shutter effect", "12 fps slow shutter", "step printing", "Wong Kar-wai effect", "Chungking Express effect", "shutter drag", "long exposure video". Floww (@goowithdafloww) posts it on Instagram as an invideo agent prompt. It also trends on TikTok and YouTube as Wong Kar-wai step-print tutorials for AE, Premiere and CapCut.

**References:**
- https://www.instagram.com/p/Dd6h1XjRau7/ (screenshots `refs/ref_1.png`, `refs/ref_2.png` result frames; `refs/ref_3.png` the prompt; `refs/ref_4.png` the agent's follow-up question; `refs/ref_5.png` post page): **Slow Shutter Effect** by Floww (@goowithdafloww), posted 30 Sep 2026. The quoted prompt line "I want to create this 12 fps, slow shutter, high motion blur effect… keep the color grading part untouched" is Floww's own invideo agent prompt, shown in the reel. The "camera and subject motion, go heavy" rule comes from the agent's follow-up options shown in the same reel. Credit: Floww.
- https://www.instagram.com/goowithdafloww/: creator page (AE/Premiere presets, invideo partner).
- https://www.indepthcine.com/videos/chungking-express: how Christopher Doyle and Wong Kar-wai got the smeared step-printed look in Chungking Express.
- https://www.austinschmidt.com/blog-/step-printing-wong-kar-wai: step printing explained (slow shutter at a low frame rate, each frame printed several times).
- https://augustinhuffman.com/blog/2020/11/5/how-to-utilize-step-printing: how to fake step printing in an edit.
- https://www.chungdha.nl/?p=26282: article on the Wong Kar-wai step-printing look (found via Exa search).
- https://www.reddit.com/r/cinematography/comments/90o6is/can_anyone_tell_me_how_this_shot_from_chungking/: r/cinematography thread on the Chungking Express smear shot.

**Example:** `example.png` (six frames of the test clip) and `before_after.png` (frame 049). This is a local approximation made with `render.py` (numpy + OpenCV). It averages a lightly dragged plate for the background. It stacks five masked echoes of the people from 2–10 frames back, each streaked along its Farneback optical flow and shifted by a per-section camera drag. The current frame goes on top with only its fast-moving parts smeared, followed by highlight bloom and grain.

## Prompt

```text
I'm uploading one video clip. Convert it into a 12 FPS SLOW-SHUTTER / STEP-PRINTED MOTION SMEAR frame-by-frame animation, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
I want to create this 12 fps, slow shutter, high motion blur effect for my video. Don't use the flat Direction Blur - generate each frame like the reference. Also keep the color grading part untouched.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
Seedream works here because every styled frame is built from several neighbouring source frames given as image inputs; no video model is needed.
CORE VISUAL STYLE
Every frame becomes ONE long exposure of a short slice of time:
* a sharp, readable LEAD exposure of the current moment
* discrete stepped GHOST copies of earlier moments trailing behind it
* streaks that follow each body part's own motion path
* hands, hair and fast limbs smeared into ribbons
* static background kept sharp where nothing moves
* a slight camera drag during the exposure so the trails read
* highlights that drag into soft glowing streaks
* fine cine grain
* the ORIGINAL colour grade, untouched
It should look like Wong Kar-wai step printing: Chungking Express, Fallen Angels.
The result should feel like someone:
SHOT THE SCENE AT A VERY SLOW SHUTTER
→ DRAGGED THE CAMERA A LITTLE DURING EACH EXPOSURE
→ PRINTED EVERY FRAME SEVERAL TIMES OVER THE NEXT ONES (STEP PRINTING)
→ KEPT ONLY 12 FRAMES PER SECOND
→ ANIMATED IT FRAME-BY-FRAME.
CHARACTER — PHOTOGRAPHIC, IN MOTION
The people stay PHOTOGRAPHIC.
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
Do NOT turn them into a cartoon or painting.
LEAD EXPOSURE
The person's CURRENT position is the lead exposure.
It is the clearest, most opaque layer.
Faces must stay readable in the lead exposure.
Only the fastest parts (a swinging hand, a head turn, flying hair) may smear inside the lead itself.
STEPPED GHOST ECHOES
Behind the lead, stack 4–6 earlier positions of the same person as translucent copies.
The echoes are DISCRETE steps, not one continuous blur.
The oldest echo is the faintest.
Each echo sits along the real path the body travelled in the source footage.
Each echo is itself streaked along its own motion direction.
Where the person barely moves, the echoes collapse onto the lead and the image stays sharp.
MOTION STREAKS, NOT DIRECTIONAL BLUR
Streaks must follow the true motion of each part of the body.
A hand moving up streaks up.
A head turning left streaks left.
The torso can stay almost sharp while a hand streaks.
Do NOT apply one flat directional blur to the whole frame.
Do NOT use a radial zoom blur.
CAMERA DRAG
Add a gentle camera drift during each exposure (slow push or sideways drift).
Keep the drift direction constant within a section of the clip.
Change direction only at section boundaries.
The background picks up only a soft drag from this drift.
BOTH CAMERA AND SUBJECT MOTION
Use both camera drag and subject motion, and go heavy like the references.
The trails must be clearly visible at phone-screen size.
COLOUR GRADE — UNTOUCHED
Keep the source colours, white balance, contrast and saturation exactly as they are.
Do NOT add a teal-orange look, a film emulation or a new LUT.
The only allowed changes:
* bright highlights may bloom softly along their streaks
* fine grain
OBJECT CONTINUITY
If the character holds or touches an object (phone, cup, bag, microphone), the object smears with the hand exactly as it moves.
Do NOT drop it from the lead exposure.
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
The lead exposure must match the source frame exactly in position, pose and timing.
The echoes come ONLY from earlier source frames.
Do NOT invent motion that is not in the footage.
Do NOT put echoes ahead of the person (no future positions).
If the person stands still, the frame is nearly sharp.
FRAME-TO-FRAME BEHAVIOUR
THIS IS CRITICAL.
Every frame is its own exposure.
Allow between consecutive frames:
* the shutter length to vary slightly (trails a little longer or shorter)
* grain to change
* highlight bloom to flicker slightly
Keep FIXED within a section:
* camera drag direction
* number of echoes
* colour grade
The 12 fps cadence must read as a stutter, like step-printed film.
DO NOT
Do NOT use a flat Direction Blur.
Do NOT use a radial or zoom blur.
Do NOT blur the whole frame evenly.
Do NOT make faces unreadable in the lead exposure.
Do NOT change the colour grade.
Do NOT add light leaks, film burns or colour shifts.
Do NOT add speed lines or drawn motion lines.
Do NOT redraw or illustrate the people.
Do NOT create new poses.
Do NOT change anatomy.
Do NOT change clothing.
Do NOT replace the person's face.
Do NOT interpolate new in-between frames.
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
* NO motion blur or echoes
* NO camera drag
* NO colour changes
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
Do NOT begin the slow-shutter transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – SLOW-SHUTTER SMEAR STYLING (AFTER MY CONFIRMATION ONLY)
First, plan the sections and list them for me: frame range, camera drag direction, and which earlier frames feed each frame's echoes (for example the frames 2, 4, 6, 8 and 10 positions back).
Then style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Give Seedream the current extracted frame as the main image input, plus the earlier frames that form its echoes as extra image inputs.
The lead exposure must come from the current frame only.
Apply every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing or the style rules broke — regenerate those frames only.
The final video must feel like STEP-PRINTED SLOW-SHUTTER FILM: every moment a long exposure with stepped ghost trails, 12 frames per second, colours untouched.
The image should deliberately contain:
* a sharp lead exposure
* stepped translucent ghost echoes
* streaks along the real motion paths
* a gentle camera drag
* soft highlight streaks
* fine grain
* the original colour grade.
Avoid polished digital perfection.
```
