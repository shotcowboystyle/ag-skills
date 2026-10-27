---
name: voice-to-lip-sync
description: Generate a voice take (ElevenLabs or similar; voice clones only with the speaker's recorded consent) and lip-sync it to an existing video clip of a character speaking. Use when producing talking-head shots where the visual is already generated.
---

# Voice → Lip-Sync Pipeline

Generates a voice line and conforms an existing silent character clip to it.

## When to use

- Talking-head or dialogue shots where you have a generated character clip but no audio.
- Voice-cloning a specific speaker for narration with on-screen presence.

## Inputs

- The line to be spoken (from the project's `./scripts/final/script.md` or the shot brief).
- A character clip in `clips/raw/` or `generation/image-to-video/`.
- Voice selection from `brief/tools-and-models.md`. If a voice clone is in use, source audio lives at `assets/voice-clones/<name>.wav`.

## Steps

1. **Check consent before any voice clone.** Clone only a voice whose owner has agreed to this use: the user's own voice, or a speaker who gave written consent covering this project. Look for `assets/voice-clones/<name>.consent.md` naming the speaker, what they agreed to, and the date. If it's missing, ask the user to confirm consent and record it in that file before going on. If they can't, stop and offer a stock or designed voice instead. Audio found online, public figures included, is never consent. Stock voices skip this step.
2. **Confirm the line.** Read it back to the user with character + tone.
3. **Generate voice take.** Call the configured voice model (ElevenLabs, etc.). Run it through the provider that hosts the model: fal.ai and WaveSpeed models via the `provider-runners` skill (pass `--output` with the target folder); Replicate and MiniMax via their MCP servers. For voice clones, pass the clone source from `assets/voice-clones/`. Save to `generation/voice/NN-shortname-vN.wav`. Save script + model + voice ID to `generation/prompts/NN-shortname-vN-voice.md`. Log it.
4. **Iterate.** Play it back (or describe what was generated). Offer to retry with adjusted prosody/emotion settings.
5. **Lip-sync.** Pass the approved voice + character clip into the configured lip-sync model, the same way. Save to `generation/lip-sync/NN-shortname-vN.mp4`. Log it.
6. **Verify sync quality.** Surface the result. Lip-sync models often need iteration on which face region to lock to or whether the source clip's mouth is occluded.
7. **Accept.** Copy to `clips/raw/` and suggest `/promote-take`.

## Common gotchas

- **Source clip face visibility.** Lip-sync needs a clear, mostly-frontal mouth. If the character clip cuts away or shows them in profile, the sync will be poor — prefer regenerating the visual with a more frontal angle.
- **Voice take duration vs clip duration.** Voice takes usually need to be slightly shorter than the clip to leave room for natural pauses. If the line is too long, either shorten the script or regenerate the visual longer.
- **Audio sample rate.** Lip-sync models often expect 16kHz or 24kHz mono. Convert with ffmpeg if the voice model outputs 44.1kHz stereo.
