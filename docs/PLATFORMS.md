# Platform API research notes

## 1. Discord — Webhook

- https://discord.com/developers/docs/resources/webhook#execute-webhook

## 2. Telegram — Bot API

- https://core.telegram.org/bots/api#sendmessage

## 3. Slack — Incoming Webhook

- https://api.slack.com/messaging/webhooks

## 4. Bluesky — AT Protocol

- **Session:** `POST /xrpc/com.atproto.server.createSession` with handle + app password
- **Post:** `POST /xrpc/com.atproto.repo.createRecord` (`app.bsky.feed.post`)
- **Auth:** App password from Bluesky settings (not main password)
- **Docs:** https://docs.bsky.app/docs/get-started

## 5. ntfy

- https://docs.ntfy.sh/publish/

<!-- Last updated: Monday, Nov 16, 2026, 04:23 PM (UTC+5:30) -->
