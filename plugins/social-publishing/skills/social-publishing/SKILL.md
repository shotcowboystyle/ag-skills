---
name: social-publishing
description: >
  Validate, schedule and publish social media posts through the SocialClaw HTTP API
  (X, LinkedIn, Instagram, Facebook Pages, TikTok, Discord, Telegram, YouTube, Reddit,
  WordPress, Pinterest), then check their status and analytics. Use when the user wants to
  publish, schedule, or inspect social posts from a SocialClaw workspace. Requires
  SC_API_KEY.
license: MIT
last_verified: 2026-10-27
metadata:
  version: "2.0.0"
  source: https://github.com/ndesv21/socialclaw
  homepage: https://getsocialclaw.com
---

# Social Publishing

[SocialClaw](https://getsocialclaw.com) is a hosted publishing service: one workspace API
key, with social accounts connected inside the SocialClaw dashboard. This skill calls its
HTTP API with `curl`. Calls and field names follow upstream `skills/socialclaw` as of
2026-10 (package `socialclaw` 0.1.22).

## Setup

1. The user signs in at `https://getsocialclaw.com/dashboard` and creates a workspace API
   key. The workspace also needs an active trial or paid plan.
2. They export it: `export SC_API_KEY="<workspace-key>"`. Never echo the key back.
3. Validate it:

```bash
SC=https://getsocialclaw.com/v1
auth=(-H "Authorization: Bearer $SC_API_KEY")
curl -sS "${auth[@]}" "$SC/keys/validate"
```

If any call returns `plan_required` or `subscription_*`, stop and send the user to
`https://getsocialclaw.com/pricing`. Retrying will not help.

## Procedure

Each step uses the `SC` and `auth` variables from Setup.

1. **List accounts** and note each target's `handle` (such as `x:@name` or
   `pinterest:board:123`) and `provider`:

   ```bash
   curl -sS "${auth[@]}" "$SC/accounts"
   ```

   A missing account gets connected with `POST $SC/connections/start` and
   `{"provider":"<provider>"}`. The user finishes OAuth in the browser; poll
   `GET $SC/connections/<connection-id>` until it completes. Telegram (`botToken`, `chatId`)
   and Discord (`webhookUrl`) connect with those fields instead of OAuth. Never ask for
   provider app secrets.
2. **Check capabilities** for each target before drafting. Media limits and settings
   differ per account:

   ```bash
   curl -sS "${auth[@]}" "$SC/accounts/<account-id>/capabilities"
   ```

3. **Upload media** once and reuse the returned delivery URL in each post:

   ```bash
   curl -sS -X POST "${auth[@]}" -F "file=@./image.png" "$SC/assets/upload"
   ```

4. **Write `schedule.json`**, one entry per account, each with its own copy. `publishAt` is
   ISO 8601 UTC; for "post now", use 2 minutes ahead
   (`date -u -v+2M '+%Y-%m-%dT%H:%M:%S.000Z'` on macOS,
   `date -u -d '+2 minutes' '+%Y-%m-%dT%H:%M:%S.000Z'` on Linux).

   ```json
   {
     "posts": [
       {
         "account": "x:@example",
         "provider": "x",
         "description": "We shipped dark mode. Try it at example.com",
         "status": "scheduled",
         "publishAt": "2026-11-02T14:00:00.000Z",
         "assets": [{ "mediaLink": "<delivery URL from upload>" }]
       }
     ]
   }
   ```

5. **Validate**, and fix every error it returns before going on:

   ```bash
   curl -sS -X POST "${auth[@]}" -H "Content-Type: application/json" \
     -d @schedule.json "$SC/posts/validate"
   ```

6. **Confirm with the user**: show each account, its copy, media and time. Applying
   publishes publicly.
7. **Apply**, and keep the returned post and run IDs:

   ```bash
   curl -sS -X POST "${auth[@]}" -H "Content-Type: application/json" \
     -d @schedule.json "$SC/posts/apply"
   ```

8. **Check status** with `GET $SC/posts/<post-id>` and `GET $SC/runs/<run-id>`, or list
   recent posts with `GET "$SC/posts?limit=20"`. A provider status of `accepted` is not
   proof the post is visible; wait for `published`.

For multi-step campaigns, use a `campaigns` array (`name`, `mode: "draft"`, `targets[]`
with `account` and `steps[]`) and preview it with `POST $SC/campaigns/preview` before
applying.

## Provider rules

| Provider id | Rule |
|---|---|
| `x` | Up to four images or one video. |
| `linkedin`, `linkedin_page` | Profile and page are separate providers. Up to twenty images or one video. |
| `facebook` | Facebook Pages only, not personal profiles. |
| `instagram_business`, `instagram` | Business (linked to a Facebook Page) and standalone professional are separate. Media required. |
| `tiktok` | One video or one photo gallery (images only, up to 35, 1080x1920 JPEG is safest). Copy goes in `description`. A specific sound cannot be chosen; `settings.autoAddMusic: true` lets TikTok pick. |
| `youtube` | One video. Defaults to `privacyStatus: "private"`; set `"public"` when asked. No Shorts or community posts. |
| `reddit` | Needs `settings.subreddit`. No native media upload. |
| `pinterest` | Board-centric (`pinterest:board:<id>`). Product, collection and idea pins are beta unless the account's capabilities list them. |
| `telegram`, `discord` | One optional image or video. |
| `wordpress` | WordPress.com or Jetpack sites. |

When a platform does not support what the user wants, say so; do not invent a workaround.

## Analytics

Pull metrics 24–48 hours after publishing. These routes come from the upstream CLI source
(`src/index.mjs`); `window` defaults to `lifetime`:

```bash
curl -sS "${auth[@]}" "$SC/analytics/posts/<post-id>?window=lifetime"
curl -sS "${auth[@]}" "$SC/analytics/runs/<run-id>?window=lifetime"
```

The optional `socialclaw` CLI (`npm install -g socialclaw`) wraps the same API, for example
`socialclaw analytics post --post-id <id> --json`.
