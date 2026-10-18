# Legal Research Workspace

A single legal matter: the context around it, the documents that bear on it, the
research written about it, and the output produced from it.

## Facts

Filled in when this workspace was provisioned. Read these rather than asking again.

- MATTER:
- JURISDICTION:
- PARTIES:
- CONFIDENTIALITY:
- SUPPRESS_DISCLAIMER: false

## Layout

```
context/            background, parties, jurisdiction notes, Typst templates
case-file/
  documents/        source documents as received — read-only
research/           analyses and research memos, one per document or question
exports/            rendered briefs and memos, with their .typ sources
logs/               one log per operation
```

## Rules

1. **Documents under `case-file/documents/` are read-only.** Analysis writes to
   `research/`; it never modifies a source.
2. **Citations are verified or marked.** Anything not confirmed is written `[verify]`
   and collected in the memo's own section. Never smooth an unchecked citation into a
   confident one.
3. **Observation is separated from inference.** What a document says is recorded apart
   from what it is taken to mean, so a reader can disagree with the second without
   re-reading the first.
4. **Every memo is preliminary analysis, not legal advice**, unless
   `SUPPRESS_DISCLAIMER` above is set to true for internal professional use.
5. **Limitation periods are flagged the moment they appear.** A date that starts a clock
   is recorded in the memo's risk flags, not left in the body text.
6. **Jurisdiction governs citation format.** Where a memo departs from the jurisdiction
   named above, it says so.

## Evidence

This workspace has no `evidence/` tree. If the matter needs chain of custody — hashing,
a custody register, timestamping, packaging — the `evidence-ops` agent creates and owns
that subtree. Read its register; never write to it.

## Working here

- `analyze-document` — read a document, write a memo to `research/`
- `generate-brief` — render a case memo or brief to `exports/`
- `redact-content` — produce a disclosure-safe copy
- `matter-status` — what is unfinished and what needs checking
