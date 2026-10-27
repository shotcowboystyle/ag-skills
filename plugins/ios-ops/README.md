[Part of the shotcowboystyle marketplace](../../README.md)

## iOS Ops Plugin

**Version:** 0.3.0

Native iOS and Apple-platform engineering guidance — SwiftUI, Liquid Glass, on-device intelligence, framework routing, and device-backed release verification, grounded in a versioned knowledge base that ships with the plugin.

Pairs with [`meta-wearables-ops`](../meta-wearables-ops/README.md), which owns Meta smart-glasses work.
Each works on its own.

## Installation

Part of the [ag-skills](../../README.md) marketplace. In Claude Code:

```bash
/plugin marketplace add shotcowboystyle/ag-skills
/plugin install ios-ops@claude-code-workflows
```

For Codex CLI, Cursor, OpenCode, Antigravity CLI, GitHub Copilot, and Pi, see
[docs/harnesses.md](../../docs/harnesses.md).

## Skills

Start with **ios-route-planner** for a new app or feature; it hands each lane to one owning skill.

| Skill | Owns |
| --- | --- |
| **ios-route-planner** | Idea to Apple framework route, data boundary, permission matrix, verification plan |
| **ios-project-target-architect** | Xcode targets, modules, packages, extensions, schemes, capabilities |
| **ios-native-design** | SwiftUI screens and flows, Liquid Glass, adaptive layout, accessibility, motion |
| **ios-on-device-intelligence** | Foundation Models, Core ML, Vision, Speech, Translation, Natural Language, App Intents for AI |
| **ios-media-and-inputs** | Camera, audio, playback, image/video processing, NFC, MusicKit, ShazamKit |
| **ios-data-and-device-services** | SwiftData, CloudKit, HealthKit, Contacts, EventKit, WeatherKit, HomeKit, Bluetooth, Nearby Interaction |
| **ios-commerce-identity-and-security** | StoreKit, Apple Pay, Wallet, sign-in, Keychain, LocalAuthentication, CryptoKit, App Attest |
| **ios-system-surfaces-and-background** | Widgets, Live Activities, extensions, File Provider, App Groups, BackgroundTasks, WebKit/PDF |
| **ios-companion-communications** | WatchConnectivity, CarPlay, App Clips, CallKit, LiveCommunicationKit, PushKit, notifications |
| **ios-spatial-graphics-and-games** | ARKit, RealityKit, Metal, SpriteKit, GameplayKit, Game Center |
| **ios-release-proof** | Swift Testing/XCTest, device and system proof, privacy manifests, performance, archives, TestFlight |
| **ios-knowledge-base** | Shared reference library the other skills cite |

## Knowledge base

`skills/ios-knowledge-base/references/` ships with the plugin and is what the skills route into. Skills link
into it with relative paths that resolve inside the installed tree and grep it rather than reading whole files.
Provenance lives in `skills/ios-knowledge-base/references/sources/`, one file per domain, which records the
official pages behind each route. The corpus was source-checked against iOS 26 / Xcode 26 on 2026-08-19.

To refresh it after an SDK release: re-open the official pages in `sources/`, update the affected documents,
bump the date in `sources/README.md` and the `last_verified` field of each skill, and rerun the quality gates.

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
