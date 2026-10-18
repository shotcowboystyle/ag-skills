---
description: Show where this trip stands — validation, reconciliation and what to do next
---

# Status

`$TPA` below is this plugin's `new-workspace` skill directory — the folder holding its `SKILL.md`,
`scripts/`, `schema/`, `typst/` and `template/`. Find it by name in your tool's skills folder (some
tools prefix it, e.g. `travel-packing-assistant__new-workspace`) and set `TPA` once per session.

Where this trip stands, in one screen.

Read whichever of `itinerary.yaml`, `allowances.yaml`, `bags.yaml`, `inventory.yaml` and
`plan.yaml` exist in the current workspace, then run:

```bash
python3 $TPA/scripts/validate.py . --json
python3 $TPA/scripts/reconcile.py . --json
```

Report, in this order:

1. Days to departure, and any deadline from `overage.md` that has not passed.
2. Binding limits, and how many allowance figures are not `confirmed`.
3. Per bag: projected or measured gross, allowance, headroom, status.
4. What is missing — the next unrun step in
   `itinerary → policies → inventory → weigh → plan → docs`.

Arithmetic first, interpretation second. Do not change any file.
