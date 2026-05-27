"""
srt_to_script.py

Converts an SRT subtitle file into a structured video script MD file,
matching the format of video-script-1.md / video-script-2.md / video-script-3.md.

Each SRT cue becomes its own segment entry — timestamps are preserved exactly
as they appear in the SRT. No regrouping, no merging.

Usage:
    python scripts/srt_to_script.py <input.srt> <"Video Title"> [output.md]

Examples:
    python scripts/srt_to_script.py my_video.srt "How Webhooks Work"
    python scripts/srt_to_script.py my_video.srt "How Webhooks Work" video-script-4.md

If no output path is given, the MD is written next to the SRT file with the same name.

Output format:
    # Video Script — <Title>

    ## Segment Breakdown

    ### [0:00 - 0:03] Segment 1
    "exact voiceover words"

    ### [0:03 - 0:07] Segment 2
    "exact voiceover words"
    ...
"""

import re
import sys
import os
from dataclasses import dataclass
from typing import List


# ---------------------------------------------------------------------------
# SRT parsing
# ---------------------------------------------------------------------------

@dataclass
class Cue:
    index: int
    start_ms: int
    end_ms: int
    text: str   # newlines collapsed to spaces, HTML/ASS tags stripped


def parse_srt(path: str) -> List[Cue]:
    """Parse an SRT file and return a list of Cue objects."""
    with open(path, encoding="utf-8-sig") as f:
        content = f.read()

    blocks = re.split(r"\n\s*\n", content.strip())
    cues = []

    for block in blocks:
        lines = block.strip().splitlines()
        if len(lines) < 3:
            continue

        # Line 0: cue index
        try:
            index = int(lines[0].strip())
        except ValueError:
            continue

        # Line 1: timecode  "00:00:01,000 --> 00:00:04,500"
        tc_match = re.match(
            r"(\d{2}):(\d{2}):(\d{2})[,.](\d{3})\s*-->\s*"
            r"(\d{2}):(\d{2}):(\d{2})[,.](\d{3})",
            lines[1].strip(),
        )
        if not tc_match:
            continue

        h1, m1, s1, ms1, h2, m2, s2, ms2 = (int(x) for x in tc_match.groups())
        start_ms = ((h1 * 60 + m1) * 60 + s1) * 1000 + ms1
        end_ms   = ((h2 * 60 + m2) * 60 + s2) * 1000 + ms2

        # Lines 2+: subtitle text
        raw_text = " ".join(lines[2:])
        text = re.sub(r"<[^>]+>", "", raw_text)   # strip HTML tags
        text = re.sub(r"\{[^}]+\}", "", text)       # strip ASS override tags
        text = re.sub(r"\s+", " ", text).strip()

        if text:
            cues.append(Cue(index=index, start_ms=start_ms, end_ms=end_ms, text=text))

    return cues


# ---------------------------------------------------------------------------
# Timestamp formatting
# ---------------------------------------------------------------------------

def ms_to_timestamp(ms: int) -> str:
    """Convert milliseconds to M:SS display format (e.g. 0:03, 1:12)."""
    total_seconds = ms // 1000
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes}:{seconds:02d}"


# ---------------------------------------------------------------------------
# MD rendering
# ---------------------------------------------------------------------------

def render_md(title: str, cues: List[Cue]) -> str:
    """Render cues into the video-script MD format, one cue per segment."""
    lines = []
    lines.append(f"# Video Script — {title}")
    lines.append("")
    lines.append("## Segment Breakdown")

    for i, cue in enumerate(cues, start=1):
        start_ts = ms_to_timestamp(cue.start_ms)
        end_ts   = ms_to_timestamp(cue.end_ms)
        lines.append("")
        lines.append(f"### [{start_ts} - {end_ts}] Segment {i}")
        lines.append(f'"{cue.text}"')

    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 3:
        print('Usage: python scripts/srt_to_script.py <input.srt> "<Video Title>" [output.md]')
        print()
        print("Examples:")
        print('  python scripts/srt_to_script.py my_video.srt "How Webhooks Work"')
        print('  python scripts/srt_to_script.py my_video.srt "How Webhooks Work" video-script-4.md')
        sys.exit(1)

    srt_path = sys.argv[1]
    title    = sys.argv[2]

    if len(sys.argv) >= 4:
        out_path = sys.argv[3]
    else:
        base = os.path.splitext(srt_path)[0]
        out_path = base + ".md"

    if not os.path.isfile(srt_path):
        print(f"Error: SRT file not found: {srt_path}")
        sys.exit(1)

    cues = parse_srt(srt_path)
    if not cues:
        print(f"Error: No valid cues found in {srt_path}")
        sys.exit(1)

    md = render_md(title, cues)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"Parsed {len(cues)} cues -> written to {out_path}")


if __name__ == "__main__":
    main()
