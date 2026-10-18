# 55 — Cyberpunk Neon City

**Look:** The room becomes a dark apartment high above a rain-soaked megacity at night. The people are relit by hard magenta light from one side and cyan from the other, with neon rim light along their edges and a wet sheen on skin and fabric. Through the window, towers of lit windows and glowing kanji signs bleed through haze. Translucent holographic HUD panels flicker in the room, rain streaks fall in front of everything, and the picture blooms, splits slightly in RGB and grains like night footage on a digital cinema camera.

**Also called / where it trends:** "Cyberpunk" (frameloop.ai style name), "neon noir", "Blade Runner look", "Shinjuku rain", "cyberpunk portrait", "neon city night", "tech-noir". It is one of the most-used presets in AI image and video tools, and a constant on Instagram, TikTok and Pinterest through neon street portrait photography in Tokyo, Hong Kong and Seoul, Cyberpunk 2077 photo mode, and gel-lit portrait tutorials.

**How it differs from 32 (Synthwave):** synthwave is a clean, nostalgic 1980s retro-future: a sunset gradient, a chrome grid floor, a striped sun, airbrushed and dry. Cyberpunk Neon City is a gritty, near-future dystopian NIGHT: rain, wet reflections, haze, dense vertical city lights, Japanese signage and HUD overlays, and no sun, grid or sunset.

**References:**
- https://frameloop.ai/visual-styles (screenshot `refs/ref_1.png`; the style's sample image `refs/ref_2.png`): the **Cyberpunk** style card. Its style prompt, credited to frameloop.ai and expanded into the workflow below: *"cyberpunk, neon lit, futuristic, dystopian, high-tech, gritty atmosphere."*
- https://picxstudio.com/templates/6536-cyberpunk-realism-portrait-in-shinjuku-rain (screenshot `refs/ref_3.png`): PicX Studio, "Cyberpunk Realism Portrait in Shinjuku Rain". A photographic portrait with magenta/cyan neon rim light, rain, wet street reflections and kanji signs, which is the same recipe applied to a real person.
- Blade Runner (1982), Blade Runner 2049 (2017) and Ghost in the Shell (1995): the canonical visual sources for rain-soaked neon megacities, holographic advertising and kanji signage.

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049), `example.mp4` (the whole clip at 12 fps with the original audio) and `preview.webp`. This is a local approximation made with `render.py` (numpy + OpenCV + the person masks). A procedural night-city plate (three layers of towers with lit window grids and 14 glowing kanji neon signs) replaces the bright window and the wall monitor. The people are desaturated and relit with a magenta→cyan key across the frame, magenta and cyan rim lights from shifted masks, light wrap and a wet high-pass sheen. Holographic HUD panels with Japanese text and readouts float in the room, hidden behind the people, with scanlines and flicker. It adds neon spill, haze, slanted rain streaks, bloom, a slight RGB split, vignette and grain.

## Prompt

```text
I'm uploading one video clip. Convert it into a CYBERPUNK NEON CITY frame-by-frame animation: every frame should look like a night scene in a rain-soaked, neon-lit, dystopian megacity, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Cyberpunk, neon lit, futuristic, dystopian, high-tech, gritty atmosphere.
Transform the footage into a cyberpunk night built from:
* NIGHT: the scene is dark, lit only by neon and screens
* MAGENTA / HOT-PINK key light from one side
* CYAN / ELECTRIC-BLUE light from the other side
* hard NEON RIM LIGHT along the people's edges
* RAIN-WET surfaces: sheen on skin, hair and fabric, reflections on hard surfaces
* a dense MEGACITY through every window: towers, lit windows, vertical neon signs
* glowing JAPANESE KANJI / KATAKANA neon signage
* translucent HOLOGRAPHIC HUD panels and readouts floating in the room
* falling RAIN streaks in front of the scene
* atmospheric HAZE catching the neon
* neon BLOOM and glow
* a slight RGB channel split and digital grain
The result should feel like someone:
MOVED THE SCENE INTO A HIGH-RISE APARTMENT IN A NEON MEGACITY
→ SWITCHED OFF EVERY NORMAL LIGHT
→ LIT THE PEOPLE WITH MAGENTA AND CYAN NEON
→ LET THE RAIN AND HAZE ROLL IN
→ PROJECTED HOLOGRAMS INTO THE ROOM
→ SHOT IT AT NIGHT FRAME-BY-FRAME.
CHARACTER — PHOTOGRAPHIC, NEON-LIT
The people stay PHOTOGRAPHIC and REAL, only relit.
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
Do NOT add cyborg implants, tattoos, visors, chrome, masks or new clothing.
Do NOT turn them into anime, a game character or a 3D render.
NEON LIGHTING ON THE PEOPLE
* The left side of each person takes MAGENTA / PINK light; the right side takes CYAN / BLUE light (or the reverse, but keep it the same in every frame).
* Thin bright RIM LIGHT traces the outline of the head, shoulders and arms, magenta on one side and cyan on the other.
* Faces stay readable: a soft fill keeps the eyes, mouth and expression visible.
* Skin, hair and glasses catch small specular neon highlights, as if slightly wet.
* Original daylight colours are mostly replaced by the neon light; only a little natural skin tone remains.
THE CITY
* Every window shows a dark megacity at night: layered towers, grids of lit windows, vertical neon signs.
* Neon signs carry Japanese text (kanji / katakana), glowing magenta, cyan, violet and a little amber.
* The city is softened by haze and rain, with glow bleeding around each sign.
* Screens and monitors in the room show glowing city or data imagery.
* The city may flicker slightly (a sign buzzing, a light switching), but it does not move or pan.
HOLOGRAPHIC OVERLAYS
* 2–4 translucent HUD panels float in the room: thin cyan frames, Japanese labels, numbers, bars.
* They are see-through, with scanlines and a slight flicker.
* They sit BEHIND the people and never cross a face or body.
* They stay in the same place from frame to frame.
RAIN, HAZE AND GLOW
* Thin, slanted rain streaks fall across the whole frame, new streaks every frame.
* A few nearer, brighter streaks catch the neon.
* Haze softens the background and makes neon light visible in the air.
* Neon sources bloom; bright edges get a soft glow.
* A tiny RGB channel offset at the edges of the frame, like a digital lens.
* Fine digital night grain.
PALETTE
Magenta, hot pink, cyan, electric blue, deep violet, near-black blue.
Small accents of acid green or amber in signs only.
Do NOT use warm daylight, sunset gradients or pastel colours.
OBJECT CONTINUITY
If the character holds an object, it stays attached to the hand, relit by the same neon.
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
The people must match the source frame exactly.
The rim light follows their outlines as they move.
The city, signs and HUD panels stay locked to the room, like real objects outside and inside it.
NO rim light lagging behind a moving arm.
NO HUD panel sliding across a face.
FRAME-TO-FRAME NIGHT LIFE
THIS IS CRITICAL.
It must feel like a real rainy night, not a still neon filter.
Allow between consecutive frames:
* rain streaks to change every frame
* neon signs to buzz and flicker slightly
* HUD panels to flicker and scanlines to roll
* haze to drift a little
* grain to change every frame
Keep FIXED:
* the magenta/cyan lighting direction
* the city layout and sign positions
* the HUD panel positions
* the overall exposure
DO NOT
Do NOT make it synthwave: no sunset, no chrome grid floor, no striped sun, no palm trees, no 1980s retro chrome text.
Do NOT make it daylight or clean.
Do NOT cover faces with holograms, rain blobs or signs.
Do NOT turn the people into cyborgs or game characters.
Do NOT outline the people with a flat glowing sticker edge.
Do NOT use random unreadable glyphs; use real Japanese words.
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
* NO relighting or neon
* NO city replacement
* NO holograms, rain or haze
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
Do NOT begin the cyberpunk neon city transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – CYBERPUNK NEON CITY STYLING (AFTER MY CONFIRMATION ONLY)
First, tell me which side gets magenta and which gets cyan, what the windows and screens will show, the Japanese words for the main neon signs, and where the HUD panels will sit.
Then style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation, so the people are exactly that frame.
Apply every style rule above, with the SAME city, signs, lighting and HUD layout in every frame.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing, the city layout or the lighting direction broke — regenerate those frames only.
The final video must feel like A RAINY NIGHT IN A NEON MEGACITY: magenta and cyan light on real people, kanji signs through the haze, holograms in the air, rain falling, 12 frames per second.
The image should deliberately contain:
* magenta and cyan neon light on the people
* neon rim light and wet highlights
* a night megacity with kanji neon signs
* translucent holographic HUD panels
* slanted rain and haze
* bloom, slight RGB split and grain.
Avoid clean daylight realism.
```
