---
name: new-workspace
description: Provision a new trip packing workspace on disk. Use when the user is starting to plan the packing for a specific itinerary — a named route, a set of flights, a trip with a departure date. Scaffolds the workspace files (itinerary.yaml, bags.yaml, inventory.yaml, AGENTS.md), personalises them from the user's global memory, and initialises a local git repo. Creates a private GitHub repo only with `--github`, after confirming.
disable-model-invocation: true
allowed-tools: Bash(mkdir *), Bash(cp *), Bash(ls *), Bash(git init *), Bash(git add *), Bash(git commit *), Bash(git push *), Bash(gh repo create *), Bash(gh auth status), Read, Write, Edit
---

# Provision a Trip Packing Workspace

One workspace per itinerary. The plugin's commands are global once installed; this skill
only creates the **data scaffold** those commands read from and write to.

Separate workspaces per trip is not bureaucracy — allowances, bag tares and the pack that
actually worked are all facts about *that journey*, and a workspace that accumulates several
trips loses the ability to say what a bag weighed leaving home.

## Arguments

`$ARGUMENTS` is parsed as:

- **First positional**: trip name, kebab-case, used as the directory and repo name. Prefer
  a route-and-date form: `bos-ath-tlv-0826`, `tlv-lhr-nov26`. Required.
- **Second positional** (optional): target parent path. Defaults to the current working
  directory. If the user's global context file names a trips folder, offer it, but do not
  use it without a yes.
- **`--github`**: also create a private GitHub repo and push to it, after confirming. Off by
  default. A packing workspace names the dates a home is empty and lists what is worth
  stealing from it, so it stays on this machine unless the user asks otherwise.
- **`--public`**: with `--github`, make the repo public. Warn that this publishes the
  travel dates, and confirm separately.

```
/travel-packing-assistant:new-trip bos-ath-tlv-0826
/travel-packing-assistant:new-trip tlv-lhr-nov26 ~/trips
/travel-packing-assistant:new-trip quick-hop --github
```

## Procedure

### 1. Resolve the scaffold

It lives at `template/trip/` inside this skill's directory. Confirm it exists before doing anything
that touches the filesystem.

### 2. Read ambient facts

Read the user's global agent context file if present (`~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`, `~/.config/opencode/AGENTS.md`, or your tool's equivalent). Extract home city/airport, currency, locale, units and
the user's name. These go into the workspace AGENTS.md so the later skills do not re-ask.

### 3. Create the workspace

```bash
mkdir -p <target-parent>/<trip-name>
cp -r <this-skill-dir>/template/trip/. <target-parent>/<trip-name>/
```


### 4. Personalise

In the new `AGENTS.md`, replace `{{TRIP_NAME}}`, `{{CREATED_ON}}` (absolute date) and the
ambient facts block. In `itinerary.yaml`, set `trip.id` to the trip name and leave the rest as
the commented skeleton — `/travel-packing-assistant:itinerary` fills it in.

### 5. Ask only what cannot be inferred

Two questions, together, then stop:

1. Where are you flying, and when? (one line is enough — the itinerary skill does the detail)
2. How many people are you packing for?

Write the answers into `AGENTS.md` under "Trip" and into `itinerary.trip`.

Do **not** start researching allowances here. That is `/travel-packing-assistant:policies`, and it needs
the full segment list first.

### 6. Git

Always commit locally:

```bash
git init && git add -A && git commit -m "Initialise trip packing workspace: <trip-name>"
```

Only with `--github`: check `gh auth status`, then show the repo name and visibility and confirm
with the user before creating it. Pushing sends the trip dates to GitHub.

```bash
gh repo create <trip-name> --private --source=. --push
```

If `gh auth status` fails or the user says no, keep the local commit, say no remote was
created, and carry on. A missing remote is not a reason to leave the workspace unbuilt.

### 7. Hand off

Tell the user the path, and that the next step is `/travel-packing-assistant:itinerary` to enter the
flights. Name the sequence so they know where they are:

```
itinerary → policies → inventory → weigh → plan → docs
                                      ↑        ↓
                                      └── overage / leave-behind if over
```
