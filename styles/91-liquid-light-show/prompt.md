# 91 — Liquid Light Show

**Look:** The office turns into a 1967 Fillmore ballroom: the room goes dark and a psychedelic "wet show" from an overhead projector is thrown over the wall and the people. Pools of transparent magenta, amber, yellow and violet dye swirl and bleed into each other, mixing subtractively into deep reds and near-black, while clusters of clear oil drops glide through them as glowing round cells with dark outlines and bright rims. The people stay exactly as filmed, lit only by the moving coloured light.

**Also called / where it trends:** "liquid light show", "wet show", "oil projection", "psychedelic light show", "60s oil wheel / overhead projector visuals", "Fillmore light show", "Joshua Light Show", "liquid loops". The 1960s concert art of the Joshua Light Show, the Single Wing Turquoise Bird and the Pink Floyd / UFO Club shows; revived as concert visuals and music-video backdrops, Instagram tags #liquidlightshow, Pinterest boards of 60s projections, Vimeo ink-and-oil test reels, and Behance motion pieces.

**References:**
- https://www.pinterest.com/search/pins/?q=liquid%20light%20show%20psychedelic%2060s (screenshot `refs/ref_1.png`, from the D2 discovery sweep): projected oil cells and dye pools over bands and dancers; orange/red discs, blue and magenta pools, round projector dish.
- https://www.joshualightshow.com/about-classic/joshua-light-show-1967-68 (screenshot `refs/ref_2.png`): the Joshua Light Show crew and projector rig at the Fillmore East, 1967–68.
- https://www.moma.org/collection/works/200467: MoMA's Joshua Light Show entry (the liquid light show as an art work).
- https://www.tate.org.uk/tate-etc/issue-4-summer-2005/tune-turn-on-light: Tate Etc. on 60s light shows (overhead projectors, coloured oils and water in clock glasses).
- https://www.youtube.com/watch?v=TW733Ut5zE0: "The Joshua Light Show – Liquid Loops (1969)", footage of the wet show in motion.
- https://www.nyhistory.org/blogs/the-joshua-light-show-and-the-rock-roll-revolution-a-qa-with-lightmaster-joshua-white: interview with Joshua White on how the shows were made.
- https://vimeo.com/235299071: liquid light show ink tests (D2 sweep).
- https://www.instagram.com/popular/liquid-light-show/ and https://www.behance.net/search/projects?search=liquid%20light%20show%20animation: current creators of liquid light show visuals.
- Differs from **56 Prismatic Dreamscape** (rainbow refraction and light leaks through a prism: here it is projected liquid dye and oil cells) and **17 Double Exposure** (a second image blended in: here coloured light falls on the scene, with oil-drop bubbles).

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049), `example.mp4` (the whole clip at 12 fps with the original audio) and `preview.webp`. A local approximation made with `render.py` (numpy + OpenCV + the person masks). Four periodic noise fields, domain-warped twice for swirls and tendrils, become dye pools that drift and rotate slowly; they multiply like stacked transparent liquids (subtractive mix). About 50 oil drops in five clusters drift with the flow and swell or shrink; touching drops merge, push the dye aside, glow amber and get a dark meniscus and a bright inner rim. A round projector dish with a hot lamp centre limits the light. The scene is darkened: the wall is treated as a projection screen, the people keep their own texture under the coloured light plus a little key light, and haze glow and 16 mm grain finish it.

## Prompt

```text
I'm uploading one video clip. Convert it into a 1960s LIQUID LIGHT SHOW frame-by-frame animation: every frame should look like the scene is standing in a dark ballroom while an overhead-projector "wet show" of coloured oil and dye is projected over the wall and the people, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
1960s psychedelic liquid light show, overhead projector wet show, coloured dye and oil in a glass dish projected onto the scene, Fillmore / Joshua Light Show, Pink Floyd UFO Club visuals, backlit transparent colour.
Transform the footage into a frame built from:
* a DARK room, lit almost only by the projector
* large swirling POOLS of transparent dye: hot magenta, amber-orange, yellow, deep violet-blue
* SUBTRACTIVE colour mixing where pools overlap: deep red, purple, dark brown, near-black
* soft organic edges with curling TENDRILS where two colours meet
* CLUSTERS of clear OIL DROPS: round cells of different sizes, glowing pale amber, each with a DARK thin meniscus outline and a BRIGHT inner rim
* drops that touch MERGE into lumpy cell clusters
* the big ROUND DISH of the projector: light fades out towards the frame corners
* a warm brighter LAMP centre
* the people LIT BY the projected colour, the dye pattern flowing over their clothes and skin
* soft HAZE glow around the brightest colour
* fine 16mm documentation grain
The result should feel like someone:
TURNED OFF THE LIGHTS
→ POURED COLOURED DYE AND MINERAL OIL INTO A CLOCK GLASS
→ SET IT ON AN OVERHEAD PROJECTOR
→ SWIRLED AND PRESSED IT BY HAND
→ PROJECTED IT OVER THE WALL AND THE PEOPLE
→ FILMED IT ON 16MM, 12 FRAMES PER SECOND.
CHARACTER — PHOTOGRAPHIC, LIT BY PROJECTION
The people stay PHOTOGRAPHIC.
They are only re-lit by the coloured projection.
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
Do NOT turn people into silhouettes.
Do NOT paint the dye ON the faces as make-up; it is LIGHT falling on them.
Keep a little dim key light on faces so they never sink to black.
THE PROJECTION
* The projected pattern is ONE continuous image over the whole frame: the wall works as the screen, and the same pattern lands on the people where they stand in front of it.
* Dye pools are big (a pool can cover a third of the frame) with softly bleeding, organic edges.
* Colours are transparent and luminous, like light through coloured liquid, never opaque paint.
* Overlaps mix like filters: magenta + yellow → red, magenta + violet → purple, yellow + violet → dark, three dyes → almost black.
* Oil drops sit in clusters of 6–15, sizes from small beads to big cells, some merged into lumpy groups.
* Inside a drop the dye is thinner, so the drop glows paler and warmer than its surroundings.
* Every drop has a dark thin outline and a bright rim just inside it.
* The projector dish is round: the light falls off into darkness near the frame corners.
* A gentle hot spot in the middle from the lamp.
PALETTE
Hot magenta, pink, amber, orange, yellow, deep red, violet, deep blue.
Near-black where dyes overlap or outside the dish.
Pale glowing amber inside oil drops.
Do NOT use green as a main colour.
Do NOT use neon digital gradients.
ROOM
The room is dark; its shapes (window, wall, plant, screen) only faintly show through the projected light.
No normal room lighting.
OBJECT CONTINUITY
If the character holds an object, it stays attached to the hand and is lit by the same projection.
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
The projection flows independently of the people, as one moving liquid image behind and on them.
NO projection pattern stuck to a person as they move.
NO cut-out halo around the people.
FRAME-TO-FRAME LIQUID MOTION
THIS IS CRITICAL.
It must feel like real liquid being swirled on a projector, not a random pattern every frame.
Between consecutive frames:
* dye pools drift and swirl a LITTLE (a few pixels), slowly rotating as a whole
* edges curl and bleed gradually
* oil drops glide with the flow, slowly swell or shrink, sometimes merge
* the lamp light pulses very slightly (±5%), like a hand-tapped dish to the music
* grain changes every frame
Keep FIXED:
* the palette
* the dish shape and position
* the darkness of the room
DO NOT
Do NOT generate a new unrelated pattern every frame.
Do NOT use sharp digital vector blobs or emoji bubbles.
Do NOT draw outline-only circles; drops are glowing cells.
Do NOT use rainbow prism refraction or lens flares.
Do NOT make the dye opaque paint over faces.
Do NOT light the room normally.
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
* NO projection, dye or oil drops
* NO darkening
* NO grain
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
Do NOT begin the liquid light show transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – LIQUID LIGHT SHOW STYLING (AFTER MY CONFIRMATION ONLY)
First, describe the dye colours, where the oil-drop clusters start, and the direction the liquid will swirl over the clip.
Then style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation, so the people are exactly that frame.
Give each frame the projection state for its moment, moved on a little from the previous frame's projection.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing, palette or the smooth liquid motion broke — regenerate those frames only.
The final video must feel like A 1967 LIQUID LIGHT SHOW projected over the people: swirling transparent dye, gliding oil cells, a dark hall, 12 frames per second.
The image should deliberately contain:
* luminous transparent dye pools in magenta, amber, yellow and violet
* subtractive overlaps going deep red, purple and near-black
* clusters of glowing oil-drop cells with dark outlines and bright rims
* a round projector dish fading to dark corners
* people lit by the coloured light
* haze glow and 16mm grain.
Avoid digital gradients and flat paint.
```
