---
name: performance-states-patterns
description: "Perceived performance and state design: skeleton screens, optimistic UI, progressive loading, notification architecture (toast, banner, badge, push), and empty, error, offline, and onboarding states. Use when a UI feels slow, or when specifying what a screen shows before, during, and after data arrives."
allowed-tools: Read, Grep, Glob
---

# Performance, States & Patterns

Loading, emptiness, failure, first contact, and disconnection occupy more of a user's time than the happy path. Specify every one of them.

## The State Lifecycle

```
EMPTY -> LOADING -> SKELETON -> PARTIAL -> COMPLETE -> ERROR -> OFFLINE
  |         |          |           |          |          |         |
  v         v          v           v          v          v         v
First-use  Spinner   Shimmer    Streaming   Ideal     Recovery  Cached
guidance   or bar    placeholders  data      render    + retry   fallback
```

- **Empty** — guide, teach, motivate (new account, no search results, cleared list).
- **Loading / Skeleton** — perceived duration matters more than actual; skeletons mirror the final layout.
- **Partial** — make arrived content usable without implying it is complete.
- **Error** — say what happened, what it means for the user, and what they can do next.
- **Offline** — serve cached content, queue writes, sync later.

Per-state definitions and the full audit checklist: `references/state-lifecycle-and-audit.md`.

## Perceived Performance

Users experience feelings about speed, not milliseconds. A 3-second load with skeletons and progressive rendering beats a 2-second blank screen followed by a content dump. Three pillars:

1. **Immediate feedback** — acknowledge every action within 100ms
2. **Visual continuity** — keep spatial relationships stable during transitions
3. **Progressive disclosure of content** — show something useful early, then enhance

## Notification Channels

| Channel | Persistence | Urgency | Context |
|---|---|---|---|
| Toast | Ephemeral (3-8s) | Low to medium | In-app, immediate |
| Banner/Alert | Until dismissed | Medium to high | In-app, contextual |
| Badge | Until addressed | Low (ambient) | In-app, persistent |
| Push | Until opened | Medium to high | OS-level, external |
| Notification Center | Permanent list | Varies | In-app, on-demand |
| Email/SMS | Permanent | Varies | External, asynchronous |

Route one event to the right channel by urgency, preferences, and context (toast if the app is open, push if not, email after hours away). If everything is critical, nothing is — avoid the "crying wolf" anti-pattern.

## Onboarding

Least to most intrusive: progressive disclosure, contextual hints, checklist (with endowed progress), interactive sandbox, guided tour (skippable, under 5 steps), video walkthrough (under 90 seconds, optional). Match the pattern to product complexity and user familiarity. The first-use empty state is the first onboarding moment: answer "What is this?" and "What do I do first?"

## Guiding Principles

1. **Every state is a design opportunity.** Empty states guide, loading reassures, errors teach, offline demonstrates reliability.
2. **Perceived speed trumps actual speed.** Invest in skeletons, optimistic updates, progressive loading.
3. **Notifications are a finite resource.** Earn the right to interrupt.
4. **Error messages are a conversation.** Plain language; never raw codes or stack traces.
5. **Onboarding should be invisible when possible.** Serve the user's first goal, not a feature tour.
6. **Offline is a state, not an error.** Cache aggressively, queue writes, synchronize gracefully.

## Minimum Coverage

For every data-dependent view: first-use empty, no-results, loading, partial, complete, error (with retry and staleness indicator), offline, permission-required. For every user action: feedback within 100ms, success confirmation, failure handling that preserves input, undo for destructive actions. For every notification: channel routing, urgency classification, user preference control, ARIA live-region announcement.

## Routing

| Question | Read |
|---|---|
| Skeletons, optimistic UI, progressive loading, progress indicators, performance budgets, offline-first, pre-fetching, psychology of waiting, layout shift | `references/perceived-performance-patterns.md` |
| Toast, banner, push, notification center, preferences, routing architecture, toast CSS, notification copy and accessibility | `references/notification-system-design.md` |
| Empty and error state patterns, error recovery, React error boundary, onboarding patterns and metrics, the onboarding spectrum | `references/empty-error-onboarding-states.md` |
| Per-state definitions, the full state design audit checklist | `references/state-lifecycle-and-audit.md` |

## Cross-References

- Loading buttons, form validation, modal errors: `component-patterns-code`
- Shimmer, toast, and progress motion timing: `interaction-motion-design`
- Pull-to-refresh, cellular offline, OS notification rules: `mobile-ux-design`
- Live regions, focus after errors, skeletons and assistive tech: `accessibility-inclusive-design`
- Time perception, interruption science, goal-gradient, loss aversion: `cognitive-psychology-ux`
- Error and empty-state copy: `micro-copy-intelligence`
