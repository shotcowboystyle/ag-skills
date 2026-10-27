# Conversion Measurement and the Optimization Process

Moved verbatim from the `conversion-optimization-patterns` SKILL.md. Figures are unverified; see the warning in SKILL.md.

## Micro-Conversions vs. Macro-Conversions

A mature conversion strategy tracks both:

**Macro-conversions** are the primary business goals:
- Completing a purchase
- Subscribing to a paid plan
- Submitting a lead form
- Creating an account

**Micro-conversions** are the stepping stones that indicate progress toward macro-conversions:
- Clicking a CTA
- Watching a product video
- Downloading a resource
- Adding an item to cart
- Starting (but not completing) a form
- Visiting the pricing page
- Using a free feature

The relationship between micro and macro conversions reveals funnel health. A product with high pricing-page visits but low signups has a pricing or trust problem. A product with high signups but low activation has an onboarding problem. A product with high activation but low paid conversion has a value-demonstration problem.

### Micro-Conversion Tracking Framework

| Funnel Stage | Micro-Conversions to Track | What They Reveal |
|---|---|---|
| Awareness | Page views, time on page, scroll depth | Content relevance and engagement |
| Interest | CTA clicks, video plays, resource downloads | Value proposition resonance |
| Consideration | Pricing page visits, feature comparisons, FAQ views | Purchase intent and objections |
| Intent | Add to cart, start trial, begin signup | Commitment level |
| Evaluation | Feature usage in trial, return visits, invite teammates | Product-market fit signal |
| Purchase | Complete checkout, upgrade from free | Revenue conversion |

## Conversion Measurement Framework

### Essential Metrics

**Conversion Rate (CR):** Total conversions / Total visitors (or total eligible users). Always segment by source, device, and user type. An aggregate conversion rate hides more than it reveals.

**Revenue Per Visitor (RPV):** Total revenue / Total visitors. RPV captures both conversion rate and average order value. An optimization that increases CR but decreases AOV might reduce RPV.

**Customer Acquisition Cost (CAC):** Total acquisition spend / New customers acquired. Conversion optimization directly reduces CAC by increasing the percentage of visitors who convert.

**Lifetime Value to CAC Ratio (LTV:CAC):** Healthy SaaS companies target 3:1 or higher. Conversion optimization that attracts low-quality customers (high churn) can improve CR while worsening LTV:CAC.

**Activation Rate:** Percentage of signups who reach the product's "aha moment." This is the most under-measured conversion metric and often the most impactful to improve.

**Time to Value (TTV):** How long it takes a new user to experience the core value proposition. Reducing TTV from 10 minutes to 2 minutes typically produces outsized conversion improvements.

**Net Revenue Retention (NRR):** Revenue from existing customers including expansion minus churn. A conversion flow that attracts wrong-fit customers will show up as low NRR even with high initial CR.

### Segmentation Principles

Never optimize for aggregate conversion rate. Always segment by:
- **Traffic source** (organic, paid, referral, direct — each has different intent levels)
- **Device** (mobile vs. desktop conversion rates differ by 2-3x in most categories)
- **New vs. returning** visitors (returning visitors usually convert higher)
- **Geography** (cultural differences in trust signals, payment preferences, form tolerance)
- **User intent** (informational vs. transactional — mixing them pollutes your data)
- **Company size / user persona** (enterprise vs. SMB have fundamentally different conversion journeys)

## Running and Analyzing the Test

How to run and analyze a test (sample size, MDE, power, duration, peeking, multiple comparisons, Bayesian vs frequentist, guardrail metrics) is owned by `ux-metrics-measurement` (see its `metrics-frameworks-compendium.md`, "Experimentation Deep Dive"). This file covers what to test and how to prioritize it.

## The Conversion Optimization Process

### Step 1: Quantitative Analysis
Identify where conversions are leaking. Use analytics to find:
- Highest-traffic pages with lowest conversion rates
- Funnel steps with highest drop-off percentages
- Device or segment-specific underperformance
- Pages with high bounce rates despite relevant traffic
- Unusual patterns in time-on-page or scroll depth

### Step 2: Qualitative Research
Understand why conversions are leaking. Methods include:
- Session recordings (Hotjar, FullStory, PostHog) to watch real user behavior
- Heatmaps to identify attention and interaction patterns
- User surveys (on-page, post-purchase, exit-intent)
- Usability testing on specific conversion flows
- Customer support ticket analysis for recurring friction themes
- Sales call recordings for objection pattern mining

### Step 3: Hypothesis Formation
Structure hypotheses as: "Because we observed [data], we believe that [change] will cause [outcome], which we will measure by [metric]."

Example: "Because we observed 67% drop-off on the second step of our signup form (session recordings show users pausing at the company-size question), we believe that removing the company-size field will increase form completion rate by 15%, which we will measure by tracking step-2-to-step-3 progression rate."

### Step 4: Prioritization (ICE or PIE Framework)

**ICE:** Impact (1-10) x Confidence (1-10) x Ease (1-10) = Score
**PIE:** Potential (1-10) x Importance (1-10) x Ease (1-10) = Score

Prioritize tests that combine high expected impact with high confidence in the hypothesis and low implementation effort. Run highest-scoring tests first.

### Step 5: Test, Measure, Learn
Run the test to its pre-planned sample size (method: `ux-metrics-measurement`). Document results regardless of outcome. Losing tests are as valuable as winning tests — they update your model of user behavior and prevent re-testing the same failed hypotheses.

### Step 6: Iterate
Winning tests become the new baseline. Losing tests inform the next hypothesis. The conversion optimization process is a continuous cycle, not a one-time project. Teams that run 2-4 tests per month consistently outperform teams that run occasional "big bang" redesigns.

## Ethical Conversion Optimization

### The Bright Line

Ethical conversion optimization helps users complete actions they already want to take. Unethical conversion optimization manufactures actions the user would not otherwise take.

**Ethical examples:**
- Simplifying a checkout form to reduce abandonment (removing friction from desired behavior)
- Adding trust signals to a pricing page (reducing anxiety about a decision the user is already considering)
- Personalizing CTAs based on user behavior (increasing relevance)
- Showing social proof from similar companies (reducing uncertainty)
- Highlighting the most popular plan (helping users make faster decisions)

**Unethical examples (dark patterns):**
- Hidden costs revealed only at checkout (bait and switch)
- Opt-out checkboxes pre-checked (exploiting defaults against user interest)
- Countdown timers that reset on refresh (manufactured scarcity)
- Making cancellation deliberately difficult (roach motel)
- Confirmshaming ("No, I don't want to save money")
- Disguised ads that look like content or navigation
- Forced continuity (charging after trial without clear notice)
- Misdirection (drawing attention away from unfavorable options)

The FTC, EU Digital Services Act, and CCPA are increasingly taking enforcement actions against dark patterns. Beyond legal risk, dark patterns erode brand trust and increase churn. Users who feel tricked do not become loyal customers — they become vocal detractors.

### The Ethical Test

Before implementing any conversion pattern, apply these four questions:
1. Would the user thank me for this if they understood exactly what it does?
2. Would I be comfortable if a journalist described this pattern in a news article about my product?
3. Does this pattern work equally well for the user and the business, or only for the business?
4. Would removing this pattern cause users to make different decisions — and would those different decisions actually be better for them?

If any answer gives you pause, redesign the pattern.
