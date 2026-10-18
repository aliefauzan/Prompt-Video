# 87 — GTA Loading-Screen Illustration

**Look:** The clip becomes the hand-painted key art an open-world crime game shows while it loads. Flat vector-like colour shapes carry soft airbrushed gradients inside each cel band. Every person gets a thick, clean black outline, with thinner black ink for faces, hair and folds. Skin glows warm under a golden-hour key light with an amber rim on one side, and shadows go violet. Behind the people, the office window opens onto a hot purple-pink-orange sunset with palm-tree and skyline silhouettes. A small white loading spinner turns in the corner.

**Also called / where it trends:** "GTA loading screen art", "GTA style", "GTA art filter", "GTA V / GTA VI loading screen", "Vice City style", "vector-vexel GTA cartoon", "turn yourself into a GTA cover". It is a long-running Photoshop/GIMP tutorial genre and an AI filter trend on TikTok and CapCut that went viral again with the GTA VI trailers. Pinterest and Instagram (#gtavicecitystyle) host fan key art, and Civitai has a "wan style" video LoRA for it (D3 sweep).

How it differs from nearby styles: **53 90s Comic Book** and **46 1950s Editorial Poster** use print texture, halftone and flat ink. **30 Spider-Verse** uses misregistration and Ben-Day dots. This one is clean digital vector-airbrush: smooth gradient fills, heavy outline, a saturated sunset palette and poster key-art lighting, with no halftone and no paper.

**References:**
- https://www.pinterest.com/search/pins/?q=gta%20loading%20screen%20art%20style (screenshot `refs/ref_1.png`, from the D2 sweep). The loading-screen key art: heavy outlines, airbrushed skin, sunset gradients, palms and skylines. Its logos are not part of this style.
- https://logosbynick.com/turn-yourself-into-a-gta-load-screen-with-gimp/ (screenshot `refs/ref_2.png`). Logos By Nick, "Turn Yourself Into a GTA Load Screen with GIMP". Photo to outline + posterised airbrush figure over a flat sunset-pink city.
- https://blog.spoongraphics.co.uk/tutorials/videos/video-tutorial-grand-theft-auto-gta-effect-photoshop: Spoon Graphics, GTA effect in Photoshop (cutout, cartoon filter, stroke outline, gradient sky).
- https://design.tutsplus.com/tutorials/how-to-create-a-gta-photo-effect-action-in-adobe-photoshop--cms-29825: Envato Tuts+, a GTA photo-effect action.
- https://www.instagram.com/popular/gta-vice-city-style/ (D2 sweep): Instagram tag page.
- https://civitai.com/models/2031050: a GTA loading-screen art video LoRA (D3 sweep).
- TikTok "gta loading screen art style filter" edits from the D1 sweep: @anne102333/video/7688553544248577310, @ngcnguynkithng3/video/7688630801646325012, @kitrp16/video/7638949974004288788.

**Example:** `example.png` shows six frames of the test clip and `before_after.png` shows frame 049. `example.mp4` is the whole clip at 12 fps with the original audio, and `preview.webp` is an animated preview. This is a local approximation made with `render.py` (numpy + OpenCV + the person masks). Repeated bilateral filtering flattens the colour, lighter on the people so faces keep their features. Lightness is soft-posterised into cel bands and mixed with a blurred copy for an airbrush gradient. Saturation is pushed, with violet shadows and amber lights, and a sunset rim light comes from the masks. The window recess is tracked through the clip with an ORB homography from frame 085 and filled with a sunset gradient, a sun, a skyline and palms; plants in front of it are kept. The room gets a golden-hour wash. A 9 px black outline surrounds each person, plus XDoG ink lines inside, and a small spinner rotates bottom-right.

## Prompt

```text
I'm uploading one video clip. Convert it into a GTA-STYLE LOADING-SCREEN ILLUSTRATION frame-by-frame animation: every frame should look like hand-painted digital key art from an open-world crime game's loading screen, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Transform the footage into a polished digital poster illustration built from:
* THICK, CLEAN BLACK OUTLINES around every person
* thinner black ink lines for facial features, glasses, hair locks and clothing folds
* FLAT VECTOR-LIKE colour shapes
* soft AIRBRUSHED GRADIENTS inside each shape (vexel / cel-plus-airbrush shading)
* 3–4 clear tone bands on skin, hair and clothes
* a warm GOLDEN-HOUR key light with an AMBER RIM on one side of each person
* VIOLET-BLUE shadows
* SATURATED, punchy colour
* a hot SUNSET SKY (violet → hot pink → orange → yellow) with PALM TREE and SKYLINE silhouettes
* poster-like key-art composition
The result should feel like someone:
SHOT A PROMO PHOTO OF THE CAST AT SUNSET
→ TRACED EVERY PERSON IN THICK BLACK LINE
→ BLOCKED IN FLAT VECTOR COLOUR
→ AIRBRUSHED THE SHADING AND THE RIM LIGHT
→ PAINTED A SUNSET CITY INTO THE WINDOW
→ PUT IT UP AS A GAME LOADING SCREEN
→ ANIMATED IT FRAME-BY-FRAME.
CHARACTER — ILLUSTRATED, SAME PEOPLE
Each person becomes an illustrated version of themselves, clearly recognisable.
Preserve the person's exact:
* identity
* face
* expression
* hairstyle
* glasses
* clothing and its pattern (batik, stripes, plain knit)
* accessories
* pose
* body proportions
* movement
* hand position
* interaction with objects
Faces: clean ink for the eyes, brows, glasses, nose and lips; skin in 3–4 airbrushed tone bands; warm highlights on the cheekbones and nose.
Hair: dark mass with a few ink locks and one airbrushed highlight band.
Clothes: flat colour with airbrushed folds; patterns simplified but kept (batik motifs, stripes).
Do NOT turn the people into anime, chibi, 3D render or comic-book halftone.
Do NOT exaggerate or caricature faces; keep realistic proportions like game key art.
OUTLINES
* Outer silhouette: thick, uniform, clean black line (about 1% of frame width).
* Interior lines: thinner, tapered, only where a real edge exists.
* Lines are smooth and confident, like vector ink, never sketchy or doubled.
LIGHT + COLOUR
* Sunset key light from one side: warm amber rim along that side of every person.
* Shadows lean violet-blue; mid-tones stay saturated; highlights lean warm yellow-cream.
* Contrast is strong but every shape stays readable.
BACKGROUND — SAME ROOM, GOLDEN HOUR
* Keep the room's layout: walls, window recess, planter, cabinets, chair and the wall screen stay in place.
* Paint the room flatter and simpler than the people, with thinner or no outlines.
* Wash the room in golden-hour light: peach-orange walls at the top, violet shadow toward the floor.
* The window recess shows a SUNSET CITY instead of blinds: a gradient sky (violet at the top → hot pink → orange → yellow at the horizon), a low sun disc, dark violet skyline blocks and 2–3 palm tree silhouettes.
* The plants in front of the window stay in front of it.
* The sunset stays locked to the window as the camera moves.
LOADING-SCREEN DETAIL
* A small white loading spinner (a ring of dots) turns in the bottom-right corner.
* No logos, no game titles, no text.
PALETTE
Hot pink, magenta-violet, sunset orange, amber, warm yellow, peach.
Violet-blue shadows, deep plum silhouettes.
Warm skin, rich brown batik, cream-and-olive stripes, slate-blue knit, black ink.
Do NOT use grey, desaturated or photographic colour.
OBJECT CONTINUITY
If the character holds an object, outline and paint it like the rest, attached to the hand.
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
The illustrated people must match the source frame exactly.
If the head moves, the outline follows.
If the hand moves, the outline follows.
NO frozen previous-frame silhouette.
NO outline lagging behind the body.
FRAME-TO-FRAME STABILITY
This is POLISHED key art, not a boiling sketch.
Keep FIXED between frames:
* outline thickness
* the tone-band positions and colours on each person
* the sunset gradient, sun and palm positions (locked to the window)
* the golden-hour grade
Allow only:
* the loading spinner to turn
* the rim light to follow the body as it moves.
DO NOT
Do NOT use halftone dots, Ben-Day dots or paper texture.
Do NOT use sketchy, doubled or scribbled lines.
Do NOT make it look like a photo with a cartoon filter or an oil painting.
Do NOT use cold, grey or teal-and-orange movie grading.
Do NOT add game logos, title text or rating badges.
Do NOT add new characters, cars or weapons.
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
* NO outlines
* NO airbrush shading
* NO sunset sky or palms
* NO colour grade
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
Do NOT begin the loading-screen illustration transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – LOADING-SCREEN ILLUSTRATION STYLING (AFTER MY CONFIRMATION ONLY)
First, tell me which side the sunset key light comes from, and describe the sunset scene you will paint into the window (sky colours, sun position, palms and skyline). Keep them fixed for the whole clip.
Then style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation, so the people are exactly that frame.
Apply every style rule above, with the SAME palette, line weight and sunset on every frame.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing, line weight or palette consistency broke — regenerate those frames only.
The final video must feel like A GAME LOADING SCREEN COME TO LIFE: thick black outlines, airbrushed vector colour, amber rim light, a hot sunset with palms in the window, 12 frames per second.
The image should deliberately contain:
* thick clean black outlines
* flat vector shapes with airbrushed gradients
* violet shadows and amber rim light
* a violet-pink-orange sunset with palm and skyline silhouettes
* saturated poster colour
* a small loading spinner.
Avoid photographic realism and print texture.
```
