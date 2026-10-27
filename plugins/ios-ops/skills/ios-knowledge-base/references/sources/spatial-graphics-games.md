# Official sources: Spatial, graphics, and games

Checked against Apple documentation on **2026-08-19** (iOS 26 / Xcode 26 SDK cycle). Apple documentation changes; re-open the page before relying on a version-sensitive API.

## GameKit and Game Center

| Topic | Official source |
| --- | --- |
| GameKit framework | [GameKit](https://developer.apple.com/documentation/gamekit/) |
| Game Center entitlement | [Game Center entitlement](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.game-center) |
| Player authentication | [Authenticating a player](https://developer.apple.com/documentation/gamekit/authenticating-a-player), [GKLocalPlayer](https://developer.apple.com/documentation/gamekit/gklocalplayer), and [GKPlayer](https://developer.apple.com/documentation/gamekit/gkplayer) |
| Access point and system surface | [GKAccessPoint](https://developer.apple.com/documentation/gamekit/gkaccesspoint) |
| Achievements | [GKAchievement](https://developer.apple.com/documentation/gamekit/gkachievement) and [GKAchievementDescription](https://developer.apple.com/documentation/gamekit/gkachievementdescription) |
| Leaderboards | [GKLeaderboard](https://developer.apple.com/documentation/gamekit/gkleaderboard) and [GKLeaderboardSet](https://developer.apple.com/documentation/gamekit/gkleaderboardset) |
| Friends and social routes | [Connecting players with their friends in your game](https://developer.apple.com/documentation/gamekit/connecting-players-with-their-friends-in-your-game) |
| Real-time multiplayer | [Finding multiple players for a game](https://developer.apple.com/documentation/gamekit/finding-multiple-players-for-a-game), [Creating real-time games](https://developer.apple.com/documentation/gamekit/creating-real-time-games), [GKMatchRequest](https://developer.apple.com/documentation/gamekit/gkmatchrequest), [GKMatchmaker](https://developer.apple.com/documentation/gamekit/gkmatchmaker), and [GKMatch](https://developer.apple.com/documentation/gamekit/gkmatch) |
| Turn-based multiplayer | [Creating turn-based games](https://developer.apple.com/documentation/gamekit/creating-turn-based-games), [Starting turn-based matches and passing turns between players](https://developer.apple.com/documentation/gamekit/starting-turn-based-matches-and-passing-turns-between-players), [GKTurnBasedMatch](https://developer.apple.com/documentation/gamekit/gkturnbasedmatch), and [GKTurnBasedEventListener](https://developer.apple.com/documentation/gamekit/gkturnbasedeventlistener) |
| Game activities | [Creating activities for your game](https://developer.apple.com/documentation/gamekit/creating-activities-for-your-game) |
| Game Center design | [Game Center](https://developer.apple.com/design/human-interface-guidelines/game-center) and [Designing for games](https://developer.apple.com/design/human-interface-guidelines/designing-for-games/) |

## SwiftUI Nearby Interaction and spatial-peer review

| Topic | Official source |
| --- | --- |
| Framework and capability | [Nearby Interaction](https://developer.apple.com/documentation/nearbyinteraction), [Initiating and maintaining a session](https://developer.apple.com/documentation/nearbyinteraction/initiating-and-maintaining-a-session), [NISession](https://developer.apple.com/documentation/nearbyinteraction/nisession), and [NISession device capabilities](https://developer.apple.com/documentation/nearbyinteraction/nisession/devicecapabilities) |
| Tokens and peer configurations | [NIDiscoveryToken](https://developer.apple.com/documentation/nearbyinteraction/nidiscoverytoken), [NISession discovery token](https://developer.apple.com/documentation/nearbyinteraction/nisession/discoverytoken), [NINearbyPeerConfiguration](https://developer.apple.com/documentation/nearbyinteraction/ninearbypeerconfiguration), and [NINearbyAccessoryConfiguration](https://developer.apple.com/documentation/nearbyinteraction/ninearbyaccessoryconfiguration) |
| Session lifecycle and measurements | [NISessionDelegate](https://developer.apple.com/documentation/nearbyinteraction/nisessiondelegate), [NINearbyObject](https://developer.apple.com/documentation/nearbyinteraction/ninearbyobject), [Nearby Interaction errors](https://developer.apple.com/documentation/nearbyinteraction/nierror), [userDidNotAllow](https://developer.apple.com/documentation/nearbyinteraction/nierror/userdidnotallow), and [NINearbyObject distance](https://developer.apple.com/documentation/nearbyinteraction/ninearbyobject/distance-676dm) |
| Peer discovery and token exchange | [Implementing interactions between users in close proximity](https://developer.apple.com/documentation/nearbyinteraction/implementing-interactions-between-users-in-close-proximity), [Discovering peers with Multipeer Connectivity](https://developer.apple.com/documentation/nearbyinteraction/discovering-peers-with-multipeer-connectivity), [Multipeer Connectivity](https://developer.apple.com/documentation/multipeerconnectivity), and [Network Framework](https://developer.apple.com/documentation/network) |
| Accessory and camera-assisted spatial routes | [Implementing spatial interactions with third-party accessories](https://developer.apple.com/documentation/nearbyinteraction/implementing-spatial-interactions-with-third-party-accessories), [Finding devices with precision](https://developer.apple.com/documentation/nearbyinteraction/finding-devices-with-precision), [NINearbyAccessoryConfiguration](https://developer.apple.com/documentation/nearbyinteraction/ninearbyaccessoryconfiguration), and [ARKit](https://developer.apple.com/documentation/arkit) |
| Privacy, design, AI, and release proof | [NSNearbyInteractionUsageDescription](https://developer.apple.com/documentation/bundleresources/information-property-list/nsnearbyinteractionusagedescription), [NSLocalNetworkUsageDescription](https://developer.apple.com/documentation/bundleresources/information-property-list/nslocalnetworkusagedescription), [NSBonjourServices](https://developer.apple.com/documentation/bundleresources/information-property-list/nsbonjourservices), [Foundation Models](https://developer.apple.com/documentation/foundationmodels), [Adopting Liquid Glass](https://developer.apple.com/documentation/technologyoverviews/liquid-glass), [Accessibility fundamentals](https://developer.apple.com/documentation/swiftui/accessibility-fundamentals), and [Testing a release build](https://developer.apple.com/documentation/xcode/testing-a-release-build) |

## Data, commerce, device, and spatial routes

| Topic | Official source |
| --- | --- |
| Local persistence | [SwiftData](https://developer.apple.com/documentation/swiftdata/) |
| SwiftData model data | [Preserving your app’s model data across launches](https://developer.apple.com/documentation/swiftdata/preserving-your-apps-model-data-across-launches) |
| Cloud data | [CloudKit](https://developer.apple.com/documentation/cloudkit) |
| Explicit private/shared synchronization | [CKSyncEngine](https://developer.apple.com/documentation/cloudkit/cksyncengine), [CKSyncEngineDelegate](https://developer.apple.com/documentation/cloudkit/cksyncenginedelegate), and [CKSyncEngine.State](https://developer.apple.com/documentation/cloudkit/cksyncengine/state) |
| SwiftData automatic iCloud sync | [Syncing model data across a person’s devices](https://developer.apple.com/documentation/swiftdata/syncing-model-data-across-a-persons-devices) |
| CloudKit sharing | [Sharing CloudKit Data with Other iCloud Users](https://developer.apple.com/documentation/cloudkit/sharing-cloudkit-data-with-other-icloud-users) and [Shared Records](https://developer.apple.com/documentation/cloudkit/shared-records) |
| Legacy/powerful persistence | [Core Data](https://developer.apple.com/documentation/coredata) |
| Digital commerce | [StoreKit](https://developer.apple.com/documentation/storekit) |
| StoreKit API choice | [Choosing a StoreKit API for In-App Purchases](https://developer.apple.com/documentation/storekit/choosing-a-storekit-api-for-in-app-purchases) |
| Maps | [MapKit](https://developer.apple.com/documentation/mapkit) |
| Location | [Core Location](https://developer.apple.com/documentation/corelocation) |
| Photo picker | [PhotosUI](https://developer.apple.com/documentation/photosui) |
| Photo library | [PhotoKit](https://developer.apple.com/documentation/photokit) |
| Audio/video | [AVFoundation](https://developer.apple.com/documentation/avfoundation) |
| Haptics | [Core Haptics](https://developer.apple.com/documentation/corehaptics) |
| Health data | [HealthKit](https://developer.apple.com/documentation/healthkit) |
| Home automation | [HomeKit](https://developer.apple.com/documentation/homekit) |
| Bluetooth | [Core Bluetooth](https://developer.apple.com/documentation/corebluetooth) |
| NFC | [Core NFC](https://developer.apple.com/documentation/corenfc) |
| Motion and fitness sensors | [Core Motion](https://developer.apple.com/documentation/coremotion) |
| AR | [ARKit](https://developer.apple.com/documentation/arkit) |
| 3D and spatial experiences | [RealityKit](https://developer.apple.com/documentation/realitykit) |
| Room scanning | [RoomPlan](https://developer.apple.com/documentation/roomplan) |
| GPU graphics | [Metal](https://developer.apple.com/documentation/metal) |
| 2D games | [SpriteKit](https://developer.apple.com/documentation/spritekit) |

## Additional framework roots

| Framework family | Official source |
| --- | --- |
| ARKit and RealityKit spatial-scene review | [ARKit](https://developer.apple.com/documentation/arkit), [ARSession](https://developer.apple.com/documentation/arkit/arsession), [ARCamera](https://developer.apple.com/documentation/arkit/arcamera), [ARWorldTrackingConfiguration](https://developer.apple.com/documentation/arkit/arworldtrackingconfiguration), [ARRaycastQuery](https://developer.apple.com/documentation/arkit/arraycastquery), [ARWorldMap](https://developer.apple.com/documentation/arkit/arworldmap), [RealityKit](https://developer.apple.com/documentation/realitykit), [ARView](https://developer.apple.com/documentation/realitykit/arview), [Entity](https://developer.apple.com/documentation/realitykit/entity), [AnchorEntity](https://developer.apple.com/documentation/realitykit/anchorentity), [AccessibilityComponent](https://developer.apple.com/documentation/realitykit/accessibilitycomponent), [Foundation Models](https://developer.apple.com/documentation/foundationmodels), and [Adopting Liquid Glass](https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass) |
| SwiftUI Metal, Core Image, and VideoToolbox GPU-media review | [SwiftUI](https://developer.apple.com/documentation/swiftui), [Canvas](https://developer.apple.com/documentation/swiftui/canvas), [GraphicsContext](https://developer.apple.com/documentation/swiftui/graphicscontext), [Shader](https://developer.apple.com/documentation/swiftui/shader), [Graphics and rendering modifiers](https://developer.apple.com/documentation/swiftui/view-graphics-and-rendering), [Core Image](https://developer.apple.com/documentation/coreimage), [CIImage](https://developer.apple.com/documentation/coreimage/ciimage), [CIContext](https://developer.apple.com/documentation/coreimage/cicontext), [CIFilter](https://developer.apple.com/documentation/coreimage/cifilter-swift.class), [Core Video](https://developer.apple.com/documentation/corevideo), [CVPixelBuffer](https://developer.apple.com/documentation/corevideo/cvpixelbuffer), [CVPixelBufferPool](https://developer.apple.com/documentation/corevideo/cvpixelbufferpool), [CVMetalTextureCache](https://developer.apple.com/documentation/corevideo/cvmetaltexturecache), [Metal](https://developer.apple.com/documentation/metal), [MTLDevice](https://developer.apple.com/documentation/metal/mtldevice), [MTLCommandQueue](https://developer.apple.com/documentation/metal/mtlcommandqueue), [MTLCommandBuffer](https://developer.apple.com/documentation/metal/mtlcommandbuffer), [MetalKit](https://developer.apple.com/documentation/metalkit), [MTKView](https://developer.apple.com/documentation/metalkit/mtkview), [VideoToolbox](https://developer.apple.com/documentation/videotoolbox), [Foundation Models](https://developer.apple.com/documentation/foundationmodels), [Adopting Liquid Glass](https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass), [Applying Liquid Glass to custom views](https://developer.apple.com/documentation/swiftui/applying-liquid-glass-to-custom-views), and [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility) |
| GameplayKit | [GameplayKit](https://developer.apple.com/documentation/gameplaykit) |
