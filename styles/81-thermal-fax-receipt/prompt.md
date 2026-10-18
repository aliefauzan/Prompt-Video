# 81 — Thermal Fax Receipt Print

**Look:** The clip becomes a printout from a thermal fax machine or receipt printer. The whole picture is printed at a coarse dot resolution. Each dot is either burnt black or left as bare paper. Tone comes from a noisy, scattered 1-bit dither. The print head leaves its marks: some rows print darker or lighter, a few dead heating elements leave thin white streaks down the page, and sometimes the paper slips and a band of rows stretches or shifts sideways. The black is blue-black and fades to grey-brown in patches, on cool off-white thermal paper with a faint sheen and curl. A fax header line runs across the top and a receipt footer (dashed rule, totals, "*** THANK YOU ***") runs across the bottom. Every frame is a new printout. The dither is stochastic and head-banded. That separates it from the toner grit and collage of 01 Punk Photocopy, the clean ordered pixel dither of 11 Pixel Dither, and the colour dots of 07 Pop Art and 53 90s Comic.

**Also called / where it trends:** "thermal printer effect", "receipt print", "receipt photo", "fax effect", "fax machine filter", "photo booth receipt", "thermal photo booth", "传真机效果" (Douyin). Receipt-printer photo booths and pocket thermal printers are a trend at weddings, cafés and events. Their 1-bit receipt strips are shared on Pinterest and Instagram. Dithering tools ship "Thermal Printer", "Fax Machine" and "Receipt Printer" presets, and fax-transmission filters are a lo-fi edit look.

**References:**
- https://github.com/gyng/ditherer (screenshot `refs/ref_1.png`): the open-source *ditherer* web tool with "Thermal Printer", "Fax Machine" and "Receipt Printer" presets. They give 1-bit noisy dots, row banding and paper tint.
- https://www.pinterest.com/search/pins/?q=thermal%20receipt%20printer%20photo%20print (screenshot `refs/ref_2.png`): receipt photo-booth strips and pocket thermal printer photos. They show 1-bit dots on curled thermal paper.
- https://onlinephototools.com/image-tools/image-fax-transmission-filter-effect-tool/: an online "fax transmission" photo filter (1-bit, scan-line noise, header).
- https://stoatworks-labs.com/software/fax/: a fax-look image tool that simulates transmission artefacts.
- https://github.com/zeck00/sunmi-photobooth: an open-source photo booth that prints photos on a receipt thermal printer.
- https://www.maxhaesslein.de/visual/objects/amelie/: Max Haesslein's "Amelie", a camera that prints photos on a thermal receipt printer.

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049), `example.mp4` (the whole clip at 12 fps with the original audio) and `preview.webp`. This is a local approximation made with `render.py` (numpy + OpenCV + PIL and the person masks). The frame is CLAHE-equalised, sharpened and brightened with blown highlights, then scaled down to 540 × 360 printer dots. Each frame gets per-row heat banding with 2–5 over- or under-heated bands. The picture is dithered to 1 bit with Floyd–Steinberg error diffusion and a randomly jittered threshold, so the dots scatter. Three fixed dead columns stay white. A paper-feed slip (rows rolled sideways or stretched) happens on about a third of the frames. A 1-bit fax header and receipt footer are stamped on in a mono dot font. The dots are scaled up as square dots, softened slightly, and printed in blue-black that fades to grey-brown in patches, on cool thermal paper with curl and sheen.

## Prompt

```text
I'm uploading one video clip. Convert it into a THERMAL FAX / RECEIPT PRINT frame-by-frame animation: every frame should look like a fresh printout from a thermal fax machine or receipt printer, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Thermal printer printout, fax transmission, receipt paper, 1-bit noisy dither, coarse dots, print-head banding, dead-pixel streaks, faded blue-black thermal ink on curled off-white paper, fax header and receipt footer.
Transform the footage into a thermal printout built from:
* ONE-BIT DOTS: every dot is burnt black or bare paper, nothing in between
* a COARSE dot resolution, like a 203 dpi print head (about 540 dots across)
* a NOISY, SCATTERED dither: tone from dot density, with random grain, not a regular pattern
* crisp, high-contrast, slightly blown-out highlights, like a fax of a photo
* row-by-row HEAT BANDING: some rows print darker, some lighter
* a few thin WHITE STREAKS running down the whole print from dead heating elements
* occasional PAPER-FEED SLIPS: a band of rows stretched or shifted sideways
* blue-black thermal ink that FADES to grey-brown in patches
* cool OFF-WHITE THERMAL PAPER with a faint sheen and a soft curl shadow at the edges
* a FAX HEADER line across the top with date, time, sender, number and "P.01"
* a RECEIPT FOOTER across the bottom: a dashed rule, "12 FRAMES/SEC x 14.9 SEC", "TOTAL 179", "*** THANK YOU ***"
The result should feel like someone:
POINTED AN OFFICE CAMERA AT THE SCENE
→ FAXED EACH FRAME DOWN A NOISY PHONE LINE
→ RECEIVED IT ON AN OLD THERMAL FAX WITH A TIRED PRINT HEAD
→ TORE OFF THE CURLING PRINTOUT
→ PRINTED A RECEIPT FOOTER UNDER IT
→ ANIMATED THE PRINTOUTS ONE BY ONE.
CHARACTER — PRINTED, NOT REPLACED
The people stay the PHOTOGRAPHIC people from the frame, printed as dots.
Preserve the person's exact:
* identity
* face
* expression
* hairstyle
* glasses
* clothing
* clothing patterns (as dot texture, not removed)
* accessories
* pose
* body proportions
* movement
* hand position
* interaction with objects
Do NOT redraw the character.
Do NOT turn them into an illustration, line drawing or cartoon.
Do NOT smooth or beautify faces.
DOT + DITHER RULES
* Only two states per dot: burnt or paper. No grey dots, no anti-aliased grey.
* Dots are small squares on a coarse grid.
* Tone comes from the DENSITY of scattered dots, with visible random grain.
* The dither is NOT a regular crosshatch, Bayer pattern or halftone screen.
* Faces must stay readable: eyes, brows, glasses, nose and mouth clearly visible.
* Highlights blow out to bare paper; deep shadows go almost solid black.
PRINT-HEAD DEFECTS
* Heat banding: thin horizontal bands where the print is darker or lighter than its neighbours.
* Three thin dead-element streaks run straight down the page and stay in the SAME columns on every frame.
* Some frames (about one in three) have a paper-feed slip: one band of rows shifted a few dots sideways or stretched vertically.
* The defects never wipe out a whole face.
PAPER AND INK
* Paper is cool off-white thermal paper, with a faint diagonal sheen.
* The edges darken softly where the paper curls.
* The black is a cool blue-black and fades to grey-brown in some patches, like an old receipt.
* Dots are slightly soft at the edges, like heat spreading.
HEADER AND FOOTER
* Top line, in a small mono dot font: "OCT-18-2026 08:44   FROM: OFFICE CAM 3   TO: +62 21 555 0112", with "P.01" at the right.
* Bottom block, in the same dot font: a dashed rule, "12 FRAMES/SEC x 14.9 SEC" at the left, "TOTAL 179" in bold at the right, and "*** THANK YOU ***" centred.
* The text is printed in the same 1-bit dots and stays identical on every frame.
PALETTE
Blue-black thermal ink, faded grey-brown ink.
Cool off-white thermal paper.
Nothing else. Do NOT add colour, sepia toning or a pink or yellow receipt tint.
OBJECT CONTINUITY
If the character holds an object, it is printed in dots like the rest and stays attached to the hand.
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
The printed people must match the source frame exactly.
The dots follow the picture as it moves.
NO dot pattern frozen in place while the body moves under it.
NO ghost of a previous frame in the print.
FRAME-TO-FRAME PRINT LIFE
THIS IS CRITICAL.
It must feel like a new printout every frame, not a still filter.
Allow between consecutive frames:
* the dither grain to change completely
* the heat bands to move to new rows
* a paper-feed slip to appear on some frames and not others
* the faded patches to drift slowly
Keep FIXED:
* the dot size and the 1-bit look
* the dead-element streaks in the same columns
* the header, footer and paper
DO NOT
Do NOT use halftone dots, Ben-Day dots or a round-dot screen.
Do NOT use a clean ordered or Bayer pixel dither, or a colour pixel-art look.
Do NOT use photocopy toner smears, torn paper or collage.
Do NOT use VHS, CRT scan lines or RGB colour noise.
Do NOT use smooth grey tones.
Do NOT add colour.
Do NOT add any text beyond the header and footer above.
Do NOT turn the people into line drawings.
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
* NO black-and-white or 1-bit conversion
* NO dither
* NO banding, streaks or feed slips
* NO header, footer or paper texture
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
Do NOT begin the thermal fax / receipt print transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – THERMAL FAX / RECEIPT PRINT STYLING (AFTER MY CONFIRMATION ONLY)
First, tell me the dot resolution you will print at, and the exact header and footer text (adjust the duration and frame total in the footer to the numbers verified in Stage 2).
Then style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation, so the people are exactly that frame.
Apply every style rule above, with the SAME dot size, dead streaks, header, footer and paper on every frame.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing, the 1-bit look or a face's legibility broke — regenerate those frames only.
The final video must feel like A STACK OF FAX PRINTOUTS FLIPPED AT 12 FRAMES PER SECOND: 1-bit noisy dots, head banding, dead streaks, fading ink, curling thermal paper.
The image should deliberately contain:
* coarse 1-bit dots with a noisy scattered dither
* horizontal heat banding
* thin white dead-element streaks
* an occasional paper-feed slip
* a fax header and receipt footer in dot font
* faded blue-black ink on off-white thermal paper.
Avoid smooth photographic grey tones.
```
