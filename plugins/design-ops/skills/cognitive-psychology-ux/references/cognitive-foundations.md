# Cognitive Foundations: Mental Models, Load, Attention, Memory, Decisions

## Mental Models: The User-System Gap

A mental model is a user's internal representation of how a system works. Users do not read documentation or inspect source code; they build a mental model from the interface's affordances, labels, feedback, and their prior experience with similar systems.

The **system model** is how the system actually works — its data structures, state machines, and business logic. The **user model** is what the user believes is happening. The **design model** (or represented model) is what the interface communicates.

Great design minimizes the gap between the user model and the system model by making the design model transparent and intuitive. When a user drags a file to the trash, the mental model is "I am throwing this away." If the system actually moves the file to a hidden `.Trash` directory and only deletes it on empty, the design model must communicate this (through the "Empty Trash" action and the recoverable state) or users will be confused when "deleted" files reappear.

**Practical techniques for aligning mental models:**
- Use familiar metaphors grounded in real-world experience (folders, shopping carts, bookmarks)
- Provide immediate, visible feedback that confirms the user's expectation of what just happened
- Use progressive disclosure to match the user's evolving understanding — do not front-load the full system model
- Run first-click tests and think-aloud protocols to surface model mismatches early
- Design error messages that correct the mental model, not just describe the system state

See `nng-ux-heuristics` (Heuristic 2: Match Between System and the Real World) for the heuristic framework that operationalizes mental model alignment.

## Cognitive Load Theory Applied to UI Design

John Sweller's Cognitive Load Theory identifies three types of cognitive load, each with distinct design implications:

**Intrinsic load** is the inherent difficulty of the task itself. Filing a tax return is intrinsically complex; toggling a light switch is intrinsically simple. Designers cannot eliminate intrinsic load, but they can manage it through task decomposition — breaking a complex task into a sequence of simpler steps (wizard patterns, progressive forms).

**Extraneous load** is unnecessary load imposed by poor design. Confusing navigation, inconsistent terminology, hidden controls, gratuitous animation, and unclear hierarchy all add extraneous load. This is the load designers should ruthlessly eliminate. Every unit of extraneous load steals cognitive capacity from the actual task.

**Germane load** is the productive load involved in learning and schema formation. Well-designed onboarding, meaningful patterns, and consistent conventions help users build reusable mental schemas. Germane load is desirable — it represents the user's investment in becoming proficient.

**The design equation:** Minimize extraneous load. Manage intrinsic load through decomposition. Maximize germane load through consistency and meaningful patterns. The total cognitive load at any moment must stay within working memory capacity, or the user will experience confusion, errors, and frustration.

**Measurable indicators of cognitive overload:**
- Task abandonment at specific steps (analytics)
- Increased time-on-task without increased accuracy (usability testing)
- User verbalization of confusion in think-aloud protocols
- Pupil dilation and galvanic skin response (neuroUX research labs)
- Increased error rates at points of high visual density

See `references/neurodesign-engagement-science.md` for Sweller's specific effects (split-attention, redundancy, modality) and measurement techniques.

## Attention: Selective, Divided, and Sustained

Attention is a finite cognitive resource, not an infinite channel. Three modes of attention are directly relevant to interface design:

**Selective attention** is the ability to focus on one stimulus while filtering out others. Users engaged in a task will literally not see elements outside their focus area — a phenomenon called inattentional blindness (Simons & Chabris, 1999). This is why banner blindness exists: users learn to selectively ignore regions associated with advertising. Design implication: critical information must be placed within the user's task-focused visual flow, not relegated to "announcement" areas the brain has learned to filter.

**Divided attention** is the attempt to process multiple information streams simultaneously. Humans are poor at this. Every additional demand — a notification badge, a chatbot popup, an autoplaying video — steals capacity from the primary task. Gloria Mark's research at UC Irvine demonstrates that a single interruption costs an average of 23 minutes and 15 seconds to fully recover from. Design implication: protect the user's primary task flow. Defer non-critical notifications. Never autoplay competing content during task execution.

**Sustained attention** is the ability to maintain focus over extended periods. It degrades predictably: after 10-15 minutes, vigilance drops measurably (the vigilance decrement). Long forms, lengthy onboarding sequences, and extended reading without visual breaks all suffer from this. Design implication: chunk long tasks with progress indicators, celebrate micro-completions, and vary visual rhythm to counteract the decrement.

See `interaction-motion-design` for techniques that direct attention through motion, and `accessibility-inclusive-design` for cognitive accessibility considerations related to attention disorders.

## Memory: Working Memory, Recognition, and Chunking

**Working memory** is the mental workspace where active processing occurs. Cowan's revised estimate places its capacity at roughly 4 chunks (plus or minus 1) for novel information — lower than Miller's original 7 plus or minus 2, which applied to well-practiced domains. This is the fundamental constraint behind every "keep it simple" design recommendation.

**Recognition versus recall** is one of the most actionable distinctions in cognitive psychology. Recognition (identifying something from visible options) is dramatically easier than recall (retrieving something from memory with no cues). Dropdown menus leverage recognition. Blank text fields demand recall. Autocomplete transforms a recall task into a recognition task — this is why it is one of the highest-impact UI patterns ever developed.

This distinction is so important that Nielsen and Norman formalized it as Heuristic 6: Recognition Rather Than Recall. See `nng-ux-heuristics` for the full treatment.

**Chunking** is the strategy of grouping individual items into meaningful clusters to fit within working memory limits. Phone numbers are chunked as 3-3-4 (in the US). Credit card numbers are chunked as 4-4-4-4. A well-designed dashboard chunks metrics into labeled groups (Revenue, Users, Performance) rather than presenting 20 ungrouped numbers.

**Serial position effects** shape what users remember from lists and sequences. The primacy effect (better recall of first items) and recency effect (better recall of last items) mean that the most important navigation items should be placed first and last. Items in the middle of a long list receive the least attention and worst recall. See `references/cognitive-biases-design-patterns.md` for the full treatment.

## Decision-Making: Satisficing, Maximizing, and Choice Architecture

Herbert Simon's concept of **satisficing** describes how humans actually make decisions: not by evaluating every possible option to find the optimal one (maximizing), but by scanning options until they find one that is "good enough." Users do not read every menu item; they click the first one that seems plausible. They do not compare all 15 pricing plans; they look for the one labeled "Most Popular."

**Choice overload** (Iyengar & Lepper, 2000) demonstrates that increasing options can decrease satisfaction and increase decision paralysis. The famous jam study showed that 24 varieties led to 3% purchase rate while 6 varieties led to 30%. In UX terms: fewer, well-curated options outperform exhaustive catalogs unless the user has explicitly entered an exploration mode.

**Choice architecture** (Thaler & Sunstein) is the deliberate structuring of how choices are presented. Smart defaults, recommended options, progressive filtering, and comparison tools are all choice architecture techniques. The ethical imperative is that choice architecture should serve the user's interests, not exploit their biases. A pre-checked "subscribe to marketing emails" checkbox exploits default bias. A pre-selected "standard shipping" option genuinely serves the most common user need.

**Decision fatigue** is the empirically demonstrated degradation of decision quality after extended sequences of choices. Judges grant parole at higher rates after meals. Users accept worse defaults later in a long configuration flow. Design implication: place the most consequential decisions early in a flow, and reduce trivial decisions through intelligent defaults.

See `ux-ethics-content-strategy` for the ethical framework around choice architecture and `references/cognitive-biases-design-patterns.md` for the complete catalog of decision biases.
