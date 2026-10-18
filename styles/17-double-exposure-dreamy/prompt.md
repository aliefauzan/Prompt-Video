# 17 — Double Exposure Dreamy

**Look:** classic in-camera / Photoshop double exposure, animated. Each person becomes a high-key, warm-mono portrait on an airy off-white ground, and a SECOND IMAGE — misty pine forest, sunset clouds, dusk city skyline or layered mountain ridges — is screened into their silhouette. Faces stay clear and photographic; hair, shoulders and clothes dissolve into the landscape. The second exposure drifts slowly inside the silhouette, birds and mist move, windows flicker. Finished with soft bloom, red-orange film halation, a drifting light leak and fresh film grain on every frame.

**Also called / where it trends:** "double exposure edit", "silhouette fill", "dreamy double exposure", "multiple exposure", "forest-in-silhouette", "sunset silhouette edit", "ethereal portrait" — CapCut and TikTok template trend (#doubleexposure, "double exposure effect"), Instagram Reels tutorials (2026), Pinterest boards, AI-photo prompt sites; the look of the True Detective title sequence and album/poster art.

**References:**
- https://www.pinterest.com/search/pins/?q=double%20exposure%20portrait%20dreamy%20clouds%20silhouette — screenshot `refs/ref_1.png`: profile and full-body silhouettes filled with clouds, forest, sunset; white grounds; dissolving edges
- https://www.capcut.com/explore/tiktok-double-exposure-effect — CapCut double-exposure templates / how-to for TikTok
- https://www.tiktok.com/@kevkevkiwi/video/7648478637317983510 — TikTok double-exposure video edit tutorial (June 2026)
- https://www.tiktok.com/discover/double-exposure-effects — TikTok discover hub for double-exposure edits (Oct 2026)
- https://www.instagram.com/reel/DZAeiVdqZT6/ — IG Reel double-exposure edit (June 2026)
- https://sandyeditz.in/new-trending-double-exposer-style-photo-editingreelg370sandyeditz/ — "new trending double exposure" editing reel (Jul 2026)
- https://capleez.com/double-exposure-ai-photo-editing-prompts/ — AI double-exposure prompts (2026)
- https://www.youtube.com/watch?v=Jf-p6yc__Y0 — double-exposure effect tutorial

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049). Local approximation rendered with `render.py` (numpy + OpenCV + person masks, with a head-finder that keeps the faces); 22 frames in `frames/`.

## Prompt

```text
I'm uploading one video clip. Convert it into a dreamy DOUBLE EXPOSURE frame-by-frame animation matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Transform the footage into a soft, poetic, classic DOUBLE EXPOSURE built from:
* each person as a HIGH-KEY, warm MONOCHROME portrait
* an airy OFF-WHITE / cream ground (no busy background)
* a SECOND IMAGE blended INSIDE each person's silhouette (screen / lighten blend)
* second images: misty PINE FOREST, SUNSET CLOUDS, DUSK CITY SKYLINE, layered MOUNTAIN RIDGES
* FACES kept clear; hair, shoulders and clothes DISSOLVE into the landscape
* soft feathered edges that melt into the ground
* the landscape bleeding faintly past the silhouette at the bottom
* soft bloom
* red-orange FILM HALATION around bright-dark edges
* a warm drifting LIGHT LEAK
* fine analogue FILM GRAIN
The result should feel like someone:
SHOT THE PEOPLE ON A ROLL OF FILM
→ REWOUND IT
→ EXPOSED THE SAME FRAMES AGAIN ON A FOREST, A SUNSET, A CITY AT DUSK
→ LET THE LIGHT BLEED
→ SCANNED IT SOFT AND WARM
→ ANIMATED IT FRAME-BY-FRAME.
CHARACTER — HIGH-KEY MONO PORTRAIT
The MAIN HUMAN SUBJECT stays PHOTOGRAPHIC.
Preserve the person's exact:
* identity
* face
* expression
* hairstyle
* clothing silhouette
* accessories
* pose
* body proportions
* movement
* hand position
* interaction with objects
Do NOT redraw the character.
Do NOT turn them into a painting, cartoon or anime.
Do NOT replace the face.
Grade the person as a soft high-key portrait:
* near-monochrome with a warm cream / sepia tone
* faces bright, clean and well exposed, with a hint of natural skin colour
* clothes and hair pushed DARKER so the second image fills them
* gentle contrast, no crushed blacks
THE SECOND EXPOSURE
THIS IS THE KEY SIGNATURE.
Blend ONE landscape per section into the silhouette using a SCREEN / LIGHTEN blend:
* where the portrait is dark (hair, clothes, shoulders), the landscape shows
* where the landscape is bright (sky, mist, clouds), the figure fades towards white
* where the landscape is dark (trees, buildings, ridges), its shapes read clearly inside the body
Place the landscape so its HORIZON sits around the shoulders / chest:
* sky, mist or clouds around the head
* trees, buildings or mountain ridges rising up through the torso
Landscapes:
* MISTY PINE FOREST: rows of pine silhouettes from pale grey-teal (far) to near-black (near), fog bands between rows, a small flock of birds
* SUNSET CLOUDS: dusty violet-blue top → rose → peach horizon, soft clouds with lavender undersides, a warm sun glow
* DUSK CITY SKYLINE: violet-blue sky → peach horizon, layered dark building silhouettes, warm lit windows
* MOUNTAIN RIDGES: 3–4 receding ridges from pale blue to deep blue-grey, mist pooling in the valleys, birds
FACES STAY CLEAR
IMPORTANT:
Every face (eyes, nose, mouth, glasses) stays readable and photographic in every frame.
Let only a faint, tinted veil of the landscape pass over the face.
Feather the face area smoothly into the landscape; no hard oval, no visible mask edge.
SOFT EDGES + BLEED
The silhouette edges are soft and slightly dissolving, not a hard cut-out.
A little of the landscape (only its darker shapes) bleeds past the silhouette and fades into the cream ground, especially near the bottom of the frame.
GROUND
For most sections: a clean, warm OFF-WHITE / cream ground with a soft vignette.
ORIGINAL ENVIRONMENT OPTION
For selected sections, keep a FADED GHOST of the original room (about 20% opacity, desaturated, lifted to near-white) behind the figures.
This keeps the original composition while staying in the style.
FILM FINISH
* soft BLOOM on highlights
* red-orange HALATION glow along bright-dark edges (film-style)
* one warm orange-pink LIGHT LEAK drifting along a frame edge
* fine FILM GRAIN, new on every frame
* very slight softness, like a scanned film frame
PALETTE RULES
Ground: warm off-white / cream.
Portrait: warm monochrome with a hint of skin colour on faces.
Landscape colours carry the section: teal-grey forest, rose-peach sunset, violet dusk city, blue-grey mountains.
Accents: red-orange halation, peach light leak.
Do NOT introduce neon, harsh saturated colours or pure black backgrounds.
Everything should feel soft, airy, nostalgic and calm.
LAYER ORDER
A typical composition reads:
CREAM GROUND (or faded ghost room)
↓
FAINT LANDSCAPE BLEED (darks only)
↓
HIGH-KEY MONO PORTRAIT
↓
SECOND EXPOSURE SCREENED INTO THE SILHOUETTE
↓
FACES RESTORED (soft feathered)
↓
BLOOM + HALATION
↓
LIGHT LEAK
↓
FILM GRAIN.
OBJECT CONTINUITY
IMPORTANT:
If the character is interacting with an object, preserve that object in the silhouette.
Examples:
* phone
* headphones
* bag
* chair
* cup
* microphone
If the object is essential to the person's action, include it within the silhouette.
Do NOT accidentally remove it while isolating the person.
CHARACTER CONTINUITY LOCK
The SAME person must remain recognizable in every frame.
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
The underlying character movement must remain exactly faithful to the source footage.
The landscape lives INSIDE the moving silhouette.
The HUMAN MOTION does NOT change.
If the head moves:
the face area and silhouette follow.
If the hand moves:
the silhouette (and the landscape inside it) follows.
If the body turns:
the silhouette updates.
If the character interacts with an object:
the object moves exactly with the original action.
NO floating silhouette.
NO previous-frame silhouette.
NO landscape stuck to the screen while the person moves out of it.
FRAME-TO-FRAME MOTION
THIS IS CRITICAL.
The double exposure is ALIVE but calm:
* the landscape pans very slowly sideways inside the silhouette, near layers faster than far layers (parallax)
* mist and clouds drift
* birds glide and flap
* city windows flicker on and off one at a time
* the light leak breathes and slides along the edge
* halation flickers slightly
* film grain is new on every frame
Within a section, keep the SAME landscape (same trees, same skyline, same ridges); only move it.
Do NOT swap the landscape every frame.
DO NOT
Do NOT hide or blur the faces.
Do NOT put the landscape behind the people instead of inside them.
Do NOT make hard paper-cut edges or a visible mask outline.
Do NOT use a black background or a busy background.
Do NOT turn the people into paintings, cartoons or anime.
Do NOT create new poses.
Do NOT change anatomy.
Do NOT change clothing silhouettes.
Do NOT add text, logos or watermarks.
Do NOT make it neon, glossy or cyberpunk.
Do NOT over-saturate.
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
* NO second exposure
* NO landscape blend
* NO silhouette fill
* NO film grain
* NO halation
* NO light leak
* NO ground replacement
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
Do NOT begin the double exposure transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – DOUBLE EXPOSURE STYLING (AFTER MY CONFIRMATION ONLY)
Style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation.
Apply every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT restyle a whole shot from one keyframe.
Plan the sections first and list them to me (frame range, landscape, ground: cream or ghost room) before generating.
Keep the same landscape within a section and only pan it slowly; check every frame that all faces are still clear. If Seedream cannot hold the landscape steady, generate one landscape plate per section and screen it into the person matte of each frame instead.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose or the style rules broke — regenerate those frames only.
The final video must feel like a DREAM ON FILM: two exposures on one frame, soft and warm, with the world living inside the people.
The image should deliberately contain:
* clear, gentle faces
* landscapes dissolving through hair and clothes
* soft feathered edges
* bloom and red-orange halation
* a warm light leak
* fine film grain.
Avoid anything hard, flat or digital-looking.
```
