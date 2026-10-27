# Conversion Psychology — Persuasion, Decision Architecture, Biases

Moved verbatim from the `conversion-optimization-patterns` SKILL.md. Figures are unverified; see the warning in SKILL.md.

## Conversion Psychology Foundations

### Cialdini's Six Principles of Persuasion

Robert Cialdini's framework, published in "Influence: The Psychology of Persuasion" (1984) and refined over four decades of research, identifies six fundamental principles that govern human compliance behavior. These are not design tricks — they are deeply rooted cognitive mechanisms that evolved for social coordination.

**Reciprocity.** When someone gives us something, we feel obligated to give something back. In product design, this manifests as free trials, free tools, valuable content, and generous free tiers. Dropbox giving 2GB of free storage created a reciprocity loop: users felt the product had invested in them before asking for payment. The key insight for designers is that reciprocity must feel genuine. A "free" ebook behind a 15-field form does not trigger reciprocity — it triggers resentment.

**Commitment and Consistency.** Once people take a small action, they are far more likely to take larger consistent actions. This is the psychological engine behind progressive onboarding, multi-step forms, and "foot in the door" sequences. Research by Freedman and Fraser (1966) showed that people who agreed to place a small sign in their window were 4x more likely to later agree to a large lawn sign. In product design: get the micro-yes (create an account) before the macro-ask (enter payment).

**Social Proof.** In uncertain situations, people look to others' behavior as a guide. This is why testimonials, user counts, star ratings, and "trending" labels influence behavior. Cialdini's research established that social proof is most powerful when the proof comes from people similar to the decision-maker. "10,000 companies trust us" is less persuasive than "500 companies in your industry trust us."

**Authority.** People defer to perceived experts and authoritative sources. In UI design, authority manifests as expert endorsements, certifications, press logos, patent numbers, and professional design quality itself. A polished, professional interface signals competence; a sloppy one signals risk. Nielsen Norman Group research consistently shows that visual credibility is the first filter users apply — within 50 milliseconds.

**Liking.** People are more likely to comply with requests from people (or brands) they like. Liking is driven by similarity, physical attractiveness, compliments, familiarity, and association with positive things. In product design, this translates to personalization, friendly microcopy, inclusive imagery, and brand personality that resonates with the target audience.

**Scarcity.** People value things more when they are rare or diminishing. Limited-time offers, limited-quantity displays, and countdown timers all leverage scarcity. However, manufactured scarcity that users can detect (e.g., a countdown timer that resets on page refresh) destroys trust more than it drives conversion. Scarcity must be real or not used at all.

### Cialdini's Seventh Principle: Unity

In "Pre-Suasion" (2016), Cialdini added a seventh principle: **Unity** — the shared identity between influencer and audience. "We are the same tribe" is more powerful than any of the original six principles. In product design, unity manifests as community features, shared identity markers ("Built by developers, for developers"), and language that positions the product and user as part of the same in-group.

### The Fogg Behavior Model (B=MAP)

BJ Fogg's Behavior Model, developed at Stanford's Persuasive Technology Lab, provides the most actionable framework for conversion optimization. It states that behavior occurs when three elements converge simultaneously:

**B = MAP** (Behavior happens when Motivation, Ability, and a Prompt converge at the same moment)

- **Motivation**: The user's desire to complete the action. Motivation is driven by pleasure/pain, hope/fear, and social acceptance/rejection.
- **Ability**: How easy the action is to complete. Ability is a function of time, money, physical effort, cognitive effort, social deviance, and non-routine-ness.
- **Prompt**: The cue that tells the user to act now (Fogg called this the "trigger" in earlier versions). Prompts include calls to action, notifications, visual cues, and environmental prompts.

The critical insight: **if motivation is high, ability can be lower (people will work harder). If ability is high (the action is trivially easy), motivation can be lower.** The conversion equation plays out on a curve, not a threshold.

For designers, the Fogg model reframes every conversion problem:
- Low conversion despite clear CTAs? Diagnose motivation or ability, not the prompt.
- Users start but don't complete flows? Ability drops mid-flow (friction spike).
- Users complete flows but don't return? Motivation was artificially inflated (urgency/scarcity) rather than intrinsic.

### BJ Fogg's Tiny Habits and Conversion

Fogg's Tiny Habits framework extends the behavior model with a practical insight: the easiest way to create a new behavior is to make it tiny, anchor it to an existing behavior, and celebrate immediately after. In conversion design:

- **Make it tiny**: The first conversion step should require minimal effort. "Enter your email" is tinier than "Fill out this 8-field form." Google's one-tap sign-in is tinier still.
- **Anchor to existing behavior**: Trigger conversion prompts at moments when users are already engaged. Post-success moments (just completed a task, just got a result) are natural anchors for upgrade prompts.
- **Celebrate**: Immediate positive feedback after micro-conversions reinforces the behavior. Confetti animations on signup, success messages after form completion, and "Welcome!" screens all serve this function.

### The Conversion Equation

The MECLABS conversion heuristic, developed by Flint McGlaughlin and validated across 20,000+ experiments, formalizes the conversion decision:

**C = 4M + 3V + 2(I - F) - 2A**

Where:
- **C** = Probability of conversion
- **M** = Motivation of the user (weighted 4x — the most important factor)
- **V** = Clarity of the value proposition (weighted 3x)
- **I** = Incentive to take action now
- **F** = Friction elements in the process
- **A** = Anxiety about giving information or committing

The equation reveals three design truths:
1. You cannot optimize your way out of a weak value proposition. No amount of CTA color testing will fix a product that users do not want.
2. Friction reduction (simplifying forms, reducing steps, improving load times) has diminishing returns once the baseline is acceptable.
3. Anxiety reduction (trust signals, guarantees, security indicators) is as important as friction reduction — and often overlooked.

## Decision Architecture

### Choice Architecture

Richard Thaler and Cass Sunstein's "Nudge" (2008) established that the way choices are presented profoundly affects which choice people make — even when all options remain available. Designers are choice architects whether they intend to be or not.

**Default Effects.** Defaults are the most powerful nudge. Research across domains shows that most people stick with the default option. In product design, defaults determine:
- Which pricing plan is pre-selected (the one you highlight will get the most signups)
- Whether annual or monthly billing is the default toggle position
- Which notification settings are on by default
- Whether the email opt-in checkbox is checked or unchecked

Ethical principle: defaults should align with what most users would choose if fully informed.

**Framing Effects.** Identical information presented differently produces different decisions. Tversky and Kahneman's (1981) research demonstrated that "90% survival rate" and "10% mortality rate" are logically identical but produce dramatically different choices. In conversion design:
- "Save $120/year" outperforms "Save $10/month" (larger number)
- "Join 50,000 teams" outperforms "Used by companies worldwide" (specificity)
- "Free forever" outperforms "No credit card required" (stronger frame)
- "You'll lose access to..." outperforms "Upgrade to keep..." (loss framing)

**Option Reduction.** Sheena Iyengar's jam study (2000) demonstrated that 24 jam varieties produced 3% purchase rates while 6 varieties produced 30%. Choice overload is real and measurable. For pricing pages, the research consensus is 3-4 tiers maximum. For feature comparison tables, highlighting the recommended option reduces choice paralysis.

### Anchoring

Tversky and Kahneman (1974) demonstrated that initial values disproportionately influence subsequent judgments. In conversion design:
- Showing the enterprise price first makes the team price feel reasonable
- Showing the original price crossed out makes the sale price feel like a deal
- Showing the per-day cost ($3.29/day) instead of the annual cost ($1,200/year) changes the reference point entirely
- Showing a competitor comparison anchors the user's value assessment

Anchoring is not manipulation when it helps users accurately assess value. It becomes manipulation when the anchor is fabricated or misleading.

## Cognitive Biases That Drive Conversion

### Loss Aversion

Kahneman and Tversky's prospect theory (1979) established that losses are psychologically roughly twice as powerful as equivalent gains. A $10 loss hurts approximately twice as much as a $10 gain pleases. In conversion design:

- "Don't lose your progress" outperforms "Save your progress" in save-state prompts
- "Your trial expires in 3 days" outperforms "Extend your trial" for upgrade prompts
- Free trial to paid conversion leverages loss aversion: users have invested time and data they don't want to lose
- "Cancel anytime" reduces the perceived risk of loss from committing

### The Endowment Effect

People value things more once they feel ownership. This is why:
- Customization during onboarding increases conversion (the user has "built" something)
- Progress bars create a sense of invested effort
- Personalized dashboards feel like "my" space
- "Your plan" language creates ownership before purchase

### Social Proof Bias

Already covered under Cialdini, but specific conversion applications deserve emphasis:
- Specific numbers outperform vague claims ("12,847 teams" > "thousands of teams")
- Recency signals amplify proof ("847 signups this week" > "50,000 total signups")
- Similarity-matched proof converts best ("Teams like yours" with relevant logos)
- Negative social proof backfires: "90% of users forget to..." normalizes the undesired behavior

### Scarcity Bias

Beyond Cialdini's principle, scarcity has specific conversion mechanics:
- Quantity scarcity ("Only 3 seats left") outperforms time scarcity ("Sale ends tonight") for immediate action
- Scarcity combined with social proof ("Only 3 seats left — 47 people viewing") amplifies urgency
- Artificial scarcity that users detect reduces trust and conversion
- "Exclusive" framing works only when exclusivity is genuine

### The Bandwagon Effect

Distinct from general social proof, the bandwagon effect describes the tendency to adopt behaviors because they are trending. Real-time activity feeds ("Sarah from London just signed up"), trending badges, and growth metrics ("Fastest-growing tool in...") leverage this bias. The bandwagon effect is strongest during product evaluation when the user has not yet formed an opinion.

### Commitment Bias and Sunk Cost

Once users have invested time, effort, or data, they are reluctant to abandon the process. This has both ethical and practical design implications:
- Multi-step onboarding with progress bars leverages commitment: users who complete step 3 of 5 are unlikely to abandon
- "You're 80% done" messages exploit sunk cost but also genuinely help users who intended to finish
- Asking for easy information first (name, email) before harder information (payment, company details) builds commitment incrementally
- Dark pattern warning: making cancellation deliberately difficult exploits commitment bias unethically

### The IKEA Effect

People overvalue things they helped create. In conversion design:
- Interactive product configurators can increase purchase intent (test it)
- "Build your plan" interfaces outperform "Pick a plan" interfaces
- Templates that users customize convert better than pre-built solutions
- Personalization during trials (custom dashboards, imported data) increases paid conversion

### Paradox of Choice and Satisficing

Barry Schwartz's research (2004) distinguishes maximizers (who seek the optimal choice) from satisficers (who seek a "good enough" choice). Most users are satisficers under time pressure. Conversion implications:
- Recommended/highlighted options serve satisficers by reducing evaluation effort
- Comparison tables serve maximizers by enabling systematic evaluation
- Both groups are served by clear differentiation between options
- Reducing options from 5 to 3 typically helps satisficers without frustrating maximizers

### The Peak-End Rule

Kahneman's research shows that people judge experiences primarily by the peak moment and the ending, not by the average. For conversion flows:
- The moment of successful signup/purchase should be a peak positive experience
- Post-purchase confirmation should reinforce the decision (reduce buyer's remorse)
- Error states during conversion are peak negative moments — invest heavily in error recovery
- The final step of any flow disproportionately affects satisfaction and likelihood of return
