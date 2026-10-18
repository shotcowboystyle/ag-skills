# iOS Commerce, Identity, and Security — details

## Framework boundaries

### StoreKit and PassKit

- StoreKit product metadata is not entitlement. Unlock digital content only from verified transaction/current-entitlement state, deliver the product before finishing the transaction, and handle updates while the app runs. Keep consumable, non-consumable, subscription, pending/Ask to Buy, refund/revocation, expiry/grace, restore, and account-change semantics explicit.
- StoreKit Testing and a local configuration are deterministic route fixtures. They do not prove App Store Connect metadata, sandbox/TestFlight account state, regional storefronts, server reconciliation, production pricing, or App Review configuration.
- Apple Pay authorizes a payment request and supplies a provider-bound token; a presented sheet or token is not provider capture, fulfillment, refund, or order success. Model provider/server processing separately and do not use Apple Pay for digital in-app content when StoreKit is the appropriate route.
- Wallet passes are signed artifacts with pass type IDs, add/update/revoke lifecycle, supported device/role rules, and privacy constraints. “Pass added” is not identity verification, payment authorization, or proof that the provider’s state is current.

### Sign in with Apple and account state

- Generate and validate nonce/state for the request, request only the scopes needed, preserve the stable Apple user identifier securely, and expect name/email availability to differ between first and subsequent authorization. Support private relay email, account linking, sign-out, credential revocation, deletion, and a returning-user path.
- Native authorization proves a system credential result for that flow. It does not grant access to app business data until the server verifies and authorizes the account. Keep Apple credential verification, session/token issuance, account ownership, organization membership, and product entitlement separate.
- Do not make Sign in with Apple mandatory for a local utility unless identity is part of the user outcome. A user identifier is not permission to access another account’s records.

### Keychain, LocalAuthentication, and CryptoKit

- Store small credentials, refresh tokens, private-key references, and stable local identifiers in Keychain. Choose item class, accessibility, synchronizability, access group, and `SecAccessControl` from the threat model; document what happens across lock, migration, backup/restore, reinstall, passcode changes, and key loss.
- LocalAuthentication evaluates a device-user policy or protected access-control operation. Success proves that policy evaluation succeeded at that moment; it is not server identity, account ownership, payment entitlement, or permission for an unrelated business action. Handle cancellation, lockout, no passcode, unavailable biometrics, enrollment changes, and fallback.
- Use CryptoKit’s established primitives and a documented protocol. Define key generation/storage/rotation, nonce/IV, associated data, algorithm/version, recovery, deletion, and server verification. Do not invent encryption, password hashing, token signing, or certificate-validation schemes.

### DeviceCheck, App Attest, and networking

- DeviceCheck and App Attest are server-managed abuse/integrity signals. Use one-time server challenges, bind assertions to request data, validate attestation/assertions server-side, prevent replay, handle unsupported/key-loss states, and feed results into a broader risk/authorization policy.
- Neither DeviceCheck nor App Attest is absolute device security, user identity, payment proof, or a replacement for server authorization. The app cannot authoritatively verify its own integrity.
- Centralize URLSession/Network request construction, TLS/ATS configuration, authentication, timeouts, cancellation, retries, idempotency, cache/offline policy, response validation, and redacted diagnostics. A client-side check or successful TLS connection is not server authorization.
- Never place secrets or personal data in query strings unless the protocol and privacy review explicitly require it. Validate response schema, expiry, signatures, and account scope before committing a server decision.


## Related routes and recipes

- [Commerce, identity, and security routes](../../ios-knowledge-base/references/40-framework-routes/05-commerce-identity-and-security.md)
- [StoreKit and entitlements](../../ios-knowledge-base/references/41-framework-deep-dives/02-storekit-and-entitlements.md)
- [Networking, security, and identity](../../ios-knowledge-base/references/42-framework-deep-dives/03-networking-security-and-identity.md)
- [Commerce, identity, and security recipes](../../ios-knowledge-base/references/70-code-recipes/17-commerce-identity-and-security-recipes.md)
- [Data and device services package](../../ios-data-and-device-services/SKILL.md)
- [Permission, entitlement, and privacy checklist](../../ios-knowledge-base/references/60-verification/04-permission-entitlement-and-privacy-checklist.md)
- [Build, device, and release checklist](../../ios-knowledge-base/references/60-verification/01-build-device-and-release-checklist.md)


## Sources

- [StoreKit](https://developer.apple.com/documentation/storekit)
- [In-App Purchase](https://developer.apple.com/documentation/storekit/in-app-purchase)
- [Product](https://developer.apple.com/documentation/storekit/product)
- [Transaction](https://developer.apple.com/documentation/storekit/transaction)
- [currentEntitlements](https://developer.apple.com/documentation/storekit/transaction/currententitlements)
- [PassKit](https://developer.apple.com/documentation/passkit)
- [Offering Apple Pay in your app](https://developer.apple.com/documentation/passkit/offering-apple-pay-in-your-app)
- [PKPaymentAuthorizationController](https://developer.apple.com/documentation/passkit/pkpaymentauthorizationcontroller)
- [Wallet](https://developer.apple.com/documentation/passkit/wallet)
- [PKAddPassesViewController](https://developer.apple.com/documentation/passkit/pkaddpassesviewcontroller)
- [Authentication Services](https://developer.apple.com/documentation/authenticationservices)
- [Implementing user authentication with Sign in with Apple](https://developer.apple.com/documentation/authenticationservices/implementing-user-authentication-with-sign-in-with-apple)
- [ASAuthorizationAppleIDProvider](https://developer.apple.com/documentation/authenticationservices/asauthorizationappleidprovider)
- [Security](https://developer.apple.com/documentation/security)
- [Keychain Services](https://developer.apple.com/documentation/security/keychain-services)
- [Using the keychain to manage user secrets](https://developer.apple.com/documentation/security/using-the-keychain-to-manage-user-secrets)
- [Restricting keychain item accessibility](https://developer.apple.com/documentation/security/restricting-keychain-item-accessibility)
- [Local Authentication](https://developer.apple.com/documentation/localauthentication)
- [LAContext](https://developer.apple.com/documentation/localauthentication/lacontext)
- [CryptoKit](https://developer.apple.com/documentation/cryptokit)
- [DeviceCheck](https://developer.apple.com/documentation/devicecheck)
- [DCDevice](https://developer.apple.com/documentation/devicecheck/dcdevice)
- [DCAppAttestService](https://developer.apple.com/documentation/devicecheck/dcappattestservice)
- [Establishing your app’s integrity](https://developer.apple.com/documentation/devicecheck/establishing-your-app-s-integrity)
- [Validating apps that connect to your server](https://developer.apple.com/documentation/devicecheck/validating-apps-that-connect-to-your-server)
- [URL Loading System](https://developer.apple.com/documentation/foundation/url_loading_system)
- [Network](https://developer.apple.com/documentation/network)
