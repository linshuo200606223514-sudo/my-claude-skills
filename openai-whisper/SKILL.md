---
name: openai-whisper
description: "Transcribe audio and video files locally using OpenAI Whisper CLI (no API key needed). Use when user wants to transcribe audio, convert speech to text, generate subtitles/captions, or translate spoken content. Requires local whisper binary."
---

# Whisper (CLI)

Use `whisper` to transcribe audio locally.

Quick start
- `whisper /path/audio.mp3 --model medium --output_format txt --output_dir .`
- `whisper /path/audio.m4a --task translate --output_format srt`

Notes
- Models download to `~/.cache/whisper` on first run.
- `"--model"` defaults to `turbo` on this install.
- Use smaller models for speed, larger for accuracy.

## Runtime Requirements

- `whisper` binary must be installed
- Install: `brew install openai-whisper` (macOS)
- Windows: `pip install openai-whisper` + ffmpeg

## Models (speed vs accuracy)

| Model    | Size   | Speed  | Accuracy |
|----------|--------|--------|----------|
| tiny     | 39M    | ████   | ★★       |
| base     | 74M    | ███    | ★★★      |
| small    | 244M   | ██     | ★★★★     |
| medium   | 769M   | █      | ★★★★★    |
| large    | 1550M  | Slow   | ★★★★★★   |
| turbo    | 809M   | ██     | ★★★★★    |

## Common Commands

```bash
# Basic transcription (txt output)
whisper audio.mp3 --output_format txt --output_dir .

# Generate SRT subtitles
whisper video.mp4 --output_format srt --output_dir ./subtitles

# Generate VTT for web
whisper audio.mp3 --output_format vtt --output_dir .

# Translate to English (from any language)
whisper audio.mp3 --task translate --output_format txt

# Specify language (faster, more accurate)
whisper audio.mp3 --language zh --model medium

# All output formats at once
whisper audio.mp3 --output_format all --output_dir .

# Multiple files
whisper file1.mp3 file2.wav --model small
```

## Output Formats

- `txt` — plain text transcript
- `srt` — SubRip subtitles with timestamps
- `vtt` — WebVTT for HTML5 video
- `tsv` — tab-separated with timing data
- `json` — full JSON with word-level timestamps
- `all` — all of the above

## Tips

- For Chinese audio: `--language zh --model medium` gives best results
- For long files: use `--model turbo` (good balance)
- ffmpeg must be installed for video files (mp4, mkv, etc.)
- First run downloads the model (can take a few minutes)
