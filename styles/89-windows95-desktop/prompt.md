# 89 — Windows 95 Desktop UI

**Look:** The clip plays inside a mid-90s PC desktop. A flat teal desktop holds a column of chunky pixel-art icons. The footage runs in a grey bevelled media-player window with a navy title bar, menu bar, play/pause/stop buttons and a seek bar that moves with the clip. The video itself is small-window 1995 playback: low resolution and 256 dithered colours. Error dialogs pop up one by one and pile into a cascade, an arrow cursor drifts over to click OK, and a grey taskbar with a Start button and clock sits along the bottom. Everything is pixel-crisp, with no anti-aliasing.

**Also called / where it trends:** "Windows 95 aesthetic", "Win95 edit", "retro OS desktop overlay", "old computer edit", "error pop-up edit", "vaporwave desktop", "Windows 98 / 9x UI". It shows up as CapCut templates ("Windows 95 Edit", 1.5K+ uses), TikTok edits that pile error pop-ups over footage, Pinterest/Tumblr vaporwave desktop mood boards, and Videohive "Windows 95 style" intro packs.

How it differs from nearby styles: **12 ASCII Terminal Phosphor** is a text-mode green screen, and **15 Y2K Chrome / Frutiger Aero** is glossy glass and bubbles. This is flat grey bevelled 9x window chrome, a teal desktop and 256-colour dithered video. The footage is framed by an operating system rather than re-rendered.

**References:**
- https://www.pinterest.com/search/pins/?q=windows%2095%20desktop%20aesthetic (screenshot `refs/ref_1.png`, from the D2 sweep). Teal desktops, grey bevelled windows, stacked "Not found" error-dialog cascades, pixel icon sets.
- https://www.capcut.com/template-detail/Windows-95-Edit/7390148344745577733 (screenshot `refs/ref_2.png`). CapCut "Windows 95 Edit" template: footage playing inside a grey media-player window with pixel desktop icons around it.
- https://www.instagram.com/popular/windows-95-aesthetic/ (D2 sweep): Instagram tag page.
- TikTok "windows 95 desktop popup edit aesthetic" edits from the D1 sweep: @s1lax.art/video/7598465499810237717, @odditylooms/video/7625183082550676758, @adxyxn_g59/video/7170185052045806854.
- https://www.editorengine.net/videohive-retro-intro-windows-95-style/: Videohive "Retro Intro // Windows 95 Style" (window pop-ins, dialogs, cursor).
- https://vaporwavecorp.tumblr.com/post/665139305838182400/hey-guys-i-made-a-windows-95-style-desktop-on: a fan-made Win95-style desktop (vaporwave scene).
- http://crash-stop.blogspot.com/2021/04/desktop-as-performative-space.html: "Desktop as performative space", on desktop-as-stage video art.

**Example:** `example.png` shows six frames of the test clip and `before_after.png` shows frame 049. `example.mp4` is the whole clip at 12 fps with the original audio, and `preview.webp` is an animated preview. This is a local approximation made with `render.py` (numpy + OpenCV + Pillow). The whole UI is drawn on an 810x540 canvas with anti-aliasing turned off and enlarged 2x with nearest neighbour. All icons are original pixel art drawn from rectangles; there are no logos. The video is downscaled to 300x200 and quantised to a 6x6x6 colour cube plus a grey ramp with an 8x8 Bayer dither, then shown 2x in the player well. The seek thumb and time readout follow the frame number. Seven error dialogs, with original joke messages and a red stop icon, appear at fixed frames and stack into a cascade over the lower right, below the faces. The cursor glides over to each new dialog's OK button. The masks are not needed: nothing is drawn over the people except the dialog cascade, which sits low in the frame.

## Prompt

```text
I'm uploading one video clip. Convert it into a WINDOWS 95 DESKTOP UI frame-by-frame animation: every frame should look like a screenshot of a mid-1990s PC desktop with the clip playing inside a media-player window, error pop-ups piling up and a cursor moving, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Transform the footage into a 1995 desktop screenshot built from:
* a FLAT TEAL desktop
* a column of chunky 32x32 PIXEL-ART desktop icons with small white labels
* a GREY BEVELLED media-player WINDOW (white top-left edges, dark grey/black bottom-right edges)
* a solid NAVY title bar with bold white title text and three small bevelled title buttons
* a menu bar (File Edit View Play Help), a sunken video well, play / pause / stop buttons, a seek bar with a thumb, a time readout
* the footage inside the well as LOW-RES 256-COLOUR video with ordered dither
* grey ERROR DIALOGS with a red round stop icon, two lines of text, OK and Cancel buttons
* a black-outlined WHITE ARROW cursor
* a grey TASKBAR: Start button, a pressed task button, a sunken tray with a clock
* bitmap system font, NO anti-aliasing anywhere: every edge pixel-crisp
The result should feel like someone:
OPENED THE CLIP IN A 1995 MEDIA PLAYER
→ ON A 640x480, 256-COLOUR DESKTOP
→ WHILE THE MACHINE THREW ERROR MESSAGES
→ CLICKED OK ON EACH ONE
→ AND SCREEN-CAPTURED THE WHOLE DESKTOP
→ FRAME-BY-FRAME.
CHARACTER — INSIDE THE PLAYER, UNCHANGED
The people stay PHOTOGRAPHIC inside the video well; only the playback quality changes.
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
Do NOT redraw, cartoonise or pixel-art the people.
Do NOT crop faces out of the video well.
VIDEO-IN-WINDOW RULES
* The whole source frame plays inside the window's video well, same composition, scaled down.
* Playback looks like 1995 software video: about 320x240 or lower, chunky square pixels.
* 256 colours: a web-safe-style colour cube with a fine ORDERED (Bayer) dither pattern in gradients.
* Slight colour banding in skin and walls is expected.
* No blur, no smoothing, no modern sharpening.
WINDOW CHROME RULES
* Light grey face colour (#C0C0C0) with the classic two-pixel bevel: white and light grey on the top-left, dark grey and black on the bottom-right.
* Title bar: solid navy (#000080) with bold white text, e.g. "office_clip.avi - Media Player".
* Pressed controls and sunken areas invert the bevel.
* The seek-bar thumb moves left to right in step with the clip's playback; the time readout counts up.
* A second, inactive window (grey title bar) may peek out behind the player.
DESKTOP RULES
* Desktop: flat teal (#008080), no wallpaper image.
* Icons down the left edge: original pixel art (a computer, folders, a text document, a globe, a bin) with white text labels.
* Taskbar along the bottom: a bevelled "Start" button with a small original computer glyph, task buttons, a sunken tray with a speaker and a clock.
ERROR DIALOG CASCADE
* Every second or two, a new grey "Error" dialog pops up with a red round stop icon, two short lines of text and OK / Cancel buttons.
* Each new dialog sits a little lower and to the right of the previous one, building a cascade.
* The cascade stays over the LOWER RIGHT of the screen and never covers a face.
* Messages are original, short, playful system-error jokes (e.g. "Cannot find FRIENDS.EXE.").
* Once a dialog appears, it stays put in later frames.
CURSOR
* A white arrow cursor with a black outline glides around the desktop and moves to the OK button of each new dialog.
* Its motion is smooth between frames; it never teleports.
PALETTE
Teal #008080, grey #C0C0C0, dark grey #808080, white, black, navy #000080.
Accent: red stop icon, yellow folders, blue screen glyphs.
The video keeps its own (256-colour) colours.
Do NOT add gradients, glass, transparency, drop shadows or rounded corners to the UI.
OBJECT CONTINUITY
If the character holds an object, it stays in the video exactly as filmed.
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
The video inside the window must match the source frame exactly.
The window, icons and taskbar do NOT move.
NO frozen video frame.
NO repeated video frame.
FRAME-TO-FRAME UI CONTINUITY
THIS IS CRITICAL.
It must feel like one continuous screen recording.
Between consecutive frames:
* the video advances one frame
* the seek thumb and time readout advance
* the cursor moves smoothly
* new dialogs pop in at their planned frames and then stay
Keep FIXED:
* window position and size
* icon positions and labels
* taskbar and clock
* the dither pattern style and palette
DO NOT
Do NOT use Windows XP / Vista / modern UI: no glossy blue title bars, rounded windows or glass.
Do NOT use any real company logo, the four-colour flag logo or a branded start orb.
Do NOT anti-alias text or edges.
Do NOT put dialogs, cursor or icons over faces.
Do NOT add CRT curvature, scanlines or VHS noise.
Do NOT turn the people into pixel art or cartoons.
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
* NO desktop, windows or taskbar
* NO dialogs or cursor
* NO colour reduction or dither
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
Do NOT begin the Windows 95 desktop transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – WINDOWS 95 DESKTOP STYLING (AFTER MY CONFIRMATION ONLY)
First, give me the layout plan: window position and size, icon list, taskbar contents, and the frame numbers and texts of every error dialog. Keep the layout fixed for the whole clip.
Then style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation, so the video inside the window is exactly that frame.
Apply every style rule above, with the SAME desktop layout on every frame.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing, layout, seek-bar progress or dialog continuity broke — regenerate those frames only.
The final video must feel like A SCREEN RECORDING FROM 1995: teal desktop, grey bevelled media player, 256-colour dithered video, error pop-ups piling up, a cursor clicking OK, 12 frames per second.
The image should deliberately contain:
* a flat teal desktop with pixel icons
* grey bevelled window chrome with a navy title bar
* low-res 256-colour dithered video
* a cascade of error dialogs
* an arrow cursor
* a grey taskbar with Start and a clock.
Avoid modern, glossy or anti-aliased UI.
```
