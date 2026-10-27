# DAT camera and audio — details

Camera and audio are separate capability contracts with their own ownership,
consent, backpressure, cancellation, and evidence. A phone microphone or a
simulated frame is not a glasses microphone or camera result.

## Symbol checks

Verify installed symbols and media types against the selected tag. The 0.9.0
notes use `DeviceSession.addCamera(config:) -> Camera`, `Camera.stream`,
`Camera.stop()`, and camera state; do not revive removed `addStream(config:)`
examples. Check `StreamError.hingesClosed`, current photo-failure cases, and
the background-camera sample behavior. Refresh the official
[DAT iOS camera/streaming skill](https://github.com/facebook/meta-wearables-dat-ios/tree/main/plugins/mwdat-ios/skills/camera-streaming)
and [debugging skill](https://github.com/facebook/meta-wearables-dat-ios/tree/main/plugins/mwdat-ios/skills/debugging).

## Camera workflow

1. Gate on registration, session readiness, model/capability, user intent, and camera permission as the current release requires.
2. Build the camera configuration from supported values in the installed API. Record resolution, frame rate, format/codec, orientation, and expected latency; do not invent a combination.
3. Own the camera from session start through `Camera.stop()` or equivalent. Cancel the consumer and stop the source on view exit, disconnect, error, and required lifecycle transitions.
4. Bound buffering. Decide whether the consumer drops, coalesces, or blocks frames, and measure the effect on UI, memory, thermal load, and battery.
5. Keep conversion and inference off the UI thread. Preserve source timestamps and ordering when downstream code needs them.
6. Test no-device, denied, interrupted, stale-session, slow-consumer, stop-while-streaming, and reconnect states.
7. Treat background continuation as target-specific `to-verify`; the sample and changelog wording is not a blanket background-capture guarantee.

## Audio workflow

1. Establish the documented audio source before designing transcription or upload. The public DAT guide documents HFP glasses-microphone input through platform audio APIs and A2DP playback; do not substitute an undocumented native module.
2. Distinguish phone microphone, HFP glasses microphone, A2DP playback, route changes, and remote transcription in names, permissions, logs, UI, and evidence.
3. Configure `AVAudioSession` (or the Android audio route) for the actual path with the required usage description. For camera + HFP follow the documented ordering and verify `bluetoothHFP`.
4. Define consent, recording indicator, pause/stop, retention, deletion, network transfer, vendor processing, and failure behavior before enabling audio.
5. Use manual text, phone mic, or an explicit unavailable state as fallback only when the product's privacy and UX contract permits it.

## Fixtures

Use the [iOS MockDevice fixture](../../meta-wearables-implementation-recipes/assets/meta-wearables-ios-mockdevice-starter/MetaWearablesMockDeviceStarter.swift)
or [Android MockDevice fixture](../../meta-wearables-implementation-recipes/assets/meta-wearables-android-mockdevice-starter/MetaWearablesAndroidMockDeviceStarter.kt)
to make denied permission, file feed, capture, fold/doff, tap, cancellation, and
teardown deterministic before requesting hardware evidence.

## Related

- [Apple media and inputs](https://github.com/shotcowboystyle/ag-skills/blob/main/plugins/ios-ops/skills/ios-media-and-inputs/SKILL.md)

## Sources

- [Meta DAT iOS camera streaming skill](https://github.com/facebook/meta-wearables-dat-ios/tree/main/plugins/mwdat-ios/skills/camera-streaming)
- [Meta DAT iOS changelog](https://github.com/facebook/meta-wearables-dat-ios/blob/main/CHANGELOG.md)
- [Meta Wearables Device Access Toolkit announcement](https://developers.meta.com/blog/introducing-meta-wearables-device-access-toolkit/)
- [Apple AVFoundation](https://developer.apple.com/documentation/avfoundation)
- [Apple AVAudioSession](https://developer.apple.com/documentation/avfaudio/avaudiosession)
- [Apple privacy manifest files](https://developer.apple.com/documentation/bundleresources/privacy-manifest-files)
- [Full Wearables platform reference](https://wearables.developer.meta.com/llms.txt?full=true)
