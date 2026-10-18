# 79 — Banknote Engraving

**Look:** The clip becomes the portrait on a banknote. The people and the room are built only from fine parallel engraved lines in one green-black intaglio ink on pale security paper. The lines swell where the picture is dark and thin to hairlines where it is light. They bend with the forms of faces and clothes, and a second and third set cross the darkest shadows. The room behind turns into a softer field of horizontal lathe lines with a gentle wave. A faint rosette and lathe underprint sits under everything. The frame is a currency border: a dark band filled with interlaced white guilloche waves, corner rosettes carrying the denomination "12", and two small legend plaques. There are no dots, no flat fills and no grey wash. That separates it from the dot screens of 07 Pop Art and 53 90s Comic, the toner of 01 Punk Photocopy, and the pixel dither of 11 Pixel Dither.

**Also called / where it trends:** "banknote portrait", "money engraving effect", "dollar bill portrait", "currency engraving", "engraved portrait", "intaglio effect", "guilloche", "put my face on money". It shows up as a photo-to-banknote AI trend: users post themselves as the portrait on a note with a guilloche oval. It also appears as Photoshop actions and plug-ins sold for "money effect" portraits, and as a preset in dithering tools ("Currency Engraving").

**References:**
- https://github.com/gyng/ditherer (screenshot `refs/ref_1.png`): the open-source *ditherer* web tool. Its "Currency Engraving" and "Etching" presets turn photos into line-hatched engraving.
- https://www.pinterest.com/search/pins/?q=banknote%20engraving%20portrait%20guilloche (screenshot `refs/ref_2.png`): banknote-engraving portraits and guilloche ovals. It includes the AI photo-to-banknote trend: a green note with a guilloche oval and an engraved portrait.
- https://www.pinterest.com/search/pins/?q=engraving%20crosshatch%20banknote: crosshatch engraving close-ups from real notes.
- https://www.instagram.com/popular/engraving-style/: Instagram engraving-style posts and portrait edits.
- https://photoshoptrainingchannel.com/how-to-make-money-with-photoshop/: Photoshop Training Channel tutorial on making a currency-style engraved portrait.
- https://blog.spoongraphics.co.uk/tutorials/create-realistic-money-effect-photoshop: Spoon Graphics "realistic money effect" tutorial (line-screen portrait, guilloche frame).
- https://creativemarket.com/studioretouch/292386390-Guilloche-Currency-Engraver-FX: a Photoshop add-on that makes guilloche and currency-engraved portraits.
- https://fotomedley.com/en/style/engraved-banknote-portrait: an AI photo style for "engraved banknote portrait".
- https://www.vofy.art/apps/dollar-engraving-style: an AI "dollar engraving style" app.
- https://buttonmonkey.com/intaglioengine/: Intaglio Engine, a tool for line-engraving security-print portraits.

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049), `example.mp4` (the whole clip at 12 fps with the original audio) and `preview.webp`. This is a local approximation made with `render.py` (numpy + OpenCV + PIL, the person masks, and Apple Vision face landmarks in `faces.json`). The people are a 35° engraved line field with its phase bent by the smoothed luminance, so the lines follow the forms. Each line's width is set by tone coverage, and faces are lightened slightly. A −40° cross-hatch is added in the shadows and an 80° third hatch in the deepest blacks. XDoG contours, fine facial-feature lines and a silhouette line are engraved on top. The room is a horizontal wavy lathe-line field. A faint rosette and lathe underprint is added. The border is a solid ink band with reversed interlaced sine guilloche, corner rosettes carrying a "12" in Copperplate, and "TWELVE FRAMES" / "ONE SECOND" plaques. Ink spread, a slight density flicker and a plate-tone wipe change from frame to frame.

## Prompt

```text
I'm uploading one video clip. Convert it into a BANKNOTE ENGRAVING frame-by-frame animation: every frame should look like the engraved portrait vignette on a banknote, printed in one intaglio ink from a hand-cut steel plate, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Banknote portrait engraving, intaglio line engraving, currency engraving, fine parallel hatching that swells and thins, cross-hatching in shadows, guilloche border, security underprint, single green-black ink on pale security paper.
Transform the footage into a currency engraving built from:
* ONE intaglio ink: deep green-black
* pale cream-green SECURITY PAPER
* every tone made ONLY of fine PARALLEL ENGRAVED LINES
* lines that SWELL in dark areas and taper to HAIRLINES in light areas
* lines that BEND around the forms of faces, hair and clothes
* a second CROSS-HATCH in the shadows and a third set in the deepest blacks
* fine engraved contour lines for eyes, brows, nose, lips and glasses
* a background of softer horizontal LATHE LINES with a gentle wave
* a faint ROSETTE and LATHE UNDERPRINT under everything
* a currency BORDER: a dark band filled with interlaced white GUILLOCHE waves
* corner ROSETTES carrying the number "12"
* two small legend plaques reading "TWELVE FRAMES" and "ONE SECOND"
The result should feel like someone:
PHOTOGRAPHED THE SITTERS FOR A NEW BANKNOTE
→ HAD A MASTER ENGRAVER CUT THEM INTO A STEEL PLATE LINE BY LINE
→ RAN THE BORDER ON A GEOMETRIC LATHE
→ PRINTED THEM BY INTAGLIO IN ONE GREEN INK ON SECURITY PAPER
→ SHEET-FED A NEW PLATE FOR EVERY FRAME
→ ANIMATED THE NOTES ONE BY ONE.
CHARACTER — ENGRAVED, NOT REPLACED
The people become ENGRAVED PORTRAITS of themselves, traced from the frame.
Preserve the person's exact:
* identity
* face
* expression
* hairstyle
* glasses
* clothing
* clothing patterns (engraved as line texture, not removed)
* accessories
* pose
* body proportions
* movement
* hand position
* interaction with objects
Do NOT turn them into historical statesmen or old-fashioned costume.
Do NOT age them, add wigs, collars or formal suits.
Do NOT idealise or re-sculpt faces.
Do NOT redraw the pose.
ENGRAVING RULES
* Tone comes ONLY from line width and line spacing. There are no dots and no flat grey areas.
* Main hatch about 35° on the people, bending with the shape of the face, hair and fabric.
* A cross-hatch at about −40° is added only where the image is in shadow.
* A third set of lines is added only in the deepest blacks (hair, collar shadows).
* Light areas, like cheeks, foreheads and highlights, thin down to hairlines or to bare paper.
* Faces stay a little lighter than the clothes and keep clean, readable features.
* Lines are crisp, continuous and evenly spaced, like a burin cut, not a sketch.
BACKGROUND
* The room stays recognisable but engraved in softer, mostly HORIZONTAL lathe lines.
* The lines carry a gentle long wave, like a security-print background.
* The background is lighter than the people so the portraits read first.
* A faint rosette and lathe UNDERPRINT shows through under the paper tone.
BORDER
* A solid ink band runs around all four edges.
* Inside the band, interlaced sine-wave GUILLOCHE lines are left white (reversed out of the ink).
* Each corner has a round ROSETTE with a fine white lathe pattern and a pale centre carrying "12" in an engraved serif face.
* Two small pale plaques at the bottom read "TWELVE FRAMES" and "ONE SECOND" in engraved capitals.
* The border is identical on every frame.
PALETTE
Deep green-black intaglio ink.
Pale cream-green security paper with a faint warm underprint.
Nothing else. Do NOT add a second colour, gold foil, holograms or rainbow tints.
OBJECT CONTINUITY
If the character holds an object, it is engraved like the rest and stays attached to the hand.
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
The engraved people must match the source frame exactly.
The hatch lines follow the forms as they move and turn.
NO line pattern frozen in place while the body moves under it.
NO lines left behind from a previous frame.
FRAME-TO-FRAME PRINT LIFE
THIS IS CRITICAL.
It must feel like a fresh intaglio print every frame, not a still filter.
Allow between consecutive frames:
* the ink to spread very slightly differently on each print
* overall ink density to flicker slightly (±5%)
* a faint plate-tone wipe to shift in the margins
Keep FIXED:
* the hatch angles and line spacing
* the green-black ink colour and the paper colour
* the border, rosettes and legend plaques
DO NOT
Do NOT use halftone dots, Ben-Day dots or a dot screen.
Do NOT use pixel dither or a pixel grid.
Do NOT use photocopy toner, grit or collage.
Do NOT use flat grey fills or soft airbrush shading.
Do NOT render it as a photo with a green tint.
Do NOT add real currency names, real bank names, serial numbers or signatures.
Do NOT copy any real banknote design.
Do NOT turn the people into historical figures.
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
* NO colour change
* NO engraving or line hatching
* NO underprint
* NO border, rosettes or plaques
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
Do NOT begin the banknote engraving transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – BANKNOTE ENGRAVING STYLING (AFTER MY CONFIRMATION ONLY)
First, tell me the hatch angles and line spacing you will use, and describe the border design.
Then style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation, so the people are exactly that frame.
Apply every style rule above, with the SAME ink, paper, hatch angles and border on every frame.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing, the line engraving or the border broke — regenerate those frames only.
The final video must feel like A BANKNOTE PORTRAIT COME ALIVE: green intaglio lines, guilloche border, "12" rosettes, 12 frames per second.
The image should deliberately contain:
* fine parallel engraved lines that swell and taper
* cross-hatching only in the shadows
* lines that follow the forms
* a wavy lathe-line background
* a reversed guilloche border with corner rosettes
* one green-black ink on pale security paper.
Avoid photographic grey tones.
```
