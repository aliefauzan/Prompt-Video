# 60 — Floral Maximalism Gouache

**Look:** every frame becomes a flat, whimsical editorial gouache illustration: the people and the room are simplified into flat pastel colour shapes with no harsh shadows (matte gouache with soft mottling and dry-brush edges), and folk-art flowers and leaves grow around and through the frame — vines climbing in from the edges, daisies, tulips, round blooms, sprigs and dot clusters packed densest at the borders, behind the people, with a few big blooms and leaves overlapping the bottom of the frame in front of them. The flowers grow in over the first seconds, then sway gently and boil on twos like hand-painted animation. Storybook / picture-book feel, matte paper grain.

**Also called / where it trends:** "floral maximalism", "folk art floral illustration", "gouache editorial illustration", "flat vector storybook style", "botanical maximalist portrait", "flower frame edit" — AI style presets (frameloop), Pinterest floral-maximalism and folk-art portrait boards, Creative Market botanical graphics packs, editorial illustrators' floral portraits (2026).

**References:**
- https://frameloop.ai/visual-styles — Frameloop "Floral Maximalism" visual style card, screenshot `refs/ref_1.png`. Frameloop's own style prompt: *"flat vector illustration, whimsical editorial art, modern gouache texture, vibrant pastel color palette, floral maximalism, intricate folk art details, storybook aesthetic, matte finish, 2D flat design, no harsh shadows"* (this prompt credits and expands it into the full video workflow below; the card's "try it" link goes to a sign-in page)
- https://www.pinterest.com/search/pins/?q=floral%20maximalism%20gouache%20folk%20art%20illustration%20portrait — Pinterest search, screenshot `refs/ref_2.png`: flat gouache portraits wrapped in folk-art flowers, pastel palettes, matte texture
- https://creativemarket.com/likorbut/292275413-Flower-Market-Botanical-Graphics — "Flower Market" botanical graphics (flat folk-art flowers, leaves, vines)
- https://visie.io/media/christina-zimpel-floral-botanical-illustration-paris-144373 — Christina Zimpel floral botanical illustration (flowers growing around and through figures)

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049), `example.mp4` (all 179 frames at 12 fps), `preview.webp`. Local approximation rendered with `render.py` (numpy + OpenCV + Pillow + person masks + Apple Vision face landmarks from `faces.swift` → `faces.json`: mean-shift flat shapes mapped to a 22-colour pastel gouache palette, gouache mottling and dry-brush, a fixed seeded layout of vines and folk-art motifs that grow in and sway, blush); the six sheet frames are in `frames/`.

## Prompt

```text
I'm uploading one video clip. Convert it into a FLORAL MAXIMALISM GOUACHE storybook frame-by-frame animation matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
STYLE SOURCE
This look starts from the Frameloop "Floral Maximalism" visual style (frameloop.ai/visual-styles), whose style prompt is:
"flat vector illustration, whimsical editorial art, modern gouache texture, vibrant pastel color palette, floral maximalism, intricate folk art details, storybook aesthetic, matte finish, 2D flat design, no harsh shadows".
Everything below expands that prompt into a full frame-by-frame video workflow.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Transform the footage into a hand-painted editorial picture-book page made from:
* FLAT 2D shapes: every area one flat colour, edges clean but hand-cut
* MODERN GOUACHE texture: opaque matte paint, soft mottling inside shapes, slightly dry-brushed edges
* a VIBRANT PASTEL palette (see below)
* NO harsh shadows: shading only as one slightly darker flat shape where really needed
* FLORAL MAXIMALISM: folk-art flowers, leaves and vines growing AROUND and THROUGH the frame
* INTRICATE FOLK-ART DETAILS: petals with dots, centres with rings, leaves with a midrib, little dot clusters and sprigs
* flowers densest at the frame edges, thinning toward the middle
* flowers and leaves BEHIND the people, and a few big ones IN FRONT of the lower frame
* soft pink cheeks, simple painted features
* storybook / whimsical editorial mood
* matte paper finish with fine grain
The result should feel like someone:
FILMED THE CLIP
→ TRACED EVERY FRAME INTO FLAT SHAPES
→ PAINTED THEM IN PASTEL GOUACHE
→ LET A FOLK-ART GARDEN GROW AROUND THE PEOPLE
→ PRINTED IT ON MATTE PAPER
→ ANIMATED IT FRAME-BY-FRAME.
CHARACTER — PAINTED PEOPLE
The MAIN HUMAN SUBJECT(S) are painted as flat gouache figures of THEMSELVES.
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
Do NOT change the people into generic storybook characters.
Do NOT cover faces with flowers.
Do NOT enlarge eyes or heads (this is flat editorial illustration, not chibi).
PAINTED FACE RULES
* skin is a flat warm pastel that matches the person's skin tone
* features are simple: eyes, brows, nose, mouth as painted shapes, faithful to the real expression
* soft pink blush circles on the cheeks
* hair is one or two flat colour masses with a few painted strands
* glasses keep their shape as a thin painted line
PALETTE RULES
Vibrant pastels, matte:
* blush pink, coral, peach, apricot
* butter yellow, mustard
* mint, sage, leaf green, deep teal-green for leaves
* powder blue, periwinkle, lilac
* cream and warm off-white for the paper and highlights
* a deep plum / indigo for the darkest shapes (never pure black)
Each piece of clothing keeps its own colour, mapped to the nearest pastel.
Stripes and prints stay, painted flat.
No grey, no muddy brown, no photographic gradients.
FLOWERS & LEAVES — THE SIGNATURE
* folk-art motifs: round blooms with ringed centres, daisies, tulips, five-petal flowers, leafy sprigs, berry and dot clusters, curling vines
* VINES climb in from the frame edges and curl around the people
* motifs packed DENSE at the borders (maximalism), sparse in the middle so faces stay clear
* most motifs sit BEHIND the people (the people are cut cleanly in front of them)
* a few big blooms and leaves sit IN FRONT of the bottom of the frame
* motifs never cover a face or a hand
* all motifs flat, painted, with small folk-art details (dots, stripes, ringed centres)
BACKGROUND OPTIONS
PAINTED ORIGINAL ROOM:
the real room simplified into flat pastel gouache shapes (windows, walls, desks, plants), with the flower garden growing over it.
PURE FLORAL FIELD (for selected sections, optional):
the room replaced by a cream or pastel ground fully covered with folk-art flowers.
The people stay exactly where they are in the original frame.
LAYER ORDER
A typical frame reads:
FLAT GOUACHE ROOM (or pastel ground)
↓
BACKGROUND VINES + FLOWERS (dense at the edges)
↓
FLAT GOUACHE PEOPLE (faces clear, blush)
↓
FOREGROUND BLOOMS + LEAVES (bottom of frame only)
↓
GOUACHE MOTTLING + DRY-BRUSH EDGES
↓
MATTE PAPER GRAIN.
OBJECT CONTINUITY
IMPORTANT:
If the character is interacting with an object, preserve that object, painted flat.
Examples:
* phone
* cup
* chair
* bag
* microphone
* headphones
If the object is essential to the person's action, keep it in front of the background flowers together with the person.
Do NOT accidentally replace it with a flower or hide it behind leaves.
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
The PAINTING changes.
The HUMAN MOTION does NOT change.
If the head moves:
the painted head moves exactly with it, and the background flowers stay behind it.
If the hand moves:
the hand stays in front of the background flowers in that same frame.
If the body turns:
the flat shapes follow the new pose in that same frame.
If the character interacts with an object:
the object moves exactly with the original action.
NO lagging shapes.
NO ghost silhouettes from previous frames.
NO flowers popping on and off at random.
FLOWER ANIMATION & CONSISTENCY
THIS IS CRITICAL.
The flower layout is LOCKED for the whole clip:
* every vine, flower and leaf has ONE fixed position, colour and design
* motifs do NOT jump, swap or change colour between frames
Animation of the garden:
* over the first ~3 seconds the flowers GROW IN: vines extend from the edges, buds open into blooms (staggered, ease-out)
* after that they SWAY gently, a few pixels, like a breeze
* petals and paint edges BOIL slightly ON TWOS (redrawn every 2 frames), like hand-painted animation
Allow, every frame:
* paper grain to change
* gouache mottling to boil slightly on twos
DO NOT
Do NOT render 3D, glossy or photographic shading.
Do NOT use harsh shadows or dark gradients.
Do NOT cover faces or hands with flowers.
Do NOT use grey or muddy brown as main colours.
Do NOT use neon or fluorescent colours.
Do NOT make it watercolour (no wet blooms, no transparent washes) — gouache is opaque and flat.
Do NOT outline everything in black ink.
Do NOT create new poses.
Do NOT change anatomy.
Do NOT change clothing.
Do NOT add text, logos, watermarks or UI.
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
* NO flat shapes
* NO gouache texture
* NO flowers or vines
* NO pastel palette
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
Do NOT begin the floral gouache transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – FLORAL GOUACHE STYLING (AFTER MY CONFIRMATION ONLY)
Style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation.
Apply every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT restyle a whole shot from one keyframe.
Before generating, paint and show me ONE flower-layout plate (the full frame of vines, flowers and leaves, background and foreground, with the growth order) and ONE palette swatch, and lock both.
Use the layout plate, the palette and the previous styled frame as consistency references for every frame; if Seedream cannot hold the flowers perfectly still, generate the painted people/room per frame and composite the locked flower layer (growth + sway) behind and in front of them.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, palette or the flower layout broke — regenerate those frames only.
The final video must feel like a PICTURE BOOK THAT CAME ALIVE: flat pastel gouache people inside a growing folk-art garden.
The image should deliberately contain:
* flat matte gouache shapes
* vibrant pastel colours
* intricate folk-art flowers, leaves and vines, densest at the edges
* clear, unobstructed faces with soft blush
* no harsh shadows
* fine matte paper grain.
Avoid clutter in the centre: the maximalism lives at the borders.
```
