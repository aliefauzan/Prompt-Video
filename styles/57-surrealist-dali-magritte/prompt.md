# 57 — Surrealist (Dalí / Magritte)

**Look:** The people stay exactly as filmed, photographic and sharp, but the room around them is gone. They now stand in an endless golden desert under a vast cloud-streaked sky, with a low horizon, a strip of distant sea and sunlit cliffs. Melting pocket watches drape over a dead branch, a stone plinth and the sand, as in Dalí's *The Persistence of Memory*. A rock castle, green apples and a bowler hat float in the air as in Magritte. A freestanding wall whose face is a patch of cloudy sky stands in the desert, a Magritte sky-wall. Late low sun throws long, hard, raking shadows across the sand, and the whole picture has the smooth varnished finish of an oil painting on canvas.

**Also called / where it trends:** "Surrealism" (frameloop.ai style name), "Dalí style", "Magritte style", "surrealist desert", "melting clocks", "dreamscape surrealism", "persistence of memory edit". It is a classic AI-art preset and a long-running trend on Instagram, TikTok and Pinterest (surreal photo-manipulation accounts, "put me in a Dalí painting" edits, floating-object and sky-door composites).

**References:**
- https://frameloop.ai/visual-styles (screenshot `refs/ref_1.png`; the style's sample image `refs/ref_2.png`): the **Surrealism** style card. Its style prompt, credited to frameloop.ai and expanded into the workflow below: *"Surrealist art style, dreamlike composition, bizarre juxtaposition of elements, melting realities, illogical scenarios, distorted perspectives, symbolic imagery, hyper-realistic rendering applied to impossible subjects, ethereal lighting, vast desert landscapes or infinite horizons, inspired by Salvador Dalí and René Magritte."*
- https://en.wikipedia.org/wiki/The_Persistence_of_Memory (screenshot `refs/ref_3.png`): Salvador Dalí, *The Persistence of Memory* (1931). Melting watches on a branch, a plinth and the ground, a golden coastal landscape with Cap de Creus cliffs, and long shadows. Collection: https://www.moma.org/collection/works/79018
- https://en.wikipedia.org/wiki/The_Son_of_Man (screenshot `refs/ref_4.png`): René Magritte, *The Son of Man* (1964). A bowler hat and a floating green apple against a low wall, sea and cloudy sky, painted in a flat, deadpan, hyper-real style.
- https://theartssociety.org/arts-news-features/understand-these-surrealist-symbols: The Arts Society, "Understand these Surrealist symbols" (melting clocks, apples, bowler hats, sky, eggs).
- René Magritte, *The Castle of the Pyrenees* (1959) and *The Empire of Light* series: the floating rock castle and sky painted where it does not belong.

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049), `example.mp4` (the whole clip at 12 fps with the original audio) and `preview.webp`. This is a local approximation made with `render.py` (numpy + OpenCV + the person masks). A procedural world replaces everything outside the masks: a low horizon at 60% height, a gradient sky with soft noise clouds that drift slowly, rippled golden sand, cliffs and a sea strip. It places a Magritte sky-wall, a stone plinth and a dead branch. Five melting watches (drawn, then warped downward) sit on the branch, plinth, sand, a floating rock and the wall top, and their hands creep forward. A floating rock castle, apples and a bowler hat bob gently with soft shadows on the sand. The people get a long sheared shadow raking across the ground, a warm key from the left and slight smoothing. It finishes with canvas weave, warm varnish and a vignette.

## Prompt

```text
I'm uploading one video clip. Convert it into a SURREALIST DALÍ / MAGRITTE frame-by-frame animation: every frame should look like a hyper-real surrealist oil painting in which the real people stand in an infinite dream desert, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Surrealist art style, dreamlike composition, bizarre juxtaposition of elements, melting realities, illogical scenarios, distorted perspectives, symbolic imagery, hyper-realistic rendering applied to impossible subjects, ethereal lighting, vast desert landscapes or infinite horizons, inspired by Salvador Dalí and René Magritte.
Transform the footage into a surrealist painting built from:
* the REAL PEOPLE, kept exact
* an INFINITE DESERT with a LOW HORIZON, replacing the room completely
* a VAST SKY with soft white clouds
* a distant sea strip and sunlit golden cliffs
* MELTING POCKET WATCHES draped over objects
* FLOATING OBJECTS: a rock castle, green apples, a bowler hat
* a Magritte SKY-WALL: a freestanding wall whose face shows cloudy sky
* a dead tree branch and a stone plinth
* a LOW SUN throwing LONG, HARD shadows across the sand
* smooth, hyper-real OIL PAINT finish with fine canvas texture and warm varnish
The result should feel like someone:
LIFTED THE PEOPLE OUT OF THEIR ROOM
→ SET THEM DOWN IN DALÍ'S DESERT AT GOLDEN HOUR
→ MELTED TIME OVER EVERYTHING AROUND THEM
→ LET MAGRITTE'S OBJECTS FLOAT IN THE AIR
→ PAINTED IT ALL IN SMOOTH HYPER-REAL OIL
→ ANIMATED IT FRAME-BY-FRAME.
CHARACTER — EXACT, PHOTOGRAPHIC, PLACED IN THE DREAM
The people are the ONE real thing in the dream. Keep them exact.
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
Do NOT melt, stretch, distort or merge the people.
Do NOT put objects on, in front of, or growing out of the people.
Do NOT turn them into statues, paintings of different people or caricatures.
Only re-light them to match the low desert sun, with a slight smooth painterly finish.
THE WORLD
* The room, furniture, window and walls are replaced completely by the desert world.
* The horizon sits LOW (about 55–62% down the frame), so most of the background is sky.
* Sand: warm ochre and gold, with soft ripples, fading into haze toward the horizon.
* Sky: deep blue at the top fading to pale warm cream at the horizon, with soft, sculpted white clouds.
* A thin strip of calm blue sea and golden cliffs sit on the horizon to one side.
* The world is empty, still and silent: no people, animals, buildings or roads other than the listed objects.
MELTING WATCHES
* 4–5 soft, melting pocket watches: gold or silver case, cream dial, black numerals and hands.
* They drape like cloth over edges: a dead branch, the edge of a stone plinth, the top of the sky-wall, the edge of a floating rock, and one lying flat on the sand.
* The hands move slowly forward over the clip, very slowly.
* They stay in the same places for the whole clip.
FLOATING OBJECTS AND MAGRITTE ELEMENTS
* A floating rock with a small castle on top, high in the sky.
* 2–3 green apples floating at different heights.
* A black bowler hat floating in the air.
* Each floating object bobs gently up and down by a few pixels and casts a soft shadow on the sand far below.
* A freestanding wall stands in the desert; its face is painted as cloudy sky, as if a piece of the sky were cut out and stood up.
* All objects sit in the GAPS between the people; none crosses a face or body.
LIGHT AND SHADOWS
* One low, warm sun from the side (the same side in every frame).
* Every person and object casts a LONG, HARD, dark shadow raking across the sand away from the sun.
* The people's shadows follow their movement exactly.
* Light is clear, warm and ethereal; shadows are cool and sharp-edged.
PAINT FINISH
* The whole frame looks like a smooth, hyper-real oil painting: no visible brush strokes, very fine canvas weave, slight warm varnish.
* A gentle vignette darkens the corners.
PALETTE
Ochre, gold, sand, burnt sienna, warm cream, cerulean and deep blue sky, white clouds, the green of the apples, black hat, gold watch cases.
Do NOT use neon colours or a cool modern grade.
OBJECT CONTINUITY
If the character holds an object, it stays exact and attached to the hand; it does not melt.
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
Their shadows move with them.
The world is a fixed stage: the horizon, wall, plinth, branch and watches never move.
NO object jumping position between frames.
NO world redesign from one frame to the next.
FRAME-TO-FRAME DREAM LIFE
THIS IS CRITICAL.
It must feel like a slow, living dream, not a still collage.
Allow between consecutive frames:
* clouds to drift slowly sideways
* floating objects to bob gently
* watch hands to creep forward
* a very slight shimmer in the canvas texture
Keep FIXED:
* the horizon height
* the layout of the world and every object
* the sun direction and shadow direction
* the paint finish and palette
DO NOT
Do NOT keep any part of the original room.
Do NOT melt, warp or distort the people.
Do NOT cover faces or bodies with objects.
Do NOT put a different face or a painted face on the people.
Do NOT make it a cartoon, a flat collage or a cheap cut-out.
Do NOT add random fantasy creatures, spaceships or modern objects.
Do NOT change the world layout between frames.
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
* NO background replacement
* NO desert, sky, watches or floating objects
* NO shadows or paint finish
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
Do NOT begin the surrealist transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – SURREALIST DALÍ / MAGRITTE STYLING (AFTER MY CONFIRMATION ONLY)
First, describe the world layout to me: horizon height, sun side, where the sky-wall, plinth and branch stand, where each melting watch lies and where each floating object hangs, checked against the gaps between the people across the whole clip.
Then style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation, so the people are exactly that frame.
Apply every style rule above, with the SAME world layout in every frame.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing, shadows or the world layout broke — regenerate those frames only.
The final video must feel like THE REAL PEOPLE WALKED INTO A DALÍ / MAGRITTE PAINTING: an endless desert, melting clocks, floating apples and hat, a sky-wall, long hard shadows, 12 frames per second.
The image should deliberately contain:
* the people, exact and photographic
* an infinite desert with a low horizon and vast cloudy sky
* melting pocket watches
* floating objects
* a Magritte sky-wall
* long, hard raking shadows
* a smooth varnished oil-paint finish.
Avoid a cut-and-paste collage look.
```
