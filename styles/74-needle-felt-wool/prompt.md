# 74 — Needle-Felt Wool World

**Look:** the whole clip rebuilt as a handmade needle-felted wool diorama, re-shot frame by frame like a felt stop-motion short. People, clothes and the room become soft, rounded, matte lumps of dyed wool. There are no hard edges anywhere: every silhouette has a fuzzy halo of stray fibres, darker felted seams sit where two colours of wool meet, and small dark wool details are needle-punched in for the eyes, brows, mouth and glasses. Lighting is warm macro tabletop light with a shallow depth of field on the felt set. The fuzz "boils" every frame while the shapes and motion hold.

**Also called / where it trends:** "needle felt style", "felt animation", "felted art", "wool felt stop motion", "felt filter", 羊毛毡风格 / 毛毡定格 (Douyin, Bilibili, Xiaohongshu). It turns up as AI video effects and templates on PixVerse ("Felted Art" restyle), Media.io, Ribbi, picxstudio, VideoCue and Aisma, in the TikTok "knitted video" / felt trend, on Pinterest and Instagram (#needlefelting, 8.7M reels), and in Civitai felt video LoRAs. All four discovery sweeps (D1–D4) found it.

**References:**
- https://www.bilibili.com/video/av114754530056606 — "用AI把经典影视换成羊毛毡风格, 爆了300万播放, 附详细教程+提示词": a viral tutorial for turning classic film clips into needle-felt style. Screenshot of the Bilibili search in `refs/ref_1.png`.
- https://www.bilibili.com/video/av115944470876451 — "Avemujica 羊毛毡风格": anime characters felted (fuzzy fibre hair, bead eyes)
- https://www.bilibili.com/video/av117117382825527 — "AI羊毛毡风格定格动画《不眠的星星》": an AI felt stop-motion short with macro tabletop light
- https://www.pinterest.com/search/pins/?q=needle%20felted%20wool%20animation — Pinterest board of real needle-felt animation (felted faces, fuzzy rims, felt dioramas). Screenshot in `refs/ref_2.png`.
- https://www.instagram.com/popular/needle-felting/ — #needlefelting on Instagram
- https://vimeo.com/640419758 — Andrea Love, a needle-felted stop-motion music video (the real hand-made look)
- https://www.media.io/ai/video-to-video/felt-animation — Media.io "Felt" video-to-video effect. Screenshot in `refs/ref_3.png`.
- https://civitai.com/models/2525862 — Civitai felt / needle-felt video LoRA
- https://ribbi.ai/skills/felt-stop-motion-animation — felt stop-motion generator ("wool-felt character sheet", cozy light)
- https://picxstudio.com/templates/19931-needle-felt-stop-motion-transformation — needle-felt stop-motion transformation template
- https://videocue.io/looks/in-shadow-felted-puppet — felted puppet stop-motion look
- https://vlogme.ai/aisma/ai-video-restyle — Aisma restyle: wool / clay / ink materials
- https://www.tiktok.com/@cozywoolvillage/video/7527089596224539934 and https://www.tiktok.com/@space.bananas.agency/video/7575209140985810231 — the TikTok wool / "knitted video" trend
- https://www.behance.net/search/projects?search=felt%20stop%20motion%20animation — felt stop-motion projects on Behance

**How it differs from taken styles:** 37 Claymation is smooth, shiny plasticine with fingerprints. 34 Cross-Stitch is a flat thread grid. 59 Kawaii Chibi is glossy 3D plastic. Felt is matte and fibrous: random fibre fuzz with no grid, no sheen and no hard edges, and a fuzzy halo on every silhouette.

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049), `example.mp4` (all 179 frames at 12 fps), `preview.webp`. This is a local approximation made with `render.py` (numpy + OpenCV + person masks). Colours are smoothed with an edge-preserving filter and snapped to a fixed dyed-wool palette (k-means, see `palette.npz`). Colour patches are puffed into wool lumps with darker seams. Dark wool details are needle-punched in from a DoG of the face. A procedural fibre field adds mottling and a fibre displacement, plus curly stray strands on the silhouettes. The set gets macro depth of field and warm tabletop light. The fibres change every frame (boil). The six sheet frames are in `frames/`.

## Prompt

```text
I'm uploading one video clip. Convert it into a handmade NEEDLE-FELTED WOOL WORLD frame-by-frame stop-motion animation matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Transform the footage into a miniature handmade felt set built from:
* NEEDLE-FELTED WOOL: dyed wool roving pressed into soft, firm shapes
* matte fibrous surfaces, no shine anywhere
* thousands of tiny visible wool fibres on every surface
* a FUZZY FIBRE HALO on every silhouette: stray fibres stand off the edges, no clean cut edge
* soft, rounded, slightly lumpy forms, as if each part was sculpted with a felting needle
* darker felted SEAMS where two colours of wool meet
* small needle-punched details in dark wool: eyes, brows, lashes, nostrils, mouth line, glasses rims
* flat-ish dyed colours, a little richer and softer than the footage, with lifted matte blacks
* the room rebuilt as a felt diorama: felt walls, felt window, felt plants, felt furniture
* warm macro tabletop lighting from the upper left, soft contact shadows
* shallow depth of field: the felt set softly out of focus behind the figures
* a gentle vignette and a cosy, handmade feel
The result should feel like someone:
FILMED THE CLIP
→ DYED WOOL ROVING TO MATCH EVERY COLOUR
→ NEEDLE-FELTED EACH PERSON, GARMENT AND PROP BY HAND
→ FELTED THE WHOLE ROOM AS A TABLETOP SET
→ LIT IT WITH A WARM DESK LAMP
→ SHOT IT WITH A MACRO LENS
→ ANIMATED IT FRAME-BY-FRAME AS STOP-MOTION.
CHARACTER — FELTED PEOPLE
The MAIN HUMAN SUBJECT(S) are rebuilt as needle-felted figures, NOT replaced by generic dolls.
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
Do NOT turn them into chibi dolls or cute plush animals.
Do NOT enlarge heads or eyes.
Do NOT smooth the face into a blank felt ball: eyes, brows, nose shadow, mouth and glasses must be readable, needle-punched in darker wool.
SKIN: felted in a wool tone that matches the person's real skin tone, with a slightly lighter felted highlight on the cheek, nose and forehead.
HAIR: felted from long dark fibres, with visible fibre direction, a fuzzy outline and loose strands.
CLOTHING: each garment felted in its real colour. Stripes and prints are needle-punched in simplified wool shapes in the real colours. Collars and seams show as felted ridges.
PALETTE RULES
* real colours of the footage, simplified to a limited set of dyed wool colours
* each area is ONE wool colour, with a soft fibre mottle inside it
* colours are slightly softer and warmer than the footage, never neon
* blacks are lifted: dark wool is charcoal, never pure digital black
* whites are cream wool, never pure digital white
* no gradients made by light alone: shading comes from the rounded felt forms
SURFACE AND EDGE RULES
* every surface shows fine wool fibres at 1–3 px scale, in slightly lighter and darker strands
* every outline is FUZZY: 3–10 px of stray fibres stand off the edge, some curling outward
* no razor-sharp edges, no clean vector edges, no plastic or clay sheen
* no visible grid, no stitches in rows, no knit loops (this is felt, not knit or cross-stitch)
* forms are soft and slightly lumpy, with darker seams where shapes are joined
BACKGROUND RULES
ORIGINAL ENVIRONMENT:
the real room rebuilt as a felt diorama: felt walls, a felt window with felt clouds of light, felt plants, felt desk and chair, the TV/monitor as a felt panel.
Simplify it more than the people (bigger wool shapes, fewer details).
It sits behind a macro depth-of-field blur: fibres still visible but soft.
SIMPLE FELT BACKDROP (for selected sections, optional):
one soft felt wall in a cream or muted colour behind the people, still out of focus.
The people stay exactly where they are in the original frame.
LAYER ORDER
A typical frame reads:
FELT DIORAMA ROOM (softly out of focus)
↓
SOFT CONTACT SHADOW of the figures on the set
↓
NEEDLE-FELTED PEOPLE (in focus)
↓
NEEDLE-PUNCHED DARK DETAILS (eyes, brows, mouth, glasses)
↓
FIBRE TEXTURE + FUZZY FIBRE HALO
↓
WARM TABLETOP LIGHT, VIGNETTE, VERY FINE GRAIN.
OBJECT CONTINUITY
IMPORTANT:
If the character is interacting with an object, preserve that object, felted.
Examples:
* phone
* cup
* chair
* bag
* microphone
* headphones
If the object is essential to the person's action, felt it in the same detail as the person, in focus.
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
The WOOL changes.
The HUMAN MOTION does NOT change.
If the head moves:
the felted head moves exactly with it.
If the hand moves:
the felted hand moves in that same frame.
If the body turns:
the felted body turns in that same frame.
If the character interacts with an object:
the felted object moves exactly with the original action.
NO lagging felt.
NO ghost fibres from previous frames.
NO shapes drifting between frames.
STOP-MOTION FIBRE BOIL
THIS IS CRITICAL.
Like a real felt puppet re-shot on every frame:
* the stray fibres on the silhouettes change slightly EVERY frame (they "boil")
* the fibre texture on the surfaces shifts slightly every frame
* fibre size, fibre density, light direction and depth of field stay LOCKED for the whole clip
* the wool COLOURS stay EXACTLY the same in every frame (one locked wool palette)
* the felt FORMS (face, hair mass, sleeves, collars, stripes) stay the same shape from frame to frame
* the felted room does not change at all, except for the fibre boil
The boil is subtle: it must read as hand-made texture, not as flicker or noise.
DO NOT
Do NOT render plasticine, clay, fingerprints or a glossy sheen (that is claymation).
Do NOT render a thread grid, cross-stitches or knit loops.
Do NOT render smooth 3D plastic or vinyl toys.
Do NOT render sharp vector edges.
Do NOT turn the people into plush animals or chibi dolls.
Do NOT use neon colours or pure black and white.
Do NOT blur the people.
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
* NO felt
* NO wool texture
* NO fibre halo
* NO depth of field
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
Do NOT begin the needle-felt transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – NEEDLE-FELT STYLING (AFTER MY CONFIRMATION ONLY)
Style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation.
Apply every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT restyle a whole shot from one keyframe.
Before generating, lock and report the look settings: the wool colour list for each person and for the room, fibre size, halo length, light direction and depth-of-field strength.
Use the previous styled frame as a consistency reference for the next one, so the wool colours, the felt forms and the felted room stay identical and only the fibres boil.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, the wool palette or the felt forms broke. Regenerate those frames only.
The final video must feel like a FELT STOP-MOTION SHORT: real needle-felted wool, fuzzy fibre halos, warm macro tabletop light, only the fibres boiling.
The image should deliberately contain:
* matte wool with visible fibres everywhere
* fuzzy fibre halos on every silhouette
* soft rounded felt forms with darker seams
* needle-punched dark wool facial details
* a felt diorama room in soft focus
* warm tabletop light and a gentle vignette.
Avoid clutter: no extra felt props, flowers or animals that were not in the source.
```
