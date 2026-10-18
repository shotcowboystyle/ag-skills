# iOS Data and Device Services — details

## Accessories, proximity, and local network

- HomeKit uses a shared Home database. Observe `HMHomeManager` state, distinguish read from physical write, confirm actions that unlock/open/heat/alarm/monitor, and label last-known values. A callback or discovered accessory does not prove a safe or permanent physical effect.
- Core Bluetooth central and peripheral roles have different radio/protocol/background boundaries. Wait for `CBCentralManager`/`CBPeripheralManager` state, scan only for supported service UUIDs, validate GATT services/characteristics and versioned payloads, stop scans, time out operations, and avoid unbounded reconnect loops.
- Nearby Interaction needs a session-specific peer/accessory configuration, discovery-token exchange, usage description, supported hardware, and session lifecycle. Distance/direction is relative framework output, not identity, location, trust, or safety proof. Use an authenticated/out-of-band exchange and a separate transport.
- Network/Bonjour discovery is not authentication. Request local-network access with the target declarations, model `NWBrowser`/`NWConnection` ready/waiting/failed/cancelled states, authenticate the peer, secure sensitive traffic, handle network changes, and retain a manual pairing route where useful.
- Keep framework availability, discovered candidate, product trust, user selection, protocol compatibility, connection, and operation result distinct. Discovery never silently authorizes a physical side effect.


## Non-negotiable safety and evidence rules

- Never present a local record, sync result, HealthKit value, contact/event, weather observation, accessory discovery, Bluetooth identifier, Nearby result, Bonjour name, or endpoint as current truth, identity, trust, medical validation, safety, or delivery proof without the separate evidence required by that domain.
- Never request a broad permission, protected data class, cloud account, accessory radio, local-network access, or telemetry path because it may be useful later. Tie every capability, entitlement, usage description, and retention rule to the stated feature.
- Treat external records, sync payloads, accessory messages, discovery results, weather responses, and local-network services as untrusted/stale. Validate IDs, dates, units, ranges, versions, signatures/authentication, payload sizes, and action targets before persistence or side effects.
- Never claim background delivery, sync timing, radio continuity, UWB support, accessory compatibility, weather freshness, or physical-world safety from a simulator, mock, fixture, preview, or one device.
- Preserve a useful local/manual path when permission, account, network, sensor, accessory, or service availability is missing. A fallback must not silently weaken security, privacy, paid access, or physical safety.


## Deliverable

Produce a compact route note or implementation change containing:

- selected framework/storage/service and rejected alternatives;
- target/device, model/schema, account, permission, usage-description, capability, entitlement, accessory/protocol, network, privacy, and retention matrix;
- authorization/discovery/trust/operation/sync state machine with conflict, stale, cancellation, retry, manual fallback, and deletion behavior;
- source/date/unit/provenance and user-review policy for imported, synced, protected, or generated values;
- exact compile, fixture, signed physical-device, multi-device/service/accessory, privacy, performance, signing, and release evidence plan;
- remaining `to-verify` gaps and claims deliberately not made.

For implementation, change only the requested target and directly related adapters/configuration. Do not add CloudKit, an account, a server, protected-data access, a radio permission, local-network access, background delivery, physical writes, analytics, or telemetry without a stated user-facing need and authorization.


## Related routes and recipes

- [Data, persistence, and sync](../../ios-knowledge-base/references/40-framework-routes/01-data-persistence-and-sync.md)
- [Location, maps, and places](../../ios-knowledge-base/references/40-framework-routes/03-location-maps-and-places.md)
- [SwiftData and local persistence](../../ios-knowledge-base/references/41-framework-deep-dives/00-swiftdata-and-local-persistence.md)
- [CloudKit and sync](../../ios-knowledge-base/references/41-framework-deep-dives/01-cloudkit-and-sync.md)
- [HealthKit and sensitive data](../../ios-knowledge-base/references/42-framework-deep-dives/01-healthkit-and-sensitive-data.md)
- [HomeKit, Bluetooth, and Nearby](../../ios-knowledge-base/references/42-framework-deep-dives/02-homekit-bluetooth-and-nearby.md)
- [Contacts, calendar, and notifications](../../ios-knowledge-base/references/43-system-framework-deep-dives/01-contacts-calendar-and-notifications.md)
- [WeatherKit and system data](../../ios-knowledge-base/references/43-system-framework-deep-dives/03-weatherkit-and-system-data.md)
- [Persistence, local-first, and sync recipes](../../ios-knowledge-base/references/70-code-recipes/11-persistence-local-first-and-sync-recipes.md)
- [Health, personal-data, and notification recipes](../../ios-knowledge-base/references/70-code-recipes/16-health-personal-data-and-notification-recipes.md)
- [HomeKit, Bluetooth, Nearby, and local-network recipes](../../ios-knowledge-base/references/70-code-recipes/15-homekit-bluetooth-and-nearby-recipes.md)
- [Permission, entitlement, and privacy checklist](../../ios-knowledge-base/references/60-verification/04-permission-entitlement-and-privacy-checklist.md)
- [Build, device, and release checklist](../../ios-knowledge-base/references/60-verification/01-build-device-and-release-checklist.md)


## Sources

- [SwiftData](https://developer.apple.com/documentation/swiftdata/)
- [ModelContainer](https://developer.apple.com/documentation/swiftdata/modelcontainer)
- [ModelContext](https://developer.apple.com/documentation/swiftdata/modelcontext)
- [VersionedSchema](https://developer.apple.com/documentation/swiftdata/versionedschema)
- [SchemaMigrationPlan](https://developer.apple.com/documentation/swiftdata/schemamigrationplan)
- [ModelActor](https://developer.apple.com/documentation/swiftdata/modelactor)
- [Syncing model data across a person’s devices](https://developer.apple.com/documentation/swiftdata/syncing-model-data-across-a-persons-devices)
- [CloudKit](https://developer.apple.com/documentation/cloudkit)
- [Deciding whether CloudKit is right for your app](https://developer.apple.com/documentation/cloudkit/deciding-whether-cloudkit-is-right-for-your-app)
- [CKContainer](https://developer.apple.com/documentation/cloudkit/ckcontainer)
- [CKSyncEngine](https://developer.apple.com/documentation/cloudkit/cksyncengine)
- [HealthKit](https://developer.apple.com/documentation/healthkit)
- [HKHealthStore](https://developer.apple.com/documentation/healthkit/hkhealthstore)
- [Authorizing access to health data](https://developer.apple.com/documentation/healthkit/authorizing-access-to-health-data)
- [Reading data from HealthKit](https://developer.apple.com/documentation/healthkit/reading-data-from-healthkit)
- [Executing observer queries](https://developer.apple.com/documentation/healthkit/executing-observer-queries)
- [Protecting user privacy](https://developer.apple.com/documentation/healthkit/protecting-user-privacy)
- [Contacts](https://developer.apple.com/documentation/contacts)
- [CNContactStore](https://developer.apple.com/documentation/contacts/cncontactstore)
- [ContactsUI](https://developer.apple.com/documentation/contactsui)
- [EventKit](https://developer.apple.com/documentation/eventkit)
- [Accessing the event store](https://developer.apple.com/documentation/eventkit/accessing-the-event-store)
- [EKEventStore](https://developer.apple.com/documentation/eventkit/ekeventstore)
- [WeatherKit](https://developer.apple.com/documentation/weatherkit)
- [WeatherService](https://developer.apple.com/documentation/weatherkit/weatherservice)
- [WeatherAttribution](https://developer.apple.com/documentation/weatherkit/weatherattribution)
- [HomeKit](https://developer.apple.com/documentation/homekit)
- [HMHomeManager](https://developer.apple.com/documentation/homekit/hmhomemanager)
- [Enabling HomeKit in your app](https://developer.apple.com/documentation/homekit/enabling-homekit-in-your-app)
- [Core Bluetooth](https://developer.apple.com/documentation/corebluetooth)
- [CBCentralManager](https://developer.apple.com/documentation/corebluetooth/cbcentralmanager)
- [CBPeripheral](https://developer.apple.com/documentation/corebluetooth/cbperipheral)
- [Nearby Interaction](https://developer.apple.com/documentation/nearbyinteraction)
- [Initiating and maintaining a session](https://developer.apple.com/documentation/nearbyinteraction/initiating-and-maintaining-a-session)
- [NISession](https://developer.apple.com/documentation/nearbyinteraction/nisession)
- [NINearbyPeerConfiguration](https://developer.apple.com/documentation/nearbyinteraction/ninearbypeerconfiguration)
- [Network](https://developer.apple.com/documentation/network)
- [NWBrowser](https://developer.apple.com/documentation/network/nwbrowser)
- [NWConnection](https://developer.apple.com/documentation/network/nwconnection)
- [Understanding local network privacy](https://developer.apple.com/documentation/technotes/tn3179-understanding-local-network-privacy)
