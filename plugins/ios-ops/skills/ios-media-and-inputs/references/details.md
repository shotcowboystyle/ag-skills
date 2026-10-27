# iOS Media, ML, and Physical Inputs — details

## Framework boundaries

### Media and image processing

- `AVPlayer`/`AVPlayerItem` and `AVPlayerViewController` own playback state and native playback surfaces, not business truth or guaranteed first-frame/audio-route availability. Handle buffering, failure, end, interruption, route changes, external playback, and lifecycle transitions.
- `CIImage` is a lazy recipe. A `CIContext` renders it; reuse an appropriate context, but isolate mutable `CIFilter` instances from concurrent access. Preserve orientation, color space, and destination format.
- VideoToolbox is a low-level compression/decompression path. Model session creation, property configuration, frame submission, callback completion, pending-frame drain, invalidation, timestamps, pixel formats, and cleanup. Prefer higher-level AVFoundation when direct codec control is not the product need.

### Vision, Core ML, and Natural Language

Model availability, preprocessing, output validation, and evaluation belong to [ios-on-device-intelligence](../../ios-on-device-intelligence/SKILL.md). This skill keeps the frame/audio source, orientation, backpressure, and teardown that feed it.

### NFC, MusicKit, and ShazamKit

- Core NFC is a user-mediated foreground reader session. Validate the entitlement, usage description, supported formats/protocols, session timeout/invalidation, multiple tags, unsupported tags, and physical-device behavior. NDEF records and tag responses are untrusted bytes; a tag is not authenticity, payment, identity, ownership, or location proof.
- MusicKit has separate authorization, Apple Music capability/subscription, catalog, user-token/account, playback, and interruption state. Request informed consent, handle denial and account changes, preserve catalog provenance, and do not equate a catalog result with ownership or licensing.
- ShazamKit returns a match, no-match, or error from an acoustic signature. A match means resemblance to the selected catalog under the tested conditions; it is not speaker identity, recording ownership, legal clearance, or universal recognition. Stop matching when the feature ends and avoid retaining raw audio when a signature/result is sufficient.


## Related routes and recipes

- [Media, camera, and sensor routes](../../ios-knowledge-base/references/40-framework-routes/02-media-camera-and-sensors.md)
- [Media, Vision, Core ML, NFC, and Music deep dive](../../ios-knowledge-base/references/42-framework-deep-dives/07-media-vision-ml-and-nfc.md)
- [Media, Vision, Core ML, NFC, and Music recipes](../../ios-knowledge-base/references/70-code-recipes/21-media-vision-ml-and-nfc-recipes.md)
- [Privacy, availability, safety, and fallback](../../ios-knowledge-base/references/30-on-device-ai/06-privacy-availability-and-fallback.md)
- [Permission, entitlement, and privacy checklist](../../ios-knowledge-base/references/60-verification/04-permission-entitlement-and-privacy-checklist.md)
- [Build, device, and release checklist](../../ios-knowledge-base/references/60-verification/01-build-device-and-release-checklist.md)


## Sources

- [AVKit](https://developer.apple.com/documentation/avkit)
- [AVPlayerViewController](https://developer.apple.com/documentation/avkit/avplayerviewcontroller)
- [AVFoundation](https://developer.apple.com/documentation/avfoundation)
- [AVPlayer](https://developer.apple.com/documentation/avfoundation/avplayer)
- [AVAudioSession](https://developer.apple.com/documentation/avfaudio/avaudiosession)
- [Core Image](https://developer.apple.com/documentation/coreimage)
- [CIContext](https://developer.apple.com/documentation/coreimage/cicontext)
- [CIFilter](https://developer.apple.com/documentation/coreimage/cifilter-swift.class)
- [Video Toolbox](https://developer.apple.com/documentation/videotoolbox)
- [VTCompressionSession](https://developer.apple.com/documentation/videotoolbox/vtcompressionsession-api-collection)
- [Vision](https://developer.apple.com/documentation/vision)
- [VNImageRequestHandler](https://developer.apple.com/documentation/vision/vnimagerequesthandler)
- [VNRecognizeTextRequest](https://developer.apple.com/documentation/vision/vnrecognizetextrequest)
- [Core ML](https://developer.apple.com/documentation/coreml)
- [MLModel](https://developer.apple.com/documentation/coreml/mlmodel)
- [MLModelConfiguration](https://developer.apple.com/documentation/coreml/mlmodelconfiguration)
- [Natural Language](https://developer.apple.com/documentation/naturallanguage)
- [Core NFC](https://developer.apple.com/documentation/corenfc)
- [NFCNDEFReaderSession](https://developer.apple.com/documentation/corenfc/nfcndefreadersession)
- [NFCTagReaderSession](https://developer.apple.com/documentation/corenfc/nfctagreadersession)
- [Building an NFC Tag-Reader App](https://developer.apple.com/documentation/corenfc/building-an-nfc-tag-reader-app)
- [MusicKit](https://developer.apple.com/documentation/musickit)
- [ShazamKit](https://developer.apple.com/documentation/shazamkit)
- [SHSession](https://developer.apple.com/documentation/shazamkit/shsession)
- [Matching audio using the built-in microphone](https://developer.apple.com/documentation/shazamkit/matching-audio-using-the-built-in-microphone)
