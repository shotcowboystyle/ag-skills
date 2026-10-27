---
name: screen-reader-testing
description: Test web applications with screen readers including VoiceOver, NVDA, and JAWS. Use when validating screen reader compatibility, debugging accessibility issues, or ensuring assistive technology support.
last_verified: 2026-10-27
---

# Screen Reader Testing

Practical guide to testing web applications with screen readers for comprehensive accessibility validation.

## When to Use This Skill

- Validating screen reader compatibility
- Testing ARIA implementations
- Debugging assistive technology issues
- Verifying form accessibility
- Testing dynamic content announcements
- Ensuring navigation accessibility

## Core Concepts

### 1. Major Screen Readers

| Screen Reader | Platform  | Browser        | Usage |
| ------------- | --------- | -------------- | ----- |
| **VoiceOver** | macOS/iOS | Safari         | ~15%  |
| **NVDA**      | Windows   | Firefox/Chrome | ~31%  |
| **JAWS**      | Windows   | Chrome/IE      | ~40%  |
| **TalkBack**  | Android   | Chrome         | ~10%  |
| **Narrator**  | Windows   | Edge           | ~4%   |

### 2. Testing Priority

```
Minimum Coverage:
1. NVDA + Firefox (Windows)
2. VoiceOver + Safari (macOS)
3. VoiceOver + Safari (iOS)

Comprehensive Coverage:
+ JAWS + Chrome (Windows)
+ TalkBack + Chrome (Android)
+ Narrator + Edge (Windows)
```

### 3. Screen Reader Modes

| Mode               | Purpose                | When Used         |
| ------------------ | ---------------------- | ----------------- |
| **Browse/Virtual** | Read content           | Default reading   |
| **Focus/Forms**    | Interact with controls | Filling forms     |
| **Application**    | Custom widgets         | ARIA applications |

Before testing on macOS, read [VoiceOver setup, commands, and checklists](references/voiceover.md).

For the required iOS Safari coverage, read [VoiceOver touch setup and gestures](references/voiceover-ios.md).

Before testing with NVDA, read [NVDA setup, modes, commands, and test scripts](references/nvda.md).

Before testing with JAWS or TalkBack, read [platform setup and commands](references/jaws-talkback.md).

## Common Test Scenarios

### 1. Modal Dialog

Prefer native `<dialog>` opened with `showModal()`: the browser makes the rest of the page inert, traps focus, closes on Escape, and exposes `role="dialog"` with `aria-modal` semantics.

```html
<dialog id="confirm-delete" aria-labelledby="dialog-title" aria-describedby="dialog-desc">
  <h2 id="dialog-title" tabindex="-1">Confirm Delete</h2>
  <p id="dialog-desc">This action cannot be undone.</p>
  <button type="button" data-close>Cancel</button>
  <button type="button">Delete</button>
</dialog>
```

```javascript
// Focus management: the heading needs tabindex="-1" to receive programmatic focus
const dialog = document.getElementById("confirm-delete");
let lastFocus = null;

function openDialog() {
  lastFocus = document.activeElement;
  dialog.showModal(); // inert background + focus containment + Escape to close
  dialog.querySelector("#dialog-title").focus();
}

dialog.addEventListener("close", () => {
  lastFocus?.focus(); // fires for Escape and dialog.close() alike
});

dialog.querySelector("[data-close]").addEventListener("click", () => dialog.close());
```

Test: on open, the screen reader announces the dialog name, role and description; Tab never reaches page content behind it; on close, focus lands back on the trigger.

### 2. Live Regions

```html
<!-- Status messages (polite) -->
<div role="status" aria-live="polite" aria-atomic="true">
  <!-- Content updates will be announced after current speech -->
</div>

<!-- Alerts (assertive) -->
<div role="alert" aria-live="assertive">
  <!-- Content updates interrupt current speech -->
</div>

<!-- Progress updates -->
<div
  role="progressbar"
  aria-valuenow="75"
  aria-valuemin="0"
  aria-valuemax="100"
  aria-label="Upload progress"
></div>

<!-- Log (additions only) -->
<div role="log" aria-live="polite" aria-relevant="additions">
  <!-- New messages announced, removals not -->
</div>
```

### 3. Tab Interface

```html
<div role="tablist" aria-label="Product information">
  <button role="tab" id="tab-1" aria-selected="true" aria-controls="panel-1">
    Description
  </button>
  <button
    role="tab"
    id="tab-2"
    aria-selected="false"
    aria-controls="panel-2"
    tabindex="-1"
  >
    Reviews
  </button>
</div>

<div role="tabpanel" id="panel-1" aria-labelledby="tab-1">
  Product description content...
</div>

<div role="tabpanel" id="panel-2" aria-labelledby="tab-2" hidden>
  Reviews content...
</div>
```

```javascript
// Tab keyboard navigation
tablist.addEventListener("keydown", (e) => {
  const tabs = [...tablist.querySelectorAll('[role="tab"]')];
  const index = tabs.indexOf(document.activeElement);

  let newIndex;
  switch (e.key) {
    case "ArrowRight":
      newIndex = (index + 1) % tabs.length;
      break;
    case "ArrowLeft":
      newIndex = (index - 1 + tabs.length) % tabs.length;
      break;
    case "Home":
      newIndex = 0;
      break;
    case "End":
      newIndex = tabs.length - 1;
      break;
    default:
      return;
  }

  tabs[newIndex].focus();
  activateTab(tabs[newIndex]);
  e.preventDefault();
});
```

## Debugging Tips

Read the browser's computed accessible name and role rather than re-deriving them: the Accessibility pane in Chrome/Edge/Firefox DevTools shows the computed name, role, states and the source of each. In tests, assert on the accessibility tree:

```javascript
// Playwright: query by role + accessible name, and snapshot the tree
await expect(page.getByRole("button", { name: "Delete" })).toBeVisible();
await expect(page.getByRole("dialog")).toMatchAriaSnapshot(`
  - dialog "Confirm Delete":
    - heading "Confirm Delete" [level=2]
    - button "Cancel"
    - button "Delete"
`);
```

For a quick DevTools-console check, resolve `aria-labelledby` IDs to their text (it holds ID references, not the name). This approximates only the first steps of the [accessible name algorithm](https://www.w3.org/TR/accname-1.2/), so trust the Accessibility pane when they disagree:

```javascript
function approxAccessibleName(el) {
  const ids = el.getAttribute("aria-labelledby");
  if (ids) {
    return ids
      .split(/\s+/)
      .map((id) => document.getElementById(id)?.textContent.trim() ?? "")
      .join(" ");
  }
  return (
    el.getAttribute("aria-label") ||
    (el.labels?.length ? [...el.labels].map((l) => l.textContent.trim()).join(" ") : "") ||
    el.getAttribute("alt") ||
    el.textContent.trim()
  );
}
```

## Best Practices

### Do's

- **Test with actual screen readers** - Not just simulators
- **Use semantic HTML first** - ARIA is supplemental
- **Test in browse and focus modes** - Different experiences
- **Verify focus management** - Especially for SPAs
- **Test keyboard only first** - Foundation for SR testing

### Don'ts

- **Don't assume one SR is enough** - Test multiple
- **Don't ignore mobile** - Growing user base
- **Don't test only happy path** - Test error states
- **Don't skip dynamic content** - Most common issues
- **Don't rely on visual testing** - Different experience
