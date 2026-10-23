---
name: ffmpeg-encoder-detect
description: Pick the ffmpeg video encoder for this host — NVENC, VideoToolbox, QSV, AMF or VAAPI when the hardware really encodes, else libx264/libx265 — by test-encoding one frame with each candidate. The one detection routine the concatenator, aspect-converter and normalizer agents share. Use when an ai-video-producer step is about to re-encode video and needs to know which encoder works here.
---

# ffmpeg encoder detection

An encoder listed by `ffmpeg -encoders` can still fail: the GPU is missing, the driver is old, or the hardware won't take that codec. `lspci` and `nvidia-smi` don't prove ffmpeg can use it. So this skill test-encodes one black frame with each candidate and takes the first that succeeds.

## Run it

The script is `scripts/detect-encoder.sh` in this skill's folder. Find the installed folder by name; some tools prefix it, e.g. `ai-video-producer__ffmpeg-encoder-detect`.

```
sh <skill-folder>/scripts/detect-encoder.sh         # H.264
sh <skill-folder>/scripts/detect-encoder.sh hevc    # HEVC
```

It tries, in order: `*_nvenc` (NVIDIA), `*_videotoolbox` (macOS), `*_qsv` (Intel), `*_amf` (AMD on Windows), `*_vaapi` on each `/dev/dri/renderD*` (Linux AMD/Intel). If none works it prints `libx264` or `libx265`.

Output is one line: the encoder, or for VAAPI the encoder and its device (`h264_vaapi /dev/dri/renderD128`). Exit 1 means ffmpeg isn't installed.

## Use the result

State it before encoding: `Detected: h264_nvenc` (or `no hardware encoder, using libx264`).

| Encoder | Typical flags |
|---------|---------------|
| `h264_nvenc` / `hevc_nvenc` | `-c:v h264_nvenc -preset p5 -b:v 12M` |
| `h264_videotoolbox` / `hevc_videotoolbox` | `-c:v h264_videotoolbox -b:v 12M` |
| `h264_qsv` / `hevc_qsv` | `-c:v h264_qsv -global_quality 23` |
| `h264_amf` / `hevc_amf` | `-c:v h264_amf -quality quality -b:v 12M` |
| `h264_vaapi` / `hevc_vaapi` | `-vaapi_device <device>` before `-i`, then `-vf '<filters>,format=nv12,hwupload' -c:v h264_vaapi -qp 23` |
| `libx264` / `libx265` | `-c:v libx264 -preset medium -crf 18` |

Hardware encoders give lower quality per bit than libx264 at the same bitrate. For a final master where time doesn't matter, offer libx264 `-crf 18` even when a GPU encoder exists.

Run the detection once per session and reuse the answer for every clip.
