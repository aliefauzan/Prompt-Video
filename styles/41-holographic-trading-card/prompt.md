# 41 — Holographic Trading Card

**Look:** every frame becomes the art window of a landscape HOLO RARE collectible card, held slightly tilted over a dark desk. The full frame sits inside a gold-framed window with the composition kept, printed with extra punch. The room behind the people is printed on rainbow holo-foil: diagonal diffraction stripes in saturated rainbow bands that sweep across the card. A soft specular glare band slides over the card every few seconds. Glitter flecks and 4-point star sparkles flash where the glare passes. The people carry only a faint sheen and stay sharp and true-colour. Around the window: a foil border, a name bar ("OFFICE TRIO", HP 270, energy badge), a stats panel (ATK / DEF / SPD / VIBE bars), a move list with damage numbers, a flavour-text strip, set number "041/179" and a "HOLO RARE" star.

**Also called / where it trends:** "make yourself a trading card", "holo card edit", "holographic card filter", "rainbow rare", "holo foil effect", "custom Pokémon-style card of yourself" (generic card, no brand). Seen in TikTok/CapCut card templates, IG Reels "turn your friends into cards" trends, the CSS holo-card demos that went viral on dev Twitter, collectible-card unboxing / pull videos ("rainbow Charizard"), and sports / team-card edits.

**References:**
- https://www.pinterest.com/search/pins/?q=holographic%20trading%20card%20of%20yourself%20custom (screenshot `refs/ref_1.png`): custom holo cards of real people, foil borders, stats panels, rainbow sheen.
- https://github.com/simeydotme/pokemon-cards-css: the viral CSS holo-foil card effects (colour-dodge rainbow, glitter and sparkle layers, glare following the tilt). The demo is at https://poke-holo.simey.me/.
- https://css-tricks.com/holographic-trading-card-effect/: how the holographic card effect is built (gradients, blend modes, tilt).
- https://github.com/daniel-ilett/shaders-holo-card: a Unity shader for holo cards (rainbow by view angle, foil mask).
- https://www.pokemoncardeffects.com/: catalogue of real card foil treatments (holo, reverse holo, cosmos, rainbow rare, galaxy).
- https://www.sarntinel.com/templates/holo-card/: a holo-card template for making your own card.
- https://www.dexerto.com/pokemon/viral-pokemon-tiktok-shows-off-insane-rainbow-charizard-card-and-how-they-got-it-1635684/: a viral TikTok of a rainbow holo card, showing the sheen in motion.
- https://www.framer.com/marketplace/components/holographiccard3d/: a 3D holographic card component (tilt + foil).

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049), `example.mp4` (full clip). Local approximation rendered with `render.py` (numpy + OpenCV + PIL + person masks for the foil / people split); the 6 sheet frames are in `frames/`. Distinct from 15 Y2K Chrome (chrome-metal type and liquid metal; here it is a printed card object with rainbow diffraction foil and game stats).

## Prompt

```text
I'm uploading one video clip. Convert it into a HOLOGRAPHIC TRADING CARD animation, frame by frame, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Transform every frame into a genuine HOLO RARE COLLECTIBLE CARD, built from:
* a landscape card filling almost the whole frame, with rounded corners
* the full original frame placed in the card's ART WINDOW (scaled, not cropped, composition kept)
* the art printed with slightly boosted contrast and saturation
* the BACKGROUND (room) of the art printed on RAINBOW HOLO-FOIL
* fine diagonal DIFFRACTION STRIPES in saturated rainbow bands (red → yellow → green → cyan → blue → magenta)
* a soft white SPECULAR GLARE band sweeping diagonally across the card
* GLITTER flecks and 4-point STAR SPARKLES that flash where the glare passes
* the people kept sharp and true-colour with only a FAINT sheen
* a metallic rainbow FOIL BORDER around the card
* game-card typography: name bar, HP, stats bars, moves, flavour text, set number, rarity star
* a very slight hand-held TILT of the card over a dark desk with a soft shadow
The result should feel like someone:
TURNED THE CLIP INTO A LIMITED-EDITION TRADING CARD
→ PRINTED THE ROOM ON RAINBOW HOLO-FOIL
→ ADDED A NAME, STATS AND MOVES
→ PULLED IT FROM A PACK
→ TILTED IT UNDER A LAMP SO THE FOIL CATCHES THE LIGHT
→ FILMED IT FRAME BY FRAME.
CHARACTER — THE CARD ART
The MAIN HUMAN SUBJECTS stay PHOTOGRAPHIC and true-colour inside the art window.
Preserve each person's exact:
* identity
* face
* expression
* hairstyle
* clothing silhouette
* clothing colours and patterns
* accessories
* pose
* body proportions
* movement
* hand position
* interaction with objects
Do NOT redraw them as anime, cartoon or game characters.
Do NOT cover their faces with rainbow foil.
People get only a faint foil sheen (about 5-18%), slightly stronger when the glare passes over them.
Skin stays natural.
THE ROOM — HOLO-FOIL BACKGROUND
The room keeps its exact layout inside the art window, but its print sits on rainbow foil:
* white and light walls turn into strong rainbow bands
* fine diagonal diffraction stripes (about 30 px period) over the bands
* the rainbow bands slowly slide across the card over time
* where the glare band passes, the foil flares brighter and glitter flashes
* darker objects (screens, plants, furniture) keep their shapes and tint with the foil
The room must remain readable as the same room.
CARD LAYOUT
Fixed layout, identical in every frame:
* outer rainbow-foil border with rounded corners
* top NAME BAR (dark ink panel, thin gold outline): "OFFICE TRIO" in bold condensed white type, "STAGE 2 / TEAM CARD" in small gold type, "HP 270", and a round gold energy badge with a white star
* ART WINDOW (about 3/4 of the card width, left side) with a thin gold frame
* right STATS PANEL (dark ink, gold outline): ATK 88, DEF 74, SPD 91, VIBE 99, each with a gold bar; then a gold divider and two moves: "SIDE-EYE 60" (Opponent's next attack does -20.) and "GROUP SMILE 120" (Flip 3 coins. +30 for each heads.)
* bottom STRIP: flavour text "Three coworkers caught mid-take. Rarely seen without a smile.", set number "041/179", gold star, "HOLO RARE"
All type must be crisp, correctly spelled and legible, never melted AI lettering.
Use generic card design: NO real game logos, NO trademarked names, NO energy symbols copied from existing card games.
FOIL AND LIGHT
* rainbow foil hue shifts along a diagonal, sweeping slowly with time
* one glare band crosses the whole card about every 3.5 seconds
* the foil border and the background foil brighten under the glare
* text panels catch only a light sheen
* glitter: hundreds of tiny fixed flecks; the ones under the glare flash; the brightest become 4-point stars
* sparkles never sit on faces
CARD IN HAND
* the card tilts a few degrees in perspective, slowly and smoothly (hand-held, never shaky)
* a soft drop shadow on a dark warm-grey desk shows around the card edge
* the card never leaves the frame and never covers less than about 95% of it
PALETTE RULES
* art window: original colours, a little more saturated
* foil: fully saturated rainbow spectrum with white glare
* panels: deep indigo ink, gold (#F6D678-like) outlines and labels, warm white type
* desk: near-black warm grey
Do NOT turn the whole image rainbow.
Do NOT use chrome / liquid-metal silver.
LAYER ORDER
A typical frame reads:
DARK DESK + CARD SHADOW
↓
CARD BODY + RAINBOW FOIL BORDER
↓
ART WINDOW: PEOPLE (true colour) OVER HOLO-FOIL ROOM
↓
DIFFRACTION STRIPES + GLARE BAND
↓
GLITTER + STAR SPARKLES
↓
NAME BAR, STATS PANEL, BOTTOM STRIP (crisp type)
↓
SLIGHT PERSPECTIVE TILT.
OBJECT CONTINUITY
IMPORTANT:
If a character interacts with an object, keep that object in the card art.
Examples:
* phone
* cup
* chair
* glasses
* bag, headphones
If the object is essential to the action, keep it clearly visible.
Do NOT accidentally remove it.
CHARACTER CONTINUITY LOCK
The SAME people must remain recognisable in every frame.
Never change:
* identity
* facial structure
* hairstyle
* clothing silhouette
* accessories
* body proportions
* anatomy
* expression
* pose
* action
* position
Generation is for VISUAL STYLE ONLY.
PERFECT MOTION TRACKING
The underlying human movement must stay exactly faithful to the source footage.
The FOIL shimmers.
The HUMAN MOTION does NOT change.
If someone moves:
they move inside the art window exactly as in the source.
If someone reaches toward the camera:
the hand stays inside the art window, at the scaled size.
NO ghost people from previous frames.
NO frozen art while the foil moves.
FRAME-TO-FRAME FOIL LIFE
THIS IS CRITICAL.
Every frame should feel like the same physical card catching light from a new angle.
Allow:
* rainbow bands to slide smoothly with time
* the glare band to travel smoothly
* glitter to twinkle differently every frame
* the card tilt to change smoothly by a fraction of a degree per frame
Keep the card layout, text, stats and border pixel-stable (only the tilt moves them).
Do NOT change the text, numbers or layout between frames.
Do NOT let the foil pattern jump randomly.
DO NOT
Do NOT crop or zoom the art; keep the full original framing inside the window.
Do NOT put rainbow foil over faces.
Do NOT make it a chrome / Y2K liquid-metal look.
Do NOT use real card-game logos, brand names or copied card designs.
Do NOT add random garbled text.
Do NOT turn the people into cartoon or anime characters.
Do NOT replace any face.
Do NOT create new poses.
Do NOT change anatomy.
Do NOT change clothing shape.
Do NOT make the card shake or spin.
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
* NO card frame
* NO holo-foil
* NO text or stats
* NO glitter or glare
* NO colour changes
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
Do NOT begin the trading-card / holo-foil transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – HOLOGRAPHIC TRADING CARD STYLING (AFTER MY CONFIRMATION ONLY)
Style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation.
Apply every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT restyle a whole shot from one keyframe.
Keep the card layout, all text, stats, colours and fonts identical in every frame; only the art, foil position, glare, glitter and tilt change.
Keep the glare sweep and foil drift continuous across frames (one glare pass about every 42 frames).
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, text or the style rules broke — regenerate those frames only.
The final video must feel like a REAL HOLO RARE CARD tilting under a lamp, with the clip playing in its art window.
The image should deliberately contain:
* a full card layout with crisp type
* rainbow diffraction foil on the background
* a sweeping glare band
* twinkling glitter and star sparkles
* sharp true-colour people
* a slight hand-held tilt.
Avoid a flat rainbow filter over the whole frame.
```
