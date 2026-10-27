---
name: hash-evidence
description: Use when a file or directory needs cryptographic hashes — computes SHA-256 by default and optionally BLAKE3, emitting a checkable manifest for directories. Triggers - "hash this file", "sha256 a folder", "make a checksum manifest".
allowed-tools: Bash(shasum *), Bash(sha256sum *), Bash(b3sum *), Bash(command *), Bash(find *), Bash(sort *), Bash(xargs *), Bash(cd *), Bash(mktemp *), Bash(test *), Bash(wc *), Bash(du *), Read, Write
---

# Hash Evidence

Compute cryptographic hashes for a file or a whole tree, and write a manifest that can
be checked later by anyone, with or without this plugin.

## When to use

- Baselining an item at the moment of acquisition.
- Producing a manifest for a batch before packaging or handover.
- Adding a second algorithm to items already recorded under SHA-256 alone.

Hashing alone establishes integrity, not custody. Pair it with log-custody.

## Inputs

- Path to a file or directory. Required.
- `--blake3` — also compute BLAKE3. Optional.
- `--out <path>` — manifest destination. Defaults to `manifests/<name>-<date>.sha256`.

## Procedure

### 1. Pick the hashing binary

macOS has no `sha256sum`. Resolve once, then reuse:

```bash
if command -v shasum >/dev/null 2>&1; then
  SHA256="shasum -a 256"
elif command -v sha256sum >/dev/null 2>&1; then
  SHA256="sha256sum"
else
  echo "no SHA-256 tool available" >&2
fi
```

Both write `<hash>  <path>`, so a manifest from one is checkable by the other.

### 2. Hash a single file

```bash
shasum -a 256 "$TARGET"
```

Report the digest in full. Never abbreviate a hash that is the point of the operation.

### 3. Hash a directory

Refuse to overwrite: if `$MANIFEST` already exists, stop and pick a new name. Then take
the file list once, from inside the target, before any manifest is written:

```bash
test -e "$MANIFEST" && echo "manifest already exists"
LIST=$(mktemp)
(cd "$TARGET" && find . -type f -print0 | sort -z) > "$LIST"
(cd "$TARGET" && xargs -0 shasum -a 256 < "$LIST") > "$MANIFEST"
```

Hashing from inside the target writes entries as `./sub/file`, relative to the hashed
directory. Because the list is taken before `$MANIFEST` exists, a manifest written into
the tree it describes never lists itself.

`sort -z` matters: without it the manifest order depends on filesystem traversal and
two runs over identical content produce different files. Sorted output diffs cleanly.

For BLAKE3, run `b3sum` over the same `$LIST` and write a sibling `.blake3` manifest, so
neither manifest lists the other. Do not interleave algorithms in one file — checkers
expect one algorithm per manifest.

### 4. Record scale

```bash
wc -l < "$MANIFEST"     # entries
du -sh "$TARGET"        # total size
```

Warn before starting if the tree is large enough that hashing will take minutes.

### 5. Report

State the digest or the manifest path, the directory that was hashed (checks run from
there), the entry count, and the total size. If any file
could not be read, name it — a manifest with silent gaps is worse than no manifest.

## Output

- For a file: digests printed, nothing written.
- For a directory: a manifest at the resolved path, plus a `.blake3` sibling if asked.

## Notes

- This skill only produces hashes. Checking them is verify-bundle's job.
- Manifest paths are relative to the directory that was hashed, so the manifest stays
  valid if the tree is moved as a unit.
- A hash proves the bytes have not changed since it was taken. It says nothing about
  where the bytes came from or whether they were authentic when acquired.
