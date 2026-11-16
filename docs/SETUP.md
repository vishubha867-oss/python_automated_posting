# Easy platform setup (5 integrations)

Text-only posts. See [PLATFORMS.md](PLATFORMS.md) for API notes.

```bash
cp .env.example .env
```

---

## 1. Discord (~2 min)

Server → **Integrations** → **Webhooks** → copy URL → `DISCORD_WEBHOOK_URL`

---

## 2. Telegram (~5 min)

[@BotFather](https://t.me/BotFather) → `/newbot` → `TELEGRAM_BOT_TOKEN`  
Add bot to channel → `TELEGRAM_CHAT_ID`

---

## 3. Slack (~5 min)

[Incoming Webhooks](https://api.slack.com/messaging/webhooks) → `SLACK_WEBHOOK_URL`

---

## 4. Bluesky (~3 min)

1. Account on [bsky.app](https://bsky.app)
2. **Settings** → **Privacy and security** → **App passwords** → **Add App Password**
3. Name it (e.g. `automated-posting`) and copy the password (shown once)
4. `.env`:

```env
BLUESKY_SERVICE_URL=https://bsky.social
BLUESKY_HANDLE=yourname.bsky.social
BLUESKY_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx
```

Use your full handle (`user.bsky.social` or custom domain). **Do not** use your main account password.

---

## 5. ntfy (~1 min)

1. Pick a unique `NTFY_TOPIC` (e.g. `yourname-posting-xyz`)
2. Test: `curl -d "hello" https://ntfy.sh/your-topic`

---

## Run

```bash
uvicorn app.main:app --host 0.0.0.0 --port 4000
```

```bash
curl -s -X POST http://localhost:4000/posting \
  -H "Content-Type: application/json" \
  -d '{"message": "Check out our latest business platform and grow your online visibility. https://example.com"}'
```

<!-- Last updated: Monday, Nov 16, 2026, 04:23 PM (UTC+5:30) -->
