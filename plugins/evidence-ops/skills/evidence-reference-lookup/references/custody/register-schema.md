# Custody Register Schema

The custody register is `evidence/register.jsonl`: one JSON object per line, appended and
never rewritten. log-custody writes it, verify-bundle reads it, and init-evidence-store
creates it empty. This file is the single definition of a record.

## Store root

Every path in a record is relative to the **store root** — the directory that contains
`evidence/`. A record never holds an absolute path, so the store stays valid when it is
moved or restored as a unit. To re-hash an item, resolve `<store root>/<stored_path>`.

## Record ids

`EV-` followed by the 1-based line number of the record, zero-padded to six digits:
`EV-000001`, `EV-000002`, and so on. The next id is the current line count plus one:

```bash
printf 'EV-%06d\n' "$(( $(wc -l < evidence/register.jsonl) + 1 ))"
```

Ids are never reused. A correction gets its own new id.

## Fields

| Field | Required | Value |
| --- | --- | --- |
| `schema` | yes | `1` |
| `id` | yes | Record id, as above. |
| `kind` | yes | `acquisition` for an item entering the collection, `transfer` for a custody transfer, `handover` for a bag handed to another party. |
| `logged_at` | yes | UTC time of logging, `YYYY-MM-DDTHH:MM:SSZ`. |
| `handler` | yes | Who wrote this record. |
| `stored_path` | `acquisition` | Path of the stored original relative to the store root, for example `evidence/originals/20261027-photo_1.jpg`. This is the path verify-bundle re-hashes. |
| `original_name` | `acquisition` | The file name as received, verbatim. |
| `sha256` | `acquisition`, `handover` | Lowercase hex digest, 64 characters. For a handover, the digest of the bag's `tagmanifest-sha256.txt`. |
| `blake3` | no | Lowercase hex digest, when `evidence/POLICY.md` lists BLAKE3. |
| `size_bytes` | `acquisition` | Integer. |
| `mime_type` | `acquisition` | As reported by `file --mime-type -b`. |
| `source` | `acquisition` | Who or what produced the item and how it reached the collection. |
| `custody_notes` | yes | Acquisition or transfer path, including any gap in the chain. |
| `confidentiality` | yes | Handling level. |
| `bag_path` | `handover` | Bag directory relative to the store root. |
| `recipient` | `transfer`, `handover` | Who received custody. |
| `subject` | `transfer` | Id of the `acquisition` record whose custody moved. |
| `metadata_summary` | no | One line carried over from metadata inspection. |
| `anomalies` | no | Array of anomaly flags from metadata inspection. |
| `supersedes` | no | Id of the record this one corrects. `null` or absent otherwise. |

## Corrections

A correction is a complete replacement record of the same `kind`, with `supersedes`
naming the record it replaces. The earlier line stays in the register untouched. A
record is **current** when no later record supersedes it. Verification checks current
records only, and reports superseded ones by id so the history stays visible.

## Derived paths

Paths that follow from `stored_path` are not stored, because the record cannot be
updated once written:

- OpenTimestamps proof: `chain-of-custody/<basename of stored_path>.ots`.

## Example

```json
{"schema":1,"id":"EV-000001","kind":"acquisition","logged_at":"2026-10-27T14:03:11Z","handler":"A. Analyst","stored_path":"evidence/originals/20261027-photo_1.jpg","original_name":"photo (1).jpg","sha256":"9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08","size_bytes":482113,"mime_type":"image/jpeg","source":"Emailed by witness, original attachment","custody_notes":"Saved from mail client to workstation, then logged","confidentiality":"restricted","supersedes":null}
```

Build each record with a JSON encoder rather than by string concatenation, so quotes and
newlines in free-text fields are escaped. A record must fit on one line.

## See also

- [Chain of Custody Principles](chain-of-custody-principles.md)
- [Algorithms and Manifests](../hashing/algorithms-and-manifests.md)
