# 88 — Persona 5 Red-Black Cutout UI

**Look:** The clip becomes a stylish JRPG menu screen in three colours: hot red, black and white. The room is reduced to a two-tone red-and-black graphic with halftone dot fades. Black jagged lightning shards and small stars hang behind the people. Each person is a flat, high-contrast black/grey/white cutout with a thick white paper-cut rim, a black rim outside it and an offset red drop shadow. Slanted, torn UI panels slam over the frame: a date box, a stacked command menu whose highlight jumps every second, and a caption, all in ransom-note lettering where every letter has its own font, size, tilt and box colour. The UI shivers a little every frame, and heads always stay in front of it.

**Also called / where it trends:** "Persona 5 style", "P5 UI", "Phantom Thieves aesthetic", "ransom-note UI", "Persona 5 menu edit", "calling card style". It runs as a fan-edit and motion-design trend on Instagram (#persona5style), Pinterest UI boards and TikTok, and UI/UX writers often cite it as the benchmark for kinetic game UI (see the design analyses below).

How it differs from nearby styles: **31 Sin City Noir Red** is a black-and-white photograph with one red accent, and **49 Chaotic Red Ink** is ink splatter. This style is flat graphic UI geometry: slanted torn panels, ransom-note type, cutout rims, halftone and stars. The people are posterised flat tones, not photographic grey. It is also unlike **01 Punk Photocopy Collage**, which is xerox grain and marker on paper; this is clean, digital, game-menu red/black/white.

**References:**
- https://www.pinterest.com/search/pins/?q=persona%205%20ui%20style (screenshot `refs/ref_1.png`, from the D2 sweep). Menu sheets: slanted red/black/white command lists, ransom-note lettering, lightning shards, cutout characters on red.
- https://www.instagram.com/popular/persona-5-style/ (D2 sweep): Instagram tag page.
- https://personacentral.com/persona-5-panel-concept-development-ui/: Atlus panel on the concept behind the UI (stylish, dynamic, red/black).
- https://personacentral.com/persona-5-interview-ui-design-sound-music/: developer interview on the UI design.
- https://ridwankhan.com/the-ui-and-ux-of-persona-5-183180eb7cce: "The UI and UX of Persona 5", a breakdown of the slanted menus, motion and typography.
- https://www.cookandbecker.com/en/article/137/persona-5-s-bombastic-art-direction.html: Cook and Becker, "Persona 5's Bombastic Art Direction".
- https://segaretro.org/images/d/d0/Persona5_StyleGuide.pdf: the published style guide (palette, type, layout rules).

**Example:** `example.png` shows six frames of the test clip and `before_after.png` shows frame 049. `example.mp4` is the whole clip at 12 fps with the original audio, and `preview.webp` is an animated preview. This is a local approximation made with `render.py` (numpy + OpenCV + Pillow + the person masks). The room is thresholded into red / dark red / black with a black halftone fade in two corners. Fixed black lightning shards and spinning stars sit behind the people and jitter a few px per frame. People are bilateral-smoothed and posterised to three tones, then given a 23 px white rim, a black rim and an offset red shadow from the dilated masks. The UI is drawn as original shapes, not game assets. Jagged slanted panels carry ransom-note text built letter by letter from 11 system fonts: "10/18 SUN / AFTER SCHOOL", a TALK / PARTY / SKILL / ITEM / SYSTEM menu whose highlight cycles every 12 frames, and "SHOW TIME!". The date box slides along the top edge to where no head is, smoothed over time. The top 260 px of every silhouette is re-composited over the UI, so faces are never covered.

## Prompt

```text
I'm uploading one video clip. Convert it into a PERSONA-5-STYLE RED-BLACK CUTOUT UI frame-by-frame animation: every frame should look like a stylish JRPG menu screen in hot red, black and white, with the people as graphic cutouts and slanted ransom-note UI panels slamming over the frame, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Transform the footage into a bold game-menu graphic built from:
* a STRICT three-colour palette: HOT RED, BLACK, WHITE (plus one mid grey)
* the room as a flat RED-and-BLACK two-tone graphic
* black HALFTONE DOT fades in the corners
* black jagged LIGHTNING SHARDS and small STARS behind the people
* people as FLAT high-contrast black / grey / white CUTOUTS
* a thick WHITE paper-cut rim, then a BLACK rim, then an offset RED drop shadow around every person
* SLANTED, TORN UI PANELS (parallelograms with jagged corners) in black, white and red
* RANSOM-NOTE lettering: every letter cut from a different font, size and tilt, each in its own little box
* a date box, a stacked command menu with a highlighted entry, and a slanted caption
The result should feel like someone:
SHOT THE CLIP
→ CUT EVERY PERSON OUT AS A HIGH-CONTRAST STICKER
→ SLAPPED THEM ON A RED-AND-BLACK GRAPHIC STAGE
→ CUT LETTERS OUT OF MAGAZINES FOR THE MENU TEXT
→ LAID SLANTED TORN PANELS OVER EVERYTHING
→ ANIMATED THE UI FRAME-BY-FRAME LIKE A GAME MENU.
CHARACTER — FLAT HIGH-CONTRAST CUTOUT
Each person becomes a flat graphic cutout in three tones: BLACK, MID GREY, WHITE.
Preserve the person's exact:
* identity
* face
* expression
* hairstyle
* glasses
* clothing and its pattern
* accessories
* pose
* body proportions
* movement
* hand position
* interaction with objects
Faces: the eyes, brows, glasses, nose shadow and mouth must stay readable in the three tones.
Hair: solid black mass with one white highlight shape.
Clothing: posterised into the same three tones; stripes and batik stay visible as flat shapes.
Do NOT keep photographic grey gradients; tones are flat.
Do NOT turn the people into anime drawings.
CUTOUT LAYERING
Around each person, in this order from inside out:
* a thick WHITE paper-cut rim (about 1.5% of frame height)
* a BLACK rim outside it
* a RED drop shadow offset down-right
The rims follow the silhouette exactly and update every frame.
BACKGROUND — RED-BLACK STAGE
* Keep the room's layout, but render it as flat graphic tones: light areas → HOT RED, mid areas → DEEP RED, dark areas → BLACK.
* Add black halftone dot fades in two opposite corners.
* Add 3–4 large black jagged lightning-bolt shards and 4–6 small stars (white or black) behind the people.
* Shards and stars keep their positions but jitter a few pixels from frame to frame.
UI PANELS + TYPOGRAPHY
* All panels are slanted (about 7–12°) parallelograms with torn, jagged corners.
* DATE BOX along the top edge: a black panel with a big ransom-note date (e.g. "10/18"), a red tab with the weekday ("SUN"), and a small line under it ("AFTER SCHOOL"). It slides along the top edge so it never sits behind or over a face.
* COMMAND MENU, bottom-right: a stack of 5 slanted entries (TALK / PARTY / SKILL / ITEM / SYSTEM). The highlighted entry is a bigger white panel on a red underlay; the others are black. The highlight moves to the next entry about once per second.
* CAPTION, bottom-left: a big slanted ransom-note phrase (e.g. "SHOW TIME!") on a black panel over a red underlay.
* RANSOM-NOTE text: every letter in a different typeface (heavy sans, serif, typewriter, condensed, italic), size and tilt, each in its own box: white on black, black on white, red on black or white on red.
* Use original wording and shapes only.
* Heads always stay IN FRONT of the UI; panels may overlap bodies but never faces.
PALETTE
Hot red (#E6121E), deep red, black, white, one mid grey for the people.
Do NOT add any other colours: no blue, yellow, skin tone or photo colour.
OBJECT CONTINUITY
If the character holds an object, it becomes part of the same three-tone cutout, inside the rims, attached to the hand.
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
The cutouts must match the source frame exactly.
If the head moves, the cutout and rims follow.
If the hand moves, the cutout and rims follow.
NO frozen previous-frame silhouette.
NO rim lagging behind the body.
FRAME-TO-FRAME UI LIFE
THIS IS CRITICAL.
It must feel like a live game menu, not a static poster.
Allow between consecutive frames:
* every ransom-note letter to wobble by 1–2° and a pixel or two
* panels and shards to jitter by a few pixels
* stars to spin slowly
* the menu highlight to jump to the next entry about once per second
Keep FIXED:
* the palette
* each letter's font and box colour
* the layout of the date box, menu and caption
* the rim widths
DO NOT
Do NOT copy any game logo, character art, calling card or UI asset; draw original shapes and lettering that evoke the style.
Do NOT use photographic colour or grey photographic gradients on the people.
Do NOT use ink splatter, paint texture or photocopy grain.
Do NOT use neon glow, chrome or gradients on the UI.
Do NOT place any panel or text over a face.
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
* NO red-black grade
* NO cutouts or rims
* NO UI panels or lettering
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
Do NOT begin the red-black cutout UI transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – RED-BLACK CUTOUT UI STYLING (AFTER MY CONFIRMATION ONLY)
First, give me the UI plan: the date-box text, the five menu entries and when the highlight moves, the caption text, and where the shards and stars sit. Keep it fixed for the whole clip.
Then style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation, so the people are exactly that frame.
Apply every style rule above, with the SAME palette, lettering and layout on every frame.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing, palette, lettering or face clearance broke — regenerate those frames only.
The final video must feel like A STYLISH RED-BLACK GAME MENU COME TO LIFE: high-contrast cutout people with white and black rims and red shadows, slanted torn panels, ransom-note letters, lightning shards and stars, 12 frames per second.
The image should deliberately contain:
* hot red, black and white only
* flat three-tone cutout people
* white + black rims and a red offset shadow
* slanted jagged UI panels
* ransom-note mixed-font lettering
* halftone dots, lightning shards and stars.
Avoid photographic colour and soft gradients.
```
