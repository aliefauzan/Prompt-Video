# 75 — Papercraft Layered Diorama

**Look:** every frame is rebuilt as a shadow-box diorama of cut, coloured card. Each colour area becomes a separate sheet of matte cardstock with clean knife-cut curves. The sheets are stacked at different heights (the room at the back, the people in front, with hair, eyes and brows as small top pieces). Every sheet casts a soft drop shadow onto the one below, and its cut edge catches a thin line of light. Warm soft studio light, visible paper grain and a slight depth of field on the back layers. It is animated as stop-motion: the cut-out people are nudged a hair each frame, and the paper set never moves.

**Also called / where it trends:** "paper cut style", "papercraft", "paper diorama", "layered paper", "paper cutout stop motion", "AI paper-cut workflow", "paper shadow box". Seen in TikTok AI paper-cut trends (@storyboard.co.th AI Paper-Cut Workflow, "Paper Diorama AI Trend", "Paper Loop" city scenes), on X (insMind and OriSilver paper-cut recipes), in Civitai paper-cut LoRAs, and in AI generator landing pages (Morphic, insMind, Korpi, feega, Framesail).

**References:**
- https://www.tiktok.com/@storyboard.co.th/video/7666704828600454408 — "AI Paper-Cut Workflow" (3.5K likes). Screenshot of the TikTok search "papercraft paper cut diorama ai video" in `refs/ref_1.png`.
- https://www.tiktok.com/@the_ai_horizon/video/7671247986906631446 — "Paper Art Stop-Motion" made with MiniMax
- https://www.tiktok.com/@ai.akshu/video/7660905625349524758 — "I made this paper-style AI video": layered card scenes
- https://morphic.com/resources/videos/paper-cutout-animation-videos — Morphic paper cutout animation: "layered paper-cutout forest with soft drop shadows", paper characters. Screenshot in `refs/ref_2.png`.
- https://civitai.com/models/2528213 — Civitai layered paper-cut video LoRA
- https://x.com/insmind_com/status/2077030549571727778 — insMind paper-cut animation recipe
- https://x.com/OriSilver/article/2078103099986657470 — OriSilver paper-cut stop-motion prompt article
- https://www.insmind.com/ai-video-generator/paper-animation — insMind AI paper animation generator
- https://korpi.ai/best-ai/paper-diorama — AI paper diorama video maker
- https://www.feega.app/paper-cutout-animation — paper cutout animation maker, "AI stop motion style"
- https://github.com/sadekxD/paper-diorama-producer — open-source paper-diorama video pipeline

**How it differs from taken styles:** 08 Scrapbook Sticker Collage and 01 Punk Photocopy Collage are messy stuck-on photo scraps, stickers and ephemera. This style uses one material only: clean, solid-coloured card with no photo texture. Depth comes from physically stacked layers with real drop shadows. 58 LEGO and 37 Claymation are 3D toy materials; this is flat paper in depth.

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049), `example.mp4` (all 179 frames at 12 fps), `preview.webp`. This is a local approximation made with `render.py` (numpy + OpenCV + person masks). Colours are flattened and snapped to a fixed cardstock palette (k-means, see `palette.npz`). A soft majority vote turns each colour into a smooth knife-cut sheet. Small dark card pieces are cut for the facial features, inside head ellipses found from the matte. Sheets are stacked by height. A multi-step offset makes the drop shadows and a lit cut edge. Paper grain and a slight depth of field are added. The people layers jitter 1 px per frame (stop-motion). The six sheet frames are in `frames/`.

## Prompt

```text
I'm uploading one video clip. Convert it into a handmade PAPERCRAFT LAYERED DIORAMA frame-by-frame stop-motion animation matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Transform the footage into a shadow-box diorama built ONLY from cut paper:
* matte coloured CARDSTOCK sheets, one solid colour per sheet
* clean, smooth, knife-cut curves (no torn edges, no jagged pixel edges)
* every sheet stacked at its own height above the one behind it
* a soft DROP SHADOW under every sheet onto the sheets below (light from the upper left, shadows to the lower right)
* a thin bright CUT EDGE on the side of each sheet that faces the light (card thickness)
* visible paper fibre grain on every sheet, slightly different on each card
* simplified shapes: a face is a few cut pieces, a shirt is a few cut panels
* small cut pieces of dark card for eyes, brows, lashes, mouth, nostrils and glasses rims
* the room built as the back layers of the diorama
* soft, warm studio light, a gentle falloff toward the corners
* a slight macro depth of field: the back layers a little soft, the front layers crisp
The result should feel like someone:
FILMED THE CLIP
→ PICKED A STACK OF COLOURED CARD TO MATCH THE SCENE
→ CUT EVERY SHAPE WITH A CRAFT KNIFE
→ LAYERED THE ROOM AS A SHADOW BOX
→ GLUED THE CUT-OUT PEOPLE ON FOAM PADS IN FRONT
→ LIT IT WITH A SOFT LAMP
→ ANIMATED IT FRAME-BY-FRAME AS PAPER STOP-MOTION.
CHARACTER — CUT-PAPER PEOPLE
The MAIN HUMAN SUBJECT(S) are rebuilt as layered cut-paper figures, NOT replaced by generic paper dolls.
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
Do NOT turn them into cartoon mascots or chibi figures.
Do NOT change body proportions.
Do NOT simplify the face into a blank shape: eyes, brows, nose, mouth and glasses must be readable as small cut pieces of darker card.
SKIN: one or two cards matching the person's real skin tone, with a slightly darker card cut for the shadow side of the face and neck.
HAIR: one dark card for the hair mass, layered ON TOP of the face card, with cut strands at the edges.
CLOTHING: each garment cut from card in its real colour. Stripes are cut strips glued on top. Prints and patterns are simplified into a few cut shapes of the real colours. Collars, sleeves and hems are separate cut pieces.
PALETTE RULES
* use the real colours of the footage, simplified to a limited set of cardstock colours
* each sheet is ONE flat matte colour (no gradients printed on the paper)
* all shading comes from the drop shadows between layers and the light falloff
* colours are clean and slightly richer than the footage, like coloured craft card
* no photo texture, no printed images, no halftone, no ink outlines
LAYER / DEPTH RULES
* the back wall is the lowest layer
* windows, screens, plants, furniture are stacked in front of the wall
* the people are the highest layers, clearly lifted above the room (longer, softer shadows behind them)
* inside each person: skin and clothes first, hair and feature pieces on top
* bigger height steps cast longer shadows
* every shadow falls in the SAME direction in every frame
BACKGROUND RULES
ORIGINAL ENVIRONMENT:
the real room rebuilt as a layered paper set: card wall, card window with cut frames, card plants with cut leaves, card desk and chair, the TV/monitor as a dark card panel.
Simplify it more than the people (bigger shapes, fewer pieces).
SIMPLE PAPER BACKDROP (for selected sections, optional):
a few large layered card shapes in the room's colours behind the people.
The people stay exactly where they are in the original frame.
LAYER ORDER
A typical frame reads:
BACK WALL CARD
↓
ROOM LAYERS (window, plants, furniture), each with a drop shadow
↓
CUT-PAPER PEOPLE, lifted, with longer drop shadows
↓
HAIR AND FEATURE PIECES on top, each with a tiny shadow
↓
LIT CUT EDGES + PAPER GRAIN
↓
SOFT WARM LIGHT, SLIGHT DEPTH OF FIELD ON THE BACK LAYERS.
OBJECT CONTINUITY
IMPORTANT:
If the character is interacting with an object, preserve that object, cut from card.
Examples:
* phone
* cup
* chair
* bag
* microphone
* headphones
If the object is essential to the person's action, cut it at the same layer height as the person's hand.
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
The PAPER changes.
The HUMAN MOTION does NOT change.
If the head moves:
the paper head moves exactly with it.
If the hand moves:
the paper hand moves in that same frame.
If the body turns:
the paper pieces are re-cut to the new pose in that same frame.
If the character interacts with an object:
the paper object moves exactly with the original action.
NO lagging pieces.
NO ghost cut-outs from previous frames.
NO pieces drifting between frames.
PAPER CONSISTENCY
THIS IS CRITICAL.
The set is built ONCE and stays put:
* the card colours are LOCKED for the whole clip (one fixed cardstock palette)
* the paper grain of each card, the light direction and the shadow direction stay the same in every frame
* the room layers do not move, re-cut or change colour at all
* the people's pieces keep the same cut style, the same colours and the same layer order from frame to frame
Allow, every frame:
* a tiny 1–2 px nudge of the people's paper pieces (hand-placed stop-motion)
* re-cut shapes only where the person really moved
Do NOT re-randomise the shapes, the colours or the layer order every frame.
Do NOT let the drop shadows flicker or change direction.
DO NOT
Do NOT use photo scraps, magazine cut-outs, stickers, tape or ephemera (that is scrapbook collage).
Do NOT print photo texture onto the paper.
Do NOT use halftone, ink outlines or black contour lines.
Do NOT render 3D plastic, clay or felt.
Do NOT use torn, ragged edges.
Do NOT flatten everything into one layer without shadows.
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
* NO paper
* NO layers
* NO drop shadows
* NO colour simplification
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
Do NOT begin the papercraft transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – PAPERCRAFT STYLING (AFTER MY CONFIRMATION ONLY)
Style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation.
Apply every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT restyle a whole shot from one keyframe.
Before generating, lock and report the build settings: the cardstock colour list for each person and for the room, the layer order, the light / shadow direction and the shadow length per height step.
Use the previous styled frame as a consistency reference for the next one, so the room stays identical and the people keep the same cards and cut style.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, the card palette, the layer order or the shadow direction broke. Regenerate those frames only.
The final video must feel like PAPER STOP-MOTION in a shadow box: real cut card, real layers, real drop shadows, only the people's pieces moving.
The image should deliberately contain:
* clean knife-cut card shapes
* flat matte card colours
* soft drop shadows between every layer
* lit cut edges
* visible paper grain
* small cut feature pieces on the faces
* a slight depth of field on the back layers.
Avoid clutter: no extra paper clouds, trees, animals or props that were not in the source.
```
