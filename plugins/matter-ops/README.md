[Part of the shotcowboystyle marketplace](https://github.com/shotcowboystyle/ai-plugins)

## Matter Ops Plugin

**Version:** 0.1.0

Working a matter — the workspace it lives in, the documents and sources that feed it,
the entities and timeline that organise it, the redacted copies that leave it, and the
written output that closes it.

Pairs with [`evidence-ops`](https://github.com/shotcowboystyle/evidence-ops-plugin),
which owns evidence handling mechanics — hashing, the custody register, timestamping,
packaging, verification, and immutable storage. Each works on its own.

## The split

| | `matter-ops` | `evidence-ops` |
| --- | --- | --- |
| Owns | the matter | the evidence item |
| Writes | analyses, findings, timelines, briefs | hashes, custody records, proofs, bags |
| Reads the custody register | yes | yes |
| Writes the custody register | never | always |

When a matter needs custody handling, `evidence-ops:init-evidence-store` creates the
`evidence/` subtree inside the workspace this plugin provisioned. This plugin never
re-implements hashing.

## Installation

Part of the [ag-skills](../../README.md) marketplace. In Claude Code:

```bash
/plugin marketplace add shotcowboystyle/ag-skills
/plugin install matter-ops@claude-code-workflows
```

For Codex CLI, Cursor, OpenCode, Antigravity CLI, GitHub Copilot, and Pi, see
[docs/harnesses.md](../../docs/harnesses.md).

## Commands

- `/matter-ops:analyze <path> [--jurisdiction <j>] [--purpose <p>]` — Read a document and write a structured memo with citations to verify and open questions.
- `/matter-ops:brief <topic> [--type <t>] [--confidential <level>] [--out <path>]` — Draft and typeset a brief, memo, or report from workspace material.
- `/matter-ops:entities [name-or-query]` — Maintain the register of people, organisations, and accounts with aliases and relationships.
- `/matter-ops:new-matter <name> [--variant <v>] [--jurisdiction <j>] [--private] [--local-only]` — Provision a matter workspace from a variant template and record its defining facts.
- `/matter-ops:redact <path> [--mode alias|random|pattern] [--scrub-metadata]` — Apply user-directed redaction to documents, writing new files and logging every replacement.
- `/matter-ops:source <url-or-description>` — Record an open-source finding with its provenance, separating observation from inference.
- `/matter-ops:status` — Report what the workspace contains, what is unfinished, and what needs checking.
- `/matter-ops:timeline [--from <date>] [--to <date>]` — Assemble a dated chronology from workspace material, marking how firmly each date is established.

## Skills

- **new-matter** — Use when starting a legal matter, an open-source investigation, or a document review — provisions a workspace from a variant template, records the facts that define the matter so later work need not re-ask, and initialises version control
- **analyze-document** — Use when a document needs structured reading — extracts its text, works out the governing jurisdiction, and writes a memo separating what the document says from what it is taken to mean, with every uncertain citation flagged for checking
- **redact-content** — Use when material must leave the workspace with names or identifiers protected — applies user-directed redaction using a stable alias mapping, per-document random replacement, or declared patterns, always writing new files and never touching the input
- **osint-source** — Use when an open-source finding needs recording — captures what was observed, where it came from, and when, keeping the observation separate from the inference and checking the finding against the workspace scope before it is written
- **build-timeline** — Use when the sequence of events matters — assembles a dated timeline from analyses, source records, and the evidence register, marking each entry with how firmly its date is established
- **track-entities** — Use when people, organisations, or accounts recur across the material — maintains a register of entities with their aliases, identifiers, and relationships, and keeps it consistent with the redaction alias mapping
- **generate-brief** — Use when workspace material must become a document someone else reads — drafts in markdown from the analyses, sources, and register already on disk, then typesets it, keeping the source file beside the output so it can be re-rendered
- **matter-status** — Use when picking a matter back up or handing it over — reports what the workspace contains, what is unfinished, which citations remain unverified, and which material has been logged but never analysed

## Workspace variants

`new-matter` provisions from `skills/new-matter/assets/templates/<variant>/`. A provisioned workspace is **data**:
it contains no agent configuration, so updating this plugin can never change or break an
existing matter.

| Variant | For | Distinctive directories |
| --- | --- | --- |
| `legal-research` | a single legal matter | `context/`, `research/`, `case-file/` |
| `osint-investigation` | a scoped open-source investigation | `sources/`, `findings/`, `leads/`, `timeline/`, `entities/` |
| `document-analysis` | systematic review of a corpus | `input/`, `analyses/`, `aliases/`, `schemas/`, `output/` |

Each ships an `AGENTS.md` carrying a labelled fact block, and a `CLAUDE.md` pointing at
it. Facts are filled in at provisioning time so later work does not have to re-ask.

## Dependencies

| Tool | Purpose |
| --- | --- |
| `pdftotext`, `pdfinfo` | text extraction from PDFs |
| `libreoffice` | office document conversion |
| `typst` | typesetting briefs and reports |
| `exiftool`, `mat2` | metadata scrubbing on redacted outputs |
| `qpdf` | PDF structure work, and the full rewrite that makes an `exiftool` PDF scrub irreversible |
| `git`, `gh` | workspace version control and optional publishing |

None is required to provision a workspace. Each skill reports what it cannot do rather
than failing silently.

## Conventions

- **Observation is separated from inference.** Every memo, finding, and report keeps what
  was read apart from what it is taken to mean.
- **Citations are never invented.** Anything unconfirmed is marked `[verify]` and
  collected in its own section. That section is never quietly dropped.
- **Inputs are read-only.** Analysis, redaction, and extraction all write new files.
- **Redaction is directed by a person.** Pattern matching assists; it never decides. The
  output always states what it did not reach.
- **Scope boundaries are enforced.** An investigation workspace declares what is out of
  bounds, and work that crosses it is refused, not footnoted.
- **Analysis is labelled preliminary** unless the workspace explicitly suppresses it for
  internal professional use.
- **Nothing is published without an explicit yes.** Repository creation defaults to
  private and is always confirmed.

## Disclaimer

This plugin is a workflow aid, not legal advice. Nothing it produces is a legal opinion,
and no output should be relied on without review by a qualified professional in the
relevant jurisdiction.

## Author

Curtis Blanton — [shotcowboystyle.com](https://shotcowboystyle.com)

## License

MIT
