---
name: setup-storage
description: Use when configuring where evidence is replicated — walks through defining a storage remote, confirms its retention or write-once behaviour, and records the destination policy without ever touching credentials. Triggers - "set up evidence storage", "configure the rclone remote", "where should evidence be backed up".
allowed-tools: Bash(rclone *), Bash(aws *), Bash(command *), Bash(mkdir *), Read, Write
---

# Set Up Storage

Define where verified evidence is replicated, and confirm that the destination actually
resists rewriting before anything is trusted to it.

## When to use

- During onboarding, once the local pipeline works.
- Adding a second, independent destination.
- Auditing whether an existing destination really is immutable.

## Procedure

### 1. Choose the protection model

Ask which of these applies, because they fail differently:

- **Object storage with a retention lock** — S3 Object Lock or an equivalent. Objects
  cannot be deleted or overwritten until their retention expires. Requires versioning
  on the bucket. Since November 2023 S3 can enable Object Lock on an existing bucket, so
  a new bucket is not required; objects already in it are not locked until a retention
  is set on each.
- **Append-only or immutable-tier storage** — provider-enforced, no client cooperation
  needed.
- **Physical write-once media** — an optical disc or a WORM cartridge. Immutable by
  construction, offline by default, and slow to recover from.
- **An ordinary remote** — no protection at all. Usable as a second copy, but must not
  be described as immutable.

Be direct if the chosen destination provides no protection. An ordinary bucket with
careful habits is not immutable storage.

### 2. Define the remote

Create the remote non-interactively, with credentials taken from the environment or the
AWS credential chain rather than stored in the remote:

```bash
rclone config create "$REMOTE" s3 provider=AWS env_auth=true region="$REGION" --non-interactive
rclone listremotes
```

Do not run bare `rclone config`: it is an interactive wizard that prompts for access
keys. Never ask for a secret in conversation, never echo one, and never write one into
the workspace. If no credentials are available in the environment, stop and tell the
user to set them up themselves (for example `aws configure` in their own terminal).

### 3. Confirm the bucket's actual settings

```bash
aws s3api get-bucket-versioning --bucket "$BUCKET"
aws s3api get-object-lock-configuration --bucket "$BUCKET"
```

Report what these return rather than what was intended. An empty or missing
Object Lock configuration means no lock, whatever the bucket was meant to have. Object
Lock can be enabled on an existing bucket (versioning must be on first), but that is a
change to the user's storage: state it and get agreement before running
`put-object-lock-configuration`. Check, do not assume.

Note which retention mode is configured. Governance mode can be bypassed by a
sufficiently privileged user; compliance mode cannot be bypassed by anyone, including
the account root, until retention expires. That difference is the whole point, and it
is also irreversible — say so before anyone chooses compliance mode.

### 4. Test with a throwaway object

Write a small file with an explicit **governance-mode** retention of one day, read it
back, then attempt to delete that object version. Under a working lock the delete must
fail. If it succeeds, the destination is not immutable, whatever the configuration
claims.

```bash
aws s3api put-object --bucket "$BUCKET" --key "_lock-test/$STAMP" --body "$TEST_FILE" \
  --object-lock-mode GOVERNANCE --object-lock-retain-until-date "$TOMORROW"
aws s3api delete-object --bucket "$BUCKET" --key "_lock-test/$STAMP" --version-id "$VERSION_ID"
```

Never test with compliance mode or a long retention: a compliance-mode test object
cannot be deleted by anyone until it expires, and it is billed until then. The governance
test object expires after a day; deleting it sooner needs
`--bypass-governance-retention` and the matching permission. An explicit retention on
the object overrides the bucket's default, so this tests the lock mechanism without
leaving an undeletable object.

### 5. Record the policy

Write the destination, protection model, retention period, and the date of this test
into `evidence/POLICY.md` under `STORAGE_REMOTE`. Record the test result, not the
intention.

## Output

- A configured remote and a recorded destination policy.
- The result of an actual immutability test.

## Notes

- A retention lock protects against deletion, not against a bad object being written in
  the first place. Verify before syncing, not after.
- Retention periods cost money for their whole duration. State that before a long
  period is set.
- One copy in one region is not a backup. Prefer two destinations with different
  failure modes.
