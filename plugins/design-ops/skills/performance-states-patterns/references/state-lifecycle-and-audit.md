# State Lifecycle and Audit Checklist

The per-state definitions behind the lifecycle diagram in `SKILL.md`, and the full audit checklist to run on every new feature, view, or component.

## The States

**Empty** is the starting point: the user has arrived but there is no content yet. This could be a brand-new account, a search with no results, or a list that has been cleared. Empty states are opportunities to guide, teach, and motivate.

**Loading** is the state of uncertainty. The system is working, but the user cannot yet see results. The perceived duration of this state is more important than its actual duration — perceived performance is a design problem, not just an engineering one.

**Skeleton** is a specific loading sub-state where placeholder shapes mirror the eventual content layout. Skeleton screens reduce perceived wait time by giving the brain structural information to process, making the transition to real content feel faster and less jarring.

**Partial** is the state where some data has arrived but not all. Streaming server-side rendering, progressive image loading, and paginated lists all produce partial states. The key design challenge is making partial content usable without misleading users about completeness.

**Complete** is the happy path — all data loaded, all interactions available. This is the state most mockups depict, but it represents only one moment in the lifecycle.

**Error** is the state where something went wrong. Network failures, server errors, validation problems, permission issues, rate limits — each error type demands a different response. The goal is always: tell the user what happened, what it means for them, and what they can do next.

**Offline** is the state where network connectivity is lost. Modern applications must handle this gracefully, serving cached content where possible and queuing actions for later synchronization.

## State Design Audit Checklist

When designing any new feature, view, or component, walk through this checklist to ensure every state has been considered. Incomplete state coverage is the single most common source of "unpolished" feelings in production software.

**For every data-dependent view, verify you have designed:**

- **First-use empty state** — What does a new user see before creating any content? Is there an illustration, explanation, and CTA? Does the empty state educate or at least orient?
- **No-results state** — If the user searches or filters and nothing matches, what do they see? Are there suggestions for broadening the search?
- **Loading state** — What does the user see during the data fetch? Is it a skeleton (preferred for content-heavy views) or a spinner (acceptable for brief waits)? Is the loading indicator accessible to screen readers?
- **Partial loaded state** — If data arrives in stages (paginated, streamed), does the partial view look intentional? Can users interact with the content that has arrived?
- **Complete state** — The standard "happy path" design. This is what most mockups show.
- **Error state** — What happens if the data fetch fails? Is there a retry button? Is the error message human-readable? If cached data exists, is it shown with a staleness indicator?
- **Offline state** — If the user loses connectivity, what degrades? What remains functional? Is there a clear indicator that the user is offline?
- **Permission-required state** — If the view depends on a user permission (location, notifications, camera), what does the user see before granting it?

**For every user action, verify you have designed:**

- **Immediate feedback** — Does something visible change within 100ms of the action? This could be a button state change, a spinner, or an optimistic update.
- **Success confirmation** — How does the user know the action succeeded? Is it a toast, an inline change, a redirect?
- **Failure handling** — If the action fails, what does the user see? Is there a retry path? Is their input preserved?
- **Undo mechanism** — For destructive or significant actions, is there a brief undo window?

**For every notification event, verify you have designed:**

- **Channel routing** — Which channel(s) will deliver this notification? Does it change based on user context (in-app vs. away)?
- **Urgency classification** — Is the urgency level appropriate? Would a user agree that this level of interruption is warranted?
- **Preference respect** — Can the user control whether they receive this notification, and through which channel?
- **Accessibility** — Does the notification announce itself to screen readers via the appropriate ARIA live region?

This checklist is not exhaustive, but completing it for every new feature will eliminate the vast majority of state-related UX gaps that erode user trust over time.
