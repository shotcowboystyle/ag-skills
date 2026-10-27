---
name: timestamp-evidence
description: Use when a file's existence at a point in time needs to be provable independently of the filesystem — anchors its hash with OpenTimestamps and stores the proof alongside the custody record. Triggers - "timestamp this evidence", "prove this existed today", "opentimestamps this file".
allowed-tools: Bash(ots *), Bash(export PATH=*), Bash(command *), Bash(shasum *), Bash(mv *), Bash(basename *), Bash(mkdir *), Bash(date *), Read, Write
---

# Timestamp Evidence

Anchor a file's hash so its existence at a point in time can be shown without relying
on the filesystem, the operating system clock, or anyone's word.

## When to use

- Immediately after an item is logged, while the acquisition is fresh.
- Before handing a bundle to another party.
- Verifying or completing a proof taken earlier.

## Inputs

- Path to a file, or to an existing `.ots` proof. Required.
- `--verify` — check an existing proof instead of creating one.
- `--upgrade` — complete a pending proof once its attestation has landed.

## Procedure

`ots` lives in the plugin virtual environment. Start every command that calls it with
the line from [tool resolution](../evidence-install-deps/references/tool-resolution.md).

There is one proof per item, and it lives at
`chain-of-custody/<basename of the item>.ots`, the path the
[register schema](../evidence-reference-lookup/references/custody/register-schema.md)
derives from the record. Every later step works on that filed copy, never on a copy
left beside the item.

### 1. Create and file the proof

```bash
ots stamp "$TARGET"
mkdir -p chain-of-custody
mv "$TARGET.ots" "chain-of-custody/$(basename "$TARGET").ots"
```

`ots stamp` writes `$TARGET.ots` next to the file; moving it straight away leaves a
single proof to upgrade. The proof commits to the file's hash, not to its contents, so
the file itself is never uploaded anywhere. If a proof already exists at the filed path,
stop and report it rather than replace it.

### 2. Explain the wait

A fresh proof is *incomplete*. It records a commitment to a calendar server and only
becomes independently verifiable once the Bitcoin attestation confirms, which takes
hours rather than minutes. Say this plainly at creation time — a proof that has not
been upgraded cannot be verified, and that is expected, not an error.

### 3. Upgrade later

```bash
ots upgrade "$PROOF"
```

`$PROOF` is the filed copy under `chain-of-custody/`. Run this once the attestation has
had time to land. On success the proof becomes self-contained and no longer depends on
the calendar server being reachable. Check the result with `ots info "$PROOF"`, which
needs no Bitcoin node and shows whether a Bitcoin attestation is present.

### 4. Verify

```bash
ots verify -f "$TARGET" "$PROOF"
```

Verification checks the Bitcoin attestation against a local Bitcoin Core node (a pruned
node is enough, reached over RPC; `--bitcoin-node` points at a non-default one). Without
a node it cannot complete. Report that as "not checked: no Bitcoin node", not as a pass
and not as a failure, and say that an upgraded proof can be verified later on any machine
that has a node.

When it does verify, report the attested time exactly as the tool gives it, and state
clearly what it means: the file existed in this form no later than that time. It does
not establish when the file was created, who made it, or that its contents are true.

## Output

- One `.ots` proof under `chain-of-custody/`, upgraded in place once it completes.
- For a verification, the attested time and an explicit statement of what it proves, or
  the reason it could not be checked.

## Notes

- Only the hash leaves the machine. The file's contents are never transmitted.
- A proof is bound to exact bytes. Re-encoding, re-saving, or stripping metadata from
  the file invalidates it — timestamp the original, never a derived copy.
- Timestamping is not signing. It says when, not who. Pair it with a signature if
  authorship needs to be shown.
