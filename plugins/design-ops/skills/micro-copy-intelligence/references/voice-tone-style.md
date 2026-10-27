# Voice, Tone, Style, and Localization

> Voice and tone calibration, sector tone guides, readability targets, inclusive language, i18n rules, the anti-pattern encyclopedia, and the writing process. Templates live in the other reference files.

## Voice and Tone Framework

**Voice** is your product's personality — it stays constant. **Tone** adapts to context.

### Voice Spectrum (Pick Your Position)

```
Formal ←————————————————→ Casual
  |                           |
  Banking, Legal,         Social, Gaming,
  Enterprise              Consumer

Serious ←————————————————→ Playful
  |                           |
  Healthcare, Finance     Entertainment,
  Security                Kids, Social

Respectful ←—————————————→ Irreverent
  |                           |
  Government, Medical     Startup, Youth
  Enterprise              Consumer

Matter-of-fact ←—————————→ Enthusiastic
  |                           |
  Utilities, Tools        E-commerce,
  Productivity            Fitness, Social
```

### Tone Spectrum (Formal to Playful)

| Tone Level | Description | Use When | Example |
|---|---|---|---|
| **Formal** | Professional, precise, no contractions | Legal agreements, medical information, financial transactions, security alerts | "Your account will be permanently deactivated. This action cannot be reversed." |
| **Professional** | Clear, direct, occasional contractions | Enterprise software, settings, documentation, admin interfaces | "You don't have permission to view this page. Contact your admin for access." |
| **Friendly** | Warm, conversational, uses "you" and "we" | Consumer apps, onboarding, success states, feature introductions | "You're all set! Your workspace is ready. Invite your team to get started." |
| **Casual** | Relaxed, playful, may use colloquialisms | Social apps, gaming, creative tools, loading states | "Nice! Your design is looking great. Share it with the world?" |
| **Playful** | Humorous, personality-driven, uses wordplay | Brand moments, easter eggs, marketing-adjacent surfaces | "Inbox zero. Go outside. Touch grass. You've earned it." |

### Context-Dependent Tone Shifts

Even within a single product, tone shifts based on context.

- **Error messages**: One notch more formal than the product's baseline. Errors are not the time for jokes.
- **Success messages**: One notch more casual than baseline. Celebrate gently.
- **Destructive actions**: Always professional or formal. "This will permanently delete your data" should never sound casual.
- **Onboarding**: One notch more friendly than baseline. First impressions benefit from warmth.
- **Help documentation**: Match the product baseline exactly. Consistency aids comprehension.

### Brand Voice Consistency

- **Create a voice chart**: Define 3-4 voice attributes (e.g., "Clear, Confident, Friendly, Never Condescending") and provide do/don't examples for each.
- **Write a word list**: Document preferred terms. Do you say "Sign in" or "Log in"? "Delete" or "Remove"? "Settings" or "Preferences"? Pick one and use it everywhere.
- **Audit regularly**: Microcopy written by different team members drifts over time. Quarterly audits catch inconsistencies before users notice them.
- **Localization consideration**: Humor, idioms, and contractions do not always translate. If your product is localized, write source copy that is clear enough to survive translation. Avoid puns, cultural references, and slang that a translator might misinterpret or be forced to abandon.

### The Golden Rules of Microcopy

1. **Clarity over cleverness.** A user who understands immediately beats a user who smiles but hesitates.
2. **Say less.** Every word competes for attention. Fewer words mean each remaining word carries more weight.
3. **Use the user's language.** If your users say "customers," do not say "contacts." If they say "send," do not say "dispatch."
4. **Front-load the important word.** "Delete 15 files permanently" puts the action first. "Are you sure you want to permanently delete the 15 files you selected?" buries it.
5. **Be specific about consequences.** "This can't be undone" is good. "Your 23 tasks and 4 attachments will be permanently deleted" is better.
6. **Test with real users.** The microcopy you think is clear may confuse the people who actually use your product. A/B test critical flows. Run comprehension tests on error messages. Watch session recordings for hesitation.

## Content Hierarchy in UI

Every UI moment has three layers of information. Not all three are always needed.

| Layer         | Purpose            | Example (File Upload)               |
| ------------- | ------------------ | ----------------------------------- |
| **Primary**   | What to do         | "Upload your photo"                 |
| **Secondary** | Why or context     | "This will be your profile picture" |
| **Tertiary**  | How or constraints | "JPG or PNG, max 5 MB"              |

**Rules:**

- Primary copy is always visible
- Secondary copy appears when context is unclear
- Tertiary copy appears on hover, in helper text, or when errors occur
- Mobile: reduce to primary + tertiary (space is precious)

## Readability Scoring for UI

Target readability for UI text:

| Component                 | Flesch-Kincaid Grade | Max Words | Max Characters |
| ------------------------- | -------------------- | --------- | -------------- |
| Button label              | Grade 3-5            | 1-4       | 25             |
| Tooltip                   | Grade 5-7            | 5-15      | 80             |
| Error headline            | Grade 4-6            | 3-8       | 50             |
| Error body                | Grade 5-7            | 10-25     | 150            |
| Empty state headline      | Grade 4-6            | 3-8       | 50             |
| Empty state body          | Grade 5-8            | 10-30     | 180            |
| Toast message             | Grade 4-6            | 3-10      | 60             |
| Notification title        | Grade 4-6            | 3-10      | 65             |
| Notification body         | Grade 5-7            | 10-25     | 150            |
| Onboarding headline       | Grade 3-5            | 3-8       | 50             |
| Onboarding body           | Grade 5-7            | 15-40     | 250            |
| Helper text               | Grade 5-7            | 5-15      | 100            |
| Confirmation dialog title | Grade 4-6            | 3-8       | 50             |
| Confirmation dialog body  | Grade 5-7            | 10-30     | 180            |
| Permission request body   | Grade 5-7            | 15-35     | 200            |
| Loading message           | Grade 3-5            | 2-8       | 50             |

**Testing readability:** Paste your copy into Hemingway Editor or use the Flesch-Kincaid formula. If a 12-year-old cannot understand it instantly, rewrite it.

## Inclusive Language Checklist

Before shipping any microcopy:

- [ ] **Gender-neutral:** "They" not "he/she". "Spouse" not "husband/wife". "Parent" not "mother/father" (unless context-specific).
- [ ] **Ability-neutral:** "Select" not "Click". "View" not "See". "Enter" not "Type". Avoid "simple", "easy", "just" (what is easy for you may not be for them).
- [ ] **Age-neutral:** Avoid generational slang. "Download" not "Yeet this to your device".
- [ ] **Culture-neutral:** Avoid idioms that do not translate ("break a leg", "piece of cake"). No sports metaphors as primary copy.
- [ ] **Jargon-free:** "Sign in" not "Authenticate". "Save" not "Persist". "Error" not "Exception".
- [ ] **No assumptions:** Do not assume family structure, location, device, connection speed, or technical literacy.
- [ ] **Respectful defaults:** "Preferred name" not "Nickname". "Phone number (optional)" not "Mobile number (required)".
- [ ] **Error messages blame the system, not the user:** "We couldn't process that" not "You made an error".

## i18n Considerations for Microcopy

Microcopy that works in English may break in translation. Plan ahead:

### Text Expansion

| Language   | Expansion vs. English                       |
| ---------- | ------------------------------------------- |
| German     | +30-35%                                     |
| French     | +15-20%                                     |
| Spanish    | +20-25%                                     |
| Italian    | +15-20%                                     |
| Portuguese | +20-30%                                     |
| Russian    | +15-20%                                     |
| Japanese   | -10-20% (character count, but wider glyphs) |
| Chinese    | -20-30% (character count)                   |
| Arabic     | +20-25% (plus RTL layout)                   |
| Korean     | -10-15%                                     |

**Rules:**

- Buttons: Allow 40% extra width or use auto-sizing
- Tooltips: Max 60% of container width in English to allow expansion
- Never hard-code string widths
- Test with German and Arabic (longest expansion + RTL)

### Cultural Sensitivity

- **Humor:** Puns and wordplay rarely translate. Stick to clear language.
- **Formality:** German, Japanese, Korean require formal register by default. "Du" vs "Sie" in German matters enormously.
- **Color of language:** "Red" means danger in the West, luck in China. Do not rely on color words alone.
- **Dates and numbers:** "1/2/2026" is January 2 (US) or February 1 (most of the world). Use explicit formats.
- **Names:** Not everyone has a first + last name structure. "Full name" is safer than "First name / Last name".
- **Icons with text:** Thumbs-up is offensive in parts of the Middle East. Always pair icons with text labels.

### String Externalization

- Every user-facing string must be in a localization file, never hard-coded
- Use ICU MessageFormat for plurals: `{count, plural, one {# item} other {# items}}`
- Avoid string concatenation: `"Welcome, " + name + "!"` breaks in languages with different word order
- Use full sentences as translation units, not fragments

## Sector Tone Guides

### Fintech / Banking

- **Voice:** Trustworthy, precise, confident
- **Tone keywords:** Secure, clear, straightforward, reliable
- **Do:** "Your transfer of $500 to Alex is complete" / "Verify your identity to protect your account"
- **Don't:** "Woohoo, money sent!" / "We need to make sure you're really you lol"
- **Button style:** "Transfer funds", "Review statement", "Verify identity"
- **Error style:** "We couldn't complete this transfer. Your account has not been charged. [Try again]"

### Healthcare / Wellness

- **Voice:** Empathetic, clear, reassuring
- **Tone keywords:** Caring, supportive, plain, calm
- **Do:** "Your appointment with Dr. Chen is confirmed for March 15 at 2:00 PM" / "Your results are ready. Tap to view."
- **Don't:** "Awesome, you're booked!" / "RESULTS ARE IN!!!"
- **Button style:** "Schedule appointment", "View results", "Message your care team"
- **Error style:** "We couldn't schedule your appointment. Dr. Chen is available at these other times: [alternatives]"

### SaaS / Productivity

- **Voice:** Efficient, empowering, knowledgeable
- **Tone keywords:** Smart, capable, streamlined, no-nonsense
- **Do:** "Project created. Invite your team to get started." / "3 tasks due today"
- **Don't:** "YAY, new project!" / "You've got stuff to do"
- **Button style:** "Create project", "Invite team", "Start timer"
- **Error style:** "This project name is already taken. Try a different name. [Rename]"

### Social / Community

- **Voice:** Warm, expressive, conversational
- **Tone keywords:** Friendly, personal, inclusive, fun
- **Do:** "Alex liked your photo" / "Share what's on your mind"
- **Don't:** "User 4829 interacted with your content" / "Compose a status update"
- **Button style:** "Share", "Like", "Comment", "Send a message"
- **Error style:** "We couldn't post that right now. Your draft is saved. [Try again]"

### E-commerce / Marketplace

- **Voice:** Helpful, enthusiastic, trustworthy
- **Tone keywords:** Exciting, confident, reassuring, action-oriented
- **Do:** "Free shipping on orders over $50" / "Only 3 left in stock"
- **Don't:** "Shipping fees may apply based on various factors" / "Limited inventory warning"
- **Button style:** "Add to cart", "Buy now", "Apply code", "Complete purchase"
- **Error style:** "This item just sold out. We'll notify you when it's back. [Get notified]"

### Education / EdTech

- **Voice:** Encouraging, patient, clear
- **Tone keywords:** Supportive, motivating, structured, approachable
- **Do:** "Great work! You completed 3 of 5 lessons." / "Pick up where you left off"
- **Don't:** "CRUSHING IT" / "Resume incomplete module"
- **Button style:** "Start lesson", "Continue learning", "Take quiz", "Review answers"
- **Error style:** "That answer didn't match. Review the hint and try again. [Show hint]"

### Developer Tools

- **Voice:** Direct, precise, technical (but not jargon-heavy)
- **Tone keywords:** Efficient, accurate, no-fluff, respectful of expertise
- **Do:** "Build succeeded in 2.3s" / "API key created. Copy it now — it won't be shown again."
- **Don't:** "Yay, your build worked!" / "Here's your secret key thingy"
- **Button style:** "Deploy", "Create API key", "View logs", "Run tests"
- **Error style:** "Build failed: missing dependency `lodash@4.17`. Run `npm install lodash` to fix. [View full log]"

### Gaming / Entertainment

- **Voice:** Energetic, immersive, personality-forward
- **Tone keywords:** Exciting, playful, dramatic, rewarding
- **Do:** "New high score! You beat your record by 200 points." / "Ready for the next challenge?"
- **Don't:** "Score updated in database" / "Proceed to next level"
- **Button style:** "Play now", "Challenge a friend", "Claim reward", "Continue quest"
- **Error style:** "Connection lost. Your progress is saved. [Reconnect]"

### Real Estate / Property

- **Voice:** Professional, informative, aspirational
- **Tone keywords:** Trustworthy, detailed, approachable, knowledgeable
- **Do:** "3 new listings match your search" / "Schedule a tour of 123 Oak Street"
- **Don't:** "OMG new houses!" / "Initiate property viewing request"
- **Button style:** "Schedule tour", "Save listing", "Contact agent", "Get pre-approved"
- **Error style:** "This listing is no longer available. Here are similar homes nearby. [View similar]"

### Travel / Hospitality

- **Voice:** Inspiring, helpful, warm
- **Tone keywords:** Adventurous, reassuring, personal, anticipatory
- **Do:** "Your trip to Tokyo is confirmed. 14 days to go!" / "Explore things to do near your hotel"
- **Don't:** "Booking reference confirmed" / "Ancillary activity discovery module"
- **Button style:** "Book now", "Explore destinations", "Check availability", "Add to trip"
- **Error style:** "These dates just got booked. Try nearby dates — we found 5 options. [View alternatives]"

## Anti-Pattern Encyclopedia (Top 25)

| #   | Anti-Pattern               | Example                                         | Fix                                                                           |
| --- | -------------------------- | ----------------------------------------------- | ----------------------------------------------------------------------------- |
| 1   | Vague button               | "Submit"                                        | "Create account" / "Send message"                                             |
| 2   | "Click here"               | "Click here to learn more"                      | "Learn more about pricing"                                                    |
| 3   | Blaming the user           | "You entered an invalid email"                  | "That doesn't look like an email address"                                     |
| 4   | ALL CAPS buttons           | "DELETE ACCOUNT"                                | "Delete account" (sentence case)                                              |
| 5   | Technical jargon           | "Error 500: Internal Server Error"              | "Something went wrong. We're looking into it."                                |
| 6   | Double negatives           | "Don't forget to not leave blank"               | "This field is required"                                                      |
| 7   | Inconsistent terms         | "Save" here, "Update" there, "Submit" elsewhere | Pick one term per action type                                                 |
| 8   | Wall of text in modal      | 200-word confirmation dialog                    | 2 sentences max in dialog body                                                |
| 9   | No recovery action         | "Payment failed." (full stop, nothing else)     | "Payment failed. Check your card details and try again. [Update payment]"     |
| 10  | Forced enthusiasm          | "AMAZING! You signed up!!!"                     | "Welcome. Your account is ready."                                             |
| 11  | Guilt-tripping             | "No thanks, I don't want to save money"         | "No thanks" / "Skip" / "Maybe later"                                          |
| 12  | Ambiguous "OK"             | Dialog with only "OK" and "Cancel"              | "Delete photo" and "Keep photo"                                               |
| 13  | Placeholder as label       | Input with only "Email" as placeholder          | Persistent label above + placeholder example                                  |
| 14  | Disappearing feedback      | Toast that vanishes in 1 second                 | Minimum 4 seconds + dismiss button                                            |
| 15  | Generic empty state        | "No items"                                      | "No projects yet. Create your first project to get started. [Create project]" |
| 16  | Permission without context | System dialog with no pre-screen                | Pre-permission screen explaining benefit first                                |
| 17  | Error with no specifics    | "Invalid" (entire message)                      | "Password must be at least 8 characters"                                      |
| 18  | Cute over clear            | "Oopsie daisy! Something went wrong uwu"        | "Something went wrong. Try refreshing the page."                              |
| 19  | Hidden destructive action  | Delete styled as primary action                 | Red text, confirmation dialog, clear consequences                             |
| 20  | Loading with no context    | Spinner with no message forever                 | "Loading your dashboard..." with progress indicator                           |
| 21  | Overloaded button          | "Save, publish, and notify team"                | Three separate actions or a split button                                      |
| 22  | Negative framing           | "You have 0 connections"                        | "Start connecting with people you know"                                       |
| 23  | Passive voice error        | "An error was encountered"                      | "We hit a snag" or "Something went wrong"                                     |
| 24  | Unexplained restriction    | "This action is not allowed"                    | "Only workspace admins can delete projects. Ask your admin for access."       |
| 25  | Untranslatable idiom       | "Piece of cake!" as success message             | "Done!" or "All set!"                                                         |

## Writing Microcopy: Step-by-Step Process

1. **Identify the moment.** What is the user doing right now? What just happened? What emotional state are they likely in?
2. **Determine the goal.** What do you need the user to understand or do next?
3. **Pick the tone.** Use the tone adaptation table — match the context, not your default voice.
4. **Draft with the formula.** [Action] + [Object] + [Benefit/Context] as needed.
5. **Cut ruthlessly.** Remove every word that is not doing work. Read it aloud — if you stumble, simplify.
6. **Check the checklist.** Inclusive? Translatable? Accessible? Consistent? Specific?
7. **Test with real users.** Show it out of context — can they tell what it means? Show it in context — do they do the right thing?
