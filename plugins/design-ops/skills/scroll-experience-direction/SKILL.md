---
name: scroll-experience-direction
description: "Art-directs cinematic scroll sites around one subject: interview, verified brand assets and facts, live references, depth planes with contact anchors, opening/midpoint/exit states, photographic compositing or real 3D, Kie AI imagery, separate phone direction, a uniqueness gate against past builds, and frame-checked packaging. Use when building premium launch, product or brand storytelling sites."
allowed-tools: Read, Grep, Glob, Write, Bash(node *), Bash(ffmpeg *)
---

# Scroll Experience Direction — a cinematic site, art-directed per subject

A premium scroll site is not a page with animations added. It is a short film the visitor
drives with one finger. The scene has real depth, a subject that rests on something, a single
peak, and an ending that resolves instead of fading into a footer. Every site this skill
produces is designed **for its subject**. There is no house template, no canon of approved
sites, and no stock "world" to reuse. The direction comes from interviewing the user,
verifying the subject, and sourcing live references this session.

`/scroll` runs this skill end to end; the skills under Cross-References supply the parts.

## Mental model

- **Truth before pixels.** Real product, real logo, real facts. Generated imagery fills
  gaps around authentic assets; it never replaces them. Anything that cannot be verified
  stays out of the copy.
- **Depth is planned, not decorated.** Every hero is a contract of independent planes. Each
  plane has its own rate. Subjects stay on their contact points. Each act is written as its
  opening, midpoint and exit before any asset exists.
- **The subject picks the renderer.** Photographic compositing, real 3D, authored video, an
  image sequence or plain CSS. Choose by what the subject needs to do: rotate, catch light,
  move through space, or just hold still beautifully.
- **Every site is its own species.** Navigation, information order, the controls, the
  signature move and the ending are chosen for this offer. They are gated against every
  earlier build so site #12 cannot quietly repeat site #3.
- **Phones get their own direction.** A phone layout is recomposed, not shrunk.
- **Only a rendered frame is evidence.** A passing build proves nothing about how it looks.
  Frames captured at the opening, midpoint and exit of every act, on desktop, phone, reduced
  motion, no-JS and no-WebGL, are the evidence.

## Stage loop

| # | Stage | Gate (must hold before the next stage) | Writes |
| --- | --- | --- | --- |
| 0 | Interview | Creative authority is clear; brief approved or explicitly delegated | `.design-ops/scroll/brief.md` |
| 1 | Subject truth | Official sources opened; every asset opened and described; unknowns listed | `scroll/subject.md`, `scroll/assets.json` |
| 2 | Sourcing | 3-5 live references kept by the user, each with frame notes | `refs/` via `/inspo`, `scroll/sourcing.md` |
| 3 | Plan | Fingerprint gate passes; user approves the plan | `scroll/plan.json` |
| 4 | Assets | Every image looked at; edges checked; provenance recorded | `scroll/assets/`, `scroll/assets.json` |
| 5 | Build | Runs locally; tokens come from `style.json` if it exists | project source |
| 6 | Verify | Frame report clean; board grade clears the wall; feel diff agrees | `scroll/verify/` |
| 7 | Package | Delivery gate passes at the package root; fingerprint row appended | package dir, `fingerprints.ndjson` |

One stage at a time. Never generate an asset before stage 3 is approved.

## Constants

- **Runtime:** follow `style.json` `project.framework`. Default to GSAP ScrollTrigger +
  Lenis, R3F (or vanilla Three.js outside React) for real 3D, and CSS for everything that
  needs no timeline. Never ship a bespoke scroll engine.
- **Acts:** 4-7 beats. A section that serves no beat is cut.
- **Peak:** exactly one. It gets the largest span, the largest asset budget, and quiet
  before it.
- **Scrub devices:** at most 2 per page. Never use the same device in two adjacent acts.
- **Parallax:** adjacent planes differ by 10-30% in rate. Several layers moving together
  count as one plane.
- **Fingerprint gate:** differ from every registry row on at least 4 of 6 dimensions.
- **Viewports verified:** 1440×900, 390×844, 360×640, plus reduced motion, no-JS and no-WebGL.
- **Contrast:** 4.5:1 for body text, 3:1 for large text and controls, measured on the
  composited frame and not on the CSS colour pair.
- **Registry:** `${DESIGN_OPS_HOME:-~/.design-ops}/fingerprints.ndjson`, append-only. Change
  the plan, never the log.

## Hard rules

| Never | Instead |
| --- | --- |
| Generate before the brief and the plan are approved | Interview, verify, plan, get approval, then generate |
| Invent stats, testimonials, prices, availability or dates | Use verified facts, or an honest flow for the subject's state |
| Recreate the real product or logo with a generator | Pass the authentic asset as a reference on every shot |
| Bake text into imagery | Semantic HTML type over a planned empty area |
| Use a generic primitive as "the 3D product" | Model the real object, use the user's GLB, or choose compositing |
| Scale the desktop composition down for phones | Recompose: crop, pivot, type position, travel and duration |
| Add scroll-hint cues, "01 / 06" counters, an eyebrow on every heading | Let the composition invite the scroll |
| Fade the last act into a footer | A close that resolves and holds, and carries the user's choices |
| Use a full-frame dark overlay to rescue contrast | Recompose the empty area, add a local scrim, or regrade the plate |
| Reduce motion to zero | Fewer and gentler moves: posters hold, scrubs become stills |
| Treat a green build as visual proof | Read the captured frames |

## Routing

- **Starting a site**, or the user hands over creative direction: `references/interview-and-subject.md` (interview questions, delegation, subject verification, asset provenance). Read it first; nothing else runs until its gate holds.
- **The hero or any layered scene**: `references/depth-and-states.md` (layer contract, contact anchors, opening/midpoint/exit, parallax numbers), before writing a prompt or a line of markup.
- **Deciding how a subject is rendered**: `references/render-route.md` (compositing vs real 3D vs video vs image sequence vs CSS; WebGL and encode rules). Then go to `animation-recipe-library` for the code: `gsap-scrolltrigger-recipes.md` for pin, scrub and Lenis, and `cursor-text-3d-effects.md` for R3F.
- **Making the site different from everything before it**: `references/uniqueness.md` (page grammars, signature move, controls, endings, feeling curve). Run its fingerprint gate before asking for plan approval.
- **Phones**: `references/phone-direction.md`, while planning, not after the desktop build.
- **Generating imagery or footage**: `references/kie-ai.md` (client, models, preamble formula, prompt rules). If `KIE_AI_API_KEY` is missing, print the specs and prompts for the user to run by hand. Never fail silently.
- **Proving it works and shipping it**: `references/verify-and-package.md` (frame capture, the scroll lens on the grade, fallbacks, delivery gate, packaging, and the script-resolution commands).

## Cross-References

- `reference-intelligence` — live sourcing, DNA capture, the board, and grading against it
- `visual-design-mastery` — the 10-dimension rubric that the scroll lens extends
- `animation-recipe-library` — GSAP ScrollTrigger, Lenis and R3F code for the planned devices
- `interaction-motion-design` — timing, easing and reduced-motion principles
- `ai-design-generation` — other generators (Stitch, Fal.ai, Recraft) when Kie is the wrong tool
- `image-media-patterns` — responsive images, `<picture>`, video and lazy loading
- `design-memory` — the `.design-ops/scroll/` subtree this skill writes
- `accessibility-inclusive-design` — keyboard, focus and vestibular safety
