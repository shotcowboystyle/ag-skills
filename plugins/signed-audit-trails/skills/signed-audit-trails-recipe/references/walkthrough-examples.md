# Walkthrough examples for the signed audit trail recipe

Examples behind Steps 3 and 6 of `SKILL.md`.

## Step 3: a sample session

Every tool call goes through both hooks:

```
You: Please read the README and summarize it.

Claude: I will read README.md.
  [PreToolUse: Read ./README.md -> allow]
  [Tool: Read executes]
  [PostToolUse: receipt rcpt-a8f3c9d2 signed to ./receipts/]

... summary of README ...
```

## Step 6: tamper script

Change the newest receipt's `decision` from `allow` to `deny`, then verify:

```bash
python3 -c "
import json
path = './receipts/receipts.jsonl'
lines = open(path).read().splitlines()
r = json.loads(lines[-1])
r['payload']['decision'] = 'deny'
lines[-1] = json.dumps(r)
open(path, 'w').write('\n'.join(lines) + '\n')
"

npx @veritasacta/verify@0.9.2 --replay-chain ./receipts/receipts.jsonl --key "$PUB"
```
