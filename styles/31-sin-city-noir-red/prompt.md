# 31 — Sin City Noir Red

**Look:** The footage is shot like *Sin City* (2005) and drawn like Frank Miller's comic. The image is crushed to pure ink black and paper white with almost no greys. Faces and clothes are cut out of the dark by hard light. White rain cuts across the frame and inverts whatever it crosses. One colour is allowed: a saturated blood red, only on lips and a few chosen objects. In some passages the shot flips into Miller's negative mode: white silhouettes with black ink lines on a black ground.

**Also called / where it trends:** "Sin City effect", "Sin City style", "selective colour / colour splash noir", "Frank Miller noir", "black white and red edit". The look is a perennial editing tutorial (After Effects, Final Cut Pro, Boris FX, Blender). It is now an AI video style preset ("High-Contrast Sin City Style" on Hypernatural), and noir "one colour" edits keep recurring on TikTok and Reels.

**References:**
- https://www.pinterest.com/search/pins/?q=sin%20city%20movie%20stills%20black%20white%20red: film stills showing the hard black/white with spot red (screenshot `refs/ref_1.png`).
- https://www.pinterest.com/search/pins/?q=frank%20miller%20sin%20city%20comic%20panel%20rain: Miller's comic panels with white rain, negative silhouettes and solid blacks (screenshot `refs/ref_2.png`).
- https://app.hypernatural.ai/video-styles/high-contrast-sin-city-style: AI video style preset described as stark black-and-white, selective colour, rain-slicked, silhouettes.
- https://borisfx.com/videos/sin-city-style-in-adobe-ae/: Boris FX, "Sin City Style in Adobe After Effects".
- https://www.reddit.com/r/VideoEditing/comments/5sgk90/sin_city_isolating_color_effect_tutorial_for/: r/VideoEditing, isolating colour for the Sin City effect.
- https://idustrialrevolution.com/blogs/tutorials/how-to-make-the-pleasantville-or-sin-city-effect-in-final-cut-pro-x-10-4: the Sin City effect in Final Cut Pro X.
- https://blenderdiplom.com/en/tutorials/all-tutorials/424-tutorial-sin-city-effect-in-blender.html: Blender Diplom, the Sin City effect in Blender's compositor.

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049), `example.mp4` (whole clip) and `preview.webp`. This is a local approximation made with `render.py` (numpy + OpenCV + the person masks + Apple Vision face landmarks in `faces.json`). The room is thresholded so that only the window and screen stay white. The people are CLAHE-lit and hard-inked with Canny lines and a white rim. 520 rain streaks are redrawn every frame and invert what they cross. The red leaves in the room and the woman's lips are the only colour. Frames 97-120 and 157-166 switch to the negative white-silhouette mode.

## Prompt

```text
I'm uploading one video clip. Convert it into a SIN CITY NOIR RED frame-by-frame animation (the Frank Miller / Sin City 2005 look), matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Transform the footage into a living Frank Miller comic panel:
* PURE INK BLACK and PAPER WHITE, with almost no grey in between
* hard, high-contrast light that carves faces and clothes out of darkness
* most of the background swallowed by solid black
* only the brightest shapes (windows, screens, lamps) stay white
* a WHITE RIM LIGHT around the people's silhouettes
* WHITE RAIN slashing diagonally across the frame, inverting what it crosses
* ONE spot colour: saturated BLOOD RED, used only on lips and a few chosen objects
* some passages flipped into NEGATIVE: white silhouettes with black ink lines on black
* film grain over everything
The result should feel like someone:
SHOT THE SCENE ON A RAIN-SOAKED NOIR SET
→ CRUSHED EVERY GREY TO BLACK OR WHITE
→ INKED THE EDGES BY HAND LIKE FRANK MILLER
→ PAINTED IN ONE COLOUR OF BLOOD RED
→ FLIPPED SOME SHOTS INTO NEGATIVE
→ ANIMATED IT FRAME-BY-FRAME.
CHARACTER — CUT FROM INK, STILL THEMSELVES
Preserve the person's exact:
* identity
* face
* expression
* hairstyle
* glasses
* clothing and clothing patterns
* accessories
* pose
* body proportions
* movement
* hand position
* interaction with objects
Keep the faces REAL and recognizable. Hard light may hide half of a face in black, but the visible half must be clearly that person.
Do NOT turn them into generic noir detectives or femme fatales.
Do NOT give them trench coats, fedoras, cigarettes or guns.
BLACK AND WHITE
* Threshold the whole image hard: each area is either ink black or paper white.
* Faces: lit side white with black ink for eyes, brows, nostrils, mouth line and jaw shadow.
* Clothes: mostly black, with white where the light hits folds, collars and patterns.
* Background: mostly solid black; keep only the brightest light sources white.
* Outline each person with a thin white rim so they separate from the black.
* No soft grey gradients.
RAIN
* Long, thin, straight white streaks at a steep diagonal (about 70°) over the whole frame.
* Where a streak crosses white it turns black, and where it crosses black it turns white (inverted).
* Over the people the rain is fainter, so faces stay readable.
* Tiny white splash specks scattered at random.
* The rain is fresh on EVERY frame: new streak positions each frame.
SPOT RED
* Lips: saturated blood red, only on the person whose face is central and best lit.
* Objects: red only on things that are already red or reddish in the source (red leaves, a red cup, a red light).
* Nothing else gets colour: no skin colour, no blue, no yellow.
* The red is flat and saturated, like printed spot ink.
NEGATIVE PASSAGES
* For one or two sections of the clip (each about 1–2 seconds), invert the scheme:
  the people become white silhouettes, their features and folds drawn in black ink lines, on a solid black ground.
* The spot red stays red in these passages.
* Cut in and out of negative mode on a hard cut, never a fade.
PALETTE
* Ink black, paper white, one blood red.
Do NOT use grey tones as a main value.
Do NOT use sepia, blue or teal tints.
OBJECT CONTINUITY
If the character interacts with an object (phone, chair, bag), ink it in the same black and white as the hand holding it. It moves exactly with the original action.
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
The people's motion must match the source footage exactly on EVERY frame.
The black shapes and white rim follow the body.
The red on the lips sits exactly on the lips in every frame.
NO black shapes left behind from the previous frame.
FRAME-BY-FRAME BOIL
THIS IS CRITICAL.
Every frame is drawn individually, so:
* the ink edges and the threshold line shift slightly on every frame
* the rain is completely new on every frame
* the grain is new on every frame
* the white rim varies a little in width
Avoid perfectly stable digital edges.
DO NOT
Do NOT make it a normal black-and-white grade with soft greys.
Do NOT colour skin, hair or clothes.
Do NOT add red to more than the lips and a few red objects.
Do NOT add costume props (fedoras, trench coats, guns, cigarettes).
Do NOT add speech balloons, captions or panel borders.
Do NOT add a blue or sepia tint.
Do NOT create new poses.
Do NOT change anatomy.
Do NOT change clothing.
Do NOT freeze the rain between frames.
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
* NO black-and-white conversion
* NO rain
* NO red
* NO negative passages
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
Do NOT begin the Sin City transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – SIN CITY STYLING (AFTER MY CONFIRMATION ONLY)
First, tell me:
(a) which person gets the red lips,
(b) which objects in the scene will be spot red,
(c) which frame ranges will be the negative passages.
Then style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation, so the pose is exactly that frame.
Keep the red-lips person, the red objects and the negative ranges fixed for the whole clip.
Apply every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing or the style rules broke (grey creeping in, red in the wrong place) — regenerate those frames only.
The final video must feel like A FRANK MILLER PANEL COME TO LIFE IN THE RAIN: ink black and paper white, white rim light, slashing inverted rain, one blood-red accent, and hard cuts into negative, 12 frames per second.
The image should deliberately contain:
* hard black/white thresholding
* hand-inked edges
* white rim light
* inverted diagonal rain
* one spot red
* film grain.
Avoid polished digital perfection.
```
