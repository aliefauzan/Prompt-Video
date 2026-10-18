# 65 — Giallo Gel Lighting

**Look:** The office becomes a set from a 1970s Italian giallo thriller. The walls drown in blood-red gel light, the window turns into a cobalt-blue light box, and the screen and plants glow emerald green. The edges of the frame fall to crushed black. Each person is lit by two hard gels, red from one side and cobalt blue from the other, with a sharp colour line running down every face. A diffusion-filter glow, warm 35 mm grain and a slight gate weave finish the frame.

**Also called / where it trends:** "giallo", "giallo aesthetic", "Argento lighting", "Suspiria lighting", "Bava colour", "70s Italian horror look", "red and blue gel lighting". Morphic and other AI-video tools list it as a named aesthetic, and it shows up in horror-themed AI video prompts on X and Reddit and in cinematography breakdowns of *Suspiria* (1977), *Blood and Black Lace* (1964) and *Deep Red* (1975).

**References:**
- https://morphic.com/resources/videos/giallo-style-videos (screenshot `refs/ref_1.png`): Morphic's giallo style page from the discovery sweep. It shows magenta and blue gels, rain on cobblestones, a final girl and an opera house.
- https://www.bfi.org.uk/features/hues-out-hell-how-dario-argento-uses-colour (screenshot `refs/ref_2.png`): BFI, "Hues out of hell: how Dario Argento uses colour". Its header still from *Inferno* (1980) shows the hard red/blue split on a face.
- https://theasc.com/article/suspiria-terror-in-technicolor/: American Cinematographer on *Suspiria*'s Technicolor primaries, lit through coloured gels and velvet.
- https://cdn.theasc.com/Suspiria-AC-Complete-Story.pdf: the full American Cinematographer story on Luciano Tovoli's lighting.
- https://cinergie.unibo.it/article/download/7375/7097/22286: academic paper on the expressionist colour palette and set design of *Suspiria*.
- https://theasc.com/article/nightmare-fuel/: ASC cinematographers on creating eerie images with colour.

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049), `example.mp4` (the whole clip at 12 fps with the original audio) and `preview.webp`. This is a local approximation made with `render.py` (numpy + OpenCV + the person masks). The background keeps only its shading. It is relit red, with the bright low-saturation window mapped to cobalt blue, the screen and plants to emerald, and a light pool that falls to black at the edges. Each body's red/blue split comes from the slope of a heavily blurred person mask, so the left flanks face a red gel and the right flanks a blue one, with a narrow amber key between. On top are a contrast curve with crushed blacks, a diffusion glow, warm grain, a heavy vignette and ±1 px of gate weave. Unlike 55 Cyberpunk Neon City, it has no signage, rain or magenta/cyan neon: it uses primary red, blue and green theatre gels and 70s film texture.

## Prompt

```text
I'm uploading one video clip. Convert it into a GIALLO GEL LIGHTING frame-by-frame animation: every frame should look like a still from a 1970s Italian giallo thriller, lit only by saturated red, blue and green theatre gels, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
1970s Italian giallo film still, Dario Argento and Mario Bava colour, hard coloured gel lighting, saturated primary reds, blues and greens, crushed blacks, diffusion filter, 35mm film grain.
Transform the footage into a giallo frame built from:
* BLOOD-RED gel light flooding the walls
* COBALT-BLUE light through the window
* EMERALD-GREEN accents (screens, plants, small practicals)
* a HARD TWO-GEL SPLIT on every person: RED from one side, BLUE from the other
* a sharp colour line down the middle of each face
* a thin AMBER key where the two gels meet
* CRUSHED BLACKS: the edges and corners of the room fall into darkness
* pools of coloured light, not even illumination
* high contrast
* a soft DIFFUSION-FILTER glow around bright areas
* warm, visible 35mm GRAIN
* a heavy vignette
The result should feel like someone:
TURNED OFF EVERY NORMAL LIGHT
→ PUT RED GELS ON THE LAMPS LEFT OF EACH ACTOR
→ PUT BLUE GELS ON THE LAMPS TO THE RIGHT
→ FLOODED THE WALLS IN RED AND THE WINDOW IN BLUE
→ SHOT IT ON 1970s 35MM THROUGH A DIFFUSION FILTER
→ RELEASED IT FRAME-BY-FRAME.
CHARACTER — PHOTOGRAPHIC, GEL-LIT
The people stay PHOTOGRAPHIC: real faces, filmed, relit.
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
Do NOT turn them into a painting, cartoon or 3D render.
Do NOT add blood, wounds, weapons, masks or horror make-up.
Do NOT add gloves, coats or props.
GEL LIGHTING ON THE PEOPLE
* Each person has their OWN split: red on their left side (screen left), blue on their right side (screen right).
* The split runs down the face, neck and body following its shape: the side of the face turned toward the red lamp is red, the side turned toward the blue lamp is blue.
* The transition is HARD and narrow, with a thin warm amber band where the two meet.
* Facial features stay readable: eyes, nose, mouth and glasses keep their shape and shading inside the colour.
* Clothing takes the same split; stripes and patterns stay visible.
* Skin colour is replaced by the gel colours; it is not natural skin tone.
THE SET
* The room stays the same room, same layout.
* Walls: deep, saturated blood red, brighter in the middle, darker toward the edges.
* Window: a glowing cobalt-blue panel, as if moonlight or a blue lamp is behind it.
* Screens and plants: emerald green.
* Floor, corners and edges: almost black.
* Do not add rain, neon signs, text or new objects.
FILM TEXTURE
* 1970s 35mm: warm grain, slightly soft.
* Diffusion glow (Pro-Mist): bright areas bleed softly into their surroundings.
* Very slight gate weave (the frame drifts by a pixel).
* Heavy vignette.
PALETTE
Blood red, crimson, cobalt blue, ultramarine, emerald green, a little amber, black.
Do NOT use magenta, purple, pink, cyan neon or teal-orange.
OBJECT CONTINUITY
If the character holds an object, it stays attached to the hand and takes the same gel light as the hand.
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
The red/blue split moves WITH each person and follows how they turn.
NO split line frozen in screen space while the person moves through it.
NO swapping sides of red and blue between frames.
FRAME-TO-FRAME FILM LIFE
THIS IS CRITICAL.
It must feel like 1970s film running through a camera, not a still filter.
Allow between consecutive frames:
* grain to change every frame
* a tiny gate weave (about one pixel)
* slight brightness flicker (±3%)
Keep FIXED:
* which side is red and which is blue
* the wall, window and screen colours
* the contrast and vignette
DO NOT
Do NOT use magenta and cyan cyberpunk neon.
Do NOT add rain, neon signage, holograms or city lights.
Do NOT make it black-and-white with red accents.
Do NOT light the scene evenly or with white light.
Do NOT let the colours blend into a muddy purple across faces.
Do NOT add gore, weapons, gloves or horror props.
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
* NO colour grade
* NO gel relighting
* NO diffusion glow or grain
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
Do NOT begin the giallo gel transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – GIALLO GEL LIGHTING STYLING (AFTER MY CONFIRMATION ONLY)
First, tell me which side of each person will be red and which blue, and which parts of the room become red, blue and green.
Then style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation, so the people are exactly that frame.
Apply every style rule above, with the SAME gel layout on every frame.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing, the gel split or colour consistency broke — regenerate those frames only.
The final video must feel like A SCENE FROM A 1970s GIALLO: blood-red walls, a cobalt window, red/blue split light down every face, crushed blacks, film grain, 12 frames per second.
The image should deliberately contain:
* saturated red, blue and green gel light
* a hard red/blue split on each face
* crushed black edges
* diffusion glow
* 35mm grain.
Avoid flat, evenly lit video.
```
