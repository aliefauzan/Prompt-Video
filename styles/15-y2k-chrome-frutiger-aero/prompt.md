# 15 — Y2K Chrome / Frutiger Aero

**Look:** the people stay photographic but are lifted into a glossy 2007 Windows-Vista-wallpaper world: cobalt-to-aqua sky with soft cumulus and a shiny green hill, iridescent glass bubbles drifting up, liquid-CHROME bubble lettering ("AERO", "Y2K", "2000s"), four-point twinkle sparkles, a frosted Aero-glass window with a glossy title bar and green progress bar, sun lens flare, soft bloom and a white-cyan outer glow around the people. Bubbles drift and sparkles twinkle every frame.

**Also called / where it trends:** "Frutiger Aero", "Frutiger Metro", "Y2K chrome", "Aero edit", "webcore / cybercore", "Vista core", "2000s aesthetic edit" — TikTok (#frutigeraero, "how to make a Frutiger Metro edit"), Pinterest boards, IG Reels; covered as a 2026 comeback by Kittl, Envato, Icons8, Design Pieces, Y2Social; original wave covered by The Guardian and i-D.

**References:**
- https://www.pinterest.com/search/pins/?q=frutiger%20aero%20y2k%20chrome%20bubbles%20edit — screenshot `refs/ref_1.png`: glass bubbles, chrome bubble type, Vista sky + grass, XP-style windows, portrait edits ("Jelly Fish")
- https://www.kittl.com/blogs/frutiger-aero-aesthetic-stl/ — "making a comeback in 2026": glassy buttons, bright skies, water droplets, floating bubbles, Y2K chrome lineage
- https://elements.envato.com/learn/frutiger-aero — why 2000s web aesthetics are trending (Aug 2026)
- https://icons8.com/blog/articles/what-is-frutiger-aero/ — Frutiger Aero explained (Oct 2026)
- https://www.designpieces.com/2026/08/frutiger-aero-design-resources/ — fonts, palettes, vectors
- https://www.tiktok.com/discover/how-to-make-a-frutiger-metro-edit — TikTok edit tutorials hub
- https://www.theguardian.com/fashion/2023/dec/14/frutiger-aero-the-windows-screen-saver-design-trend-taking-tiktok-by-storm — "the Windows screen saver design trend taking TikTok by storm"
- https://i-d.co/article/what-frutiger-aero-teaches-us-about-niche-internet-aesthetics/ — i-D on the aesthetic

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049). Local approximation rendered with `render.py` (numpy + OpenCV + Pillow + person masks); 22 frames in `frames/`.

## Prompt

```text
I'm uploading one video clip. Convert it into a glossy Y2K CHROME / FRUTIGER AERO frame-by-frame animation matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Transform the footage into an optimistic early-2000s tech-ad / Windows Vista wallpaper world built from:
* PHOTOGRAPHIC people, cleanly cut out and slightly glossy
* bright COBALT → AZURE → AQUA sky gradient
* soft white cumulus clouds
* a shiny rolling GREEN grass hill with a glossy rim light
* iridescent GLASS / SOAP BUBBLES that refract what is behind them
* liquid CHROME bubble lettering
* four-point TWINKLE sparkles
* a frosted AERO-GLASS window with a glossy blue title bar and green progress bar
* sun glow and lens-flare streak with flare ghosts
* soft bloom and dreamy digital-camera glow
* a soft white-cyan outer glow around the people
* aqua / white / cobalt palette with a touch of grass green
The result should feel like someone:
SHOT THE CLIP IN 2007
→ CUT THE PEOPLE OUT
→ DROPPED THEM INTO A WINDOWS VISTA WALLPAPER
→ ADDED GLASS BUBBLES AND CHROME TYPE
→ OPENED A SHINY AERO WINDOW ON TOP
→ SPRINKLED SPARKLES AND LENS FLARE
→ EXPORTED IT AS A WMV
→ ANIMATED IT FRAME-BY-FRAME.
CHARACTER — GLOSSY PHOTO CUTOUT
The MAIN HUMAN SUBJECT stays PHOTOGRAPHIC.
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
Do NOT redraw the character.
Do NOT turn them into a 3D avatar, a doll, a cartoon or anime.
Do NOT make their skin plastic or airbrushed.
Grade the people bright, clean and slightly COOL:
* lifted, airy exposure
* gentle extra saturation
* cool cyan-blue tint in shadows
* a soft glossy sheen from the top-left light
* natural skin tone underneath
CLEAN CUTOUT + AERO GLOW
Cut the people cleanly from the original room.
Edges should be clean and natural (hair strands kept), NOT jagged, NOT paper-cut.
Around the cutout, add a soft WHITE-CYAN outer glow (20–40 px, soft falloff), like a Vista-era product shot.
No hard outline stroke.
BACKGROUND — VISTA SKY
For most sections, replace the room with:
* a vertical sky gradient: deep COBALT at the top → AZURE → pale AQUA / white haze near the horizon
* soft, bright, slightly blue-shaded cumulus clouds
* a smooth, rolling, saturated GREEN grass hill across the bottom with a glossy highlight along its crest
* a warm-white sun glow in the upper-left corner
ORIGINAL ENVIRONMENT OPTION
For selected sections, keep the original room in the exact same layout but wash it in AQUA:
* cool cyan-white grade over the whole room
* bubbles, sparkles, chrome type and window still on top
This keeps the original composition while staying in the style.
GLASS BUBBLES
THIS IS A KEY SIGNATURE.
Add 15–30 glass / soap bubbles of mixed sizes (tiny to about a sixth of the frame height).
Each bubble must look like real glass:
* it REFRACTS and slightly magnifies / flips what is behind it
* a thin iridescent thin-film rim (cyan, magenta, gold shifting around the edge)
* a big soft white specular highlight top-left
* a small secondary highlight bottom-right
* a bright thin outer edge
Big bubbles float BEHIND the people (in the sky).
A few small bubbles float IN FRONT.
NEVER put a bubble over a face.
CHROME LETTERING
Each section has ONE short chrome word: AERO, Y2K, 2000s, AQUA.
The lettering is:
* fat, rounded, bubbly letterforms (rounded sans, like Arial Rounded Bold)
* liquid CHROME: mirror bands of white, sky blue and deep navy, as if reflecting the sky and horizon
* bevelled and puffy, with sharp white specular hits and a dark navy rim
* a soft cyan outer glow and a soft drop shadow
* tiny sparkles glinting on the letters
* placed in an empty area, never over faces
* gently floating (bobbing a few pixels up and down)
AERO GLASS WINDOW
Add one small UI window per section, in a corner away from faces:
* frosted translucent glass body (blurred background showing through, white-blue tint)
* glossy blue gradient title bar with a filename ("aero_dreams.exe", "bubble_mail.exe", "dreamscape.wmv")
* minimise / maximise / red close buttons
* a green segmented progress bar filling up ("loading good vibes...")
SPARKLES + LENS FLARE
* 10–20 four-point white twinkle stars with soft cyan glow, scattered in the sky and around the people
* a horizontal sun lens-flare streak from the upper-left
* 3–4 soft coloured flare ghosts along the flare axis
PALETTE RULES
Dominant: COBALT BLUE, AZURE, AQUA / CYAN, WHITE.
Secondary: GRASS GREEN.
Accents: iridescent rims (tiny magenta / gold), red close button.
The people keep their own (cool-graded) colours.
Do NOT introduce dark, gritty, grungy, neon-pink cyberpunk or vaporwave purple palettes.
Everything should feel bright, clean, optimistic and glossy.
LAYER ORDER
A typical composition reads:
VISTA SKY (or aqua-washed room)
↓
CLOUDS + GREEN HILL + SUN GLOW
↓
BIG GLASS BUBBLES (behind the people)
↓
WHITE-CYAN OUTER GLOW
↓
PHOTOGRAPHIC PEOPLE (glossy grade)
↓
SMALL BUBBLES IN FRONT (never over faces)
↓
AERO GLASS WINDOW
↓
CHROME WORD
↓
SPARKLES + LENS FLARE
↓
SOFT BLOOM.
OBJECT CONTINUITY
IMPORTANT:
If the character is interacting with an object, preserve that object in the photographic cutout.
Examples:
* phone
* headphones
* bag
* chair
* cup
* microphone
If the object is essential to the person's action, include it within the cutout.
Do NOT accidentally remove it while isolating the person.
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
The WORLD around them floats and twinkles.
The HUMAN MOTION does NOT change.
If the head moves:
the cutout and glow follow.
If the hand moves:
the cutout follows; bubbles never stick to the hand.
If the body turns:
the silhouette updates.
If the character interacts with an object:
the object moves exactly with the original action.
NO floating cutout.
NO previous-frame silhouette.
NO lagging glow.
FRAME-TO-FRAME MOTION
THIS IS CRITICAL.
The decorative world is ALIVE, but smooth and continuous (not boiling):
* bubbles drift slowly UPWARD and sway sideways a little each frame, along continuous paths
* bubble thin-film colours slowly rotate
* sparkles twinkle (grow / shrink / fade) at different rhythms
* the chrome word bobs gently
* the progress bar fills step by step
* clouds drift very slowly
* lens-flare ghosts shimmer slightly
Within a section, the sky, hill, window and chrome word stay in the same place.
Bubbles must not pop in and out randomly; they enter and leave the frame by drifting.
DO NOT
Do NOT make it dark, grungy or gritty.
Do NOT add photocopy texture, halftone, paper or collage.
Do NOT make it neon cyberpunk or vaporwave purple-pink.
Do NOT turn people into 3D avatars, dolls or cartoons.
Do NOT airbrush or replace faces.
Do NOT put bubbles, windows or chrome type over faces.
Do NOT create new poses.
Do NOT change anatomy.
Do NOT change clothing.
Do NOT use flat, matte, outlined or pixel type; the type must be CHROME.
Do NOT misspell the chrome words or add random gibberish text.
Do NOT use real logos (no Windows flag, no brand names).
Do NOT leave hard jagged cutout edges.
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
* NO sky replacement
* NO bubbles
* NO chrome type
* NO sparkles
* NO lens flare
* NO cutouts
* NO glow
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
Do NOT begin the Y2K chrome / Frutiger Aero transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – Y2K CHROME / FRUTIGER AERO STYLING (AFTER MY CONFIRMATION ONLY)
Style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation.
Apply every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT restyle a whole shot from one keyframe.
Plan the sections first and list them to me (frame range, background: Vista sky or aqua room, chrome word, window title) before generating.
Keep the sky, hill, window and chrome word identical within a section; move bubbles and sparkles along continuous per-frame paths. If Seedream cannot keep the chrome word consistent, generate the background + people frames with Seedream and composite one locked chrome-word layer on top.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose or the style rules broke — regenerate those frames only.
The final video must feel like a GLOSSY 2000s TECH DREAM: clean sky, shiny glass, liquid chrome, sparkles and light.
The image should deliberately contain:
* refraction inside the bubbles
* iridescent rims
* specular highlights everywhere light hits
* soft bloom
* lens flare
* gentle glow around the people.
Avoid anything dirty, flat or matte.
```
