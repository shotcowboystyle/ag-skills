---
name: micro-copy-intelligence
description: "1000+ microcopy and UX-writing templates by component, tone and sector: button labels, every error message and failure state, empty states, tooltips, confirmations, permission requests and notifications. Use when writing any interface string — robotic copy is the loudest slop tell."
allowed-tools: Read, Grep, Glob
---

# Micro-Copy Intelligence

Copy-paste-ready microcopy templates for every UI component and state, with tone variants, character counts, accessibility notes, and i18n notes. This skill owns all interface-string templates in design-ops.

## Core Principle: Clear > Clever

The single most important rule in UX writing: **clarity beats cleverness every time**. Users are not reading your interface for entertainment. They are trying to accomplish a task. Every word should reduce cognitive load, not add to it.

| Principle             | Description                                | Example                                                            |
| --------------------- | ------------------------------------------ | ------------------------------------------------------------------ |
| Clear > Clever        | Plain language over puns or jargon         | "Save changes" not "Commit your brilliance"                        |
| Specific > Generic    | Tell them exactly what happens             | "Delete 3 photos" not "Delete items"                               |
| Human > Robotic       | Write like a helpful person, not a machine | "We couldn't find that page" not "Error 404: Resource not located" |
| Short > Long          | Every extra word is cognitive cost         | "Saved" not "Your changes have been successfully saved"            |
| Active > Passive      | Direct the user with active voice          | "Enter your email" not "Email should be entered"                   |
| Consistent > Creative | Same action = same word everywhere         | Always "Remove" or always "Delete", never both                     |
| Helpful > Blaming     | Guide, don't accuse                        | "That password is too short" not "You entered an invalid password" |

## Tone Adaptation by Context

The same product shifts tone based on what the user is experiencing:

| Context                 | Tone Shift                 | Why                                                    |
| ----------------------- | -------------------------- | ------------------------------------------------------ |
| **Errors**              | Empathetic, calm, helpful  | User is frustrated — don't add to it                   |
| **Success**             | Warm, affirming, brief     | User accomplished something — celebrate proportionally |
| **Empty states**        | Encouraging, instructional | User sees nothing — guide them to value                |
| **Destructive actions** | Cautious, specific, clear  | High stakes — no ambiguity allowed                     |
| **Onboarding**          | Welcoming, motivating      | First impressions — build confidence                   |
| **Loading/waiting**     | Light, reassuring          | User is stuck — ease anxiety                           |
| **Permission requests** | Transparent, benefit-led   | User must trust you — explain why                      |
| **Pricing/payment**     | Trustworthy, precise       | Money is involved — no vagueness                       |
| **Legal/compliance**    | Plain, clear, accessible   | Required info — make it readable                       |

## The Microcopy Formula

For any UI element, apply this structure:

```
[Action Verb] + [Object] + [Benefit/Context]
```

**Examples:**

- "Save changes" = action + object
- "Upload photo to complete your profile" = action + object + benefit
- "Delete this project permanently" = action + object + context
- "Invite teammates to collaborate" = action + object + benefit

**When to add benefit/context:**

- The action is unfamiliar (onboarding)
- The action is irreversible (destructive)
- The action requires trust (permissions, payments)
- The action has a non-obvious outcome

## Routing

| Question | Read |
| --- | --- |
| Button, link or CTA label; choosing the verb (action verb matrix, pairing, char counts) | `references/button-label-templates.md` |
| Something went wrong, or succeeded (validation, system, permission, business-logic errors; success copy; celebration proportionality) | `references/error-success-messages.md` |
| Nothing to show (first use, no results, cleared, error, no access) | `references/empty-state-copy.md` |
| First launch, setup, feature tours, value proposition, permission priming and denial recovery | `references/onboarding-permission-copy.md` |
| Push, in-app, toast, tooltip, helper text, confirmation dialogs, loading copy, changelog, placeholders, banners | `references/notification-tooltip-copy.md` |
| How to write a given component (structure rules for buttons, errors, empty states, confirmation severity tiers, placeholders, tooltips, onboarding, notification channel limits, success, loading by wait length) | `references/component-copy-guidelines.md` |
| Voice and tone calibration, sector tone guides, readability targets by component, inclusive language, i18n expansion, top-25 anti-patterns, step-by-step writing process | `references/voice-tone-style.md` |

For a full screen, combine templates from several files, then filter them through the sector tone guide in `voice-tone-style.md`. For a copy audit, check against the principles below, the quality checklist, and the anti-pattern encyclopedia.

## Quality Checklist for Any Microcopy

Before shipping any piece of UI text, verify:

- [ ] Is it clear on first read? (No re-reading needed)
- [ ] Is it specific? (User knows exactly what will happen)
- [ ] Is it actionable? (User knows what to do next)
- [ ] Is it consistent? (Same terms used across the product)
- [ ] Is it concise? (No unnecessary words)
- [ ] Is it inclusive? (No gendered, ableist, or culturally specific language)
- [ ] Is it translatable? (No idioms, puns, concatenated strings)
- [ ] Is it accessible? (Works with screen readers, announced properly)
- [ ] Does it match the product voice? (Tone is appropriate for context)
- [ ] Is it tested? (Real users understood it without explanation)

## Accessibility Requirements for Microcopy

- **ARIA live regions:** Error messages and success confirmations must be announced to screen readers via `aria-live="polite"` (success) or `aria-live="assertive"` (errors).
- **Error association:** Every error message must be programmatically associated with its input via `aria-describedby`.
- **Button labels:** If a button uses only an icon, provide `aria-label` with the full text label.
- **Tooltip accessibility:** Tooltips must be reachable via keyboard (focus, not just hover) and announced by screen readers.
- **Loading announcements:** Announce loading start and completion to screen readers.
- **Confirmation dialogs:** Focus must move to the dialog when it opens and return to the trigger when it closes.
- **Status messages:** Use `role="status"` for non-critical updates and `role="alert"` for urgent messages.
- **No time pressure:** If a toast auto-dismisses, the information must be available elsewhere (notification center, status area).
