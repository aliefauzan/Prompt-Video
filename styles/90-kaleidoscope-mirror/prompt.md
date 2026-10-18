# 90 — Kaleidoscope Mirror

**Look:** The room behind the people is folded into a turning kaleidoscope: the footage itself (wall, window, batik, stripes, faces) is cut into one wedge and mirrored around a centre into an 8-fold mandala of 16 mirror-image petals, with thin bright glass seams between them. The mandala slowly rotates and its petals keep changing as the "tube" turns, while the three real people stand in front of it, sharp and untouched.

**Also called / where it trends:** "kaleidoscope effect", "kaleidoscope mirror", "mirror mandala", "mandala edit", "trippy mirror effect", 旋转 镜像 万花筒 (rotating mirror kaleidoscope) on Bilibili/Douyin. A one-tap effect in CapCut, TikTok and Instagram edits and a classic After Effects / Premiere "Kaleidoscope" (CC Kaleida) look; Pinterest boards of kaleidoscope portraits; Morphic lists it as a psychedelic aesthetic; Vimeo music videos use it as a full-frame treatment.

**References:**
- https://www.pinterest.com/search/pins/?q=kaleidoscope%20mirror%20effect (screenshot `refs/ref_1.png`, from the D2 discovery sweep): radial mirror tunnels and portrait mandalas; faces repeated round a centre.
- https://www.pinterest.com/search/pins/?q=kaleidoscope%20effect%20portrait%20mandala (screenshot `refs/ref_3.png`): portrait kaleidoscopes; one pin shows a person standing untouched in front of a mirrored mandala made from the photo, which is the layout used here.
- https://morphic.com/resources/videos/kaleidoscope-effect-videos (screenshot `refs/ref_2.png`, from the D3 sweep): "Kaleidoscope effect" as a named psychedelic AI-video aesthetic, whole frame folded into rotating radial petals.
- https://www.tiktok.com/@jonsimo/video/7190839394457095429 and https://www.tiktok.com/@kfconcept/video/7564643516916256022 (D1 sweep): TikTok kaleidoscope-mirror edits, footage mirrored into 6–8 radial segments.
- https://www.capcut.com/explore/kaleidoscope-effect/7520684433386735634: CapCut "Kaleidoscope Effect" templates (trippy mirrored mandala edits).
- https://helpx.adobe.com/ph_fil/after-effects/how-to/kaleidoscope-effect.html: Adobe's After Effects kaleidoscope how-to (mirror wedge, number of segments, rotate over time).
- https://vimeo.com/850736526: Vimeo Staff Pick music video built on a kaleidoscope treatment.
- https://www.instagram.com/popular/kaleidoscope-effect/ and https://www.behance.net/search/projects?search=kaleidoscope%20animation: Instagram and Behance kaleidoscope animation work.
- Differs from **44 Broken Mirror Shards** (irregular cracked glass pieces with random angles: here the symmetry is strict and radial) and **56 Prismatic Dreamscape** (rainbow colour refraction: here there is no rainbow dispersion, only mirrored tiling of the real footage).

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049), `example.mp4` (the whole clip at 12 fps with the original audio) and `preview.webp`. A local approximation made with `render.py` (numpy + OpenCV + the person masks): a polar mirror remap folds a wedge of the saturated frame into 16 alternating petals around a point above the frame centre; the mandala turns about 1.7° per frame while the source wedge sweeps from the right-hand person through the striped shirt to the batik, so the pattern evolves smoothly. Alternate petals are a little darker and cooler (each mirror bounce loses light), the seams get a thin white glass edge, a bright point marks the centre and a round eyepiece vignette closes the corners. The people are laid back on top from the masks, unchanged, with a soft shadow on the mandala behind them.

## Prompt

```text
I'm uploading one video clip. Convert it into a KALEIDOSCOPE MIRROR frame-by-frame animation: the world behind the people becomes a slowly turning mirror mandala built from the footage itself, while the people stay exactly as filmed, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Kaleidoscope mirror effect, radial mirror symmetry, 8-fold mandala made from the video's own imagery, mirrored wedges, glass mirror seams, rotating kaleidoscope tube, rich jewel colour.
Transform the footage into a frame built from:
* the REAL PEOPLE, untouched, in front
* behind them, a RADIAL MANDALA made only from the clip's own pixels
* ONE WEDGE of the frame mirrored into 16 PETALS (8-fold symmetry)
* every second petal a MIRROR IMAGE of its neighbour
* thin bright GLASS SEAMS where two mirrors meet
* a small bright JEWEL POINT at the centre of the mandala
* alternate petals very slightly darker and cooler (light lost in each mirror bounce)
* concentric rings of repetition: faces, stripes, batik and window light repeating round the centre
* saturated, rich, jewel-like colour
* a soft dark round EYEPIECE vignette in the corners
* the mandala TURNING slowly from frame to frame
The result should feel like someone:
FILMED THE SCENE
→ LOOKED AT IT THROUGH A THREE-MIRROR KALEIDOSCOPE TUBE
→ CUT THE PEOPLE OUT CLEANLY
→ STOOD THEM BACK IN FRONT OF THE TURNING MANDALA
→ TURNED THE TUBE A LITTLE FOR EVERY FRAME
→ PLAYED IT BACK AT 12 FPS.
CHARACTER — UNTOUCHED, IN FRONT
The people are NOT mirrored, NOT split and NOT tiled.
They stand whole, in their exact place, in front of the mandala.
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
Do NOT run a mirror seam through a face or body.
Do NOT duplicate a person in the foreground.
Only a slight saturation lift on the people so they sit with the mandala.
A soft shadow on the mandala right behind the people separates them from it.
THE MANDALA — HOW TO BUILD IT
* Take ONE wedge of the CURRENT frame (wall, window, plant, screen, batik, stripes, faces all allowed inside the wedge).
* Mirror it around a centre point into 16 petals: wedge, mirror image, wedge, mirror image… all the way round (8-fold symmetry, 22.5° per petal).
* Place the centre above the middle of the frame, roughly behind the middle person's head, so rays fan out between and above the people.
* The petals must join seamlessly in content (true mirror symmetry), with a 1–2 px bright glass line on each seam.
* Each frame, rotate the whole mandala a little (about 1.5–2° per frame, always the same direction).
* Slowly sweep which part of the frame the wedge is taken from, so the mandala's content keeps evolving: sometimes faces, sometimes the stripes, sometimes the batik.
* Tame blown highlights (the window) so the mandala stays coloured, not white.
* The mandala fills ALL background areas visible around the people, edge to edge.
COLOUR
* Push saturation up so the mandala looks jewel-like: warm browns and amber from the batik, rose skin tones, greens from the plant and clothes, blue from the screen.
* Contrast a little punchier than the source.
* No rainbow fringes, no colour shift that is not in the footage.
EYEPIECE + SEAMS
* Corners fall off into a soft dark round vignette, as if seen through the tube.
* Seams are thin, bright, slightly glowing glass edges.
* A small bright point marks the exact centre when it is visible.
PALETTE
Only the colours of the clip itself, saturated: amber, brown, rose, olive green, slate blue, cream, white glints.
Do NOT add colours that are not in the footage.
OBJECT CONTINUITY
If the character holds an object, it stays with the person in front of the mandala, unchanged.
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
The people must match the source frame exactly, every frame.
The mandala is rebuilt from the CURRENT frame each time, so when people move the mirrored copies in the mandala move too.
NO frozen mandala reused from a previous frame.
NO cut-out edge jumping around the people.
FRAME-TO-FRAME KALEIDOSCOPE TURN
THIS IS CRITICAL.
It must feel like a kaleidoscope tube being turned steadily, not a random pattern every frame.
Between consecutive frames:
* rotate the mandala by the same small angle (about 1.5–2°)
* move the source wedge only a little
* let the mirrored content change with the footage
Keep FIXED:
* the symmetry count (8-fold, 16 petals)
* the centre point
* seam style and vignette
* the people's look
DO NOT
Do NOT mirror, split or tile the people in the foreground.
Do NOT use irregular broken-glass shards (that is a different style).
Do NOT add rainbow prism refraction.
Do NOT change the number of petals between frames.
Do NOT jump the rotation or reverse it.
Do NOT let the mandala go white from the window.
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
* NO mirroring or kaleidoscope
* NO colour changes
* NO cut-outs
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
Do NOT begin the kaleidoscope transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – KALEIDOSCOPE MIRROR STYLING (AFTER MY CONFIRMATION ONLY)
First, tell me the mandala centre point, the symmetry count (8-fold) and the rotation per frame you will use.
Then style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation, so the people are exactly that frame and the mandala is built from that frame.
Apply every style rule above, advancing the rotation by the same angle each frame.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing, the symmetry count or the rotation direction broke — regenerate those frames only.
The final video must feel like LOOKING AT THE ROOM THROUGH A TURNING KALEIDOSCOPE while the people stand in front of it: real people, mirror mandala, steady turn, 12 frames per second.
The image should deliberately contain:
* untouched people in front
* an 8-fold mirrored mandala made from the clip itself
* thin bright glass seams
* a slow steady rotation
* jewel-rich colour
* a round eyepiece vignette.
Avoid random tiling and broken-glass shards.
```
