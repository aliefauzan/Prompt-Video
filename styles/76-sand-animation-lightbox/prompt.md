# 76 — Sand Animation Lightbox

**Look:** the clip performed live as a sand drawing on a glowing light table and filmed from above. There is only one material: dark sand on warm amber light. Thick sand blocks the light and reads as deep brown-black. Bare glass glows cream-amber, hottest in the middle and turning orange toward the edges. Thin, feathered sand turns granular, and loose single grains lie scattered on the glass. Faces are left mostly as bare glass, with eyes, brows, mouth and outlines trickled in thin sand lines. Contours in heavy sand are scraped out with a fingertip as bright lines. The room is drawn sparser and softer, with cleared glass around the figures. The sand around the people is re-poured every frame while the room's sand stays put.

**Also called / where it trends:** "sand animation", "sand art", "sand painting on light box", "sand drawing performance", 沙画 (China), песочная анимация (Russia / Ukraine). The best-known example is Kseniya Simonova's sand animation on Ukraine's Got Talent (2009). Today it shows up as AI video aesthetics: Morphic "Sand animation" ("sand figure forming on a glowing lightbox, warm backlight"), and sand-art performance clips on YouTube / TikTok / Douyin.

**References:**
- https://morphic.com/resources/videos/sand-animation-videos — Morphic sand animation AI videos: "Sand figure forming on a glowing lightbox, warm backlight", "warm amber glow, fine grain", lightbox transformation and hand-drawn landscape. Screenshots in `refs/ref_1.png` (figures) and `refs/ref_2.png` (scenes).
- https://www.youtube.com/watch?v=518XP8prwZo — Kseniya Simonova, Sand Animation (Ukraine's Got Talent): the classic live sand-drawing performance
- https://www.youtube.com/watch?v=XP1zA2yR7WY — sand animation on a light box (live performance)
- https://www.youtube.com/watch?v=u2JPEU3aM2w — sand art on a light table, top-down
- https://www.youtube.com/watch?v=0yRRFSJVUiI — "Oyasumi ~ Lullaby of Flame ~": a Japanese sand animation short
- https://www.wimp.com/making-pictures-using-sand-on-a-glass-top-with-light-underneath-it/ — "Making pictures using sand on a glass top with light underneath it"
- https://www.redcoolmedia.net/download/videos/animation/video-bindi — "Bindi", a sand animation film

**How it differs from taken styles:** 48 Charcoal Expressionism and 18/19 pencil and watercolour are pigment on paper, seen by reflected light. Sand animation is backlit: translucent granular amber light with no pigment, no paper, no strokes and no colour except the warm lamp. 43 Dark Stage Spotlight is a lighting grade on the real footage, while here the whole image is redrawn in sand. 77 Shadow Puppet is also backlit, but it shows flat coloured leather figures in front of a screen, not loose sand.

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049), `example.mp4` (all 179 frames at 12 fps), `preview.webp`. This is a local approximation made with `render.py` (numpy + OpenCV + person masks). The frame is simplified into sand density with a few tone steps; the people get their own tonal stretch, and the room is sparser with a cleared ring around the figures. A grain field makes the thin sand granular. DoG lines become dark sand lines, and Canny edges in the room become scraped lines. The light table has a warm amber falloff and bloom. The sand of the people is re-poured each frame while the room's sand is static. The six sheet frames are in `frames/`.

## Prompt

```text
I'm uploading one video clip. Convert it into a live SAND ANIMATION ON A LIGHTBOX frame-by-frame animation matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Transform the footage into a sand drawing on a glowing light table, filmed from directly above:
* ONE material only: fine dark sand on a sheet of backlit glass
* the light table glows WARM AMBER: cream-gold in the middle, deeper orange toward the edges
* thick sand blocks the light and reads as deep brown-black
* thin sand is translucent warm brown, and you can see the individual GRAINS where it thins out
* bare glass is the brightest part of the image and glows softly (light bleeding around it)
* soft, feathered gradients where the sand was pushed thinner with a palm or fingertip
* FINGERTIP LINES: bright lines scraped through thick sand (contours, hair strands, folds)
* TRICKLED LINES: thin dark lines of sand drawn across bare glass (eyes, brows, mouth, outlines)
* loose single grains scattered on the bare glass
* no colour other than the warm lamp light and the sand
* a soft vignette where the light table falls off at the frame edge
The result should feel like someone:
FILMED THE CLIP
→ SWITCHED ON A WARM LIGHT TABLE
→ POURED A LAYER OF FINE SAND
→ SWEPT AWAY THE BRIGHT AREAS WITH A PALM
→ DREW THE FACES WITH A FINGERTIP
→ RE-POURED THE FIGURES FOR EVERY FRAME
→ FILMED IT FROM ABOVE AS A LIVE SAND PERFORMANCE.
CHARACTER — SAND-DRAWN PEOPLE
The MAIN HUMAN SUBJECT(S) are drawn in sand, NOT replaced by generic sand figures.
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
Do NOT turn them into faceless silhouettes.
Do NOT change body proportions.
FACES: mostly bare glowing glass with a light veil of sand for the shadow side. Eyes, brows, nostrils, mouth line and glasses rims are thin dark lines of trickled sand. The face must stay recognisable.
HAIR: thick dark sand, with a few bright fingertip strands scraped through it.
CLOTHING: thick, medium or thin sand following the real tone of each garment (dark clothes = thick sand, light clothes = thin veil or bare glass). Stripes and prints become scraped lines or trickled lines. Collars and seams are fingertip lines.
TONE RULES
* only a few tone steps: bare glass, thin veil, medium sand, thick sand
* tone comes from the AMOUNT of sand, never from colour
* the brightest values are bare glass near the centre of the light table
* the darkest values are the thickest sand piles (deep brown-black, never pure digital black)
* every mid-tone is visibly GRANULAR, never a smooth digital grey
BACKGROUND RULES
ORIGINAL ENVIRONMENT:
the real room drawn much sparser than the people: a few soft sand areas and scraped outline lines for the window, wall edges, plants, screen and chair.
Leave a ring of bare, glowing glass around the people so they stand out.
EMPTY LIGHTBOX (for selected sections, optional):
only the people, drawn in sand on the bare glowing glass.
The people stay exactly where they are in the original frame.
LAYER ORDER
A typical frame reads:
GLOWING AMBER LIGHT TABLE
↓
SPARSE SAND DRAWING OF THE ROOM
↓
CLEARED GLASS AROUND THE FIGURES
↓
SAND-DRAWN PEOPLE (thick / medium / thin sand)
↓
FINGERTIP SCRAPED LINES + TRICKLED SAND LINES
↓
LOOSE GRAINS, LIGHT BLEED, VIGNETTE.
OBJECT CONTINUITY
IMPORTANT:
If the character is interacting with an object, preserve that object, drawn in sand.
Examples:
* phone
* cup
* chair
* bag
* microphone
* headphones
If the object is essential to the person's action, draw it with the same detail as the person.
Do NOT accidentally merge it into the background or drop it.
CHARACTER CONTINUITY LOCK
The SAME person must remain recognizable in every frame.
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
The underlying character movement must remain exactly faithful to the source footage.
The SAND changes.
The HUMAN MOTION does NOT change.
If the head moves:
the sand-drawn head moves exactly with it.
If the hand moves:
the sand-drawn hand moves in that same frame.
If the body turns:
the sand is redrawn to the new pose in that same frame.
If the character interacts with an object:
the sand-drawn object moves exactly with the original action.
NO lagging sand.
NO ghost figures from previous frames.
NO smeared morphing between frames (this is not a morph transition).
SAND CONSISTENCY
THIS IS CRITICAL.
Like a live sand artist redrawing only what moves:
* the light table colour, brightness, falloff and grain size are LOCKED for the whole clip
* the sand drawing of the room does NOT change from frame to frame
* the sand of the people is redrawn every frame: the grains along their edges and in the thin areas shift slightly ("boil")
* the faces keep the same line style and the same amount of sand in every frame
Allow, every frame:
* the grain pattern on the people to change slightly
* a very slight flicker of the lamp (1–2 %)
Do NOT let the room's sand crawl or shimmer.
Do NOT turn the whole image into TV static.
DO NOT
Do NOT add colour (no blue, green, red): only warm lamp light and sand.
Do NOT render pencil, charcoal, ink or paint strokes.
Do NOT render paper texture.
Do NOT show the artist's hands in the frame.
Do NOT turn the people into solid black silhouettes.
Do NOT use smooth digital gradients without grain.
Do NOT create new poses.
Do NOT change anatomy.
Do NOT change clothing.
Do NOT add text, watermarks or UI.
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
* NO sand
* NO lightbox glow
* NO grain
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
Do NOT begin the sand transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – SAND ANIMATION STYLING (AFTER MY CONFIRMATION ONLY)
Style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation.
Apply every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT restyle a whole shot from one keyframe.
Before generating, lock and report the look settings: light table colours (centre and edge), sand colour, grain size, the four tone steps, and how sparse the room is drawn.
Use the previous styled frame as a consistency reference for the next one, so the room's sand and the light table stay identical and only the people's sand is redrawn.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, the light table or the room's sand broke. Regenerate those frames only.
The final video must feel like a LIVE SAND PERFORMANCE: warm glowing glass, real sand grains, fingertip lines, only the figures being redrawn.
The image should deliberately contain:
* a warm amber glowing light table
* thick, medium and thin sand with visible grains
* bright fingertip lines scraped through the sand
* thin trickled sand lines for the faces
* loose grains on the bare glass
* a cleared glow around the figures
* a soft vignette.
Avoid clutter: no extra sand drawings, symbols, suns or birds that were not in the source.
```
