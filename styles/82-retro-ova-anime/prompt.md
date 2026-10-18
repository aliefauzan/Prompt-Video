# 82 — Retro 80s-90s OVA Anime

**Look:** The clip becomes a scene from a late-80s / early-90s OVA (original video animation) shot on film. The people are hand-painted cels with flat colours, one hard violet-tinted shadow, a sharp sheen band on the hair and thin dark-brown ink lines. They stand in front of a matte painting, not a photo: an airbrushed room at dusk with a city-pop violet-magenta-amber sky in the window. Highlights halate and bloom, the print is slightly faded, coarse film grain and dust sit on top, and the picture is framed 4:3.

**Also called / where it trends:** "retro anime", "90s anime aesthetic", "80s anime", "OVA / OAV look", "vintage cel anime", "Golden Boy style", "Akira / Bubblegum Crisis / City Hunter look", "city pop anime", "nostalgic OVA aesthetic" (Krea moodboard), "90s anime filter". It trends as Wan 2.x video LoRAs on Civitai (the Retro 90's Anime / Golden Boy LoRA has ~9k downloads), as Midjourney `--sref` codes shared on X (e.g. @Artedeingenio, sref 2726004757), and as "90s anime filter" edits on TikTok and Instagram, often set to city-pop songs.

**References:**
- https://civitai.com/models/1671285 (screenshot `refs/ref_1.png`): "Retro 90's Anime / Golden Boy Style" LoRA for Wan 2.2 / 2.1 video, ~9k downloads. Painted backgrounds, flat cel people, film-print colour.
- https://civitai.com/models/1833906: a second retro-anime video LoRA from the same discovery sweep (D3).
- https://www.krea.ai/moodboard-feed/nostalgic-ova-aesthetic-cfac0412-e8ae-5bcc-a69e-9109c379961d (screenshot `refs/ref_2.png`): Krea "Nostalgic OVA Aesthetic" moodboard. Its tags are "1990s anime style", "hand-painted cel animation", "vintage OVA aesthetic", "painterly gouache backgrounds", "cinematic lighting" and "subtle film grain".
- https://x.com/Artedeingenio: Midjourney video `--sref 2726004757` retro-anime posts (from D3).
- https://videocue.io/looks/akira-bebop-90s-ova-cel: "Akira / Cowboy Bebop 1990s OVA cel" look notes: cel paint warmth, dense painted backgrounds, film texture.
- https://grokcine.com/styles/aesthetics/90s-anime-aesthetic/ and https://z-image.me/en/styles/90s-anime-ova: style-library entries for "90s anime OVA" (cel shading, film grain, muted palette).

How it differs from the styles already in the library: **10 Anime Cel Shade** is clean modern digital cel with pink blush, bright blue sky and speed lines. **52 Retro 90s Cartoon** is a western TV cartoon with thick black wobbly outlines and SD video artefacts. **51 Ghibli Painted Anime** is soft pastoral watercolour in daylight. This one is Japanese OVA on FILM: violet-shadowed cels, airbrushed dusk matte painting, halation, grain and a 4:3 frame.

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049), `example.mp4` (the whole clip at 12 fps with the original audio) and `preview.webp`. This is a local approximation made with `render.py` (numpy + OpenCV + the person masks). The people are labelled against one fixed cel colour model (k-means over the clip), then get one violet-shifted hard shadow, a hard highlight, violet-black hair (found from head boxes in the matte) with a mauve sheen, and thin dark ink lines with a small boil. The room is mean-shift smoothed and blended with a wide blur for an airbrushed look, then graded to dusk. The blown-out window is replaced by a painted gradient sky with streak clouds, mapped to the window's shape each frame. On top: red-orange halation, bloom, a faded print curve, coarse grain, gate weave, dust, vignette and 4:3 pillarbox bars.

## Prompt

```text
I'm uploading one video clip. Convert it into a RETRO 80s-90s OVA ANIME frame-by-frame animation: every frame should look like a frame from a Japanese original video animation of around 1988-1994, painted on cels, shot on film and transferred from a worn print, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Retro 1990s anime, vintage OVA aesthetic, hand-painted cel animation, painterly gouache matte backgrounds, cinematic dusk lighting, subtle film grain, soft halation, faded film print.
Transform the footage into an OVA frame built from:
* HAND-PAINTED CELS for the people: flat, opaque colour fills
* ONE hard-edged SHADOW tone on every surface, tinted VIOLET / mauve (not just darker)
* a hard, small HIGHLIGHT shape on cheeks, noses and fabric folds
* a sharp SHEEN BAND on the hair (lilac or mauve on dark hair)
* THIN dark-brown / deep-violet INK LINES, slightly uneven, hand-traced
* a MATTE PAINTING background: airbrushed gradients, gouache texture, no outlines
* DUSK light: warm amber key light, violet shadows
* a CITY-POP SKY in any window: violet top, magenta middle, amber horizon, long streaky clouds
* soft red-orange HALATION and bloom around bright areas
* a slightly FADED film print: lifted blacks, warm-magenta cast
* coarse 35mm FILM GRAIN, a little dust
* a 4:3 frame (pillarbox bars on a 16:9 or 3:2 source)
The result should feel like someone:
TRACED EVERY FRAME ONTO CELS
→ PAINTED THEM WITH FLAT CEL VINYL, ONE SHADOW, ONE HIGHLIGHT
→ LAID THEM OVER AN AIRBRUSHED MATTE PAINTING OF THE ROOM AT DUSK
→ SHOT THE STACK ON A ROSTRUM CAMERA ONTO 35MM FILM
→ PRINTED IT, LET THE PRINT AGE
→ TRANSFERRED IT AT 4:3 FRAME-BY-FRAME.
CHARACTER — PAINTED CEL
Redraw each person as a hand-painted anime cel, but keep them unmistakably the SAME person.
Preserve the person's exact:
* identity
* face shape and features
* expression
* hairstyle and hair length
* glasses
* clothing and its pattern (stripes stay stripes, batik stays batik, simplified into cel shapes)
* accessories
* pose
* body proportions
* movement
* hand position
* interaction with objects
Use realistic adult OVA proportions (like late-80s character designs), NOT chibi, NOT big-eyed moe faces.
Eyes, brows, nose and mouth stay where they are on the real face, drawn with thin dark lines.
Do NOT beautify, slim, age or de-age anyone.
CEL PAINT
* Skin: warm peach-tan base, ONE violet-rose shadow shape, a small hard highlight.
* Hair: deep violet-black base with ONE sharp lilac / mauve sheen band following the hair's curve.
* Clothes: flat base colour + one violet-shifted shadow shape + an occasional hard highlight.
* Every shadow edge is HARD; no soft gradients on the cels.
* Paint colours are slightly richer than the footage, then faded by the film print.
* Same paint colours for each person on every frame.
INK LINES
* Thin, dark-brown or deep-violet, not pure black, not thick.
* Outline every person and trace main folds, collar, sleeves, hair strands, facial features.
* No outlines on shadow edges, and NO outlines in the background.
BACKGROUND — MATTE PAINTING AT DUSK
* Keep the SAME room layout, furniture, window, plants, screen and perspective.
* Repaint it as an airbrushed gouache matte painting: soft gradients, simplified shapes, gentle paint texture.
* Grade it to dusk: amber light from the window, violet-blue shadows in corners and under furniture.
* The window shows a painted CITY-POP DUSK SKY: violet at the top, magenta, then amber-peach at the horizon, with long horizontal streak clouds lit from below.
* Light from the window spills warm onto nearby walls and onto the people's edges.
* The background is ONE painting under the cels: it stays still except for camera movement from the source.
FILM PRINT
* Red-orange halation around bright edges (the window, white stripes, skin highlights).
* Soft bloom on the brightest areas.
* Lifted, slightly milky blacks; gentle highlight roll-off; a faint warm-magenta cast.
* Coarse 35mm grain over everything, slightly stronger in mid-tones.
* A few dust specks, now and then a short hair, never on faces.
* A soft vignette.
* 4:3 frame: the picture is 4:3 with black pillarbox bars on the sides. Keep every face inside it.
PALETTE
Peach-tan skin, violet-rose shadows, violet-black hair with mauve sheen.
Warm amber, peach, magenta, violet, dusk blue.
Muted browns, olive, slate grey for clothes.
Do NOT use neon, pure white digital highlights or flat grey.
OBJECT CONTINUITY
If the character holds an object, it is painted as part of the same cel, attached to the hand.
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
The cels must match the source frame exactly: same silhouette, same pose, same position.
The background painting follows the real camera movement of the source.
NO cel left behind from a previous frame.
NO background element that pops in or out.
FRAME-TO-FRAME CEL LIFE
THIS IS CRITICAL.
It must feel like hand-traced cels filmed one by one, not a still filter.
Allow between consecutive frames:
* ink lines to shift by 1-2 px (trace boil)
* shadow shapes to move slightly with the pose
* film grain and dust to change every frame
* halation to shimmer slightly
* a tiny gate weave (1-2 px)
Keep FIXED:
* the cel paint colours of each person
* the background painting and its dusk grade
* the sky colours
* the 4:3 frame
DO NOT
Do NOT use modern clean digital cel shading or glossy gradients.
Do NOT add speed lines, sparkles, blush stickers or emoji.
Do NOT make a western cartoon with thick black outlines.
Do NOT make a soft Ghibli watercolour daylight scene.
Do NOT use VHS tracking lines or scanlines (this is film, not tape).
Do NOT leave the room photographic behind painted people.
Do NOT give anyone big moe eyes or chibi proportions.
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
* NO cel painting or ink
* NO background repaint or sky
* NO halation, grain or dust
* NO 4:3 crop or bars
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
Do NOT begin the OVA anime transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – RETRO OVA ANIME STYLING (AFTER MY CONFIRMATION ONLY)
First, tell me the cel paint model you will use for each person (base, shadow and highlight colour for skin, hair and each garment), the dusk sky colours, and where the 4:3 frame sits.
Then style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation, so the people are exactly that frame.
Keep the same cel paint model, background painting and film treatment on every frame.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing, paint colours, sky or the 4:3 frame broke — regenerate those frames only.
The final video must feel like A SCENE FROM A 1990 OVA ON A WORN FILM PRINT: violet-shadowed cels, airbrushed dusk room, city-pop sky, halation, grain, 4:3, 12 frames per second.
The image should deliberately contain:
* flat cel paint with ONE hard violet shadow
* a sharp sheen band on the hair
* thin dark ink lines
* an airbrushed matte-painting background at dusk
* a violet-magenta-amber sky in the window
* halation, coarse grain and a faded print
* a 4:3 frame.
Avoid clean modern digital anime.
```
