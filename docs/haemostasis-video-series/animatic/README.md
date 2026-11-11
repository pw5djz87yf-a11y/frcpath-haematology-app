# Module animatic builder

Builds a narrated animatic MP4: flat, colour-coded frames timed to an offline text-to-speech voice, with burned-in captions and an `.srt` caption file.

- `scenes.py`: the shot list (narration, on-screen text, visual build steps)
- `icons.py`: the shared flat icon set (one icon per character)
- `build.py`: the pipeline (speech → frames → MP4)
- `shoot.js`: renders the HTML frames to PNG using Playwright

## Requirements

- espeak-ng, mbrola and mbrola-en1 (the default voice is `mb-en1`, a British male voice)
- ffmpeg
- Node with Playwright

## Run

```
python3 build.py --out build
```

Preview selected shots only:

```
python3 build.py --out build --only 5.3,8.3
```

The voice is a computer voice, meant only as a guide for timing. The final video would replace it with a human narrator or a commercial text-to-speech voice.

Output: `../video/module1_the_day_the_wall_tore_animatic.mp4` (about 9.7 min) and the matching `.srt` file.

## Using a macOS voice (e.g. Jamie (Premium))

1. `python3 build.py --export-mac ../video/make_jamie_voice.sh` writes a script that needs nothing beyond the tools built into macOS.
2. On the Mac, run `bash ~/Downloads/make_jamie_voice.sh`. It records every line with `say` and leaves `jamie_audio.zip` on the Desktop. You can pass a different voice and speaking rate: `bash make_jamie_voice.sh "Serena (Premium)" 165`.
3. Unzip the file here and rebuild: `python3 build.py --out build --audio-dir path/to/jamie_audio`.
