---
name: script-to-tts
description: Reformat an existing script for a specific text-to-speech model (ElevenLabs, OpenAI TTS, Google, Azure, Hume, Chatterbox, etc.). Splits VO into model-friendly chunks, inserts pacing/emphasis/SSML markers where the model supports them, strips bracketed visual direction, normalises numbers/abbreviations the way the chosen voice expects, and emits a clean `scripts/tts/<model>/<NN>.txt` (or `.ssml`) file per beat. Use when the user has a locked script and is about to generate VO.
---

# Script → TTS reformatter

You take a finished script and produce per-model, per-line TTS input files.

## Inputs

- `scripts/final/script.md` (or a draft path the user passes).
- Target model — ask if not stated. Common: `elevenlabs-v3`, `elevenlabs-v2`, `openai-tts`, `google-tts`, `azure-tts`, `hume`, `chatterbox`.
- Voice ID / preset, if known. Pull from `brief/tools-and-models.md` if listed.

## Per-model behaviour

| Model | Format | Notable conventions |
|-------|--------|---------------------|
| ElevenLabs v3 | plain text + audio tags (`[pause]`, `[short pause]`, `[long pause]`, `[whispers]`, …) | No SSML: `<break>` tags are not supported and get read or ignored. Use audio tags sparingly, plus punctuation. Check the current character limit for the model. |
| ElevenLabs Multilingual v2 / Flash v2.5 | plain text + inline `<break time="0.5s"/>` | Breaks up to 3 s. Too many in one request makes delivery unstable. Audio tags are v3-only. |
| OpenAI TTS | plain text | No SSML. Use punctuation for pacing. ≤ 4096 chars per request. |
| Google Cloud TTS | SSML | Full SSML supported: `<break>`, `<emphasis>`, `<prosody rate="…" pitch="…">`. |
| Azure (neural) | SSML with `<voice>` + `mstts:express-as` styles | Style + degree work for some voices; check voice's supported styles. |
| Hume | plain text + emotional context note | Hume responds to expressed emotion in the prompt itself. |
| Chatterbox | plain text + reference voice | No SSML; rely on punctuation and the reference clip for prosody. |

## Steps

1. Read script. Identify VO segments (drop bracketed visual direction like `[wide shot of skyline]`).
2. Split by beat — one file per numbered beat/scene so files map to storyboard shots.
3. Normalise:
   - Spell out unusual abbreviations (`API` → keep, `e.g.` → "for example") if the model is known to mangle them.
   - Numbers: large/contextual numbers spelled out (`2026` → "twenty twenty-six" usually unnecessary for ElevenLabs but required for some Azure voices).
   - Quotes/dashes: convert smart quotes to straight, em-dashes to commas where pause is wanted.
4. Insert pacing markers per the model's supported syntax. Be conservative — a comma is usually enough.
5. Save:
   - SSML models: `scripts/tts/<model>/<NN>-<slug>.ssml`
   - Plain models: `scripts/tts/<model>/<NN>-<slug>.txt`
6. Emit a `scripts/tts/<model>/INDEX.md` listing each file, character count, estimated duration (words ÷ ~150 words per minute, a typical narration rate; adjust after the first take), and the voice ID to use.

## Discipline

- Don't add SSML to models that don't support it — it'll be read aloud literally.
- Don't merge multiple beats into one file even if they're short; that breaks the shot mapping.
- Show the first generated file to the user before generating the rest, so they can adjust style.
- Keep each request under the model's character limit; chunk if necessary and number `01a`, `01b`.
