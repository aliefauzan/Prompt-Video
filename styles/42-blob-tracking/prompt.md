# 42 — Blob Tracking

**Look:** Creative-coding "blob tracking". The footage goes near-monochrome with hard contrast. Dozens of thin square tracking boxes lock onto bright features and move with them. Each box has a centre crosshair and a monospace ID and x/y readout. Some boxes are filled with an inverted, thresholded or zoomed copy of the picture inside. Thin plexus lines join neighbouring boxes, and a small HUD prints the blob count and frame number. Boxes are born, follow the motion for a second or two, then die. Section 2 adds red tagged boxes, and section 3 goes darker and denser.

**Also called / where it trends:** "blob tracking effect", "blob track", "TouchDesigner blob tracking", "tracking line effect", "codecore", "tracery / tracker edit", "data overlay edit". It is all over TikTok, Instagram Reels and YouTube Shorts as TouchDesigner, After Effects and CapCut tutorials. Higgsfield ships it as the **Tracking** preset in Mixed Media.

**References:**
- https://www.youtube.com/watch?v=CErVm4lTgPY (`refs/ref_1.png`): thomas devl, "Blob Tracking Effect" TouchDesigner tutorial (YouTube search result). Source of the box + label + link-line anatomy.
- https://www.youtube.com/watch?v=RGq3euLyVQM: blob tracking tutorial for After Effects; the boxes follow tracked points and carry coordinate text.
- YouTube Shorts results row (`refs/ref_2.png`): "tracking LINE effect" (68K views), After Effects blob tracking, "tracery blob tracking capcut" and similar Shorts. Shows how wide the trend is on Shorts.
- https://higgsfield.ai/mixed-media (`refs/ref_3.png`): Higgsfield Mixed Media preset grid with the **Tracking**, Toxic, Windows and Acid tiles. Tracking is the commercial "one-click" version of this look.
- https://www.tiktok.com/@archduchie/video/7486601949828205867: TikTok blob tracking edit.
- https://derivative.ca/community-post/tutorial/make-viral-blob-tracking-effect-touchdesigner-free/74680: Derivative (TouchDesigner) community tutorial, "Make the viral blob tracking effect in TouchDesigner".
- https://www.instagram.com/dcheesman/reel/DAWCoyDPVul/: Dean Cheesman (@dcheesman), blob tracking reel.
- https://www.instagram.com/reel/DUcgc1HkVSf/: @theisaacmatthew, "Blob tracking, codecore, touch designer".
- https://www.instagram.com/erto_tokyo/reel/DFx0RyCyAOn/: @erto_tokyo blob tracking reel; credits the tutorial by @pppanik at https://www.youtube.com/watch?v=gtP1Ae35RqY.
- https://github.com/alexjiganov179-lab/blob-tracker: open-source blob tracker that renders the same boxes + IDs + lines over video (read via the burner GitHub account).

**Example:** `example.png` (six frames of the test clip) and `before_after.png` (frame 049). This is a local approximation made with `render.py` (numpy + OpenCV). Each frame is greyed and given a hard contrast. Shi-Tomasi corners are picked, 75% on the people, and followed with Lucas-Kanade optical flow. Each tracker has its own size, life span and fill (invert, threshold, 2× zoom or empty). It draws boxes, crosshairs, ID/coordinate labels, nearest-neighbour link lines and a HUD, plus light sensor noise. There are three sections: mono white, red tags, dense dark.

## Prompt

```text
I'm uploading one video clip. Convert it into a 12 FPS BLOB TRACKING / TOUCHDESIGNER DATA-OVERLAY frame-by-frame animation, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
Seedream works here because every frame is the source frame with a graphic overlay drawn on top; the tracker list from the previous frame is passed along as text so the boxes stay locked.
CORE VISUAL STYLE
Every frame looks like the live output of a computer-vision patch:
* footage pushed to near-monochrome with hard contrast
* thin square tracking boxes locked onto bright features of the people
* a small centre crosshair inside every box
* a monospace label on each box: a 3-digit ID, and on bigger boxes "x0.412 y0.287" style coordinates
* some boxes filled with an inverted, thresholded or 2× zoomed copy of the picture inside them
* thin straight plexus lines joining neighbouring boxes, plus 2–3 long lines across the frame
* a small HUD: "BLOB_TRACK blobs:NN frame:NNN 12fps" in one corner, the patch name in another
* light digital sensor noise
It should look like a viral TouchDesigner blob-tracking edit, the Higgsfield "Tracking" mixed-media preset.
The result should feel like someone:
FED THE CLIP INTO TOUCHDESIGNER
→ THRESHOLDED IT AND RAN A BLOB TRACKER
→ DREW EVERY BLOB AS A LABELLED BOX
→ LINKED THE BLOBS WITH LINES
→ RECORDED THE OUTPUT AT 12 FRAMES PER SECOND
→ ANIMATED IT FRAME-BY-FRAME.
COLOUR AND GRADE
Use only:
* greys from black to white (the footage)
* pure white for boxes, labels, lines and HUD
* one accent: signal red (#E8202A), only in the section that uses it
Desaturate the footage almost completely.
Raise contrast hard: deep blacks, clipped whites.
Do NOT add colour gradients, neon glow or bloom.
CHARACTER — PHOTOGRAPHIC UNDER THE OVERLAY
The people stay PHOTOGRAPHIC under the overlay.
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
Do NOT turn them into a cartoon, outline or silhouette.
Faces must stay readable between the boxes.
TRACKING BOXES
Boxes are perfect squares, 1–2 px lines, never rounded.
Sizes vary a lot: many small boxes (30–60 px), some medium, a few large (120–150 px at 1080p).
About three quarters of the boxes sit on the people: eyes, glasses, collars, hands, hair edges, shirt patterns.
The rest sit on bright points of the room: lamps, screens, window edges.
Boxes never overlap heavily; keep a small gap between box centres.
Each box follows its feature exactly as it moves in the footage.
BOX FILLS
About one box in three has a fill:
* INVERTED: the picture inside the box shown as a negative
* THRESHOLD: the picture inside reduced to pure black and white
* ZOOM: the picture inside magnified 2×
The rest are empty outlines.
A box keeps the same fill for its whole life.
LABELS AND HUD
Labels use a small monospace font, white, set just above the box (below it if there is no room).
Small boxes show only the ID. Bigger boxes add x/y coordinates normalised 0–1 to 3 decimals.
Red boxes carry their label on a filled red tag with white text.
The HUD frame counter goes up by exactly 1 every frame.
The HUD blob count is the real number of boxes in the frame.
Never write any other words on the frame.
LINK LINES
Thin 1 px straight lines join each box to its 1–2 nearest neighbours.
Add 2–3 long lines between random boxes; change them every 3 frames.
Lines start and end exactly at box centres.
BACKGROUND
Keep the real room, desaturated and contrasted like the people.
Do NOT replace, blur or darken the background to black.
SECTIONS
Split the clip into 3 sections of roughly equal length:
* Section 1, MONO: all boxes white, about 25 boxes, footage fully grey.
* Section 2, RED TAGS: about 35 boxes, roughly 45% of them red with red tags, a trace of the original colour (25%).
* Section 3, DENSE DARK: about 45 boxes, footage darkened to half brightness so the white graphics dominate, a few red boxes, more long lines.
TRACKER LIFE (BOIL RULES)
THIS IS CRITICAL.
Boxes must NOT be redrawn at random positions every frame.
A box is born on a feature, follows it for 10–40 frames, then disappears.
When a box dies, a new one is born on another feature, so the count stays roughly constant.
A box keeps its ID, size and fill for its whole life.
IDs only count upward; never reuse an ID.
Allow between consecutive frames:
* boxes moving with their features
* a few boxes being born and a few dying
* sensor noise changing
* the long lines changing every 3 frames
OBJECT CONTINUITY
If the character holds or touches an object (phone, cup, bag, microphone), it stays photographic and may carry its own box.
Do NOT erase it.
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
The footage under the overlay must match the source frame exactly in position, pose and timing.
Every box must sit on the same feature it sat on in the previous frame, moved by that feature's real motion.
Do NOT invent motion that is not in the footage.
DO NOT
Do NOT use rounded boxes, circles or glowing outlines.
Do NOT add neon colours, gradients or bloom.
Do NOT add words, logos or captions other than the labels and HUD.
Do NOT put boxes in random places that are not on a feature.
Do NOT let boxes jump to new places between frames.
Do NOT cover faces completely with filled boxes.
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
* NO tracking boxes, labels or link lines
* NO HUD
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
Do NOT begin the blob-tracking transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – BLOB TRACKING STYLING (AFTER MY CONFIRMATION ONLY)
First, plan the sections and list them for me: frame range, box count, colour rule and grade for each section.
Then style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Give Seedream the current extracted frame as the image input, plus the previous styled frame as a second image input so the boxes stay where they were.
Keep a running tracker list in text (ID, centre, size, fill, colour, frames left) and pass it with every frame; update it from the real motion between the two source frames.
Apply every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing, box tracking or the style rules broke — regenerate those frames only.
The final video must feel like a LIVE TOUCHDESIGNER BLOB TRACKER: hard grey footage, labelled boxes locked to the people, plexus lines, a ticking HUD, 12 frames per second.
The image should deliberately contain:
* hard-contrast grey footage
* square boxes with crosshairs
* monospace ID and coordinate labels
* inverted, thresholded and zoomed box fills
* thin link lines
* a HUD with blob count and frame number
* light sensor noise.
Avoid polished motion-graphics perfection.
```

## Other candidates found

Trend scouting for this batch (TikTok, IG Reels, X, Pinterest, YT Shorts, r/aivideo, preset sites and prompt creators), October 2026. The four picked are 42–45. The others either need a video model (not a frame-by-frame restyle) or overlap styles 01–41.

| # | Candidate | Links | Verdict |
|---|---|---|---|
| 1 | **Blob tracking** (TouchDesigner / CapCut / Higgsfield "Tracking") | https://www.youtube.com/watch?v=CErVm4lTgPY · https://derivative.ca/community-post/tutorial/make-viral-blob-tracking-effect-touchdesigner-free/74680 · https://www.instagram.com/reel/DUcgc1HkVSf/ · https://higgsfield.ai/mixed-media | **Picked → 42** |
| 2 | **Dark Stage effect** (#darkstageeffect, black-void spotlight portrait) | https://www.tiktok.com/discover/dark-stage-effect · https://www.tiktok.com/@marina_199199/video/7660562291175263510 · https://randomprompts.org/blog/ai-dark-stage-effect-guide-tiktok-viral-dark-portrait-2026 · https://videosprompt.org/blogs/viral-ai-video-trends-october-2026 | **Picked → 43** |
| 3 | **Broken mirror / shattered glass** (Higgsfield + Melies viral look, CapCut glass shatter) | https://higgsfield.ai/effects/examples/broken-mirror · https://melies.co/cinematic-techniques/viral-looks · https://www.capcut.com/explore/broken-glass-effect · https://www.tiktok.com/@kyvnme/video/7457874096425094405 | **Picked → 44** |
| 4 | **Marble statue** (TikTok marble statue filter, Higgsfield/Melies "Marble") | https://www.tiktok.com/discover/marble-statue-effect · https://www.tiktok.com/@neural.max/video/7323190055848185094 · https://melies.co/cinematic-techniques/viral-looks · https://cliptrend.ai/ai-video-effects/ai-statue-generator | **Picked → 45** |
| 5 | Storm Dance (dancing inside an AI storm) | https://videosprompt.org/blogs/viral-ai-video-trends-october-2026 | Needs a video model (new weather and motion), not a restyle |
| 6 | AI Duet / Hug Younger Self | https://videosprompt.org/blogs/viral-ai-video-trends-october-2026 · https://polox.ai/blog/8-ai-video-trends-taking-over-tiktok-and-instagram-october-2026 | Adds a new person; not a restyle |
| 7 | Earth Zoom Out | https://videosprompt.org/blogs/viral-ai-video-trends-october-2026 · https://www.opus.pro/blog/viral-ai-video-styles-2026 | New camera move; needs a video model |
| 8 | Mini-me food characters | https://videosprompt.org/blogs/viral-ai-video-trends-october-2026 | Generative character swap; not a restyle |
| 9 | Lofi dusk / fake golden hour grade | https://www.instagram.com/reel/DcBXp_qskZ1/ · https://osmtemplate.in/instagram-lofi-dusk-filter-ai-photo-editing-prompts/ | Restyle-able but thin (a grade, close to 03/17/26) |
| 10 | Windows 98 error pop-up cascade | https://videoeffectvibe.com/assets/retro-windows-95-error-cascade · https://higgsfield.ai/mixed-media ("Windows") | Good backup; overlay-heavy, close to 14 and 41 |
| 11 | Jigsaw puzzle edit | https://www.capcut.com/template-detail/jigsaw-edit/7282299273365015813 | Backup; close to 21 stained glass and 44 |
| 12 | Ultraviolet / blacklight | https://higgsfield.ai/viral-presets/examples/ultraviolet · https://melies.co/cinematic-techniques/viral-looks | Backup; overlaps 33 aerochrome and 16 thermal |
| 13 | Ink riot | https://higgsfield.ai/viral-presets/examples/ink-riot | Overlaps 19 watercolor ink and 49 red ink |
| 14 | Mixed-media layered animation | https://www.reddit.com/r/AfterEffects/comments/1qvntah/how_i_make_my_mixed_media_animations/ · https://higgsfield.ai/mixed-media-intro | Overlaps 01, 08 and 25 |
| 15 | Acid / LSD / Toxic presets | https://higgsfield.ai/mixed-media · https://melies.co/cinematic-techniques/viral-looks | Overlaps 05 datamosh and 13 neon |
| 16 | 2000s paparazzi flash | https://melies.co/cinematic-techniques/viral-looks | Overlaps 04 Y2K digicam flash |
| 17 | Halftone dot print, compression breakdown, CRT phosphor glitch (sibling leftovers) | shared notes of the parent session | Overlap 07, 05 and 27 |
| 18 | "Hail Mary" slit-scan (Floww) | https://www.instagram.com/goowithdafloww/ | Temporal effect close to 26 slow shutter |

Roundups used for scouting: https://scripthooks.ai/blog/weekly-trends-october-11-2026 · https://www.opus.pro/blog/viral-ai-video-styles-2026 · https://polox.ai/blog/8-ai-video-trends-taking-over-tiktok-and-instagram-october-2026 · https://miraflow.ai/blog/ai-dark-stage-effect-prompts-2026 · https://phototrend.me/trends/dark-stage-portrait/
