# Editorial Patterns Reference

## The Retention Architecture

Short-form motion graphic videos (30-90 seconds) do not lose viewers randomly. They lose viewers at predictable moments. The job of the director is to engineer against every known drop-off point. These patterns are the tools for doing that.

---

## The Tension Curve

Every video must follow a deliberate tension curve. Plot this before designing any segment.

```
Tension
  ^
  |        Pattern    Climax
  |  Hook   Interrupt  Peak
  |   ^        ^         ^    Resolution
  |   |        |         |       ^
  |   |   Build|    Build|       |   CTA
  |   |        |         |       |   Vacuum
  +---+--------+---------+-------+-------> Time
  Start      Early      Mid     Late    END
```

**Hook** (opening seconds): Maximum intrigue, minimum explanation. Force the viewer to ask a question they need answered.

**Build** (early section): Establish the world, introduce the problem, layer in complexity. Tension rises.

**Pattern Interrupt** (typically in the first quarter, when retention first dips): A sudden, jarring tonal shift that shatters the established expectation. Resets the viewer's attention span. See below.

**Teaching sequence** (middle section — the bulk of the video): The core of the video. Dense, layered, fast-paced. Multiple mini-tensions and releases. This is where the "staccato pop" and "visual overload" patterns live.

**Climax** (late middle): The payoff of the core metaphor. The moment where "it all clicks." The visual equivalent of the penny dropping.

**Resolution** (near end): The satisfying "snap" — modular pieces click together, metaphors resolve, narrative arc closes visually.

**CTA Vacuum** (final few seconds): See CTA Vacuum section below.

---

## The Pattern Interrupt

**What it is**: A sudden, unexpected tonal or aesthetic shift that happens when the viewer's attention is about to drop (typically 8-12 seconds in, and again around 30-35 seconds).

**Why it works**: The human brain habituates to predictable stimuli. When a pattern is broken, it triggers an orienting response — involuntary refocusing of attention. This resets the viewer's attention budget.

**Techniques:**

**The Meme Drop** — Build a polished, serious, high-production environment, then cut instantly to a low-resolution internet meme. The quality contrast is violent and funny. The viewer laughs (or at least reacts), which resets their attention.
- Must be tonally relevant — the meme's content should mirror the viewer's feeling at that moment
- Duration: 1-2 seconds max before transitioning to the next serious segment

**The Void Cut** — Cut from a complex, colorful, busy scene to a pure black void with a single 3D object. The sudden darkness commands attention.
- Best used for hyperbolic statements ("this is essentially black magic")
- The 3D object in the void should be dramatic — glowing, slowly rotating

**The Aesthetic Crash** — Shift the entire visual register without warning. If the video has been serious and technical, suddenly use a hand-drawn cartoon or a retro illustration. The register mismatch is the interrupt.

**Tonal Whiplash Text** — After a series of dense technical visuals, cut to a single line of slang or humor rendered in large, bold text. The sudden simplicity after complexity creates a comedic beat.

**Rules for pattern interrupts:**
- One per roughly the first and second half of the video (two maximum in a 60-second video)
- Must be followed immediately by a smooth re-entry into the main content — the interrupt is not a tangent
- The "instead" pivot — after the interrupt, use a text card like "Here's what to do instead" or "But here's the thing" to guide the viewer back

---

## Cognitive Relief

**What it is**: A deliberate slowdown after a sustained period of high visual density.

**Why it works**: The brain has a cognitive load limit. Dense, fast-paced sequences build tension and engagement but also fatigue. If sustained too long (more than 8-10 seconds), the viewer experiences overwhelm and swipes. A deliberate release resets their capacity to engage for the next dense sequence.

**How to design it:**
- After a "visual overload" sequence (rapid checkmarks, cascading checklists, tab frenzy), cut to a single, static element on a clean background
- Slow the animation — something drifts or slides in slowly instead of snapping
- The voiceover also slows here — this is not a coincidence, it's synchronized
- Duration: 3-6 seconds. Long enough to feel like a breath, short enough not to lose momentum

**Cognitive relief signals to design:**
- Background lightens (or darkens if previous was light)
- Number of elements on screen drops from 5+ to 1-2
- No rapid animations — one slow, smooth entrance
- The text in this segment is usually the "teaching" line — "Now that the AI knows what you want…"

**Warning**: Do not use cognitive relief at the beginning of a video. Relief requires prior tension. If there is no tension, relief is just boredom.

---

## Visual Metaphor Construction

The quality gap between a mediocre motion graphic and a great one is almost entirely the quality of its visual metaphors. Text on screen with animations is a slideshow. A visual metaphor *shows* the idea rather than labeling it.

### The Metaphor Construction Formula

1. **Identify the abstract concept** (e.g., "context window degradation")
2. **Find a physical analogue every person already understands** (e.g., a gas gauge, a battery, a volume slider)
3. **Map the failure state** (e.g., the slider moves into the red zone)
4. **Use the viewer's existing emotional response to that analogue** (e.g., "I know that sinking feeling when my phone hits 20% battery")

The best metaphors feel inevitable in retrospect — the viewer thinks "of course, why would you show it any other way?"

### Metaphor Levels

| Level | Description | Example |
|---|---|---|
| Label | Just showing the thing's name on screen | "CONTEXT WINDOW" in text |
| Diagram | Showing its structure | A bar chart of token counts |
| Metaphor | Replacing it with a relatable analogue | A robot on a slider running from green to red |
| Embodied metaphor | The viewer *feels* the concept physically | The slider's slow inevitable creep creating dread |

Always aim for level 3 minimum. Level 4 is the target for key concepts.

### Visual Metaphors for Common Tech Concepts

| Concept | Metaphor |
|---|---|
| Data compression | A large box shrinking into a tiny box; a word physically squishing |
| AI context window | A fuel gauge, battery indicator, or slider running out |
| Modular/component architecture | Distinct floating 3D blocks that snap together |
| System overload | Pop-up storm, cascading windows, infinite scroll blur |
| Algorithm hunting for patterns | Pac-Man eating dots in a maze |
| Brand attraction | Planet pulling meteors via gravity |
| Forgetting/memory loss | The robot slider moving toward red |
| Breaking from convention | A photograph physically shattering to reveal the reality underneath |
| A pipeline/workflow | Nodes connected by self-drawing animated lines |
| Transformation/change | A shape morphing into a new shape (funnel → tombstone) |

---

## The Hook Architecture

The opening seconds determine if the viewer stays. Design the hook last — after you understand the whole video — because it needs to promise the exact payoff the video delivers.

### Hook Types

**The Absurdity Hook** — Visualize something physically impossible or counterintuitive. The viewer's brain flags it as "this can't be right, I need to understand this."
- Example: A 2MB box stretching to become a 75GB card

**The Attack Hook** — Aggressively destroy a conventional wisdom the viewer holds. Kill something they thought was true.
- Example: A marketing funnel morphing into a tombstone with "R.I.P."

**The Command Hook** — State exactly what the viewer is doing wrong. Fast, direct, slightly confrontational.
- Example: "CLAUDE CODE" in glitch text + immediately cutting to a meme that says "Your AI slop bores me"

**The Mystery Hook** — Show something impressive happening without explanation, forcing the viewer to want to know how.
- Example: A checklist with 50 items all getting checkmarks in rapid fire, with no context yet

**Rules:**
- The hook must create a question in the viewer's mind that they must watch to answer
- No "Hi, in this video I'm going to explain…" — this kills retention immediately
- No logos or intros before the hook — jump straight in
- The hook's visual should be the most visually ambitious scene in the video

---

## The CTA Vacuum

**What it is**: The deliberate removal of all visual complexity in the final 4-8 seconds to force the viewer's attention onto a single text-based call to action.

**Why it works**: After 40-50 seconds of non-stop motion, cuts, and visual stimulation, the viewer's brain has been trained to track movement. When all movement stops and the screen becomes dead still, there is nothing else to look at. The eye locks onto the only element left: the text. This maximizes CTA comprehension and conversion rate.

**How to design it:**
1. The second-to-last segment resolves the narrative arc (stacking animation, final metaphor payoff, checkmark, etc.)
2. In one frame — not a fade, not a wipe — everything disappears. Instant cut.
3. What remains: clean background (usually white or near-white), single line of dark text, centered
4. Zero animation for the remaining duration
5. The text is the CTA: "Comment X and I'll send you Y" or the punchline statement if it's not CTA-driven

**Critical rules:**
- The background must contrast maximally with the previous segment — if the video was dark, go light; if it was colorful, go white
- The text must be readable in under 2 seconds (the viewer needs the full remaining time to act)
- No music stingers, no animations, no subtle movements — dead still
- The transition into the vacuum should be the most jarring cut in the entire video — that contrast is the mechanism

---

## The Authority Anchor

When a video is teaching something, skepticism is the primary obstacle. Viewers mentally ask "who is this person and why should I believe them?"

**Technique**: Cut to external proof of authority — footage of a recognized figure, a well-known brand logo, a screenshot of a respected product.

**Rules:**
- Use it early in the teaching section (not the hook)
- Keep it brief (1-2 seconds) — it's a credibility stamp, not a feature
- The authority must be relevant — a Silicon Valley CEO for tech advice, a designer brand logo for design advice
- Return immediately to your own content after — the anchor borrows credibility, it doesn't replace your own voice

---

## Synchronized Audio-Visual Design

Even when no actual audio is embedded, the design must account for the voiceover timing. The visual track and audio track must be synchronized:

**Rules:**
- Key visual reveals should land on stressed syllables in the voiceover
- Complex animations should not play during dense voiceover — one thing at a time
- A voiceover pause = visual breathing room (let the last animation settle)
- The "staccato pop" sequence should match the rhythm of enumerated items in the VO (one pop per item)
- The slow linear slide should give the VO exactly the time it needs to deliver its line — not faster, not slower

**Timing calibration:**
- Average spoken word rate: 2-3 words per second for educational content
- The SRT timestamps tell you exactly how long each segment is — let the actual VO density guide how much you pack into a scene, not a fixed second count
- Dense visual segments should have shorter, punchier VO lines
- Resolution/vacuum segments can have longer, slower, more deliberate VO

---

## Narrative Arc Patterns

### The "Problem → Solution → Proof" Arc (most common)
1. Show the wrong way (red X, death animation, meme)
2. Introduce the correct approach (new concept, tool, method)
3. Visualize the approach working (checkmarks, graph rising, metaphor resolving)
4. Show the result (the "stacked blocks" / "final product" moment)

### The "Mystery → Explanation → Connection" Arc
1. Show something counterintuitive or absurd (the hook absurdity)
2. Explain the underlying mechanism step by step
3. Connect it to something the viewer cares about (the "and this is why GPT can do what it does" pivot)

### The "Rules" Arc
1. Establish the paradigm shift (old way is dead)
2. Deliver Rule 1 with proof
3. Deliver Rule 2 with proof
4. Deliver Rule 3 with proof
5. Resolve the central metaphor introduced in the hook
