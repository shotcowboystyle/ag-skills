[Part of the shotcowboystyle marketplace](../../README.md)

## Meta Wearables Ops Plugin

**Version:** 0.2.0

Meta smart-glasses engineering — Wearables Device Access SDK integration on iOS and Android, camera, display, sensors, transport reliability, on-device compliance, and device-backed release proof.

Pairs with [`ios-ops`](../ios-ops/README.md), which owns general Apple-platform work.
Each works on its own.

## Installation

Part of the [ag-skills](../../README.md) marketplace. In Claude Code:

```bash
/plugin marketplace add shotcowboystyle/ag-skills
/plugin install meta-wearables-ops@claude-code-workflows
```

For Codex CLI, Cursor, OpenCode, Antigravity CLI, GitHub Copilot, and Pi, see
[docs/harnesses.md](../../docs/harnesses.md).

## Commands


## Skills

- **meta-dat-android-api-atlas** — Map and review the public Meta Wearables Device Access Toolkit Android API and artifact surface with exact Gradle/Maven coordinates, Kotlin/Java symbols, 0.9 migrations, Display/camera/MockDevice/debugging boundaries, and separate compile, mock, connected, physical, and release evidence. Use for Android DAT implementation, Kotlin or Java parity, full-SDK audits, or any request involving Android Meta glasses capabilities.
- **meta-dat-android-integration** — Integrate and review the public Meta Wearables Device Access Toolkit for Android with exact Maven artifacts, Gradle/Manifest configuration, registration, typed DatResult flows, sessions, camera, Display, MockDevice, privacy, and separate physical-device evidence. Use when a request mentions DAT Android, Kotlin, Gradle, Android glasses integration, or cross-platform parity.
- **meta-dat-api-atlas** — Map and refresh the public Meta DAT iOS API surface, upstream role skills, sample apps, MCP/docs tooling, configuration keys, and DAT-versus-Web-Apps boundary without inventing release-specific symbols. Use when an implementation needs exact MWDAT modules, current 0.9 migration details, debugging tools, or broader SDK coverage.
- **meta-dat-camera-audio** — Design and review Meta DAT camera and audio features with exact SDK-version checks, stream ownership, cancellation, AVFoundation boundaries, privacy-aware consent, and separate phone/mock/connected-glasses evidence. Use for wearable camera, microphone, preview, capture, transcription, or media-processing requests.
- **meta-dat-display** — Design and implement native Meta DAT Display surfaces with capability gating, compact glanceable state, ButtonGroup/input handling, clear teardown, phone handoff, and physical Ray-Ban Display evidence. Use for native glasses UI requests, not for Web App HTML surfaces.
- **meta-dat-ios-integration** — Integrate the current Meta Wearables Device Access Toolkit into a native iOS companion app with source-checked package setup, registration, permissions, URL callbacks, session lifecycle, privacy controls, and testable unavailable states. Use when adding or reviewing DAT iOS code.
- **meta-wearables-agentic-team** — Orchestrate source-grounded iOS companion apps, Meta Wearables Device Access Toolkit integrations, Meta Ray-Ban Display Web Apps, and physical-device proof across Ray-Ban Meta, Oakley Meta, and other supported Meta wearables. Use when planning, building, reviewing, or releasing a wearable feature that needs an explicit route, privacy contract, device matrix, or evidence ledger.
- **meta-wearables-app-architecture** — Architect maintainable iOS, Android, and Ray-Ban Display applications on top of Meta Wearables DAT without leaking platform SDKs into UI or domain code. Use when starting a wearable app, adding camera/audio/Display/Web App capabilities, sharing behavior across Swift and Kotlin, designing phone-first fallbacks, or turning a DAT feature plan into adapters, state machines, test seams, and release-ready modules.
- **meta-wearables-debugging-observability** — Diagnose Meta Wearables DAT iOS and Android setup, registration, permission, device-link, session, camera, audio, Display, and transport failures with source-grounded, read-only evidence. Use when a DAT app cannot communicate with glasses, a stream or Display session fails, live DAT Inspector MCP tools are available, logs need a redacted diagnostic bundle, or a team must separate app bugs from Meta AI companion, firmware, device, and release-channel boundaries.
- **meta-wearables-developer-operations** — Operate and audit the Meta Wearables Developer Center lifecycle for DAT iOS/Android and Ray-Ban Display Web Apps, including Managed Meta Account organization/team access, projects, platform app identities, product listings, permission justifications, versions, release channels, testers, Meta AI channel state, telemetry, and recovery. Use when onboarding a team, configuring a project, preparing a DAT release, diagnosing channel access, reviewing telemetry/privacy, or separating Developer Mode from signed distribution.
- **meta-wearables-device-compatibility** — Resolve Meta Wearables product labels, DAT iOS/Android versions, Web Apps revisions, glasses firmware, Meta AI companion versions, and capability support without inventing Gen 3 or “regular SDK” mappings. Use for Gen 2/Gen 3 support, firmware drift, version-dependency tables, device compatibility failures, release upgrades, cross-platform matrices, or any claim that a named Ray-Ban/Meta wearable is supported.
- **meta-wearables-device-proof** — Plan and audit reproducible target preflight and evidence for Meta Wearables apps across source inspection, iOS/Android/Web App inventory, unit/build checks, DAT MockDevice, browser simulator, connected-device tests, and physical Ray-Ban/Oakley/Meta glasses. Use whenever a result could be mistaken for hardware, model, camera, audio, Display, input, or release proof.
- **meta-wearables-full-sdk-audit** — Audit whether a Meta Wearables iOS, Android, or Ray-Ban Display Web App request actually covers the full public SDK surface, exact modules/artifacts, capability gates, upstream source conflicts, privacy boundaries, and required evidence. Use when a request says full SDK, regular SDK, all capabilities, Gen 2/Gen 3 support, or cross-platform parity.
- **meta-wearables-implementation-recipes** — Turn a selected Meta Wearables API row and vertical-slice playbook into source-aligned Swift, Kotlin/Java, or Ray-Ban Display Web App implementation scaffolding with explicit compile, privacy, lifecycle, fallback, and physical-device gates. Use when building or reviewing a concrete iOS DAT, Android DAT, native Display, Web App, or cross-platform wearable feature after route selection.
- **meta-wearables-input-sensors** — Design and verify Meta Wearables physical input and sensor experiences across native DAT Display, Ray-Ban Display Web Apps, and phone fallbacks, while keeping hardware signals, browser APIs, permissions, lifecycle, and physical-device evidence separate.
- **meta-wearables-on-device-compliance** — Enforce on-device and product-compliance boundaries for Meta Wearables iOS DAT, Android DAT, native Display, and Ray-Ban Display Web Apps. Use when designing or reviewing camera, glasses-microphone, audio, sensor, Display, local-first, privacy, permission, thermal, network, background, fallback, or release behavior.
- **meta-wearables-operational-readiness** — Diagnose and harden Meta Wearables DAT iOS, DAT Android, native Display, and Ray-Ban Display Web App integrations across firmware, Meta AI companion, Developer Mode, release channels, DAT app provisioning, compatibility, thermal and link failures, and recovery evidence. Use when an integration will not register, cannot start a session, reports an update or device-unavailable error, moves from Developer Mode to a signed release channel, or needs a repeatable operational-readiness packet.
- **meta-wearables-privacy-publishing** — Audit privacy, consent, iOS permissions, data flows, Meta Wearables terms, acceptable use, App Store metadata, and release gates for DAT and Web App products. Use whenever a wearable feature captures camera/audio, uses personal context, connects a cloud service, or is prepared for testing or publishing.
- **meta-wearables-route-planner** — Choose the correct Meta Wearables route across native iOS DAT, native Display, Ray-Ban Display Web Apps, phone fallback, and unsupported or unverified device requests. Use before implementation whenever a product mentions Ray-Ban Meta, Oakley Meta, Meta Glasses, Display, camera, audio, input, sensors, Gen 2, Gen 3, or the Meta Wearables SDK.
- **meta-wearables-security-attestation** — Audit Meta Wearables DAT iOS and Android identity, attestation, callback, release-channel, package-token, privacy-manifest, and secret-handling boundaries. Use when configuring Developer Mode or release builds, reviewing MetaAppID/ClientToken/application IDs, diagnosing registration failures, protecting Android package credentials, validating callback inputs, or making on-device and publishing claims for native DAT or Ray-Ban Display Web Apps.
- **meta-wearables-source-refresh** — Refresh the Meta Wearables DAT, Web Apps, device, terms, and Apple integration knowledge base with exact official URLs, release/tag/commit, retrieval date, API migrations, access gaps, and evidence boundaries, including a portable public Git ref drift check. Use before version-sensitive implementation, after an SDK release, or when a device-generation claim may have drifted.
- **meta-wearables-transport-reliability** — Design and review Meta Wearables DAT transport and runtime reliability across Bluetooth, Wi-Fi/local network, HFP/A2DP audio, camera and Display backpressure, background, thermal/power, disconnect, and recovery paths on iOS and Android. Use for Wi-Fi streaming, local-network configuration, audio-route failures, link instability, latency, dropped frames, transport parity, or reliability claims.
- **meta-wearables-web-apps** — Build and review Meta Wearables Web Apps for the Ray-Ban Display with the official HTML/CSS/JavaScript route, 600×600 display contract, public HTTPS delivery, focus and D-pad/EMG input, performance limits, source-conflict handling, and separate simulator/physical-device evidence.

## Knowledge base

`skills/meta-wearables-knowledge-base/references/70-meta-wearables/` ships with the plugin and is what the skills route into. Skills link
into it with relative paths that resolve inside the installed tree. Provenance lives in
`skills/meta-wearables-knowledge-base/references/sources/`, which records which upstream documents back the corpus and
when they were last checked.

## Conventions

- **Cite or say you cannot.** Substantive claims trace to a knowledge-base document or to
  upstream documentation. Uncited claims are marked unverified.
- **Written is not verified.** Documentation says one thing; a device shows another. The
  two are never conflated.
- **Never invent a proof.** An unrun verification leaves its row empty.

## Author

Curtis Blanton — [shotcowboystyle.com](https://shotcowboystyle.com)

## License

MIT
