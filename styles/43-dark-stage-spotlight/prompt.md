# 43 — Dark Stage Spotlight

**Look:** The "Dark Stage" portrait. The room disappears into a black void. Each person is lit by one hard key light from high camera-left, so faces carve out of the dark with deep shadow on the far side. Light falls off fast toward the floor. A thin rim catches the shadow-side edge, and a faint haze beam hangs in the black. There are three lighting sections: a classic white softbox, a colour-gel look (blue shadows, amber rim), and warm Rembrandt gold.

**Also called / where it trends:** "Dark Stage effect", "#darkstageeffect", "dark stage portrait", "AI dark portrait", "spotlight in the void", "black background studio portrait". It is the October 2026 TikTok and Instagram AI-photo trend, with top posts at about 1.6M views. Prompt guides list rim-light, colour-gel and Rembrandt variants.

**References:**
- https://www.tiktok.com/discover/dark-stage-effect (`refs/ref_1.png`): TikTok discover page "Dark Stage Effect" (screenshot cropped to the post grid). Posts on it:
  - https://www.tiktok.com/@marina_199199/video/7660562291175263510: @marina_199199, 67.2K likes, about 1.6M views.
  - https://www.tiktok.com/@jimmy.zakariyah/video/7662461405471231246: @jimmy.zakariyah, 168.6K views.
  - https://www.tiktok.com/@meredith0869/video/7658503607553182998: @meredith0869, how-to tutorial.
  - https://www.tiktok.com/@tammypark2/video/7660537691049692438: @tammypark2.
- https://randomprompts.org/blog/ai-dark-stage-effect-guide-tiktok-viral-dark-portrait-2026: Dark Stage prompt guide. Rules taken from it: pure black background, a single key light at 45°, deep shadows, rim / colour-gel / Rembrandt variants, the #darkstageeffect tag.
- https://miraflow.ai/blog/ai-dark-stage-effect-prompts-2026: Dark Stage prompt pack (spotlight, haze, gel variants).
- https://phototrend.me/trends/dark-stage-portrait/: trend page for the dark stage portrait.
- https://videosprompt.org/blogs/viral-ai-video-trends-october-2026: lists Dark Stage among the October 2026 viral AI trends.
- https://scripthooks.ai/blog/weekly-trends-october-11-2026: weekly trend roundup (week of 11 Oct 2026).

**Example:** `example.png` (six frames of the test clip) and `before_after.png` (frame 049). This is a local approximation made with `render.py` (numpy + OpenCV). The people are cut out with the matte, and their edge colours are cleaned so no bright wall bleeds in. They are relit with a wrap-Lambert key from a dome normal map plus the frame's own luminance. Light falls off toward the floor and the sides. A rim appears only on edges facing away from the key. The room is crushed to near black with a slow haze beam. Vignette and grain are added per frame. There are three sections: softbox, gel, Rembrandt gold. Frames whose matte breaks under motion blur (023, 068) borrow the area that both neighbouring mattes agree on.

## Prompt

```text
I'm uploading one video clip. Convert it into a 12 FPS DARK STAGE / SINGLE-SPOTLIGHT PORTRAIT frame-by-frame animation, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
Seedream works here because each frame is a relight of the same source frame; no video model is needed.
CORE VISUAL STYLE
Every frame looks like a portrait shot on a black stage:
* the room gone, replaced by a pure black void
* ONE hard key light from high camera-left, about 45°
* faces carved out of the dark: lit cheek, deep shadow on the far side
* fast light falloff toward the feet and the frame edges
* a thin rim light on the shadow-side edge of hair and shoulders
* a faint haze beam from the key hanging in the black
* deep, clean blacks; no fill light
* fine film grain and a soft vignette
It should look like the viral TikTok "Dark Stage" effect: a photo-studio portrait in a black void.
The result should feel like someone:
PUT THE PEOPLE ON AN EMPTY BLACK STAGE
→ KILLED EVERY LIGHT BUT ONE SPOT
→ ADDED A THIN RIM FROM BEHIND AND A LITTLE HAZE
→ SHOT IT AT 12 FRAMES PER SECOND
→ ANIMATED IT FRAME-BY-FRAME.
LIGHT AND PALETTE RULES
The background is black (#000000 to #080808), never grey.
The key light is the brightest thing in the frame.
Lit skin keeps its natural colour; shadow skin falls to near black.
The contrast ratio between lit and shadow sides is high (about 8:1).
Light falls off fast below the chest.
Each section has one light colour scheme (see SECTIONS).
CHARACTER — PHOTOGRAPHIC, RELIT
The people stay PHOTOGRAPHIC; only the lighting changes.
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
Do NOT turn them into a painting or a silhouette.
The lit side of every face must stay readable.
SKIN, HAIR AND CLOTHES UNDER THE KEY
Skin keeps its texture and real tone where the light hits.
Hair catches the rim as a thin bright line.
Clothes keep their colours and patterns, darkened by the falloff.
Glasses may catch one small hard highlight.
Do NOT smooth or beautify skin.
BACKGROUND
Remove the room: walls, windows, plants, screens and furniture all go to black.
Only a faint haze beam from the key and the softest floor glow may show.
Edges of the people must be clean: no bright halo, no leftover wall colour.
SECTIONS
Split the clip into 3 sections of roughly equal length:
* Section 1, CLASSIC SOFTBOX: white key, white rim, neutral blacks.
* Section 2, COLOUR GEL: key a little cooler, shadows tinted deep blue, warm amber rim.
* Section 3, REMBRANDT GOLD: warm golden key, a small light triangle on the shadow cheek, warm rim.
The key direction stays the same in every section.
FRAME-TO-FRAME BEHAVIOUR (BOIL RULES)
THIS IS CRITICAL.
The light is a fixed lamp on a stand: it does NOT move between frames.
The people move through the light, so their lit and shadow areas follow the real motion.
Allow between consecutive frames:
* grain to change
* the haze to drift slowly
Keep FIXED within a section:
* key direction and colour
* rim colour
* background black level
OBJECT CONTINUITY
If the character holds or touches an object (phone, cup, bag, microphone), it is lit by the same key and stays in place.
Do NOT drop it into the black.
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
Every person must match the source frame exactly in position, pose and timing.
Do NOT invent motion that is not in the footage.
DO NOT
Do NOT keep the room visible.
Do NOT use a grey or gradient studio backdrop.
Do NOT add a second key light or a flat fill light.
Do NOT outline every edge with rim light.
Do NOT add lens flares, sparkles or smoke clouds.
Do NOT add stage props, curtains or a floor.
Do NOT beautify or smooth faces.
Do NOT redraw or illustrate the people.
Do NOT create new poses.
Do NOT change anatomy.
Do NOT change clothing.
Do NOT replace the person's face.
Do NOT interpolate new in-between frames.
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
* NO relighting
* NO black background
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
Do NOT begin the dark-stage transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – DARK STAGE STYLING (AFTER MY CONFIRMATION ONLY)
First, plan the sections and list them for me: frame range, key colour, rim colour and shadow tint for each section.
Then style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Give Seedream the current extracted frame as the image input, plus the first styled frame of its section as a lighting reference so the lamp stays in the same place.
Apply every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing, light direction or the style rules broke — regenerate those frames only.
The final video must feel like a DARK STAGE PORTRAIT IN MOTION: the people carved out of a black void by one hard spotlight, 12 frames per second.
The image should deliberately contain:
* a pure black void
* one hard key from high left
* deep shadows on the far side of every face
* fast falloff toward the floor
* a thin rim on the shadow side
* a faint haze beam
* fine grain and a soft vignette.
Avoid polished digital perfection.
```
