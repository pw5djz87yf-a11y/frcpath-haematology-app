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
