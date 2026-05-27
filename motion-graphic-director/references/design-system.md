# Design System Reference

## Color Architecture

### The Rule of the Single Accent

Every high-quality motion graphic video is built around a **single blazing accent color** on a neutral background. This is not a stylistic preference — it is a retention mechanic. The viewer's eye tracks the accent color. When it appears, attention spikes. When it disappears, the viewer waits for it. This creates subconscious engagement loops.

**Structure:**
- **Background**: Dark (near-black, charcoal, deep desaturated grey) OR Light (warm off-white, soft beige, muted grey). Never mid-tone — mid-tone is the enemy of contrast.
- **Primary Accent**: One blazing color. Neon mint-green, safety orange, electric cyan, hot lime. Must pop with maximum luminosity against the background.
- **State Color**: A second color used ONLY to signal failure/warning/wrong. Typically red or orange. Introduced only when needed — never decorative.
- **Typography**: White or near-white on dark backgrounds. Near-black on light backgrounds. The accent color should touch text sparingly — only to highlight specific words.

**Palette examples from reference videos:**
- Video 1 (Claude Code): Near-black bg + neon mint-green accent + red for error states
- Video 2 (ZIP compression): Warm beige bg + safety orange accent + cinematic black void for dramatic cuts
- Video 3 (Brand Gravity): Muted mint-green bg + forest green accent + desaturated grey for "enemy" sequences

### Color Storytelling

The viewer learns your color system in the first 8 seconds. After that, colors carry meaning without explanation.

| Color role | What it signals | When to use |
|---|---|---|
| Primary accent | Progress, correct, energy, the "solution" | Main UI elements, checkmarks, positive animations |
| Red / state color | Wrong, warning, threat, the "problem" | X marks, error states, tension-building moments |
| Desaturated / grey | Neutral, past, context, background noise | Non-active elements, "before" states |
| White / void | Absolute focus, clarity, the payoff | CTA scenes, punchline moments, visual vacuum |

**Rule**: Once you establish that green = correct, NEVER use green for a mistake. Color vocabulary breaks = viewer confusion = watch time drop.

### Vignette & Cinematic Tints

Dark-background videos should almost always have a subtle vignette (screen edges 10-20% darker than center). This keeps the eye locked to the center and creates a cinematic, produced feeling. Without it, the video looks like a screen recording, not a motion graphic.

Background color shifts between segments are meaningful:
- **Shift to lighter background** = entering solution/teaching phase
- **Shift to darker background** = entering tension/problem phase  
- **Shift to void/pure black** = dramatic emphasis, hyperbole, "black magic" moment
- **Shift to pure white** = payoff, clarity, visual vacuum for CTA

---

## Typography System

### Choose One Typographic Register and Own It

| Register | Associations | Best for |
|---|---|---|
| Monospace / terminal | Technical, hacker, raw power, authenticity | Dev tools, AI, coding, engineering |
| Bold geometric sans | Modern, confident, assertive, no-nonsense | Business, finance, productivity |
| Bouncy serif | Playful, approachable, editorial | Marketing, consumer, creative industries |
| Clean minimal sans | Premium, design-forward, Swiss | SaaS, branding, design tools |

**Never mix more than two typographic registers in one video.** Main body can use one, accent words/headers can use a second. Three or more = visual chaos.

### Kinetic Typography Rules

Kinetic text is text that moves — not just fades in. It should:
- Build from a physical direction (slides in from left/right/bottom, never just appears)
- Use pronounced easing (spring bounce, or aggressive slow-in)
- Match the energy of the voiceover: fast VO = fast type, slow deliberate VO = slow deliberate entrance
- Stack or overlap for emphasis — the words "stacking" on screen mirrors urgency
- Exit in the opposite direction it entered, or wipe away with the transition

**Text size hierarchy (for 1080x1920 / 9:16 vertical video):**
- Hero text (central single concept): 64-96px equivalent
- Secondary labels / subtitles: 32-48px
- Terminal/code text: 18-24px monospace
- UI interface labels: 14-18px

---

## Motion Vocabulary

### Easing as Emotional Language

The easing curve of an animation communicates emotion before the viewer consciously registers what moved.

| Easing type | Emotional read | Remotion implementation |
|---|---|---|
| Spring (damping 10-14) | Alive, bouncy, playful, tactile | `spring({ damping: 12, stiffness: 200 })` |
| Spring (damping 100+) | Heavy, magnetic, satisfying "click" | `spring({ damping: 100, stiffness: 80 })` |
| Linear | Mechanical, algorithmic, inevitable | `interpolate(f, [0,30], [0,1])` |
| Ease-in-out (cubic) | Smooth, premium, polished | `Easing.inOut(Easing.cubic)` |
| Hard cut (instant) | Shock, surprise, pattern interrupt | Frame-exact conditional rendering |
| Staccato pop (0→120%→100%) | Rhythmic, dopamine, drumbeat | Spring overshoot, scale keyframes |

**The "magnetic click"** — used for stacking/snapping animations. Objects move fast then decelerate hard as they connect. Created with high-damping spring. Feels like heavy blocks clicking into place. Use for resolution moments.

**The "staccato pop"** — rapid sequential appearance of identical elements (checkmarks, icons, dots). Each pops from 0 to 120% scale then snaps to 100%. The rhythm is the message: "look how many things happened."

**The "slow inevitable creep"** — a single element moves linearly toward a threshold (like a slider). Creates dread or anticipation. The viewer knows it's going to hit the red zone. Linear interpolation, no easing.

### Signature Animation Patterns

Pick 2-3 of these and use them consistently throughout your video as part of its visual identity:

**Bouncy 3D UI elements** — Buttons, cards, and icons that drop into frame with a spring bounce. They feel physical and graspable. Make abstract concepts feel like tools.

**Radial wipe / expanding shape** — A shape (star, circle, blob) expands from center and acts as a wipe, clearing the frame for the next visual. More interesting than a fade.

**SVG stroke-dashoffset drawing** — Lines, flowcharts, graphs, and paths that draw themselves across the screen. Used to connect concepts, show pipelines, visualize progress. Timed to the voiceover pace.

**Liquid/fluid shape wipe** — A fluid organic shape (not geometric) pulls across the screen to reveal the next scene. Premium, editorial feel. Created with SVG path animation or CSS clip-path.

**Particle burst** — On a key moment (success, completion, revelation), a burst of small particles radiates outward from the subject. Adds kinetic energy to a static "result" moment.

**Orbiting elements** — Small icons or dots orbiting a central subject. Visualizes systems, ecosystems, attraction. Animated with `Math.sin(frame * speed) + Math.cos(frame * speed)` for circular motion.

**Morph transition** — One shape physically transforms into another shape (e.g., funnel becomes tombstone, small box stretches into large card). The most powerful visual for showing transformation or contrast. Use CSS clip-path morphing or SVG path interpolation.

---

## Background Architecture

The background is a character in the video — not a canvas. It should:

1. **Shift color between conceptual phases** — not just within single scenes
2. **Have depth** — subtle gradient, vignette, noise texture, or slow-moving blob shapes
3. **React to the foreground energy** — when the content is hyper-dense, the background should be still and neutral; when content is sparse, the background can have ambient animation

**Ambient background patterns:**
- Slow-moving blurred color orbs (Gaussian blur, low opacity, scale 150-200% of frame)
- Subtle noise texture overlay at 5-10% opacity
- Diagonal gradient that shifts hue very slowly
- Static mesh gradient for "premium" feeling

**Never use**: Solid flat color with no depth treatment at all. It makes everything feel like a PowerPoint.

---

## Scene Density Calibration

Every segment should be designed with an intentional density level:

| Density level | Elements on screen | Animation activity | Use when |
|---|---|---|---|
| Overload | 5+ simultaneous elements | Constant motion everywhere | Conveying "complexity" or "AI doing a lot of work" — the viewer feels the density even if they can't read it |
| High | 3-4 elements | 2-3 things animating at once | Teaching a concept with multiple parts |
| Medium | 2-3 elements | 1-2 animations | Standard teaching, transition segments |
| Low | 1-2 elements | Single focus animation | Resolution, emotional beat, "here's the answer" |
| Vacuum | 1 element or text only | No motion | CTA, punchline, the most important single idea |

**Density must vary across the video.** A video that is always "High" density causes viewer fatigue. A video that is always "Low" is boring. The pattern is: build density → release → build again → final release (vacuum).
