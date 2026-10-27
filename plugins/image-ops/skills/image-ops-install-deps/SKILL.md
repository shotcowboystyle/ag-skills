---
name: image-ops-install-deps
description: Provision the plugin's tools — system binaries via the host package manager, Python tools into a plugin-owned uv venv at <data-dir>/venv/. Idempotent doctor — run before any command reports a missing dep. Never touches system Python or fights PEP 668. Use when a command reports a missing tool, or on a new machine.
disable-model-invocation: true
allowed-tools: Bash(which *), Bash(command *), Bash(uname *), Bash(test *), Bash(ls *), Bash(brew *), Bash(uv *), Bash(python3 *), Bash(magick *), Bash(convert *), Bash(identify *), Bash(exiftool *), Bash(fdupes *), Bash(vips *), Bash(vipsthumbnail *), Bash(heif-convert *), Bash(oxipng *), Bash(pngquant *), Bash(jpegoptim *), Bash(cjpeg *), Bash(cwebp *), Bash(avifenc *), Bash(cjxl *), Bash(djxl *), Bash(img2pdf *), Bash(pdftoppm *), Bash(jq *), Bash(upscayl-bin *), Bash(realesrgan-ncnn-vulkan *), Bash(darktable-cli *), Read, Write
---

# Install Dependencies

Two surfaces:

1. **System binaries** — required: `ImageMagick`, `exiftool`. Optional: `libvips-tools`, `libheif-examples`, `oxipng`, `pngquant`, `jpegoptim`, `mozjpeg`, `webp`, `libavif-bin`, `libjxl-tools`, `poppler-utils`, `img2pdf`, `jq`, `fdupes`, Upscayl / `realesrgan-ncnn-vulkan`, `darktable-cli`.
2. **Python tools** — `imagehash`, `Pillow` (perceptual dedupe). Installed into a plugin-owned uv venv at `<data-dir>/venv/`.

The plugin invokes Python via `<data-dir>/venv/bin/python`, so the user's system Python stays untouched and PEP 668 / externally-managed-environment errors never occur.

## Resolve paths

```bash
PLUGIN_DATA_DIR="${CLAUDE_USER_DATA:-${XDG_DATA_HOME:-$HOME/.local/share}/claude-plugins}/image-ops"
VENV_DIR="$PLUGIN_DATA_DIR/venv"
```

## Rules for this skill

**Confirm with the user before executing any command that installs software.** Show the exact command, say what it installs, and wait. This applies to every row of the matrix below and to the `uv` bootstrap, not only the rows with an inline caveat.

No privileged or remote-code command is pre-approved. `sudo`, `curl`, `sh`, `apt`, `dnf`, `pacman`, `cargo` and `pipx` are left out of `allowed-tools`, since `Bash(sudo *)` is an unrestricted root grant. Each one goes through the normal permission prompt or is handed to the user to run (in Claude Code: `! sudo apt install …`).

Never install anything the user did not ask for. A missing *optional* tool is a reported status, not a task.

## Procedure

### 1. Detect host

```bash
uname -s
which apt-get apt brew dnf pacman 2>/dev/null
which uv 2>/dev/null
```

Record what's available; this drives which install commands you propose.

### 2. Ensure `uv` is available

`uv` is the only hard prerequisite for the Python side. If missing, propose:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Ask before running, and say it pipes a remote script into a shell unverified. Offer `brew install uv`, `pipx install uv` or the distro package instead. Fall back to system pip with `--break-system-packages` only if the user declines all of them — prefer `uv`.

### 3. Walk the system-binary matrix

| Tool | Detect | Required? | Install (apt) | Install (brew) |
|---|---|---|---|---|
| `magick` / `convert` / `identify` | `which magick \|\| which convert` | required | `sudo apt install imagemagick` | `brew install imagemagick` |
| `exiftool` | `which exiftool` | required | `sudo apt install libimage-exiftool-perl` | `brew install exiftool` |
| `fdupes` | `which fdupes` | optional | `sudo apt install fdupes` | `brew install fdupes` |
| `vips` / `vipsthumbnail` | `which vips` | optional (recommended >500 images) | `sudo apt install libvips-tools` | `brew install vips` |
| `heif-convert` | `which heif-convert` | optional | `sudo apt install libheif-examples` | `brew install libheif` |
| `oxipng` | `which oxipng` | optional | `sudo apt install oxipng` | `brew install oxipng` |
| `pngquant` | `which pngquant` | optional | `sudo apt install pngquant` | `brew install pngquant` |
| `jpegoptim` | `which jpegoptim` | optional | `sudo apt install jpegoptim` | `brew install jpegoptim` |
| `cwebp` | `which cwebp` | optional (`web-ready`, `/convert-to-webp`) | `sudo apt install webp` | `brew install webp` |
| `mozjpeg` | `ls "$(brew --prefix mozjpeg 2>/dev/null)/bin/cjpeg" /opt/mozjpeg/bin/cjpeg 2>/dev/null` | optional | build from source, or a distro package if one exists | `brew install mozjpeg` |
| `avifenc` | `which avifenc` | optional | `sudo apt install libavif-bin` | `brew install libavif` |
| `cjxl` / `djxl` | `which cjxl` | optional | `sudo apt install libjxl-tools` | `brew install jpeg-xl` |
| `pdftoppm` / `pdfimages` / `pdfinfo` (poppler) | `which pdftoppm` | optional (`pdf-to-images`, `pdf-extract-embedded-images`) | `sudo apt install poppler-utils` | `brew install poppler` |
| `jq` | `which jq` | optional (`read-metadata` summaries) | `sudo apt install jq` | `brew install jq` |
| `upscayl-bin` | `which upscayl-bin \|\| ls /opt/Upscayl/resources/bin/upscayl-bin /Applications/Upscayl.app/Contents/Resources/bin/upscayl-bin 2>/dev/null` | optional | install Upscayl from <https://upscayl.org> (deb / flatpak / appimage) | `brew install --cask upscayl` |
| `realesrgan-ncnn-vulkan` (fallback) | `which realesrgan-ncnn-vulkan` | optional | binary release from upstream | binary release from upstream |
| `darktable-cli` | `which darktable-cli` | optional | `sudo apt install darktable` (GUI + CLI) | `brew install darktable` |
| `img2pdf` | `which img2pdf` | optional | `uv tool install img2pdf` (or `sudo apt install python3-img2pdf`) | `pipx install img2pdf` |

For each missing tool, stage its install command tagged required/optional. A missing required tool blocks the install; say so clearly.

`realesrgan-ncnn-vulkan` and `mozjpeg` are not in apt: point at the upstream releases, never auto-download. Ask before placing binaries under `~/bin/`.

**mozjpeg's binaries are named `cjpeg` / `djpeg` / `jpegtran`, exactly like libjpeg-turbo's.** Homebrew keeps the formula keg-only so it does not shadow the system copies, which means `which cjpeg` finding something proves nothing about mozjpeg. Detect it by prefix path (as in the matrix row above) and report the resolved directory in the status table — `optimize-jpeg` and `web-ready` both need that path, not a bare binary name.

### 4. Provision the venv

If `<VENV_DIR>` doesn't exist:

```bash
uv venv "$VENV_DIR" --python 3.11
```

If it exists, leave it.

### 5. Install Python packages into the venv

| Package | Required? | Used by |
|---|---|---|
| `Pillow` | required | dedupe (perceptual), inspection |
| `imagehash` | required | dedupe (perceptual) |
| `numpy` | required (Pillow/imagehash dep) | dedupe |
| `cairosvg` | optional | `svg-to-raster` (SVG → PNG/PDF). Needs system `libcairo2` (preinstalled on most Linux/macOS). |
| `vtracer` | optional | `vectorize` (raster → SVG). Self-contained wheel (bundled Rust binary). |
| `opencv-python-headless` | optional | `auto-deskew` photo mode (Hough-line skew detection). |

Stage:

```bash
uv pip install --python "$VENV_DIR/bin/python" Pillow imagehash numpy
# Optional — only if the user wants SVG conversion / vectorization / photo deskew:
uv pip install --python "$VENV_DIR/bin/python" cairosvg vtracer opencv-python-headless
```

`--python "$VENV_DIR/bin/python"` avoids `source`-ing an activate script, which would not survive to the next Bash call.

If `cairosvg` import fails at runtime with a libcairo error, prompt the user to install the system lib: `sudo apt install libcairo2` (Linux) / `brew install cairo` (macOS).

### 6. Verify

After installs, re-run the detect commands and report a green/red status table per tool. List the install commands the user still needs to run themselves (every `sudo` command, plus any they declined).

## Output

Single status report:
- Required system bins: present / missing.
- Optional system bins: present / missing (with one-line reason to install each).
- mozjpeg: the resolved prefix directory, or missing.
- Venv: provisioned at `<VENV_DIR>`, Python `<version>`.
- Python packages: installed.

Refuse to mark "OK" if any required tool is missing.
