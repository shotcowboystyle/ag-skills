---
name: meta-wearables-web-apps
description: Build and review Meta Wearables Web Apps for the Ray-Ban Display with the official HTML/CSS/JavaScript route, 600×600 display contract, public HTTPS delivery, focus and D-pad/EMG input, performance limits, source-conflict handling, and separate simulator/physical-device evidence. Use when building or reviewing a Ray-Ban Display Web App, or deciding between a Web App and native DAT Display.
last_verified: 2026-08-22
allowed-tools: Bash(uv run *), Bash(node *), Read, Grep, Glob
---

# Meta Wearables Web Apps

Use the official Web App surface when the experience should reach the Meta Ray-Ban Display as a web page. Keep it separate from a native iOS/Android DAT companion app and from native DAT Display code.

Apply the [shared rules](../meta-wearables-knowledge-base/references/shared-rules.md) — evidence ladder, device labels, secrets, claims.

## Read before acting

- Inspect the actual Web App source, build toolchain, URL/deployment target, assets, state model, and any companion phone integration.
- Read the local [display and input contract](references/display-contract.md) — it holds the source conflict, layout/input/delivery rules, and the reading list of knowledge-base routes for input, compliance, security, operations, and architecture.
- Load the Web Apps `api_surface.rows` from the [source-pinned manifest](../meta-wearables-sdk-audit/references/surface-manifest.yaml) and keep each runtime/source-conflict row separate.
- Read the [toolkit skill map](references/toolkit-skill-map.md) for scaffolding, text entry, gestures, sensors, offline, API connection, staging, or publishing.
- Read the official [Web App repository](https://github.com/facebook/meta-wearables-webapp), its [agent guidance](https://github.com/facebook/meta-wearables-webapp/blob/main/AGENTS.md), [Display guidelines](https://github.com/facebook/meta-wearables-webapp/blob/main/plugins/meta-wearables-webapp/references/display-guidelines.md), [performance guidelines](https://github.com/facebook/meta-wearables-webapp/blob/main/plugins/meta-wearables-webapp/references/performance-guidelines.md), and the current [Web Apps documentation](https://wearables.developer.meta.com/docs/develop/webapps).

## Scripts

`$SKILL` below is this skill's directory — the folder holding this SKILL.md. Find it by name in your tool's skills folder (some tools prefix it, e.g. `meta-wearables-ops__meta-wearables-web-apps`).

Preflight the real entrypoint before calling a local HTML/JS surface a Meta delivery target:

```bash
uv run $SKILL/scripts/run_webapp_preflight.py <web-app-root> --require-meta-markers \
  --origin <https-url> --check-origin --require-https-origin
```

Drop the `--origin` flags when no public URL exists yet. The receipt keeps hosted HTTPS evidence separate from browser-simulator and physical Display evidence.

For a new reducer-first scaffold, copy the [dependency-free Web App starter](../meta-wearables-implementation-recipes/assets/meta-wearables-web-starter) and run its `node --test test/display-state.test.mjs` before binding the selected toolkit revision.

## Workflow

1. Define the glanceable outcome and whether the Web App is standalone or paired with a phone service.
2. Build the smallest HTML/CSS/JS surface inside the 600×600 contract: additive content, short text, clear hierarchy, no phone-viewport assumptions. Gate source-conflicted features behind explicit capability/fallback decisions.
3. Implement focus and input deliberately: visible focus, deterministic D-pad/EMG action mapping, clear selection, dismiss, and recovery.
4. Use the current metadata/launch contract and a public HTTPS URL. Never ship a localhost URL, private tunnel, secret-bearing URL, or native DAT import in a Web App.
5. Design loading, stale, offline, consent handoff, invalid input, and service-failure states. Keep data minimal.
6. Follow the official performance budget; measure load and interaction latency on the target surface.
7. Test in the official [browser simulator](https://chromewebstore.google.com/detail/meta-ray-ban-display-web/jpjlmmodokemlepklkdbimceggpbjcll), then the deployed URL, then the same script on physical Ray-Ban Display hardware. Stop at the first unavailable gate and record each result separately.

## Source conflict

The full Developer Center index (reviewed 2026-08-22) lists no camera, microphone, text input, offline support, notifications, or back navigation. The toolkit `main` at `a2714f862c61b1ce9c6cb624fc7e4938087102db` documents a handwriting/voice composer, service-worker offline, Escape/back, gestures, and sensors. Carry each of those as `source-conflict`/`to-verify` with a phone/manual fallback until runtime and current docs agree. Record details per the [display contract](references/display-contract.md#source-conflict).

## Required output

1. Route decision: Web App versus native DAT Display.
2. Public URL, launch metadata, and the preflight receipt.
3. Display/input state map and performance budget.
4. Source-conflict rows with fallback and release decision.
5. Simulator test cases and results.
6. Physical Ray-Ban Display test script with evidence status per the ladder.
7. Phone handoff, privacy, and failure behavior.

## Hard boundaries

- A browser simulator proves web behavior and some input logic, not glasses rendering, brightness, latency, comfort, or hardware input.
- Never represent a Web App as a native DAT integration in store copy or source documentation.
- Never assume arbitrary browser APIs, background execution, camera/microphone, notifications, or Meta AI voice commands on the Display.
- Never put secrets or raw personal media in a public URL or client bundle.

## Related skills

- [Route planner](../meta-wearables-route-planner/SKILL.md) — route choice and app architecture
- [Device capabilities](../meta-wearables-device-capabilities/SKILL.md) — native DAT Display, input, and sensors
- [Device proof](../meta-wearables-device-proof/SKILL.md) — physical evidence plans
- [Trust and release](../meta-wearables-trust-and-release/SKILL.md) — privacy, compliance, publishing
- [Diagnostics](../meta-wearables-diagnostics/SKILL.md) — operational readiness and recovery
