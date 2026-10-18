# Document Analysis Workspace

Systematic review of a document corpus: reading each document to the same shape, and
producing disclosure-safe copies where they are needed.

## Facts

Filled in when this workspace was provisioned. Read these rather than asking again.

- CORPUS:
- JURISDICTION:
- CONFIDENTIALITY:
- SUPPRESS_DISCLAIMER: false

## Layout

```
context/            the review brief, what is being looked for
input/              the corpus as received — read-only
analyses/           one memo per document, same structure throughout
aliases/            active_mapping.json — real value to pseudonym, sensitive
schemas/            patterns.json — declared redaction patterns
output/             redacted copies
exports/            rendered document reviews, with their .typ sources
logs/               one log per operation, including redaction logs
```

## Rules

1. **`input/` is read-only.** Every operation writes elsewhere.
2. **Every document gets the same memo shape**, so the corpus can be read across rather
   than one document at a time.
3. **The alias mapping is more sensitive than the documents.** It unmasks all of them.
   Never commit it to a public remote, and say so before any remote is added.
4. **Redaction is directed by a person.** Patterns assist; they never decide. Every run
   states what it did not reach — images, scanned pages, embedded attachments, metadata.
5. **Text-layer redaction is not visual redaction.** Where irreversible removal is
   required, the output says plainly that this workspace did not produce it.
6. **Consistency across documents is deliberate.** In alias mode the same real name is
   always the same pseudonym. In random mode it never is. Choosing between them is a
   decision about linkability, and it is recorded.

## Evidence

This workspace has no `evidence/` tree. Where a document is itself evidence and needs
hashing or a custody record, the `evidence-ops` agent creates and owns that subtree.

## Working here

- `analyze-document` — read a document, write a memo to `analyses/`
- `redact-content` — produce disclosure-safe copies into `output/`
- `track-entities` — keep names consistent with the alias mapping
- `generate-brief` — render a document review
- `matter-status` — what is unanalysed and what needs checking
