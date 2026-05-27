# Design Document Format

## Overview

The design document (`video-design-[name].md`) is the artifact produced after script analysis and visual ideation. It is what the user reviews and approves before any code is written. It must be detailed enough that a skilled Remotion developer could implement every scene without asking questions.

## Script MD Format

`script-[name].md` — produced from an SRT or raw voiceover:

```markdown
# Video Script — [Topic]

**Duration:** ~[N] seconds  
**Core Thesis:** [One sentence: what is this video proving?]  
**Target Viewer:** [Who is this for, what do they care about?]

---

## Segment Breakdown

### [0:00 - 0:04] [Scene Name]
> "[Exact voiceover words]"

### [0:04 - 0:08] [Scene Name]
> "[Exact voiceover words]"

[...continue for all segments...]
```

---

## Design Document Format

`video-design-[name].md` — the ideation output for user approval:

### Header Block (before segments)

```markdown
# Video Design — [Topic]

## Visual Identity

**Palette:** [Background color description] + [Primary accent: hex/name] + [State color if used]  
**Color Meaning:** [Accent] = [what it signals] | [State color] = [what it signals]  
**Typography:** [Chosen register and why — e.g., "Monospace for terminal authenticity"]  
**Dominant Metaphor:** [The central visual metaphor for the video's core thesis]  
**Narrative Arc:** [e.g., "Problem → Solution → Proof" or "Mystery → Explanation → Connection"]  
**Signature Animations:** [2-3 animation moves used consistently, e.g., "bouncy 3D button drops, radial star wipes, staccato checkmark pops"]

---
```

### Per-Segment Format

Each segment uses this exact 4-subsection structure:

```markdown
## [timestamp range] | [Scene Name]

**Backgrounds & Tints:** [Color, texture, vignette, depth treatment. What is the environment doing and what does that signal to the viewer?]

**Motion Graphics & Typography:** [Every element on screen: what it is, how it enters, what it does, how it exits. Be specific about direction, scale, easing character. Include exact text content.]

**Transitions & Pacing:** [How this segment transitions out. Easing curve description. Density level. Timing relationship to voiceover.]

**Editorial Thinking/Intent:** [Why these specific choices were made. What is the viewer's mental state? What question does this segment answer or raise? What psychological mechanism is being used?]
```

---

## Worked Example

Below is a partial design document demonstrating the correct level of detail. Use this as the quality bar.

---

### Example: Hypothetical "How Webhooks Work" video

```markdown
# Video Design — How Webhooks Work

## Visual Identity

**Palette:** Near-black (#0D0D0D) background + electric cyan (#00E5FF) accent + warning red (#FF3B30) for failure states  
**Color Meaning:** Cyan = data flowing correctly / active system | Red = failure, disconnection, broken state  
**Typography:** Monospace (terminal font) for all code/data elements; bold geometric sans for concept labels  
**Dominant Metaphor:** Webhooks as a doorbell — the house (your app) doesn't keep checking the street; it waits to be rung  
**Narrative Arc:** Problem → Solution → Proof  
**Signature Animations:** Spring-bounce UI panels, SVG line self-drawing for data paths, staccato pop for success confirmations

---

## 0:00 - 0:04 | The Polling Problem

**Backgrounds & Tints:** Near-black background with a heavy cinematic vignette. The center of the frame is slightly lighter than the edges. No texture yet — pure void aesthetic to establish a technical, serious tone from frame one.

**Motion Graphics & Typography:** A stylized browser window (white, rounded corners, drop shadow) sits centered. Inside it, a rotating loading spinner in cyan cycles. Above the window, a counter labeled "Request #1... #2... #3... #47..." increments rapidly in monospace font. Each number ticks up in a hard cut, no easing — mechanical and relentless.

**Transitions & Pacing:** After the counter hits #47, it freezes. A large red "NOTHING" label stamps down over the window with a heavy spring bounce (damping 8, overshoot to 115%). The pacing here is dense — the counter ticks fast enough to feel exhausting. This is the viewer feeling the problem, not just seeing it.

**Editorial Thinking/Intent:** The viewer is being made to feel the inefficiency of polling before the word "polling" is ever spoken. By making the counter feel relentless and the payoff be "NOTHING," we create frustration in the opening segment. This hooks the viewer because they recognize the feeling and want to know how to fix it.

---

## 0:04 - 0:08 | The Pattern Interrupt

**Backgrounds & Tints:** Background flashes briefly to pure white for 3 frames (the interrupt flash), then settles to a warm off-white. The stark tonal shift from void-black to near-white is jarring — this is intentional.

**Motion Graphics & Typography:** The browser window shrinks and slides off-screen left (spring, damping 15). A black-and-white image of someone furiously refreshing a browser (recognizable internet behavior) pops in from the right with an orange drop shadow. The text "literally you right now" appears below it in a casual handwritten font. After 1.5 seconds, the image shatters (shatter effect, shards fly outward) and the frame clears.

**Transitions & Pacing:** Hard cut in, hard cut out. No easing on the meme — it snaps in, sits, then disappears. The total duration of the meme moment is 2 seconds. The remaining 2 seconds transition to the solution text.

**Editorial Thinking/Intent:** This is the pattern interrupt. The video built a tense, serious technical environment, then immediately broke it with a relatable, low-effort meme. The viewer laughs (or at least reacts) — this involuntary response resets their attention. The "literally you right now" text confirms the video is talking to them personally, building rapport before the teaching begins.

---

## 0:08 - 0:12 | Introducing the Doorbell

**Backgrounds & Tints:** Background settles to clean off-white. The darkness of the opening is gone — we are in "solution mode" now. The color shift from dark to light is the subconscious signal that we've moved from problem to answer.

**Motion Graphics & Typography:** A simple, flat-style house illustration drops into frame from above (spring, damping 12). To the left of the house, a server rack icon slides in from the left. Between them, a doorbell button icon appears with a small "DING" label. The label "Your App" appears below the house; "External Service" below the server. These labels fade in at 60% opacity — supporting info, not the focus.

**Transitions & Pacing:** Medium density. Three elements, all entering within 2 seconds of each other. Entrance animations are playful spring bounces — this is the moment of relief after the tense opening. The doorbell button pulses subtly (scale 1.0 → 1.05 → 1.0 loop) to draw the eye to it.

**Editorial Thinking/Intent:** The doorbell metaphor is introduced before the voiceover explains it. The viewer sees the setup (house, server, doorbell) and their brain begins making the connection before the words arrive. When the VO then says "instead of your app constantly asking if anything changed, the server rings your doorbell," the visual and audio track arrive at the same conclusion simultaneously — this double-confirmation creates a strong comprehension moment.
```

---

## Completeness Checklist

Before finalizing the design doc, verify every segment has:

- [ ] A background description with color AND depth treatment (not just "dark background")
- [ ] Every on-screen element named explicitly (not "some text" — write the actual text content)
- [ ] Easing described in human terms (not just "animates in" — describe the character: spring bounce, magnetic click, slow creep)
- [ ] Density level implied by the description (can a developer tell if this is 2 elements or 8?)
- [ ] Editorial intent explaining viewer psychology (not what happens — why those choices)
- [ ] Transition out described (where does the viewer's eye go next?)

## Anti-Patterns to Avoid

**Do not write:**
- "A cool animation plays" → Write exactly what animates and how
- "Text fades in" → Text does not just fade in. It slides from a direction, springs up, snaps in, or typewriters. Specify which and why.
- "The background changes" → Changes to what? What does that shift signal?
- "Some UI elements appear" → Name them. Describe their visual style. Are they 3D? Flat? What easing?
- "This establishes the topic" → This is editorial intent done wrong. Say what the viewer feels and what question it raises in their mind.
