---
name: video-inspect
description: Inspect and analyze video files for quality issues. Use when user wants to check video quality, detect black frames, find silence, analyze video metadata, debug video problems, or verify video output. Runs ffmpeg-based analysis and reports issues.
---

# Video Inspector

Analyze video files for quality issues including black frames, silence, corruption, and metadata problems.

## Usage

Run the inspection script on any video file:

```bash
python ~/.claude/skills/video-inspect/scripts/video_inspect.py "<video_path>"
```

The script uses `imageio_ffmpeg` (bundled with moviepy) so no system ffmpeg install is needed.

## What it detects

- **Black frames**: Segments where the screen is black (using ffmpeg `blackdetect` filter)
- **Silent segments**: Audio silence periods (using ffmpeg `silencedetect` filter)
- **Low bitrate**: Videos that may look blocky or compressed
- **Low resolution**: Below 640x360
- **Frame brightness**: Statistical analysis of sampled frames
- **Metadata**: Codec, resolution, FPS, audio format, duration, file size

## Output

- Human-readable report printed to stdout
- JSON report saved as `<video_path>.inspect.json` for programmatic use

## Interpreting results

- **Black segments at start/end**: Usually intro/outro issues or encoding problems
- **Black segments in middle**: Possible source video corruption or bad cuts
- **Frame brightness avg < 20**: Video is extremely dark, likely black screen issue
- **Frame brightness avg 20-50**: Very dark video, may need brightness adjustment
- **High silence percentage**: Audio track may be missing or corrupted
