---
name: analyze-document
description: Use when a document needs structured reading — extracts its text, works out the governing jurisdiction, and writes a memo separating what the document says from what it is taken to mean, with every uncertain citation flagged for checking. Triggers - "analyse this contract", "review this filing", "what does this document establish".
allowed-tools: Bash(pdftotext *), Bash(pdfinfo *), Bash(libreoffice *), Bash(file *), Bash(command *), Bash(mkdir *), Bash(wc *), Read, Write
---

# Analyze Document

Read a document closely and write a memo that separates what it says from what it is
taken to mean.

## When to use

- A contract, filing, report, or item of correspondence needs structured reading.
- A document's significance to the matter has to be recorded before it is cited.

## Inputs

- Path to the document. Required.
- `--jurisdiction <code>` — override the workspace default for this analysis.
- `--purpose <contract-review|filing-review|correspondence|disclosure|osint-source>` —
  shapes the memo's emphasis.

## Procedure

### 1. Extract the text

```bash
file --mime-type -b "$DOC"
pdftotext -layout "$DOC" -          # PDFs; -layout preserves columns and tables
pdfinfo "$DOC"                      # page count, producer, embedded dates
libreoffice --headless --convert-to txt --outdir "$TMP" "$DOC"   # office formats
```

If `pdftotext` returns little or nothing, the PDF is probably scanned images. Say so and
stop — optical character recognition is out of scope unless the workspace has enabled
it. Do not analyse a document whose text could not be read.

### 2. Establish the governing jurisdiction

Take it from the flag, then the workspace fact block, then ask. Never assume one from
the document's language or apparent origin.

### 3. Read for the record

Work through the document and note, with page or section references:

- Defined terms and where they are defined.
- Dates, deadlines, and any period that runs from an event.
- Money, quantities, and how they are calculated.
- Obligations, and which party bears each.
- Conditions, exclusions, and anything that survives termination.

### 4. Write the memo

Sections, adapted in emphasis but not in order:

1. **Document identity** — title, author, date, parties, page count, format.
2. **What it says** — the terms and facts above, cited to their location. Description
   only; no interpretation in this section.
3. **What it establishes or undermines** — the inference, stated as inference, with the
   material from section 2 it rests on.
4. **Citations to verify** — every statute, case, regulation, or external fact relied
   on. Anything not confirmed is marked `[verify]` here and nowhere else. Never smooth an
   unchecked citation into a confident one.
5. **Open questions** — what a qualified professional should confirm.
6. **Risk flags** — limitation periods, privilege, confidentiality, disclosure exposure.

### 5. Save it

- `legal-research` → `research/<slug>-analysis.md`
- `document-analysis` → `analyses/<slug>.md`
- `osint-investigation` → `findings/<slug>.md`

Carry the workspace confidentiality level into the memo header.

## Output

- One memo at the variant's path.
- A short summary naming the risk flags and the count of citations to verify.

## Notes

- Every memo carries a visible line stating it is preliminary analysis and not legal
  advice, unless the workspace explicitly suppresses it for internal professional use.
- The source document is never modified.
- A memo about a document is not evidence of the document. If the document itself
  matters, register it with the companion evidence agent.
