# Motion Graphic Director Skill

A creative direction and design intelligence skill for AI coding assistants. Use this skill when you need an AI agent to think like a professional motion graphic director — not just a programmer — before generating Remotion videos.

## Installation

```bash
npx skills add MaizeCobra/motion-graphic-director-skill
```

## What This Skill Does

Most AI agents approach motion graphic generation as a coding task. They produce technically correct Remotion code that looks like an animated PowerPoint. This skill fixes that by forcing the agent through a full **director's pipeline** before a single line of code is written:

```
SRT/Script Input
      ↓
Script Analysis   →  script-[name].md
      ↓
Visual Ideation   →  video-design-[name].md  ← user approves this
      ↓
Remotion Build    →  uses remotion-best-practices skill
```

The design document the agent produces covers every segment: background treatment, motion graphics and typography, transitions and pacing, and — most importantly — the editorial intent explaining *why* each choice was made in terms of viewer psychology.

## Why This Skill Exists

The gap between a mediocre AI-generated motion graphic and a great one is almost entirely the quality of the design decisions, not the code. This skill provides:

- **Visual metaphor thinking** — concepts are visualised, not just labelled
- **Tension curve architecture** — retention-engineered pacing across the video
- **Color storytelling** — every color has a meaning the viewer learns to decode
- **Pattern interrupt design** — deliberate tonal shifts to reset viewer attention
- **Editorial intent** — every design choice is justified in terms of viewer psychology

## What's Included

```
motion-graphic-director/
├── SKILL.md                         # Main pipeline, design framework, quality checklist
├── examples/
│   ├── video-example-1.md           # Shot-by-shot breakdown: Claude Code tips (~54s)
│   ├── video-example-2.md           # Shot-by-shot breakdown: ZIP compression (~56s)
│   ├── video-example-3.md           # Shot-by-shot breakdown: Brand Gravity (~80s)
│   ├── video-script-1.md            # Voiceover script for example 1
│   ├── video-script-2.md            # Voiceover script for example 2
│   └── video-script-3.md            # Voiceover script for example 3
├── references/
│   ├── design-system.md             # Color architecture, typography, easing as emotion
│   ├── editorial-patterns.md        # Tension curve, pattern interrupts, CTA vacuum
│   ├── design-doc-format.md         # Exact format spec + worked example
│   └── motion-graphic-prompts.md    # Library of 75 animation concepts
└── scripts/
    └── srt_to_script.py             # Converts SRT subtitle files to structured script MD
```

The six example files (`video-example-*.md` + `video-script-*.md`) are the most important assets — they are real shot-by-shot breakdowns of high-performing motion graphic videos. The agent reads all six before designing anything, internalising the quality bar they demonstrate.

## Key Features

- **SRT-to-script converter** — `srt_to_script.py` parses any SRT file into a structured script MD with exact timestamps and voiceover text, one cue per segment
- **Worked design doc example** — `references/design-doc-format.md` includes a complete webhooks video design doc showing the exact level of detail required
- **75 animation prompts** — categorised idea library across UI Chaos, Liquid Transitions, 3D Effects, Typography Animations, and Advanced/Experimental techniques
- **Design approval gate** — the agent presents the full design doc for user approval before writing any code; revisions happen at the design stage, not the code stage

## Compatibility

Works with any AI coding assistant that supports file reading. Designed for use with Remotion but the design methodology applies to any motion graphic tool.

Built for: OpenCode, Claude Code, Cursor, Aider, and similar agentic environments.

## License

MIT License — see [LICENSE](LICENSE)
