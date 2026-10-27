# Meta DAT iOS integration — details

## Required output

Return:

- package/tag/commit and actual module/product names;
- target configuration and callback/permission inventory;
- adapter state machine and lifecycle table;
- mock and build-test plan;
- privacy/data-handling decisions;
- exact unresolved API or device questions.


## Hard boundaries

- Do not put registration or permission calls in a view initializer.
- Do not treat pairing as a permanent authorization; model denial, revocation, disconnect, and re-registration.
- Do not log access tokens, callback URLs containing secrets, raw media, or persistent device identifiers.
- Do not claim a device is supported because the package compiles; runtime model/capability and hardware proof are separate.
- Do not assume iOS background execution, Meta AI voice commands, or raw glasses audio from DAT’s existence.


## Related routes

- [Meta route planner](../../meta-wearables-route-planner/SKILL.md)
- [Camera and audio](../../meta-dat-camera-audio/SKILL.md)
- [Display](../../meta-dat-display/SKILL.md)
- [Device proof](../../meta-wearables-device-proof/SKILL.md)
- [Operational readiness](../../meta-wearables-operational-readiness/SKILL.md)
- [Debugging and observability](../../meta-wearables-debugging-observability/SKILL.md)
- [Application architecture](../../meta-wearables-app-architecture/SKILL.md)
- [Apple system surfaces](https://github.com/shotcowboystyle/ag-skills/blob/main/plugins/ios-ops/skills/ios-system-surfaces-and-background/SKILL.md)
- [Apple privacy and release proof](https://github.com/shotcowboystyle/ag-skills/blob/main/plugins/ios-ops/skills/ios-release-proof/SKILL.md)


## Sources

- [Meta DAT iOS repository](https://github.com/facebook/meta-wearables-dat-ios)
- [Meta DAT iOS changelog](https://github.com/facebook/meta-wearables-dat-ios/blob/main/CHANGELOG.md)
- [DAT iOS permissions and registration skill](https://github.com/facebook/meta-wearables-dat-ios/tree/main/plugins/mwdat-ios/skills/permissions-registration)
- [DAT iOS session lifecycle skill](https://github.com/facebook/meta-wearables-dat-ios/tree/main/plugins/mwdat-ios/skills/session-lifecycle)
- [DAT iOS sample-app guide](https://github.com/facebook/meta-wearables-dat-ios/tree/main/plugins/mwdat-ios/skills/sample-app-guide)
- [Full Wearables platform reference](https://wearables.developer.meta.com/llms.txt?full=true)
- [Build integration for iOS](https://wearables.developer.meta.com/docs/build-integration-ios)
- [Apple app life cycle](https://developer.apple.com/documentation/uikit/managing-your-app-s-life-cycle)
- [Apple privacy manifest files](https://developer.apple.com/documentation/bundleresources/privacy-manifest-files)
