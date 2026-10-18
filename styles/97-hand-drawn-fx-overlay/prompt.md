# 97 — Hand-Drawn Frame-by-Frame FX

**Look:** The footage stays real, but cartoon effects are painted over it, one fresh drawing per frame. Cel-shaded flames lick up from the people's heads and shoulders. Puffs of cartoon smoke rise and break apart, and a big smoke cloud wipes the screen. Jagged blue-white lightning crawls along their outlines, and a crescent slash flashes across the frame on the beat. Every effect is flat colour in hard bands (dark edge, mid tone, bright core, no gradients), with a soft glow. The light it throws falls on the real people: orange from fire, blue from lightning, green from spirit flame. The shapes "boil" a little every frame, because each one is redrawn by hand.

**Also called / where it trends:** "手绘逐帧特效" (hand-drawn frame-by-frame FX), "手绘特效", "街头美漫 VFX" (street American-comic VFX) and "卡通风格化特效" on Bilibili. In English: "2D FX animation", "2DFX", "hand-drawn VFX over live action", "draw on your videos", "cartoon FX pack" (After Effects / Premiere / Resolve / CapCut packs of fire, smoke, lightning and slash elements). Arcane-style 2DFX reels and Michel Gagné's FX animation are the high end. Edits that draw sakuga-style fire and lightning over real people are an AI-video ask too.

**References:**
- Bilibili search 手绘逐帧 特效 街头美漫 VFX (screenshot `refs/ref_1.png`, from discovery D4): https://www.bilibili.com/video/av116018609456464 (AE 手绘逐帧街头美漫 VFX 动画风格流程), https://www.bilibili.com/video/av708819741 (卡通风格化特效), https://www.bilibili.com/video/av342965495 (手绘逐帧特效合集), https://www.bilibili.com/video/av115717408098101 (风格化流体、烟火、战斗特效), https://www.bilibili.com/video/av117236014517806 (风格化手绘特效), https://www.bilibili.com/video/av116879895638848 (动画2D闪电特效的秘诀, the drawing process)
- YouTube contact sheet (`refs/ref_2.png`): https://www.youtube.com/watch?v=92R-XUprQLw ("2D in Live Action – VFX Breakdown"), https://www.youtube.com/watch?v=IPTm8L_4LVU (Michel Gagné, hand-drawn electricity drip over live action for an indie film), https://www.youtube.com/watch?v=Ji04neCDVCU (Michel Gagné's raw 2D FX animation for "Space Jam 2"), https://www.youtube.com/watch?v=KEuD0s0qdl8 ("ARCANE 2DFX" reel), https://www.youtube.com/watch?v=0kV0lDT66rY ("How I draw on top of my videos"), https://www.youtube.com/watch?v=QQ0w18PyG2I (free cartoon FX pack: fire, smoke, slash, impact), https://www.youtube.com/watch?v=7VTK_ZHqySg (cartoon explosion elements for edits), https://www.youtube.com/watch?v=Hu9ik0PcrWM (cel fire elements, with and without glow)
- https://vfxreactor.com/clips/12674: a hand-painted lightning clip from film, the analogue ancestor of the look.

How it differs from taken styles: **13 Neon Scribble** and **23 Boogley Doodles** draw *lines*: outline scribbles and doodle accents. Here the effects are *filled, shaded elemental matter* (fire, smoke, electricity, slash). They are painted in hard cel bands with a dark edge and a bright core, they squash, rise and break up like animated FX, and they light the real people. The footage itself is not redrawn, so it is not a full-frame cartoon conversion either.

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049), `example.mp4` (the whole clip at 12 fps with the original audio) and `preview.webp`. This is a local approximation made with `render.py` (numpy + OpenCV). The footage is darkened and desaturated a little. The people's outlines come from the source mattes, and Apple Vision face boxes (`../94-xray-skeleton-scan/pose.json`) keep flames off faces. From 0–5 s, flame tongues grow from the upward-facing outline points. They are summed into a heat field and posterized into five cel bands, with cel smoke puffs and embers rising from the tips. Around 5 s a three-tone cartoon smoke cloud wipes the frame (covering the hand-over-lens shot). From 5–10 s, midpoint-displacement lightning hugs the outlines and forks outward, with a blue rim light and one-frame flashes. From 10–15 s, green spirit flame plays with crescent slash arcs on the beat. Every shape gets new random wobble each frame (the boil), while its size follows slow noise. Glow and cast light are added back onto the people.

## Prompt

```text
I'm uploading one video clip. Convert it into a HAND-DRAWN FRAME-BY-FRAME FX animation (手绘逐帧特效): keep the live-action footage, and paint cel-shaded cartoon effects (fire, smoke, lightning, slash arcs) over it, freshly drawn on every frame, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Hand-drawn 2D FX animation composited over live action, cel-shaded elemental effects, street American-comic VFX, sakuga fire, smoke and lightning, flat colour bands with glow.
Transform the footage into live action plus painted effects built from:
* the ORIGINAL FOOTAGE kept photographic, slightly darkened and slightly desaturated so the effects read
* CEL-PAINTED FIRE: flame tongues rising from the people's heads, shoulders and arms, with teardrop tips, S-curved bodies and split tongues
* every effect in HARD CEL BANDS, without gradients: dark edge, deep tone, mid tone, light tone, near-white core
* CARTOON SMOKE: round puffy clusters with a darker body, a lighter top-left highlight and a thin dark edge, rising, growing, then breaking into smaller puffs and vanishing
* LIGHTNING: jagged, branching blue-white bolts crawling along the people's outlines and forking outward, with a thick dark-blue edge, a blue body and a white core
* SLASH ARCS: crescent sweeps, thick in the middle and tapering to sharp points, that appear, stretch and break apart over three or four frames
* EMBERS and SPARKS: small diamond-shaped sparks flying up and out
* a SOFT GLOW around every effect, and the effect's colour CAST AS LIGHT on the nearby people (orange from fire, blue from lightning, green from spirit flame)
* a big CARTOON SMOKE CLOUD that wipes the whole frame once, as a transition
The result should feel like someone:
SHOT THE SCENE ON A PHONE
→ PRINTED EVERY FRAME
→ LAID A SHEET OF ANIMATION PAPER ON TOP
→ HAND-PAINTED FIRE, SMOKE, LIGHTNING AND SLASHES IN FLAT CEL COLOURS
→ COMPOSITED THEM BACK WITH GLOW
→ PLAYED IT FRAME-BY-FRAME.
CHARACTER — REAL PEOPLE, PAINTED POWER
The people stay PHOTOGRAPHIC.
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
Do NOT redraw, cartoonize or anime-fy the people.
Do NOT cover faces with effects. Flames rise from above the head and from the shoulders, never across the eyes, nose or mouth.
Do NOT beautify or re-sculpt faces.
FX DRAWING RULES (WHAT MAKES IT HAND-DRAWN FX)
* Draw every effect as FILLED SHAPES, not outlines or scribbles.
* Use 4–5 flat colour bands per effect. The band edges are crisp. The darkest band sits on the outside edge, the brightest at the core.
* Fire: base colours deep red, red-orange, orange, yellow, cream-white core. Tongues lean together in one wind direction and sway over time.
* Spirit flame (last section): the same shapes in deep green, green, lime, pale mint and white.
* Smoke: lavender-grey puffs with lighter tops and a thin dark edge, semi-opaque, rising and drifting.
* Lightning: thick, jagged and branching, never a smooth curve. It flickers to a new shape every frame and hugs the body outline.
* Slash: one clean crescent with a coloured body and white core, drawn in 3–4 frames: sweep in, full, thin, breaking into dashes.
* Effects are anchored to the people and follow them exactly as they move.
* Effects can overlap the people's outline and the room behind, but stay off faces.
* Add a soft bloom around effects, and coloured light on the people near them.
EFFECT TIMELINE
* About 0–5 s: fire on everyone, with smoke puffs and embers.
* Around 5 s: a big cartoon smoke cloud fills the frame and clears again (a transition).
* About 5–10 s: lightning crawling over the outlines, with blue rim light and an occasional one-frame blue flash.
* About 10–15 s: green spirit flame, with crescent slash arcs on the beat.
PALETTE
Natural footage, slightly dimmed.
Fire: #7A1812 edge, #E13C0A, #FF8C00, #FFD746, #FFF8CD core.
Lightning: #0A1E78 edge, #1E78FF, #6ED2FF, #DCF5FF, white core.
Spirit flame: #0A501E edge, #19A028, #50E146, #B9FFAA, #F0FFEB core.
Smoke: #463C5A shadow, #8C7D96 body, #D2C8D7 highlight, #23192D edge.
OBJECT CONTINUITY
If the character holds an object, it stays photographic. Effects may wrap around it but never replace it.
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
Effects stay attached to the same body parts as people move: flames on the same head and shoulders, lightning on the same outline.
NO frozen effect from a previous frame.
NO effect left floating where a person used to be.
FRAME-TO-FRAME FX LIFE
THIS IS CRITICAL.
It must feel HAND-ANIMATED ON ONES at 12 fps.
Change between consecutive frames:
* every flame tongue is redrawn: tips flick, split and merge, with a slight wobble ("boil")
* smoke puffs rise, swell, then shrink and break apart
* lightning takes a brand-new jagged path every frame
* sparks fly outward and vanish
Keep FIXED:
* the colour bands and palette of each effect
* the overall size of the fire (it breathes, it does not pop in and out)
* the glow strength
* the footage grade
DO NOT
Do NOT draw line-art scribbles or neon outlines instead of filled effects.
Do NOT use realistic, photographic fire, smoke or particle simulations.
Do NOT use smooth gradients inside effects.
Do NOT cover faces.
Do NOT turn the people or the room into a cartoon.
Do NOT add text, stickers or emoji.
Do NOT let effects flicker on and off at random.
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
* NO colour change
* NO painted FX, glow or cast light
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
Do NOT begin the FX painting.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – HAND-DRAWN FX STYLING (AFTER MY CONFIRMATION ONLY)
First, tell me the effect timeline you will use (which frames get fire, the smoke wipe, lightning, spirit flame and each slash), and where on each person the effects anchor.
Then style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation, so the people and the room are exactly that frame.
Apply every style rule above, with the SAME palettes, band count and glow on every frame, and a freshly drawn effect shape on every frame.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing, an effect covering a face, or an effect detached from its person appears — regenerate those frames only.
The final video must feel like A 2D FX ANIMATOR PAINTED POWERS ONTO REAL FOOTAGE: cel fire, cartoon smoke, crawling lightning and slashes, 12 frames per second.
The image should deliberately contain:
* the real, photographic people
* filled cel-shaded effects in hard colour bands with bright cores
* glow and coloured light cast onto the people
* a slight hand-drawn boil from frame to frame.
Avoid line-only doodles and realistic simulated fire.
```
