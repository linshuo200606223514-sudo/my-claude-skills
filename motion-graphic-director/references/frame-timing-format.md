# Frame Timing Document Format

## What This Document Is

The **frame timing document** (`frame-timing-[name].md`) is the engineering specification
produced between design approval and code. It translates every creative decision in the design
doc into exact frame numbers, range by range.

**Frame is the unit of everything here.** Not seconds. Not "about halfway through the scene."
Absolute frame numbers across the full composition, plus local frame numbers inside each scene
component. Both are always shown so there is never any ambiguity when writing code.

This document answers four questions before a single line of Remotion is written:

1. At exactly which absolute frame does each visual event start and end?
2. What is the local frame equivalent (what `useCurrentFrame()` returns inside the component)?
3. What is happening during every transition window and why that transition?
4. Is there any dead air, frame math error, or spring misconfiguration that will look wrong at render?

If you cannot fill in this document precisely, the design is not ready for code. Go back to
the design doc and sharpen the decisions.

---

## How to Produce It

### Step 1 — Run the frame calculator

```bash
python scripts/frame_calculator.py \
  --fps 30 \
  --durations <S1> <S2> ... <SN> \
  --transition <T> \
  --names "<name1>" "<name2>" ... \
  --last-anim <last_anim_local_1> <last_anim_local_2> ... \
  --springs "label:damping:stiffness" ...
```

Copy the output verbatim into the header of your frame timing document. This is your
ground truth. Do not compute these numbers by hand — arithmetic errors propagate silently
into code and produce videos that cut early, cut late, or have wrong-duration transitions.

### Step 2 — Fill the per-scene beat tables

For every scene, produce a table of frame ranges covering every distinct animation beat:
entry, hold, state change, exit. Ranges must be contiguous — there must be no gap and no
overlap between rows (except during the transition window rows, which are explicitly tagged).

### Step 3 — Fill the per-transition sections

For every transition, write a dedicated section describing:
- The absolute overlap window (start/end frame, which is also scene N local end and scene N+1 local start)
- What presentation is used and the exact API call
- The editorial reason this transition type was chosen at this narrative beat
- What each scene is doing during the overlap (scene N exiting, scene N+1 entering)
- Any known risks specific to this transition at this position

### Step 4 — Run dead air and spring checks

The calculator flags dead air automatically (given `--last-anim`). For springs, pass
every `spring()` config used in the video to `--springs` and verify all ζ values are in
the intended range before writing code.

---

## Document Format

```
# Frame Timing Document: [Video Name]

**Composition:** [width]×[height] | [fps]fps | Total: [N]f ([Ns]s)
**Transition duration:** [T]f each | [count] transitions

---

## Absolute Frame Map

[paste calculator output here verbatim]

---

## Scene [N] — [Name]
**Absolute: [start]–[end] | Duration: [dur]f | Local 0 = absolute [start]**

| Frame Range (local) | Absolute Range | What Happens | Notes / Risks |
|---------------------|----------------|--------------|---------------|
| 0–N                 | A–B            | ...          | ...           |
| ...                 | ...            | ...          | ...           |

**Dead air check:** [result from calculator, or manual reasoning]
**Spring configs used:** [list every spring() call with ζ and settle frames]

---

## Transition [N]→[N+1]: [PresentationName]({ [options] })
**Absolute overlap: [start]–[end] | Duration: [T]f**
**Scene [N]  local [exit_start]–[exit_end]  [exiting]**
**Scene [N+1] local 0–[T-1]  [entering]**

**Presentation:** `[import path]` — `[function]({ [options] })`
**Timing:** `linearTiming({ durationInFrames: [T] })` (or springTiming if applicable)

**Intent:** [Why this specific transition type at this specific narrative beat. What spatial
or emotional logic does the motion reinforce? What would be wrong about using a different type here?]

**What each scene is doing during the overlap:**
- Scene [N] (local [exit_start]–[exit_end]): [describe what is still visible / animating]
- Scene [N+1] (local 0–[T-1]): [describe what the new scene shows during its entry frames]

**Risk:** [Anything that can go wrong at this specific transition point]

---
```

---

## Worked Example: VibeCodingPRD

The following is the complete frame timing document for the VibeCodingPRD video. Use this
as the quality and detail benchmark. Every future video must meet this standard.

---

# Frame Timing Document: VibeCodingPRD

**Composition:** 1080×1920 | 30fps | Total: 935f (31.17s)
**Transition duration:** 15f each | 5 transitions

---

## Absolute Frame Map

```
======================================================================
  ABSOLUTE FRAME TIMELINE
  FPS: 30  |  Transition: 15f each  |  Total: 935f = 31.17s
======================================================================

  [   0–149]  SCENE 1: Hook           (150f = 5.0s)
              local 0 = absolute 0  |  local 149 = absolute 149

  [ 135–149]  ── TRANSITION 1→2  (15f) ──
              Hook                  local 135–149  [exiting]
              Definition            local   0– 14  [entering]
              Scene 2 local 0 = absolute 135

  [ 135–314]  SCENE 2: Definition     (180f = 6.0s)
              local 0 = absolute 135  |  local 179 = absolute 314

  [ 300–314]  ── TRANSITION 2→3  (15f) ──
              Definition            local 165–179  [exiting]
              Solution              local   0– 14  [entering]
              Scene 3 local 0 = absolute 300

  [ 300–449]  SCENE 3: Solution       (150f = 5.0s)
              local 0 = absolute 300  |  local 149 = absolute 449

  [ 435–449]  ── TRANSITION 3→4  (15f) ──
              Solution              local 135–149  [exiting]
              Demo                  local   0– 14  [entering]
              Scene 4 local 0 = absolute 435

  [ 435–644]  SCENE 4: Demo           (210f = 7.0s)
              local 0 = absolute 435  |  local 209 = absolute 644

  [ 630–644]  ── TRANSITION 4→5  (15f) ──
              Demo                  local 195–209  [exiting]
              Processing            local   0– 14  [entering]
              Scene 5 local 0 = absolute 630

  [ 630–829]  SCENE 5: Processing     (200f = 6.7s)
              local 0 = absolute 630  |  local 199 = absolute 829

  [ 815–829]  ── TRANSITION 5→6  (15f) ──
              Processing            local 185–199  [exiting]
              Dialogue              local   0– 14  [entering]
              Scene 6 local 0 = absolute 815

  [ 815–934]  SCENE 6: Dialogue       (120f = 4.0s)
              local 0 = absolute 815  |  local 119 = absolute 934

======================================================================
  TOTAL: 935 frames = 31.17s
  Verify: 150+180+150+210+200+120 - (5×15) = 1010 - 75 = 935
======================================================================
```

---

## Scene 1 — Hook
**Absolute: 0–149 | Duration: 150f | Local 0 = absolute 0**

| Frame Range (local) | Absolute Range | What Happens | Notes / Risks |
|---------------------|----------------|--------------|---------------|
| 0–44                | 0–44           | 20 terminal chaos lines scroll upward via `translateY` 0→-420px. Lines are dim `#3A3A5A`. Vignette fades in 0–15. | Scroll speed must feel frantic, not leisurely. `-420px` over 45f = 9.3px/frame. |
| 45                  | 45             | Hard freeze — all lines snap to `COLORS.STATE_ERROR` (red). Instant, no easing. | Single-frame color swap. The snap IS the effect. No interpolation. |
| 46–52               | 46–52          | ERROR stamp springs into center. `spring({ damping:10, stiffness:300 })` ζ≈0.63. Scale 0→1 with slight overshoot. Border + glow also appear. | Settles ~20f. ζ=0.63 gives a readable single overshoot pop. If damping drops below 8 this oscillates. |
| 53–72               | 53–72          | **ERROR_HOLD** — stamp is fully visible, nothing moves. Deliberate 20-frame static hold (~0.67s). | This is intentional dead air. The viewer must have time to read "[ERROR]" and feel the problem before the glitch punishes it. Do not shorten. |
| 73–78               | 73–78          | RGB glitch overlay — red channel offset +6px, cyan channel offset -4px. Intensity driven by `Math.sin((frame - 73) * 2.5)`. | 6 frames only. Longer reads as lag, not glitch. |
| 79–90               | 79–90          | Chaos lines + ERROR stamp fade out together (`interpolate` opacity 1→0 over 12f). | Both elements must exit simultaneously so nothing lingers to ghost into the void. |
| 91–98               | 91–98          | **Void** — pure black screen. 8 frames of breath. Nothing moves. | Intentional vacuum beat. Viewer's eye resets. Do not fill with anything. |
| 99–110              | 99–110         | "PRD" typewriters in: 3 chars × 4f each. 120px JetBrains Mono, `COLORS.ACCENT`. `voidProgress` opacity 0→1 from frame 91. | Cursor `|` blinks every 8f during typing. Cursor stays visible until frame 141. |
| 111–125             | 111–125        | "// the fix" fades in below PRD. `interpolate` opacity 0→1 over 15f. 28px, `COLORS.TEXT_DIM`. | Gives narrative purpose to "PRD" appearing. Without this, 3 green letters floating on black read as incomplete. |
| 126–134             | 126–134        | Hold. PRD glow pulse (`Math.sin` on `textShadow` intensity). Cursor blinks. | Alive — not static. Two micro-animations keep the frame from dying before the transition exit. |
| 135–149             | 135–149        | **TRANSITION EXIT** — TransitionSeries slides Scene 1 leftward as Scene 2 arrives. Scene 1 is still rendering its local frames 135–149 during this window. | PRD + subtitle remain visible and legible as they slide out. Glow pulse continues. |

**Dead air check:** Last authored animation ends at local 125 (subtitle fade complete).
Frames 126–134 have glow pulse + cursor blink — never fully static. Transition exit
begins at local 135. That is 9 idle frames (125→134) — well inside the 22f budget. ✓

**Spring configs used:**
- ERROR stamp entrance: `damping:10, stiffness:300` → ζ = 0.632. Settles ≈ 20f. Single overshoot to ~108% scale. ✓

---

## Transition 1→2: `slide({ direction: 'from-right' })`
**Absolute overlap: 135–149 | Duration: 15f**
**Scene 1 local 135–149 [exiting, slides left]**
**Scene 2 local 0–14 [entering, slides in from right]**

**Presentation:** `import { slide } from '@remotion/transitions/slide'` — `slide({ direction: 'from-right' })`
**Timing:** `linearTiming({ durationInFrames: 15 })`

**Intent:** The PRD has appeared as the answer to chaos. Now the actual PRD document
physically pushes in from the right — as if the document is arriving in response to the
idea. Spatial logic reinforces narrative: PRD concept (Scene 1, now exiting left) → PRD
document (Scene 2, arriving from right). The rightward direction = "the next thing" in
Western reading culture. A fade here would dissolve the spatial momentum. A wipe would be
arbitrary. Slide is the only choice that creates physical causality between scenes.

**What each scene is doing during the overlap:**
- Scene 1 (local 135–149): PRD text + "// the fix" subtitle are still visible, sliding
  leftward with the container. Glow pulse is still running.
- Scene 2 (local 0–14): Scene 2 uses `WIPE_DURATION = 10`, meaning document lines do not
  start drawing until local frame 10. During local 0–9 the Scene 2 container is the navy
  background arriving from the right — no premature content flash.

**Risk:** Scene 2's outermost `AbsoluteFill` must not have a `clipPath`, `transform`, or
any entry animation on it. TransitionSeries wraps the component in its own container and
applies the slide transform to that wrapper. Any clip-path on the inner `AbsoluteFill` will
clip the content to nothing during the entry slide and the scene will appear as a blank
panel arriving. The `clipPath` radial wipe that was originally on Scene 2 caused exactly
this failure — the container slid in but the circle was at 0% radius so nothing was visible.

---

## Scene 2 — Definition
**Absolute: 135–314 | Duration: 180f | Local 0 = absolute 135**

| Frame Range (local) | Absolute Range | What Happens | Notes / Risks |
|---------------------|----------------|--------------|---------------|
| 0–14                | 135–149        | **Transition overlap** — Scene 2 is arriving (TransitionSeries slide). Navy BG visible. No content yet. Intentional. | `WIPE_DURATION = 10` means lines don't start until local 10. Use this buffer: 10 frames of clean navy arrival before content appears. |
| 0–9                 | 135–144        | Navy background settles in. `// product-requirements.md` label fades in (`interpolate` 0→1 from local `WIPE_DURATION` to `WIPE_DURATION + 15`). | Label fade starts at local 10, overlapping with lines. Fine — different vertical position. |
| 10–149              | 145–284        | 14 doc lines draw themselves one by one. Each line: 10f to draw. `lineStart = WIPE_DURATION + i * 10`. Headers snap to `COLORS.ACCENT` on completion. Progress bar fills on right edge. | Cursor `|` blinks on the actively-drawing line. Each completed header gets a green glow. The visual rhythm of completion is the teaching. |
| 158                 | 293            | Last line draw completes (14 lines × 10f + 10 offset = 150f → local 150. Wait, let's be precise: last line i=13, lineStart = 10 + 13*10 = 140, lineEnd = 150. So last line completes at local 150, absolute 285). | Verify: DOC_LINES.length = 14 including empty spacer lines. Empty spacers render as 12px height divs, not drawn lines. Actual text lines = 11. Adjust i count. |
| 150–165             | 285–300        | All lines drawn. Progress bar at 100%. Hold — headers glow softly. | 15f of rest after completion. Not dead air: 3 green headers are glowing. |
| 165–179             | 300–314        | **TRANSITION EXIT** — Scene 2 slides/wipes out as Scene 3 arrives. | Scene 2 still rendering during this overlap window. |

**Dead air check:** Last animation (line draw completion) ends at approximately local 150.
Transition exit begins at local 165. That is 15f of hold — within the 22f budget. ✓
The 3 green glowing headers make this read as a living frame, not a freeze. ✓

**Spring configs used:** None. All animations in this scene use `interpolate`.

---

## Transition 2→3: `wipe({ direction: 'from-left' })`
**Absolute overlap: 300–314 | Duration: 15f**
**Scene 2 local 165–179 [exiting, wiped away from left]**
**Scene 3 local 0–14 [entering, wipes in from left]**

**Presentation:** `import { wipe } from '@remotion/transitions/wipe'` — `wipe({ direction: 'from-left' })`
**Timing:** `linearTiming({ durationInFrames: 15 })`

**Intent:** The PRD document has been defined. Now the solution — the custom GPT tool —
sweeps in from the left like a page being turned. The wipe direction (left → right) visually
reads as "flipping to the answer" — the same left-to-right direction as reading, the same
direction as progress. A slide would feel redundant (we already slid in Scene 2). A fade
would lose the spatial decisiveness. The wipe has a hard edge that feels like a reveal — the
GPT is being unveiled.

**What each scene is doing during the overlap:**
- Scene 2 (local 165–179): All doc lines fully drawn, headers glowing green. This completed
  state is what gets wiped away — the viewer's last impression of the doc is "done, structured,
  complete" before the tool that generates it is revealed.
- Scene 3 (local 0–14): Scene 3's entry animation (if any) runs during these frames. Ensure
  no Scene 3 intro clip-path or entry transform on the outermost element.

**Risk:** Same outermost-element rule applies. Scene 3 must not have a clip-path or entry
transform on its container.

---

## Scene 3 — Solution
**Absolute: 300–449 | Duration: 150f | Local 0 = absolute 300**

| Frame Range (local) | Absolute Range | What Happens | Notes / Risks |
|---------------------|----------------|--------------|---------------|
| 0–14                | 300–314        | Transition overlap — Scene 3 arriving via wipe. | Scene 3 content should be immediately visible as the wipe line crosses. |
| 0–20                | 300–320        | Scene label `// custom-gpt.tool` fades in. Card A (Without GPT) springs in from left. | Card A width is a fixed value. Do not use a hard frame switch for Card B width. |
| 20–60               | 320–360        | Card A content types in line by line. Card A shows "before" state (red/dim content). | Typewriter paced at character/frame rate matching readability at 30fps. |
| 60–90               | 360–390        | Card B (With GPT) springs in from right. Width begins interpolating from 0 to full. | **Card B width MUST be interpolated, not a hard conditional.** `interpolate(frame, [60, 75], [0, cardWidth], { extrapolateRight: 'clamp' })`. Hard switch = visible snap. |
| 70–110              | 370–410        | Card B content types in. Green accent highlights on each completed line. | Cursor on active line. Color: `COLORS.ACCENT`. |
| 110–130             | 410–430        | Both cards fully drawn. Side-by-side contrast fully visible. | Both cards alive — green glow on Card B headers. |
| 130–149             | 430–449        | Hold. Both cards static but visually rich (glowing headers). Transition exit begins at local 135. | 5f of hold (130–135) before transition exits. Tight but acceptable given visual richness. |

**Dead air check:** Last authored animation ends local ≈ 110. Transition starts local 135.
That is 25f of hold — 3f over the 22f budget. If it reads static in preview, shorten
scene to 145f (trim 5f, cut the budget to 10f over, but glowing cards reduce the dead-air
read). Alternatively add a subtle ambient animation (glow pulse on Card B) from local 110
to bridge.

**Spring configs used:**
- Card A entrance: `damping:12, stiffness:200` → ζ = 0.849. Settles ≈ 16f. Near-critical, smooth. ✓
- Card B entrance: `damping:12, stiffness:200` → ζ = 0.849. ✓

---

## Transition 3→4: `fade()`
**Absolute overlap: 435–449 | Duration: 15f**
**Scene 3 local 135–149 [exiting, fading out]**
**Scene 4 local 0–14 [entering, fading in]**

**Presentation:** `import { fade } from '@remotion/transitions/fade'` — `fade()`
**Timing:** `linearTiming({ durationInFrames: 15 })`

**Intent:** The solution has been presented (Scene 3 — static, analytical, side-by-side
comparison). Scene 4 is a live demo — dynamic, personal, in-progress. The tonal register
changes completely. A slide or wipe here would impose spatial logic on a conceptual jump.
A fade dissolves cleanly — "we're moving to a different dimension of the same story, not
a different location." Fade = temporal shift, wipe/slide = spatial shift. This beat is
temporal.

**What each scene is doing during the overlap:**
- Scene 3 (local 135–149): Both cards at full opacity, glowing. They dissolve out.
- Scene 4 (local 0–14): Waveform and REC indicator fade in (`waveformOpacity` interpolates
  0→1 over local 0–10). The waveform appearing through the fade-out of the cards creates
  a "the tool coming to life" visual metaphor.

**Risk:** None specific. `fade()` is the safest transition type — no spatial conflicts
possible. Both scenes simply cross-dissolve via opacity.

---

## Scene 4 — Demo
**Absolute: 435–644 | Duration: 210f | Local 0 = absolute 435**

| Frame Range (local) | Absolute Range | What Happens | Notes / Risks |
|---------------------|----------------|--------------|---------------|
| 0–10                | 435–445        | Waveform bars fade in. REC indicator appears (blinks every 15f). Scene label fades in. | Waveform multi-frequency sine: `Math.sin(frame/7 + i*0.5)` + harmonics. Always moving. |
| 8–N                 | 443–...        | Transcription typewriter begins. `CHARS_PER_FRAME = 0.8`. 74-char TRANSCRIPT → `TRANSCRIPT_END = 8 + ceil(74/0.8) = 8 + 93 = 101`. | **TRANSCRIPT_END must be derived from actual char count, never hardcoded.** Hardcoding causes PHASE2 to fire mid-sentence. |
| 101                 | 536            | Transcript complete. | PHASE2_START = 101 + 12 = 113. 12f deliberate pause before pills. |
| 113–178             | 548–613        | 4 question pills pop in. `PILL_INTERVAL = 8`. Pill i starts at `PHASE2_START + 12 + i*8`. Waveform fades to 20% opacity. REC fades out over 10f. Transcript fades to 40% opacity. | `staccatoPop: damping:28, stiffness:400` → ζ = 0.700. Single overshoot to ≈105%, settles ≈12f. **Must not use damping:8 — that is ζ=0.200, continuous oscillation.** |
| 178–194             | 613–629        | All 4 pills fully settled. Blinking cursor `> |` appears after last pill. | Pills alive via cursor blink. Not dead air. |
| 195–209             | 630–644        | **TRANSITION EXIT** — Demo slides upward as Processing arrives from bottom. | Scene 4 content still rendering and moving (cursor blink) during the exit slide. |

**Dead air check:** Last animation (last pill settle) ends at approximately local 178.
Transition starts at local 195. That is 17f of hold — within the 22f budget. ✓
Cursor blink is running throughout this hold — frame is alive. ✓

**Spring configs used:**
- `staccatoPop`: `damping:28, stiffness:400` → ζ = 0.700. Settles ≈ 12f. Single clean overshoot. ✓

---

## Transition 4→5: `slide({ direction: 'from-bottom' })`
**Absolute overlap: 630–644 | Duration: 15f**
**Scene 4 local 195–209 [exiting, slides upward]**
**Scene 5 local 0–14 [entering, slides up from bottom]**

**Presentation:** `import { slide } from '@remotion/transitions/slide'` — `slide({ direction: 'from-bottom' })`
**Timing:** `linearTiming({ durationInFrames: 15 })`

**Intent:** The question pills are on screen — the viewer has asked the AI questions and is
waiting. Scene 5 (the AI response — alignment + PRD delivery) physically rises up from below,
as if the answer is emerging from underneath, being produced. The upward direction creates
momentum toward the CTA. It also creates vertical spatial logic: question (demo, on screen)
→ answer (processing, rising from below). A fade here would lose this emergence quality.

**What each scene is doing during the overlap:**
- Scene 4 (local 195–209): Question pills at full opacity with cursor blinking. They slide
  upward and off screen as Scene 5 rises. The pills exiting upward while Scene 5 rises from
  below creates a visual exchange — pills go up, answers come up behind them.
- Scene 5 (local 0–14): Scene 5 has a green bar entry sweep (local 0–12) followed by a
  flash fade (local 12–18). During the transition overlap (local 0–14), the green sweep bar
  is actively animating. This means the transition landing is not blank — the green flash
  plays simultaneously with the slide, creating a kinetic entry moment.

**Risk:** The Scene 5 green entry sweep is intentionally kept. It is a within-scene
animation, not an entry transform on the container, so it does not conflict with
TransitionSeries. Verified: the green sweep is a positioned `div` with an interpolated
`width`, not a clip-path on the outermost `AbsoluteFill`.

---

## Scene 5 — Processing
**Absolute: 630–829 | Duration: 200f | Local 0 = absolute 630**

| Frame Range (local) | Absolute Range | What Happens | Notes / Risks |
|---------------------|----------------|--------------|---------------|
| 0–12                | 630–642        | Green sweep bar races across screen (width 0→100% over 12f). | Entry flash. Linear, fast — ~91px/frame at 1080px width. |
| 12–18               | 642–648        | Green bar fades out (opacity 1→0 over 6f). | Bar exits before content appears. |
| 18–N                | 648–...        | Alignment section: icons fade in, doc sections stack. `ICONS_START = 18`. | Section order tied to `ALIGN_FADE_OUT` and `DOC_DROP_START`. |
| N–177               | ...–807        | Last doc section settled / last glow flash complete. | Final authored animation. |
| 177–184             | 807–814        | Hold — doc visible, glow on final section. | 7f before transition exit. Tight but alive — glow is running. |
| 185–199             | 815–829        | **TRANSITION EXIT** — Processing fades out as Dialogue fades in. | `fade()` transition — both scenes cross-dissolve. |

**Dead air check:** Last animation ends local ≈ 177. Transition starts at local 185. 8f hold. ✓

---

## Transition 5→6: `fade()`
**Absolute overlap: 815–829 | Duration: 15f**
**Scene 5 local 185–199 [exiting, fading out]**
**Scene 6 local 0–14 [entering, fading in]**

**Presentation:** `import { fade } from '@remotion/transitions/fade'` — `fade()`
**Timing:** `linearTiming({ durationInFrames: 15 })`

**Intent:** Scene 5 is high-information density — alignment checks, doc sections, glow
effects. Scene 6 is the CTA vacuum — near-white, minimal, one call to action. The tonal
shift is the most extreme in the video. A hard cut or directional slide would be jarring.
A fade is the cinematic convention for "the last image dissolves and we emerge into something
new" — it signals finality and resolution, not continuation. The fade pulls the viewer from
the technical into the human.

**What each scene is doing during the overlap:**
- Scene 5 (local 185–199): All doc sections fully visible. Fading out. The complexity
  dissolves.
- Scene 6 (local 0–14): Scene 6 has a white background layer that fades in over 6 frames,
  and the editor content that fades in. During the fade transition the light background of
  Scene 6 is bleeding in through the fade — creating a brightening effect as the dark
  complexity of Scene 5 dissolves away.

**Risk:** Scene 6 must not have an abrupt vacuum cut (instant jump to white). The white
background must fade in over ≥6 frames (interpolated opacity) so there is no single-frame
white flash. A single-frame white flash reads as a encoding error to viewers.

---

## Scene 6 — Dialogue
**Absolute: 815–934 | Duration: 120f | Local 0 = absolute 815**

| Frame Range (local) | Absolute Range | What Happens | Notes / Risks |
|---------------------|----------------|--------------|---------------|
| 0–6                 | 815–821        | White background layer fades in (opacity 0→1 over 6f). | Prevents flash. Must be an interpolated fade, not instant. |
| 0–14                | 815–829        | Transition overlap — Scene 6 brightening as Scene 5 dissolves. | White BG + fade transition = controlled brightening effect. |
| 15–89               | 830–904        | Editor UI elements fade in. Typewriter content. CTA text appears. | Transition fully resolved by local 14. All Scene 6 content in clean frame. |
| 89–95               | 904–910        | Dissolve moment — editor fades, CTA holds. | 6f dissolve, not instant. Must be interpolated. |
| 95–119              | 910–934        | CTA holds. Minimal motion — vacuum aesthetic. | A single-pixel cursor blink or button pulse keeps it alive. Pure static is wrong. |

**Dead air check:** Last authored animation (CTA settling) ends at approximately local 95.
Scene ends at local 119. That is 24f of hold — 2f over the 22f budget. CTA scene holds are
acceptable at 25f because the viewer is reading the call to action. Ensure a micro-animation
(cursor blink, button pulse) runs through this hold.

---

## Frame Math Verification

```
TOTAL = 150 + 180 + 150 + 210 + 200 + 120 - (5 × 15)
      = 1010 - 75
      = 935 frames = 31.17s  ✓

Root.tsx durationInFrames = SCENE_TIMING.TOTAL = 935  ✓

Transition windows (no gaps, no overlaps):
  T1: abs 135–149  (S1 end overlap)
  T2: abs 300–314  (S2 end overlap)
  T3: abs 435–449  (S3 end overlap)
  T4: abs 630–644  (S4 end overlap)
  T5: abs 815–829  (S5 end overlap)
```

---

## Rules for Writing Frame Timing Documents

**1. Frame ranges are inclusive on both ends.**
`[0–44]` means frames 0, 1, 2, … 44. That is 45 frames. `[44–44]` is a single frame.

**2. Every beat table must be exhaustive.**
There must be no unexplained gap. If a range has nothing authored, say "Hold — [description
of what is still visible / what micro-animation keeps it alive]". Never write a table that
skips a range.

**3. Local and absolute are always both shown.**
Every range shows `(local)` and `(absolute)` columns. Never drop one. The developer will
write code in local frames (`useCurrentFrame()`) and you need to verify intent in absolute
frames. Having only one is how timing bugs go undetected.

**4. Transition sections are mandatory for every transition.**
Do not summarize transitions in the scene table and move on. Each transition deserves its
own section with intent, API call, risk, and a description of what both scenes are doing
during the overlap window.

**5. Dead air check is mandatory for every scene.**
Calculate: `idle_frames = (scene_duration - transition_duration) - last_animation_end_local`.
If `idle_frames > 22`, the scene has a static tail. Either shorten the duration or add a
micro-animation (pulse, blink, glow) to bridge the gap.

**6. Spring configs must be verified before code is written.**
Run every `spring()` call through the calculator. If ζ < 0.5, the spring is misconfigured
for a pop — it will oscillate continuously. Fix damping before writing the component.

**7. Do not write this document in seconds.**
Duration of 5.0s is a label only. The spec is in frames. "Frame 53" not "frame at 1.77s."
The developer uses frames. Seconds are for human legibility in headings only.
