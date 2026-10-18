# 66 — Weirdcore / Dreamcore

**Look:** The clip becomes a re-uploaded, over-compressed internet image that feels like a half-remembered dream. Colours are over-bright and over-saturated with a milky pastel lift. A clip-art blue sky with fluffy clouds is pasted into the window, a rainbow arcs across the room, daisies with human eyes for centres sit in the plant row, and loose eyes float on the wall, drifting and blinking. Small plain-font captions ("WAKE UP", "do you remember this place?") change every few seconds. Everything is low-resolution and blocky with JPEG artefacts.

**Also called / where it trends:** weirdcore, dreamcore, "weirdcore edit", "dreamcore edit", "how to make your photos weirdcore", liminal core, "something isn't right" edits; TikTok #weirdcore / #dreamcore (tutorials such as "how to make a basic weirdcore image" and "this filter makes any photo weirdcore"), Instagram reels (#weirdcore 7.3M, #dreamcore 6.6M reels), Pinterest boards, Tumblr and Aesthetics Wiki. The Chinese variant is **中式梦核 (Chinese millennium dreamcore, "千禧梦核")** on Bilibili and Xiaohongshu: the same dream-memory feeling built from 2000s Chinese apartment blocks, school corridors and family living rooms, with a washed teal-green cast, soft low-res haze and no eyes or rainbows. Neighbours: 怪核 (weirdcore) and 后室 (backrooms, see style 67).

**References:**
- https://www.tiktok.com/@ayitsphotography/video/7687341476929408263: "how to make your photos weirdcore" tutorial, 37.4K likes (TikTok search screenshot `refs/ref_1.png`, from the discovery sweep D1).
- https://www.tiktok.com/@ninanayko/video/7533697244235599112: weirdcore edit, 232K likes.
- https://www.tiktok.com/@_ilikebugsandmoths_/video/7189624672579882245: weirdcore edit.
- https://www.youtube.com/watch?v=SuaK3EZZUNE: weirdcore edit tutorial.
- https://www.pinterest.com/search/pins/?q=weirdcore%20aesthetic (screenshot `refs/ref_2.png`): daisies with eyes, "WAKE UP" and "something isn't right" captions, clouds pasted into stairwells, rainbows, doors in fields, low-res JPEG look.
- https://www.pinterest.com/search/pins/?q=dreamcore%20aesthetic and https://www.instagram.com/popular/dreamcore-aesthetic/: dreamcore pastel skies and empty doorways.
- https://morphic.com/resources/videos/dreamcore-videos: dreamcore as an AI-video aesthetic (overexposed rooms, pastel bloom, soft focus).
- https://en.wikipedia.org/wiki/Dreamcore_(aesthetic) and https://aesthetics.fandom.com/wiki/Dreamcore: definitions (surreal, nostalgic, uncanny; eyes, clouds, rainbows, low-quality images, cryptic text).
- https://www.nylon.com/fashion/dreamcore-aesthetic-weirdcore: Nylon on dreamcore as "sister to weirdcore".
- https://apeironaut.substack.com/p/the-anatomy-of-weirdcore: the anatomy of a weirdcore image (low-res, MS-Paint-like edits, captions in default fonts).
- Chinese variant 中式梦核: Bilibili https://www.bilibili.com/video/av1801274686 , https://www.bilibili.com/video/av822461061 , https://www.bilibili.com/video/av1703595960 (contact sheet `refs/ref_3.png`, from discovery sweep D4); https://www.chinanews.com.cn/sh/2025/03-19/10385517.shtml (China News: why young people love 中式梦核); https://www.huxiu.com/article/4780809.html ; https://www.sixthtone.com/news/1018582.

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049), `example.mp4` (the whole clip at 12 fps with the original audio) and `preview.webp`. This is a local approximation made with `render.py` (numpy + OpenCV + Pillow + the person masks). It works at 648×432: over-bright saturated grade with a lavender-pink lift, the bright window and white wall replaced by a procedural clip-art cloud sky, a 7-band rainbow, four daisy-eyes and three floating eyes with drifting pupils and blinks (all behind the people), Times / Arial / Comic Sans captions, bloom, then two rounds of heavy JPEG compression and an upscale. Masks with a dropped motion-blurred hand (frames 23, 68) are filled from the neighbours.

## Prompt

```text
I'm uploading one video clip. Convert it into a WEIRDCORE / DREAMCORE frame-by-frame animation: every frame should look like an over-compressed, over-bright internet image of a half-remembered dream, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Weirdcore / dreamcore internet aesthetic: surreal, nostalgic, uncanny, low-quality, as if the image has been saved and re-uploaded many times.
Transform the footage into a dream-memory edit built from:
* OVER-BRIGHT, OVEREXPOSED light
* OVER-SATURATED colours with a milky PASTEL lift (lavender, baby pink, sky blue)
* a CLIP-ART BLUE SKY with fluffy white cumulus clouds pasted where the window and bright wall are
* a soft RAINBOW arcing across the room behind the people
* WHITE DAISIES with a realistic HUMAN EYE in place of the yellow centre
* loose floating human EYES on the walls, staring
* small CAPTIONS in plain default fonts (Times New Roman, Arial, Comic Sans), red or white
* LOW RESOLUTION, soft and slightly blurry
* heavy JPEG COMPRESSION blocks and ringing around edges
* soft BLOOM on bright areas
* a gentle vignette
The result should feel like someone:
TOOK A PHOTO OF A FAMILIAR ROOM
→ OPENED IT IN AN OLD PHOTO EDITOR
→ PASTED IN CLIP-ART SKY, RAINBOW, DAISIES AND EYES
→ TYPED A CRYPTIC CAPTION IN A DEFAULT FONT
→ SAVED IT AS A LOW-QUALITY JPEG, RE-UPLOADED IT, SAVED IT AGAIN
→ ANIMATED IT FRAME-BY-FRAME.
CHARACTER — PHOTOGRAPHIC, BLOWN-OUT
The people stay PHOTOGRAPHIC: the same real people, just over-bright, over-saturated and degraded like the rest of the image.
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
Do NOT turn them into a cartoon, painting or 3D render.
Do NOT add eyes, masks or anything else onto the people's faces or bodies.
The people always stand IN FRONT of every pasted element.
COLOUR AND LIGHT
* Push brightness up so whites clip softly and the room feels flooded with light.
* Saturation high, but lifted toward pastel: skies baby blue, walls milky, shadows lavender-grey.
* Skin may glow warm pink; never neon.
* No dark, moody or horror grading: weirdcore is unsettling because it is BRIGHT and innocent.
PASTED DREAM ELEMENTS
* SKY: the window and the brightest white wall areas become a flat clip-art sky: saturated blue gradient, fluffy white clouds with soft grey-blue undersides. Edges look cut-and-pasted, not blended into a real window.
* RAINBOW: one soft 7-band rainbow (red outside to violet inside) arcing across the background, semi-transparent, behind the people.
* DAISY-EYES: 3–5 white daisies with a realistic human eye in the centre, placed in the plant row; the eyes look around slowly.
* FLOATING EYES: 2–3 loose clip-art eyes on the upper wall, slightly different sizes, staring.
* Eyes BLINK occasionally (one or two frames shut), never all at once.
* Pasted elements keep their place in the room from frame to frame.
CAPTIONS
* One short caption on screen at a time, in a plain default font, small, centred or slightly off-centre near the top or bottom.
* Red or white text; white text may have a thin black outline.
* Lines like: "do you remember this place?", "WAKE UP", "you are not alone here", "it's okay. you can stay.", "something isn't right".
* Change the caption every 3 seconds; hold it perfectly still while it is on screen.
* Never place a caption over a face.
IMAGE QUALITY
* Low resolution (as if from a 640 px image), soft.
* Visible 8×8 JPEG blocks and ringing around text, eyes and edges.
* The compression should look like a re-saved meme, not like digital glitch art.
* Light bloom around the window, captions and highlights.
VARIANT — 中式梦核 (CHINESE MILLENNIUM DREAMCORE)
If I ask for the Chinese variant: drop the eyes, daisies and rainbow; keep the low-res haze and emptiness; grade washed teal-green with soft milky highlights; captions in small Song/Hei typeface Chinese; the mood is a 2000s childhood memory (apartment block, school corridor, family living room).
OBJECT CONTINUITY
If the character holds an object, it stays attached to the hand and degraded like the rest.
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
Pasted elements sit behind the people and are hidden wherever a person passes in front of them.
NO pasted element on top of a person.
NO caption jumping between frames while it should hold.
FRAME-TO-FRAME DREAM LIFE
THIS IS CRITICAL.
It must feel like a living, slightly wrong memory, not a still filter.
Allow between consecutive frames:
* JPEG block patterns to change every frame
* fine noise to change every frame
* eye pupils to drift slowly; an occasional blink
* clouds to drift very slowly sideways
* the rainbow to breathe slightly in opacity (±8%)
* daisies and floating eyes to bob by a pixel or two
Keep FIXED:
* the grade (no exposure pumping)
* the position of every pasted element in the room
* the caption while it is on screen
DO NOT
Do NOT make it dark, gory or horror-movie.
Do NOT add VHS tape lines, tracking noise or date stamps.
Do NOT add datamosh, pixel sorting or RGB glitch effects.
Do NOT turn it into a clean, high-resolution fantasy painting.
Do NOT double-expose the people with landscapes.
Do NOT put eyes, flowers or captions over faces.
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
* NO pasted sky, rainbow, daisies or eyes
* NO captions
* NO compression or low-res treatment
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
Do NOT begin the weirdcore / dreamcore transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – WEIRDCORE / DREAMCORE STYLING (AFTER MY CONFIRMATION ONLY)
First, tell me where in the room you will paste the sky, the rainbow, the daisy-eyes and the floating eyes, and list the captions with the frame range of each.
Then style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation, so the people are exactly that frame.
Apply every style rule above, with the SAME grade and the SAME pasted elements in the same places on every frame.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing, a pasted element in front of a person, or a jumping caption broke — regenerate those frames only.
The final video must feel like A DREAM YOU ALMOST REMEMBER, SAVED AS A BAD JPEG: over-bright pastel light, clip-art sky, rainbow, staring daisy-eyes, a cryptic caption, 12 frames per second.
The image should deliberately contain:
* over-bright, over-saturated pastel colour
* a pasted clip-art cloud sky and a rainbow
* daisies with human eyes and floating eyes
* one plain-font cryptic caption
* low resolution with visible JPEG blocks.
Avoid clean, sharp, professional imagery.
```
