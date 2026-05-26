# mp4-to-mp3

Convert MP4 video files to MP3 audio using FFmpeg.

## Trigger

Use when user wants to:
- Convert MP4 to MP3
- Extract audio from video
- 把MP4转成MP3
- 提取视频音频

## Usage

```
/mp4-to-mp3 <file_path>
/mp4-to-mp3 <file_path> [output_path]
```

## Instructions

1. Parse the arguments:
   - First arg: input MP4 file path (required)
   - Second arg: output MP3 file path (optional, defaults to same directory with `.mp3` extension)

2. Verify FFmpeg is available: `ffmpeg -version`

3. If no output path given, replace the file extension with `.mp3` in the same directory.

4. Run the conversion:
   ```bash
   ffmpeg -i "<input>" -vn -acodec libmp3lame -q:a 2 "<output>"
   ```
   - `-vn` strips video
   - `-acodec libmp3lame` uses MP3 encoder
   - `-q:a 2` = ~190kbps VBR (high quality)

5. Report the output file path and size on success.

## Examples

```
/mp4-to-mp3 C:/Users/clown/Videos/clip.mp4
/mp4-to-mp3 C:/Videos/input.mp4 D:/output/audio.mp3
```
