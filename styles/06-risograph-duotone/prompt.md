# 06 — Risograph Duotone Print

**Look:** every frame is printed on a two-drum risograph in FLUORESCENT PINK + BLUE on off-white uncoated paper: coarse grainy halftone screens, flat solid ink areas, mottled soy-ink coverage, starved and blotchy patches, the pink plate misregistered a few pixels off the blue, a purple third colour where the inks overprint, and a bare paper margin. Sections swap between duotone room, flat pink field and white paper with a pink sun, and the grain and registration boil every frame.

**Also called / where it trends:** "risograph effect", "riso print edit", "riso texture", "2-colour riso", "duotone print effect", "zine print look". Seen in After Effects / CapCut tutorials on TikTok and YouTube, in animated riso music videos and on Pinterest riso portrait boards. Riso-style video effect presets are offered by AI effect apps such as effect.app.

**References:**
- https://www.tiktok.com/@chrismoran__/video/7613430695691701535 — "Risograph in After Effects" tutorial (24.8K likes): grainy two-colour screen, misregistration
- https://www.tiktok.com/search/video?q=risograph%20effect%20edit — TikTok search, screenshot `refs/ref_2.png`: riso edits and tutorials
- https://www.pinterest.com/search/pins/?q=risograph%20portrait%20pink%20blue — Pinterest search, screenshot `refs/ref_1.png`: pink + blue riso portraits, halftone, offset plates
- https://vocab.design/risograph — how riso works: one drum per ink, misregistration halos, soy-ink mottling, overprint makes a third colour
- https://www.designstylebook.com/graphic-design/risograph — risograph as a graphic-design style: limited spot inks, grain, imperfection
- https://studio-ity.com/riso/ — Riso ink colour list (Fluorescent Pink, Blue, etc.)
- https://design.tutsplus.com/tutorials/how-to-make-a-risograph-texture-effect--cms-38557 — Photoshop riso texture: split channels, grain, offset
- https://effect.app/effects/risograph — risograph video effect preset
- https://www.jenschier.com/work/music/after-later-risograph-animated-music-video — fully riso-printed animated music video (the frame-by-frame print look)
- https://www.youtube.com/watch?v=imjAeIZVmVI — Jamie Windsor on the photocopy / riso print look in video
- https://github.com/guitheodoros/risograph — open-source riso simulation (plate separation + grain)

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049). Local approximation rendered with `render.py` (numpy + OpenCV + person masks).

## Prompt

```text
FULL PROMPT FOR RISOGRAPH DUOTONE EDIT:

I'm uploading one video clip. Convert it into a handmade TWO-COLOUR RISOGRAPH PRINT frame-by-frame animation: FLUORESCENT PINK + BLUE ink on off-white paper.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.

TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.

CORE VISUAL STYLE
Transform the footage into a stencil-duplicator (Riso) print built from:
* exactly TWO spot inks: FLUORESCENT PINK and BLUE
* off-white uncoated paper
* coarse grainy halftone screens
* flat solid ink areas
* mottled, uneven soy-ink coverage
* starved, pale ink patches
* tiny white paper-fibre dropouts
* visible misregistration between the two plates
* a PURPLE / deep violet third colour where pink overprints blue
* bare paper halos where the plates miss each other
* a bare paper margin around the print
* zine / art-print aesthetics
The result should feel like someone:
PRINTED THE VIDEO FRAME
→ SEPARATED IT INTO A PINK PLATE AND A BLUE PLATE
→ BURNED EACH PLATE ONTO A RISO MASTER
→ RAN THE PAPER THROUGH THE BLUE DRUM
→ RAN IT AGAIN THROUGH THE PINK DRUM, SLIGHTLY OFF
→ LET THE SOY INK DRY UNEVENLY
→ SCANNED THE PRINT BACK IN
→ ANIMATED IT FRAME-BY-FRAME.

TWO-PLATE SEPARATION
Split every frame into two ink plates.
BLUE PLATE = the key plate:
* shadows
* hair
* dark clothing
* outlines of features
* the deepest tones of the room
PINK PLATE = mid-tones and warmth:
* skin
* lips and cheeks
* mid-tone clothing
* warm objects
* large flat pink graphic shapes.
Where both plates print, the inks overprint and make PURPLE / deep violet.
Where neither plate prints, the PAPER shows through as the highlight.
There is NO white ink, NO black ink and NO other colour.

INK COLOURS
Use the real Riso spot colours:
* FLUORESCENT PINK, approximately #FF48B0 — bright, slightly glowing on paper
* BLUE, approximately #0078BF — clean medium blue
* PAPER, warm off-white, approximately #F6F2E6
* OVERPRINT, the natural multiply of pink over blue (deep violet)
Do NOT add yellow, green, black, orange or any other ink.
The restricted two-ink palette is essential.

HALFTONE / GRAIN SCREEN
Tones are made from a coarse screen of ONE ink, not from smooth gradients.
Use:
* visible round-dot halftone in mid-tones
* the pink and blue screens at different angles (e.g. 15° and 75°)
* grainy, noisy dot edges (riso screens are never clean)
* stochastic grain mixed into the screen
* solid flat ink in the heaviest areas
* clean paper in the lightest areas
It should NOT look like a smooth digital duotone gradient map.
It must look physically printed.

INK TEXTURE
Riso soy ink sits unevenly on uncoated paper.
Include:
* mottled ink density inside solid areas
* blotchy, starved patches where the drum ran low
* tiny white fibre specks and clustered dropouts
* slight ink spread and soft dot gain
* faint drum-roller banding
* occasional tiny ink smudges on the paper
Every solid area should breathe slightly.

MISREGISTRATION
The pink plate must sit OFF the blue plate.
* offset of roughly 4–12 px at 1080p
* the offset direction can change between sections
* a sliver of bare paper or pure pink along one side of every edge
* a sliver of pure blue along the opposite side
* the two plates may also be very slightly rotated against each other
This offset is the signature of the style.
Do NOT align the plates perfectly.
Do NOT make the offset so large that faces become unreadable.

CHARACTER — PRINTED IN BOTH INKS
The people remain PHOTOGRAPHIC, just printed in two inks.
Preserve each person's exact:
* identity
* face
* expression
* hairstyle
* clothing and its patterns
* accessories (e.g. glasses)
* pose
* body proportions
* movement
* hand position
* interaction with objects
Do NOT redraw the people.
Do NOT turn them into a cartoon or vector illustration.
Faces must stay readable: eyes, brows, nostrils and mouth come mostly from the BLUE plate, skin tone from the PINK plate.

BACKGROUND OPTIONS
Switch between these background treatments in sections of a few seconds:
1. DUOTONE ROOM — the original environment printed in both inks, lighter and screened.
2. FLAT PINK FIELD — the whole background is one flat fluorescent pink plate. The people are knocked out of it with a thin bare-paper trap line around them, then printed in both inks.
3. WHITE PAPER + GRAPHICS — the background drops to bare paper, with a big flat PINK SUN / circle behind the group, a flat pink floor band and a pink offset "shadow" silhouette of the people, shifted down-right.
Keep the original composition in all three.
Graphic shapes are flat ink, never gradients.

PAPER
* off-white uncoated stock with slight warmth
* fine paper grain
* a bare paper MARGIN of a few percent around the whole print (no full bleed)
* the ink edge at the margin slightly uneven
* faint scanner dust

OBJECT CONTINUITY
IMPORTANT:
If a person is interacting with an object, keep that object.
Examples:
* phone
* chair
* bag
* glasses
* clothing accessory
Print it in the same two inks.
Do NOT accidentally remove it.

DO NOT
Do NOT make it polished or glossy.
Do NOT use a smooth digital duotone / gradient map.
Do NOT add a third ink or full-colour photography.
Do NOT use black ink.
Do NOT align the plates perfectly.
Do NOT smooth away the grain or the mottling.
Do NOT use a comic-book / Ben-Day pop-art look.
Do NOT add neon glow, chrome or light leaks.
Do NOT create new poses.
Do NOT change anatomy.
Do NOT change clothing.
Do NOT replace anyone's face.
Do NOT turn the people into drawings.
It must feel PRINTED, INKED and PHYSICAL.

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
* NO plate separation
* NO halftone
* NO pink or blue ink
* NO misregistration
* NO paper texture
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
Do NOT begin the risograph transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.

STAGE 3 – RISOGRAPH STYLING (AFTER MY CONFIRMATION ONLY)
Style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation.
Apply every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT restyle a whole shot from one keyframe.
Plan the sections first and list them to me (frame range, background option, pink offset direction, graphic shapes) before generating.
Within a section keep the same background option, the same graphic shapes in the same place and the same rough offset direction.

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

PERFECT MOTION TRACKING
The STYLE jitters.
The HUMAN MOTION does NOT.
The underlying movement must remain exactly faithful to the source footage.
If a head moves, the print follows.
If a hand moves, the print follows.
The pink shadow silhouette and the knock-out trap line follow the people in the same frame.
NO delayed plate.
NO previous-frame silhouette.

FRAME-BY-FRAME BOILING EFFECT
THIS IS CRITICAL.
Every frame should feel separately printed on its own sheet.
Allow between consecutive frames:
* the halftone grain to change
* the screen phase to shift
* the ink mottling and starved patches to move
* fibre dropouts to appear and disappear
* the pink plate offset to wobble by 1–2 px around its section offset
* the paper margin edge to wobble
* graphic shapes to shift by 1–2 px
Do NOT make the wobble so large that the image swims.
The result must feel like a STACK OF RISO PRINTS flipped by hand.

The image should deliberately contain:
* coarse grainy screens
* flat fluorescent pink
* clean riso blue
* violet overprint
* plate misregistration
* mottled soy ink
* bare paper halos and margin
* paper grain and dust.
Avoid polished digital perfection.
```
