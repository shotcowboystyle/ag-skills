# OSINT Investigation Workspace

A scoped open-source investigation: what is being looked into, where the findings came
from, who is involved, and when things happened.

## Facts

Filled in when this workspace was provisioned. Read these rather than asking again.

- SUBJECT:
- SCOPE:
- BOUNDARIES:
- CONFIDENTIALITY:
- SUPPRESS_DISCLAIMER: false

## Layout

```
context/            the brief, the questions being asked, methodology notes
sources/            register.jsonl — one record per source, append-only
findings/           readable findings, one per source or question
leads/              things to follow that have not been run down yet
timeline/           timeline.md, regenerated from the material
entities/           register.jsonl — people, organisations, accounts
exports/            rendered reports, with their .typ sources
logs/               one log per operation
```

## Rules

1. **BOUNDARIES above are binding.** Work that crosses them is refused before it is
   started, not recorded and then footnoted. If a boundary is unclear, ask rather than
   interpret it generously.
2. **Observation, inference, and confidence are three separate fields.** What the
   material literally shows is recorded so a second person can confirm every word of it.
   What it is taken to mean is recorded separately, with reasoning.
3. **A live URL is not a record.** Preserve the material before relying on it. A source
   with no archived copy is recorded as unpreserved, which is a stated weakness.
4. **Contradictions are kept, not resolved by overwriting.** Where a new finding
   contradicts an earlier one, both stay on the record.
5. **Absence of a result is a finding.** Record what was searched and how, not only what
   was found.
6. **Public availability is not free use.** Note where material carries constraints.
7. **The entity register identifies within this matter only.** It is not a dossier and
   covers only what the scope reaches.

## Evidence

This workspace has no `evidence/` tree. Where a source needs hashing, timestamping, or a
custody record, the `evidence-ops` agent creates and owns that subtree. Read its
register; never write to it.

## Working here

- `osint-source` — record a finding with its provenance
- `track-entities` — maintain the entity register
- `build-timeline` — regenerate the chronology
- `generate-brief` — render an investigation report
- `matter-status` — what is unfinished and what needs checking
