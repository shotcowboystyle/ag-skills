# Component Copy Guidelines

> Writing guidance per component type: what each piece of copy must do and how to structure it. Pair with the template files for ready-made strings.

### Button Labels

Write button labels as specific action verbs that tell the user exactly what will happen.

**Primary actions.** "Save changes," "Send message," "Create account," "Place order," "Publish post," "Start trial," "Download report," "Submit request."

**Confirmation actions.** "Confirm deletion," "Yes, cancel subscription," "Approve and send."

**Navigation actions.** "Continue to payment," "Back to dashboard," "View details," "Show more."

**Negative actions.** "Cancel" (abort the current action), "Discard changes," "Remove item," "Delete permanently."

**Avoid generic labels.** Never use "Submit," "OK," "Yes," "No," or "Click here" as standalone button labels. Each button should answer the question: "What will happen when I press this?"

**Button label length.** Aim for two to four words. One word is acceptable for universally understood actions ("Save," "Send," "Delete"). Five or more words indicate the button is trying to do too much — simplify the action or move context to surrounding copy.

### Error Messages

Structure every error message with three components: (1) what happened, (2) why it happened, and (3) what to do next.

**Validation errors.** "Enter a valid email address (example: name@domain.com)." "Password must be at least 8 characters with one number and one letter." "Phone number must include a country code."

**Permission errors.** "You don't have access to this file. Contact the workspace owner to request access." "This action requires admin permissions. Ask your team admin to help."

**Server errors.** "Something went wrong on our end. Try again in a few minutes. If this keeps happening, contact support." Never display raw error codes, stack traces, or technical identifiers to end users.

**Network errors.** "Check your internet connection and try again." "We couldn't reach the server. This usually means a network issue — try reconnecting."

**Not found errors.** "This page doesn't exist. It may have been moved or deleted. Go to the homepage to find what you're looking for." Provide a search field or navigation links on 404 pages.

**Error message tone.** Never blame the user. Replace "You entered an invalid email" with "That doesn't look like an email address." Use "we" to take responsibility for system failures: "We couldn't save your changes" not "Save failed."

### Empty States

Write empty state messages that orient the user and provide a clear next action.

**First use.** "No projects yet. Create your first project to get started." Include a primary action button directly in the empty state.

**No results (search).** "No results for 'quarterly report.' Try different keywords or check for typos." Offer suggestions: "Did you mean 'quarterly review'?"

**No data (dashboard/analytics).** "No data to display yet. Data will appear here once activity begins." Set expectations for when data will populate: "Check back after your first campaign sends."

**Error state (failed load).** "We couldn't load your messages. Check your connection and try again." Include a "Retry" button.

**Filtered empty state.** "No items match these filters. Try adjusting your filter criteria or clear all filters." Include a "Clear filters" link inline.

### Confirmation Dialogs

Structure confirmation dialogs based on the severity and reversibility of the action.

**Low severity (reversible).** Title: "Archive this conversation?" Body: "You can find archived conversations in the Archive folder." Actions: "Archive" / "Cancel."

**Medium severity (consequential).** Title: "Remove this team member?" Body: "Alex Johnson will lose access to all shared files and channels. You can re-invite them later." Actions: "Remove member" / "Keep member."

**High severity (irreversible).** Title: "Permanently delete this account?" Body: "This will delete all your data, including files, messages, and settings. This action cannot be undone." Actions: "Delete my account" (red/destructive styling) / "Keep my account." Consider requiring typed confirmation for irreversible destructive actions: "Type DELETE to confirm."

**Never use "Are you sure?" as a confirmation dialog title.** It is vague, does not describe the action, and does not help the user make an informed decision.

### Placeholder Text

Use placeholder text sparingly and intentionally.

**When to use.** Use placeholders to show the expected format of input: "name@example.com" in an email field, "MM/DD/YYYY" in a date field, "Search by name or ID" in a search field.

**When to avoid.** Never use placeholder text as a substitute for a label. Placeholders disappear on focus, removing the instruction when the user needs it most. Never put critical instructions in placeholder text. Never use "Type here..." or "Enter text..." — they add no information.

**Format.** Use a lighter text color (minimum 4.5:1 contrast ratio against the background, or use a visible label alongside the placeholder). Use sentence case. Keep to a short phrase, not a full sentence.

### Tooltips and Help Text

Apply progressive disclosure: show the minimum information needed to complete the task, with more detail available on demand.

**Inline help text.** Place persistent help text below form fields for inputs that commonly cause confusion. Keep to one sentence. Example below a "Username" field: "This will be your public display name."

**Tooltips.** Use tooltips for supplementary information that most users do not need. Trigger on hover (desktop) or tap (mobile). Keep to 1-2 sentences. Do not put essential information in tooltips — if the user cannot complete the task without the tooltip content, it should be inline help text instead.

**Contextual help.** For complex features, provide a "Learn more" link that opens documentation or an in-context help panel. Do not force users to leave their current task to get help.

### Onboarding Copy

Write onboarding copy that reduces time-to-value and builds confidence.

**Welcome screen.** State the core value proposition in one sentence. Follow with the first action: "Welcome to [Product]. Let's set up your workspace." Not: "Welcome to [Product]! We're so excited to have you! There are so many amazing features waiting for you!"

**Step-by-step setup.** Number the steps. Show progress. Use action-oriented headings: "Connect your calendar," "Invite your team," "Choose your preferences." For each step, explain why it matters in one sentence: "Connecting your calendar lets us schedule meetings without back-and-forth."

**Feature introduction.** Introduce features at the moment of relevance, not all at once. When the user first encounters a feature, provide a brief tooltip or callout: "This is your activity feed. Recent updates from your team appear here."

**Completion.** Acknowledge setup completion: "You're all set. Here's your dashboard." Offer a guided tour as an option, not a requirement.

### Notification Copy

Adapt copy to the constraints and context of each notification channel.

**Push notifications.** Maximum 50 characters for the title, 100 for the body. Lead with the essential information. "Alex commented on your proposal" not "You have a new notification." Include enough context to decide whether to open the app.

**Email notifications.** Subject line: action-oriented, under 50 characters. Body: one clear action per email. State what happened, why it matters, and what to do. Include a direct link to the relevant item. Provide an unsubscribe link in every non-transactional email.

**In-app notifications.** Keep to one sentence. Provide a direct link to the relevant item. Allow dismissal. Group related notifications to prevent overload.

### Success and Celebration Copy

Acknowledge user achievements without being excessive.

**Task completion.** "Changes saved." "Message sent." "File uploaded successfully." Simple, factual confirmation is sufficient for routine actions.

**Milestone achievements.** "You've completed 100 tasks this month." Acknowledge the accomplishment factually. Avoid forced enthusiasm: "Wow! Amazing! You're on fire!" is patronizing.

**Onboarding completion.** "Setup complete. Your workspace is ready." A single warm acknowledgment is appropriate. Do not use confetti animations or excessive celebration for completing basic setup.

**Failure of celebration.** Celebratory copy in the wrong context destroys trust. Never celebrate after a destructive action ("Account deleted successfully!" with a party emoji). Never celebrate routine actions with excessive enthusiasm.

### Loading State Copy

Tell users what is happening during waits.

**Short waits (under 3 seconds).** A spinner or progress indicator is sufficient. No copy needed unless the action is ambiguous.

**Medium waits (3-10 seconds).** Add contextual copy: "Loading your dashboard..." "Generating report..." "Syncing your files..." Use present participle (verb + -ing) to convey ongoing action.

**Long waits (over 10 seconds).** Provide progress information: "Processing 847 of 2,400 records..." "This usually takes 1-2 minutes." If the user can navigate away, say so: "We'll notify you when your export is ready. You can close this page."

**Background processing.** "Your report is being generated. We'll email you when it's ready." Always provide a way to check status.
