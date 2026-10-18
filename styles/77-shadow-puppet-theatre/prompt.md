# 77 — Shadow Puppet Theatre (皮影)

**Look:** the clip staged as a Chinese shadow-puppet play (皮影戏), seen from the audience side of a glowing paper screen. A warm lamp behind the screen makes a hot centre that falls off to deep orange, with a fine cloth weave and a slight oil-lamp flicker. The people become flat puppets of translucent dyed leather pressed against the screen: hair and dark clothes in black leather, faces carved open as pale amber with black-lined features (空脸), and garments dyed vermilion, green, ochre and indigo, each patch outlined in black. Punched rosettes and dots are cut through the clothing so the lamp shines through. A control rod runs from each puppet's neck down out of frame, and rivets mark the joints. The room becomes soft, blurred scenery shadows further behind the screen.

**Also called / where it trends:** 皮影 / 皮影戏 / 皮影风格 (shadow-puppet style), 驴皮影 (donkey-hide shadow puppets), "Chinese shadow puppetry", "shadow play", "piying". It trends in Bilibili and Douyin AI animation as 皮影风格 AI动画 (the 《白素贞》 and 《纸山与火》 AI shorts, the classic 《大闹天宫》 look) and in national-style (国风) edits. It is on UNESCO's Intangible Cultural Heritage list (2011).

**References:**
- https://www.bilibili.com/video/av115846861100593 — 「皮影《白素贞》」, an AI shadow-puppet short (Bilibili AI creation contest). Screenshot of the Bilibili search "皮影风格 AI动画" in `refs/ref_1.png`.
- https://www.bilibili.com/video/av115851374107335 — 《张飞审瓜》, a classic Chinese paper-cut / shadow-puppet animation
- https://www.bilibili.com/video/av1455315280 — 《大闹天宫》, whose character design draws on folk shadow puppets (皮影戏)
- https://www.bilibili.com/video/av117443531903425 — 《纸山与火》, a self-made AI animation in shadow-puppet style
- https://artsandculture.google.com/story/the-traditional-art-form-of-chinese-shadow-puppetry-king-shadow-museum/yAXRvop6wTndJw?hl=en — Google Arts & Culture / Wang's Shadow Museum: a lit screen, a red stage frame, rod-held translucent puppets. Screenshot in `refs/ref_2.png`.
- https://ich.unesco.org/en/RL/chinese-shadow-puppetry-00421 — UNESCO: Chinese shadow puppetry
- https://english.beijing.gov.cn/beijinginfo/culture/beijingfolklore/acrobatics/202312/t20231210_3494416.html — donkey-leather shadow-puppet carving (punched patterns, dyed leather)
- https://chiculture.org.hk/en/china-five-thousand-years/1832 — Academy of Chinese Studies: Chinese shadow puppetry (jointed limbs, rods, carving)
- http://en.chinaculture.org/2020-12/18/content_1487732.htm — China Culture: Chinese shadow puppetry

**How it differs from taken styles:** 43 Dark Stage Spotlight is a lighting grade on the real footage. 35 Ukiyo-e is a printed woodblock look. 47 Two-Tone Screen Print is opaque ink on paper. Shadow puppetry is backlit: flat, translucent, saturated dyed leather with black carved outlines, punched ornament holes the lamp shines through, rods and joint rivets, all on a glowing screen. 76 Sand Animation is also backlit, but it is loose monochrome sand, not coloured leather figures.

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049), `example.mp4` (all 179 frames at 12 fps), `preview.webp`. This is a local approximation made with `render.py` (numpy + OpenCV + person masks). The screen is a warm radial lamp with a cloth weave and flicker. The room becomes blurred, half-transparent scenery shadows. The people's colours are classified into black leather, a carved-open face (skin plus head ellipses found from the matte), and vermilion / green / ochre / indigo dyes. Each patch is outlined in black, and DoG lines become the facial features. A rosette ornament is punched through the clothing, anchored to each head so it moves with the puppet. The neck rods and rivets come from the head finder. The six sheet frames are in `frames/`.

## Prompt

```text
I'm uploading one video clip. Convert it into a traditional Chinese SHADOW PUPPET THEATRE (皮影戏) frame-by-frame animation matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Transform the footage into a shadow-puppet play seen from the audience side of the screen:
* a glowing paper / silk SCREEN lit from behind by a warm lamp
* a hot centre (cream-gold) falling off to deep amber-orange at the edges
* a fine cloth weave visible on the screen
* the people as FLAT PUPPETS of translucent dyed LEATHER (donkey hide), pressed against the screen and perfectly sharp
* saturated, glowing dye colours where the lamp shines through the leather: vermilion red, green, ochre yellow, indigo, and black
* BLACK CARVED OUTLINES around every colour patch and around the whole puppet
* PUNCHED ORNAMENT cut through the clothing: rosettes, dots, scallops and cloud scrolls, glowing bright where the lamp shines through
* faces carved OPEN (空脸): pale amber leather with fine black lines for eyes, brows, nose, mouth and glasses
* a thin control ROD from each puppet's neck down out of the frame, plus small RIVETS at the neck and shoulder joints
* the room as soft carved SCENERY shadows further behind the screen: blurred, half-transparent brown shapes
* a faint soft shadow ring around the leather where it presses on the screen
* a subtle oil-lamp flicker and a warm theatre vignette
The result should feel like someone:
FILMED THE CLIP
→ TRACED EVERY PERSON ONTO SCRAPED DONKEY HIDE
→ CARVED THE OUTLINES AND PUNCHED THE ORNAMENT
→ DYED THE LEATHER RED, GREEN, OCHRE AND BLACK
→ RIVETED THE JOINTS AND ATTACHED THE RODS
→ PRESSED THE PUPPETS AGAINST A LAMP-LIT SCREEN
→ PERFORMED THE CLIP FRAME-BY-FRAME AS A SHADOW PLAY.
CHARACTER — LEATHER PUPPETS
The MAIN HUMAN SUBJECT(S) become shadow puppets that keep their real look, NOT replaced by stock opera characters.
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
Do NOT turn them into profile-only opera figures: keep the real viewing angle (frontal or three-quarter).
Do NOT add opera headdresses, beards, armour or weapons.
Do NOT change body proportions.
FACES: carved open, pale translucent amber leather. Eyes, brows, nose, mouth, glasses and the face outline are fine black carved lines. The face must stay recognisable.
HAIR: solid black leather with a carved edge, with a few fine carved strand lines.
CLOTHING: each garment keeps its shape and is dyed in the traditional colour closest to its real colour (warm or brown = vermilion, light or beige = ochre, grey or green = green, blue = indigo, black = black). Stripes and prints become carved bands and patches in those dyes. Punched ornament fills the larger garment areas.
DYE / PALETTE RULES
* only these dyes: vermilion red, ochre yellow, green, indigo, black, plus the pale amber of the open face
* every colour glows because the lamp shines THROUGH it (translucent, never opaque paint)
* the leather is slightly uneven in thickness: soft mottling inside each colour
* black outlines separate every colour patch
* punched holes are the brightest points on the puppet
BACKGROUND RULES
ORIGINAL ENVIRONMENT:
the real room becomes stage scenery behind the screen: the window frame, wall edges, plants, screen and chair as soft, blurred, half-transparent brown shadows, simplified into carved prop shapes.
They must stay much softer and lighter than the puppets (further from the screen = blurrier).
BARE SCREEN (for selected sections, optional):
only the glowing screen behind the puppets, no scenery.
The people stay exactly where they are in the original frame.
LAYER ORDER
A typical frame reads:
LAMP-LIT SCREEN (hot centre, cloth weave)
↓
SOFT SCENERY SHADOWS (the room)
↓
SOFT PRESS-SHADOW RING
↓
TRANSLUCENT LEATHER PUPPETS (dyed colours)
↓
BLACK CARVED OUTLINES + PUNCHED ORNAMENT
↓
RODS AND JOINT RIVETS
↓
SCREEN GLOW, LAMP FLICKER, WARM VIGNETTE.
OBJECT CONTINUITY
IMPORTANT:
If the character is interacting with an object, preserve that object as a carved leather prop.
Examples:
* phone
* cup
* chair
* bag
* microphone
* headphones
If the object is essential to the person's action, carve it on the same puppet, pressed on the screen, sharp.
Do NOT accidentally merge it into the scenery shadows or drop it.
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
The PUPPET changes.
The HUMAN MOTION does NOT change.
If the head moves:
the puppet head moves exactly with it.
If the hand moves:
the puppet hand moves in that same frame.
If the body turns:
the puppet is re-carved to the new pose in that same frame.
If the character interacts with an object:
the leather prop moves exactly with the original action.
NO lagging limbs.
NO ghost puppets from previous frames.
NO puppets drifting off the person's real position.
PUPPET CONSISTENCY
THIS IS CRITICAL.
Each puppet is carved ONCE:
* every person keeps the SAME dye colours, the SAME outline style and the SAME ornament pattern in every frame
* the punched ornament MOVES WITH the puppet: it is cut into the leather and never slides across it
* the screen colour, lamp position, cloth weave and scenery shadows stay the same for the whole clip
* the rods stay attached at the same point on each puppet
Allow, every frame:
* a subtle oil-lamp flicker (1–3 % brightness, the hot spot drifting a few pixels)
Do NOT re-randomise dye colours or ornament patterns between frames.
Do NOT let the scenery shadows move unless the camera moves.
DO NOT
Do NOT render opaque paint, ink washes or woodblock print texture.
Do NOT render solid black silhouettes with no colour or detail.
Do NOT render 3D puppets, marionettes or dolls.
Do NOT add opera costumes, headdresses, weapons or horses.
Do NOT add Chinese characters, seals, titles or subtitles.
Do NOT show the puppeteers.
Do NOT blur the puppets.
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
* NO puppets
* NO screen glow
* NO carving or ornament
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
Do NOT begin the shadow-puppet transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – SHADOW PUPPET STYLING (AFTER MY CONFIRMATION ONLY)
Style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation.
Apply every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT restyle a whole shot from one keyframe.
Before generating, lock and report the look settings: the dye assigned to every garment of every person, the ornament pattern per puppet, the rod attachment points, the screen colours (centre and edge) and the lamp position.
Use the previous styled frame as a consistency reference for the next one, so each puppet keeps its dyes, outlines and ornament and the screen and scenery stay identical.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, a puppet's dyes or ornament, or the screen broke. Regenerate those frames only.
The final video must feel like a SHADOW PLAY performed live: glowing screen, translucent carved leather, punched light, rods and rivets, real motion.
The image should deliberately contain:
* a warm lamp-lit screen with a hot centre
* translucent dyed leather in vermilion, green, ochre, indigo and black
* black carved outlines on every patch
* punched ornament glowing through the clothing
* carved-open faces with fine black features
* control rods and joint rivets
* soft scenery shadows behind the screen.
Avoid clutter: no extra puppets, animals, clouds, mountains or props that were not in the source.
```
