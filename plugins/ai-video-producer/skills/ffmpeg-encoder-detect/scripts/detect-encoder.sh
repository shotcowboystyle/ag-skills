#!/usr/bin/env sh
# Print the first hardware video encoder that actually encodes on this host,
# else the CPU encoder. Output: "<encoder>" or, for VAAPI, "<encoder> <device>".
# Usage: detect-encoder.sh [h264|hevc]   (default h264)
set -u
codec=${1:-h264}
case $codec in
  h264) cpu=libx264 ;;
  hevc) cpu=libx265 ;;
  *) echo "usage: detect-encoder.sh [h264|hevc]" >&2; exit 2 ;;
esac
command -v ffmpeg >/dev/null || { echo "detect-encoder: ffmpeg not found" >&2; exit 1; }

# A listed encoder can still fail (no GPU, no driver), so encode one real frame.
src="-f lavfi -i color=c=black:s=256x256:d=0.1"
for enc in "${codec}_nvenc" "${codec}_videotoolbox" "${codec}_qsv" "${codec}_amf"; do
  # shellcheck disable=SC2086
  if ffmpeg -hide_banner -loglevel error $src -frames:v 1 -c:v "$enc" -f null - >/dev/null 2>&1; then
    echo "$enc"; exit 0
  fi
done
for dev in /dev/dri/renderD*; do
  [ -e "$dev" ] || continue
  # shellcheck disable=SC2086
  if ffmpeg -hide_banner -loglevel error -vaapi_device "$dev" $src -frames:v 1 \
       -vf format=nv12,hwupload -c:v "${codec}_vaapi" -f null - >/dev/null 2>&1; then
    echo "${codec}_vaapi $dev"; exit 0
  fi
done
echo "$cpu"
