# AI Audio Editing Tools

A curated index of GitHub projects that give AI agents reliable, programmatic ways to edit, process, transcribe, and synthesise audio — skills, CLIs, MCP servers, and podcast production pipelines.

**Last Updated:** 2026-04-26
**Entries:** 14

---

## Scope

**OUT OF SCOPE:** Models (Whisper weights, Bark, XTTS, DeepFilterNet checkpoints, etc.), DAWs and human-facing GUI apps (Audacity, Reaper, Logic Pro). MCP/CLI wrappers around DAWs are in scope when they expose an agent-callable surface.

**FOCUS:** Tooling (MCPs, Agent Skills, CLIs) that gives AI agents reliable, programmatic ways to handle audio production: normalization (LUFS / EBU R128), denoising, EQ, de-essing, silence trimming, format conversion, splicing, leveling, mastering, transcription (STT), and speech synthesis (TTS).

**DEFINING FEATURE:** Built **for agents with human users** — not for human UIs. Inclusion criterion is a stable agent-callable surface (skill, CLI, MCP, SDK) rather than a GUI workflow.

**In scope:** skills, CLIs, MCPs, podcast production pipelines.

> **Note on coverage:** the agent-native audio space is genuinely thinner than image and video right now — most production-grade EQ, de-essing, and mastering still lives behind GUI/VST surfaces. Submissions welcome.

---

## Table of Contents

- [CLIs](#clis)
- [MCPs](#mcps)
- [Skills — Editing & Processing](#skills-editing-&-processing)
- [Skills — Podcast Pipelines](#skills-podcast-pipelines)
- [Skills — Synthesis (TTS)](#skills-synthesis-tts)
- [Skills — Transcription](#skills-transcription)

---

## CLIs

### ffmpeg-normalize

Audio Normalization for Python/ffmpeg

![Stars](https://img.shields.io/github/stars/slhck/ffmpeg-normalize?style=flat) ![Last commit](https://img.shields.io/github/last-commit/slhck/ffmpeg-normalize?style=flat) ![Language](https://img.shields.io/github/languages/top/slhck/ffmpeg-normalize?style=flat)

⭐ 1500 · Last updated: 2026-04-13 · [slhck/ffmpeg-normalize](https://github.com/slhck/ffmpeg-normalize)

### podwise-cli

CLI client for podwise.ai — turn any podcast episode into AI-powered insights, designed for use in AI agents and skills workflows.

![Stars](https://img.shields.io/github/stars/hardhackerlabs/podwise-cli?style=flat) ![Last commit](https://img.shields.io/github/last-commit/hardhackerlabs/podwise-cli?style=flat) ![Language](https://img.shields.io/github/languages/top/hardhackerlabs/podwise-cli?style=flat)

⭐ 224 · Last updated: 2026-04-04 · [hardhackerlabs/podwise-cli](https://github.com/hardhackerlabs/podwise-cli)

---

## MCPs

### elevenlabs-mcp

The official ElevenLabs MCP server

![Stars](https://img.shields.io/github/stars/elevenlabs/elevenlabs-mcp?style=flat) ![Last commit](https://img.shields.io/github/last-commit/elevenlabs/elevenlabs-mcp?style=flat) ![Language](https://img.shields.io/github/languages/top/elevenlabs/elevenlabs-mcp?style=flat)

⭐ 1330 · Last updated: 2026-03-20 · [elevenlabs/elevenlabs-mcp](https://github.com/elevenlabs/elevenlabs-mcp)

### notebooklm-mcp

Bridge Google NotebookLM with Claude via MCP. Full programmatic access to create notebooks, manage sources, and generate AI-powered content — podcasts, videos, slides, mind maps, quizzes, flashcards, and reports — all through natural language.

![Stars](https://img.shields.io/github/stars/alfredang/notebooklm-mcp?style=flat) ![Last commit](https://img.shields.io/github/last-commit/alfredang/notebooklm-mcp?style=flat) ![Language](https://img.shields.io/github/languages/top/alfredang/notebooklm-mcp?style=flat)

⭐ 17 · Last updated: 2026-01-26 · [alfredang/notebooklm-mcp](https://github.com/alfredang/notebooklm-mcp)

### REAPER-MCP-Skills-Example

MCP server for controlling REAPER DAW through Python scripts.

![Stars](https://img.shields.io/github/stars/wastee/REAPER-MCP-Skills-Example?style=flat) ![Last commit](https://img.shields.io/github/last-commit/wastee/REAPER-MCP-Skills-Example?style=flat) ![Language](https://img.shields.io/github/languages/top/wastee/REAPER-MCP-Skills-Example?style=flat)

⭐ 5 · Last updated: 2026-01-27 · [wastee/REAPER-MCP-Skills-Example](https://github.com/wastee/REAPER-MCP-Skills-Example)

### video-audio-mcp

An FFMPEG powered MCP server for basic Video and Audio editing

![Stars](https://img.shields.io/github/stars/misbahsy/video-audio-mcp?style=flat) ![Last commit](https://img.shields.io/github/last-commit/misbahsy/video-audio-mcp?style=flat) ![Language](https://img.shields.io/github/languages/top/misbahsy/video-audio-mcp?style=flat)

⭐ 71 · Last updated: 2025-05-24 · [misbahsy/video-audio-mcp](https://github.com/misbahsy/video-audio-mcp)

---

## Skills — Editing & Processing

### Claude-Audio-Production-Plugin

Claude Code plugin: audio production workflow — normalize, VAD, transcribe, diarize, podcast assembly, with engineering/podcast/transcript variants.

![Stars](https://img.shields.io/github/stars/danielrosehill/Claude-Audio-Production-Plugin?style=flat) ![Last commit](https://img.shields.io/github/last-commit/danielrosehill/Claude-Audio-Production-Plugin?style=flat) ![Language](https://img.shields.io/github/languages/top/danielrosehill/Claude-Audio-Production-Plugin?style=flat)

⭐ 0 · Last updated: 2026-04-19 · [danielrosehill/Claude-Audio-Production-Plugin](https://github.com/danielrosehill/Claude-Audio-Production-Plugin)

---

## Skills — Podcast Pipelines

### content-pipeline

AI-powered content production pipeline for creators. One prompt → multi-platform publishing. Claude Code Skill.

![Stars](https://img.shields.io/github/stars/OrangeViolin/content-pipeline?style=flat) ![Last commit](https://img.shields.io/github/last-commit/OrangeViolin/content-pipeline?style=flat) ![Language](https://img.shields.io/github/languages/top/OrangeViolin/content-pipeline?style=flat)

⭐ 146 · Last updated: 2026-04-12 · [OrangeViolin/content-pipeline](https://github.com/OrangeViolin/content-pipeline)

### podcast-content-studio

Agent skill for generating podcast show notes from transcripts

![Stars](https://img.shields.io/github/stars/fanyu-meng/podcast-content-studio?style=flat) ![Last commit](https://img.shields.io/github/last-commit/fanyu-meng/podcast-content-studio?style=flat) ![Language](https://img.shields.io/github/languages/top/fanyu-meng/podcast-content-studio?style=flat)

⭐ 7 · Last updated: 2026-04-01 · [fanyu-meng/podcast-content-studio](https://github.com/fanyu-meng/podcast-content-studio)

### podcastcut-skills

Claude Code Skills for podcast/video editing: transcription, content editing, rough/fine cut, final polish

![Stars](https://img.shields.io/github/stars/luoyuweidu1/podcastcut-skills?style=flat) ![Last commit](https://img.shields.io/github/last-commit/luoyuweidu1/podcastcut-skills?style=flat) ![Language](https://img.shields.io/github/languages/top/luoyuweidu1/podcastcut-skills?style=flat)

⭐ 28 · Last updated: 2026-03-17 · [luoyuweidu1/podcastcut-skills](https://github.com/luoyuweidu1/podcastcut-skills)

### podcastfy-clawdbot-skill

A Clawdbot skill that generates a podcast-style MP3 from one or more URLs using the open-source Podcastfy project.

![Stars](https://img.shields.io/github/stars/win4r/podcastfy-clawdbot-skill?style=flat) ![Last commit](https://img.shields.io/github/last-commit/win4r/podcastfy-clawdbot-skill?style=flat) ![Language](https://img.shields.io/github/languages/top/win4r/podcastfy-clawdbot-skill?style=flat)

⭐ 16 · Last updated: 2026-01-31 · [win4r/podcastfy-clawdbot-skill](https://github.com/win4r/podcastfy-clawdbot-skill)

### video-podcast-maker

AI-powered video podcast creation skill for coding agents. Supports Bilibili & YouTube, multi-language (zh-CN/en-US), 6 TTS engines (Edge/Azure/ElevenLabs/OpenAI/Doubao/CosyVoice), 4K Remotion rendering.

![Stars](https://img.shields.io/github/stars/Agents365-ai/video-podcast-maker?style=flat) ![Last commit](https://img.shields.io/github/last-commit/Agents365-ai/video-podcast-maker?style=flat) ![Language](https://img.shields.io/github/languages/top/Agents365-ai/video-podcast-maker?style=flat)

⭐ 606 · Last updated: 2026-04-26 · [Agents365-ai/video-podcast-maker](https://github.com/Agents365-ai/video-podcast-maker)

---

## Skills — Synthesis (TTS)

### Generative-Media-Skills

Multi-modal Generative Media Skills for AI Agents (Claude Code, Cursor, Gemini CLI). High-quality image, video, and audio generation powered by muapi.ai.

![Stars](https://img.shields.io/github/stars/SamurAIGPT/Generative-Media-Skills?style=flat) ![Last commit](https://img.shields.io/github/last-commit/SamurAIGPT/Generative-Media-Skills?style=flat) ![Language](https://img.shields.io/github/languages/top/SamurAIGPT/Generative-Media-Skills?style=flat)

⭐ 3107 · Last updated: 2026-04-26 · [SamurAIGPT/Generative-Media-Skills](https://github.com/SamurAIGPT/Generative-Media-Skills)

---

## Skills — Transcription

### podcast-transcript-txt-skill

Turn any podcast source into clean TXT — YouTube, episode webpages, Xiaoyuzhou, Apple Podcasts, X links, or just a title.

![Stars](https://img.shields.io/github/stars/KingJing1/podcast-transcript-txt-skill?style=flat) ![Last commit](https://img.shields.io/github/last-commit/KingJing1/podcast-transcript-txt-skill?style=flat) ![Language](https://img.shields.io/github/languages/top/KingJing1/podcast-transcript-txt-skill?style=flat)

⭐ 21 · Last updated: 2026-04-04 · [KingJing1/podcast-transcript-txt-skill](https://github.com/KingJing1/podcast-transcript-txt-skill)

---

## License

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

---

## Attribution

Fork of [danielrosehill/AI-Audio-Editing-Tools](https://github.com/danielrosehill/AI-Audio-Editing-Tools) by Daniel Rosehill,
licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Maintained here for local
modification; changes since the fork are the maintainer's own.
