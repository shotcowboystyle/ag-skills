# Meta Wearables source refresh — details

## Refresh workflow

1. Run the bundled public-ref checker, source-tree inventory checker, and team-manifest validator, then record UTC/local date, URL, page title, repository commit/tag, release, retrieval method, and every expected/observed root AI file, plugin manifest, product, exact plugin-role name, sample, artifact, SDK, reference, example, template, and local-handoff result. A `DRIFT` result is a refresh blocker, not permission to silently rewrite the manifest.
2. Compare current sources with the prior snapshot for package products, minimum OS/toolchain, registration/permission rules, session lifecycle, camera/audio, Display/input, MockDevice, Web Apps, device models, terms, and release limitations.
3. For every changed symbol, write a migration note: old wording/API, new wording/API, affected role package, code-review action, and test fixture.
4. Reconcile iOS/Android/Web sources without treating platform parity as proof that symbols or behavior are identical; update the Android API atlas when artifact/API conflicts change.
5. Re-check product-generation mappings. Preserve `to-verify` when an official API/model enum or physical device is missing.
6. Update the registry and freshness log, then run local link/fence/whitespace/required-`## Sources` validation.
7. Report what was source-proven, what was locally build-proven, and what still needs an authenticated doc, account, or physical hardware.


## Current snapshot fields

At minimum, track:

- DAT iOS tag/commit and release date;
- DAT Android tag/commit when parity is being discussed;
- iOS minimum and sample toolchain;
- camera/audio/session/display/mock changes;
- Web App repository/docs commit and constraints;
- device enum/model/capability changes;
- preview/access/terms/publishing changes;
- unresolved “Gen 3,” “regular SDK,” MCP, and physical-device questions.
- product announcements versus SDK identity, and authenticated Developer Center
  access state;
- full-reference module names versus importable package products, HFP/A2DP/IMU availability, and current App Store/release-channel policy.
- upstream `AGENTS.md`/plugin examples versus versioned changelog/package guidance,
  including iOS/Android minimums, DAM metadata, and `Session`/`DeviceSession`
  names;
- Web App capability conflicts between the full Developer Center index and the
  toolkit `main`; preserve the revisions and carry text/offline/back/gesture/
  sensor behavior as `source-conflict`/`to-verify` until target evidence closes
  the gap.
- version-dependency and operational signals, including Meta AI/firmware
  prerequisites, on-glasses DAT-app update routes, Developer Mode versus
  release-channel behavior, and first-party versus community troubleshooting
  reports; keep access-gated values and issue reports separately labeled.


## Hard boundaries

- Do not cite search snippets as the API contract when an official page or repository is available.
- Do not silently overwrite a previous source snapshot; preserve historical release notes.
- Do not infer a model mapping from a press release, and do not infer hardware support from an enum alone.
- Do not claim “full SDK coverage” while authenticated or unpublished docs, private preview behavior, or physical hardware remain unexamined.
- Do not resolve an official-source conflict by silently preferring a moving
  toolkit branch over a versioned/public Developer Center contract; record both
  and route the feature to the evidence packet.
- Do not copy upstream skill files wholesale; synthesize a source-linked local route and retain the upstream URL.


## Related routes

- [Meta agentic team](../../meta-wearables-agentic-team/SKILL.md)
- [Route planner](../../meta-wearables-route-planner/SKILL.md)
- [DAT iOS integration](../../meta-dat-ios-integration/SKILL.md)
- [Device proof](../../meta-wearables-device-proof/SKILL.md)
- [Operational readiness](../../meta-wearables-operational-readiness/SKILL.md)
- [Transport and runtime reliability](../../meta-wearables-transport-reliability/SKILL.md)
- [Debugging and observability](../../meta-wearables-debugging-observability/SKILL.md)
- [Application architecture](../../meta-wearables-app-architecture/SKILL.md)
- [Apple source refresh](https://github.com/shotcowboystyle/ios-ops-plugin/blob/main/.agent/skills/ios-source-refresh-and-availability/SKILL.md)


## Sources

- [Meta DAT iOS repository](https://github.com/facebook/meta-wearables-dat-ios)
- [Meta DAT Android repository](https://github.com/facebook/meta-wearables-dat-android)
- [DAT Android API surface atlas](../../meta-wearables-knowledge-base/references/70-meta-wearables/20-dat-android-api-surface-atlas.md)
- [Developer Center operations](../../meta-wearables-developer-operations/SKILL.md)
- [Meta DAT iOS changelog](https://github.com/facebook/meta-wearables-dat-ios/blob/main/CHANGELOG.md)
- [Meta Wearables Web App repository](https://github.com/facebook/meta-wearables-webapp)
- [Wearables Developer Center](https://wearables.developer.meta.com/docs/develop/)
- [Meta Wearables terms](https://wearables.developer.meta.com/docs/terms)
- [Meta Wearables acceptable use policy](https://wearables.developer.meta.com/docs/acceptable-use-policy)
- [Full Wearables platform reference](https://wearables.developer.meta.com/llms.txt?full=true)
- [Wearables version dependencies](https://wearables.developer.meta.com/docs/version-dependencies)
- [Wearables known issues](https://wearables.developer.meta.com/docs/knownissues)
- [Wearables release-channel guidance](https://wearables.developer.meta.com/docs/develop/dat/set-up-release-channels/)
- [Ray-Ban Meta Gen 2 announcement](https://about.fb.com/news/2025/09/ray-ban-meta-gen-2-better-battery-life-video-capture/)
- [Ray-Ban Meta Gen 2 and Optics announcement](https://about.fb.com/news/2026/03/meta-ai-glasses-built-for-prescriptions/)
- [Meta Glasses announcement](https://about.fb.com/news/2026/06/meta-essilorluxottica-partner-launch-meta-glasses/)
