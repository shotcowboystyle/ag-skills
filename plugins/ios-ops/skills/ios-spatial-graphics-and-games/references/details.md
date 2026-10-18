# iOS Spatial, Graphics, and Games — details

## Non-negotiable safety and evidence rules

- Do not present tracking, spatial mapping, an AR observation, a generated placement, or a static scene as identity, location truth, measurement, safety assurance, or physical-world guarantee without separate domain validation.
- Do not claim frame rate, GPU support, shader compatibility, memory headroom, battery life, thermal safety, controller ergonomics, spatial comfort, or multiplayer reliability from a preview, simulator, screenshot, newest-device run, or successful command buffer.
- Keep camera permission, tracking support, session readiness, entity loading, input availability, and current pose separate. A supported configuration can still be limited by lighting, surfaces, movement, device, or environment.
- Keep authentication, match connection, message delivery, server authority, and simulation state separate. A Game Center player or received packet is not permission, identity proof, trusted game state, or a successful multiplayer session.
- Treat assets, network messages, controller events, spatial observations, and saved transforms as untrusted or stale. Validate bounds/types, version protocols, reject malformed input, and require user confirmation before consequential external actions.
- Stop sessions, pause loops, cancel loads, release resources, and ignore stale callbacks on view disappearance, backgrounding, interruption, reset/relocalization, disconnect, cancellation, and teardown.


## Deliverable

Produce a compact route note or implementation change containing:

- selected framework and rejected alternatives;
- target/platform/device, scene role, permission, capability, entitlement, asset, input, Game Center, privacy, and fallback matrix;
- session/render/game state machine with pause, interruption, cancellation, cleanup, retry, and deterministic fixtures;
- domain/simulation-to-scene adapter boundary and persistence/provenance policy;
- accessibility and non-spatial completion path;
- source links plus exact compile, simulator, physical-device, performance, system-surface, signing, and release evidence plan;
- remaining `to-verify` gaps and claims deliberately not made.

For implementation, change only the requested target and directly related adapters/configuration. Do not add camera capture, motion/location access, multiplayer servers, Game Center features, cloud saves, analytics, telemetry, or entitlements without a stated user-facing need and authorization.


## Related routes and recipes

- [Spatial, graphics, and game routes](../../ios-knowledge-base/references/40-framework-routes/06-spatial-graphics-and-games.md)
- [RealityKit, ARKit, and spatial experiences](../../ios-knowledge-base/references/42-framework-deep-dives/04-realitykit-arkit-and-spatial.md)
- [Metal, SpriteKit, and game routes](../../ios-knowledge-base/references/42-framework-deep-dives/05-metal-spritekit-and-game-routes.md)
- [Spatial, graphics, and game recipes](../../ios-knowledge-base/references/70-code-recipes/18-spatial-graphics-and-game-recipes.md)
- [Accessibility and adaptability checklist](../../ios-knowledge-base/references/60-verification/02-accessibility-and-adaptability-checklist.md)
- [Build, device, and release checklist](../../ios-knowledge-base/references/60-verification/01-build-device-and-release-checklist.md)


## Sources

- [RealityKit](https://developer.apple.com/documentation/realitykit)
- [RealityView](https://developer.apple.com/documentation/realitykit/realityview)
- [Entity](https://developer.apple.com/documentation/realitykit/entity)
- [SceneEvents](https://developer.apple.com/documentation/realitykit/sceneevents)
- [ARKit](https://developer.apple.com/documentation/arkit)
- [ARSession](https://developer.apple.com/documentation/arkit/arsession)
- [run(_:options:)](https://developer.apple.com/documentation/arkit/arsession/run%28_%3Aoptions%3A%29)
- [ARWorldTrackingConfiguration](https://developer.apple.com/documentation/arkit/arworldtrackingconfiguration)
- [Tracking and visualizing planes](https://developer.apple.com/documentation/arkit/tracking-and-visualizing-planes)
- [ARPlaneAnchor](https://developer.apple.com/documentation/arkit/arplaneanchor)
- [Immersive spaces](https://developer.apple.com/documentation/swiftui/immersive-spaces)
- [ImmersiveSpace](https://developer.apple.com/documentation/swiftui/immersivespace)
- [Adding 3D content to your app](https://developer.apple.com/documentation/visionos/adding-3d-content-to-your-app)
- [Bringing your ARKit app to visionOS](https://developer.apple.com/documentation/visionos/bringing-your-arkit-app-to-visionos)
- [Creating fully immersive experiences in your app](https://developer.apple.com/documentation/visionos/creating-fully-immersive-experiences)
- [Metal](https://developer.apple.com/documentation/metal)
- [MTLDevice](https://developer.apple.com/documentation/metal/mtldevice)
- [SpriteKit](https://developer.apple.com/documentation/spritekit)
- [SpriteView](https://developer.apple.com/documentation/spritekit/spriteview)
- [SKScene](https://developer.apple.com/documentation/spritekit/skscene)
- [GameplayKit](https://developer.apple.com/documentation/gameplaykit)
- [GKStateMachine](https://developer.apple.com/documentation/gameplaykit/gkstatemachine)
- [GKEntity](https://developer.apple.com/documentation/gameplaykit/gkentity)
- [GKGraph](https://developer.apple.com/documentation/gameplaykit/gkgraph)
- [GameKit](https://developer.apple.com/documentation/gamekit)
- [Authenticating a player](https://developer.apple.com/documentation/gamekit/authenticating-a-player)
- [GKLocalPlayer](https://developer.apple.com/documentation/gamekit/gklocalplayer)
- [GKMatch](https://developer.apple.com/documentation/gamekit/gkmatch)
- [Improving your game’s graphics performance and settings](https://developer.apple.com/documentation/metal/improving-your-games-graphics-performance-and-settings)
- [Core Haptics](https://developer.apple.com/documentation/corehaptics)
