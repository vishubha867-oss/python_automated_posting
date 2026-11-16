# Automated Multi-Platform Posting System

FastAPI service that validates a short marketing message (with **exactly one** CTA URL) and publishes it to **five** third-party platforms via their official APIs. Each platform is handled independently; one failure does not stop the others.

## Platforms integrated

| Platform | API | Credentials (`.env`) |
|----------|-----|----------------------|
| **Discord** | [Webhooks](https://discord.com/developers/docs/resources/webhook) | `DISCORD_WEBHOOK_URL` |
| **Telegram** | [Bot API](https://core.telegram.org/bots/api#sendmessage) | `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` |
| **Slack** | [Incoming Webhooks](https://api.slack.com/messaging/webhooks) | `SLACK_WEBHOOK_URL` |
| **Bluesky** | [AT Protocol](https://docs.bsky.app/docs/get-started) | `BLUESKY_HANDLE`, `BLUESKY_APP_PASSWORD` |
| **Ntfy** | [ntfy.sh publish](https://docs.ntfy.sh/publish/) | `NTFY_TOPIC` |

## Project structure

```text
automated-posting/
├── app/
│   ├── main.py
│   ├── schemas.py
│   ├── config.py
│   ├── platforms/
│   │   ├── base.py
│   │   ├── discord.py
│   │   ├── telegram.py
│   │   ├── slack.py
│   │   ├── bluesky.py
│   │   └── ntfy.py
│   └── services/
│       └── posting_service.py
├── tests/
│   └── test_posting.py
├── scripts/
│   ├── run_live_demo.py
│   └── export_openapi.py
├── docs/
│   ├── SETUP.md
│   ├── PLATFORMS.md
│   ├── SUBMISSION.md
│   ├── openapi.json
│   ├── logs/
│   └── screenshots/
├── .env.example
├── requirements.txt
└── README.md
```

## Setup

### 1. Clone and virtual environment

```bash
cd automated-posting
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment variables

```bash
cp .env.example .env
# Edit .env and add your credentials (never commit .env)
```

**Step-by-step credential setup for all five platforms:** [docs/SETUP.md](docs/SETUP.md)

Quick map:

| Platform | Main `.env` keys |
|----------|------------------|
| Discord | `DISCORD_WEBHOOK_URL` |
| Telegram | `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` |
| Slack | `SLACK_WEBHOOK_URL` |
| Bluesky | `BLUESKY_HANDLE`, `BLUESKY_APP_PASSWORD` |
| Ntfy | `NTFY_TOPIC` |

### 3. Run the server

```bash
uvicorn app.main:app --host 0.0.0.0 --port 4000
```

Open interactive docs: [http://localhost:4000/docs](http://localhost:4000/docs)

## API

### `POST /posting`

**Request:**

```json
{
  "message": "Check out our latest business platform and grow your online visibility. https://example.com"
}
```

**Validation:**

- `message` ≤ 200 characters (after strip)
- Exactly **one** `http://` or `https://` URL (CTA)
- URL must be syntactically valid

**Example success response:**

```json
{
  "success": true,
  "results": [
    {
      "platform": "Bluesky",
      "status": "success",
      "posted_url": "https://bsky.app/profile/you.bsky.social/post/3kx...",
      "public_access": true,
      "date": "2026-11-16",
      "time": "05:42:00",
      "error": null
    },
    {
      "platform": "Discord",
      "status": "failed",
      "posted_url": null,
      "public_access": false,
      "date": null,
      "time": null,
      "error": "Discord is not configured. Set the required environment variables (see .env.example)."
    }
  ]
}
```

`success` is `true` if **at least one** platform posted successfully.

### Sample `curl`

```bash
curl -s -X POST http://localhost:4000/posting \
  -H "Content-Type: application/json" \
  -d '{"message": "Check out our latest business platform and grow your online visibility. https://example.com"}' | jq
```

## Tests

```bash
pytest -v
```

Live social API test (optional, needs `.env` + network):

```bash
RUN_INTEGRATION=1 pytest -v -m integration
```

## Demo scripts

```bash
python scripts/export_openapi.py   # writes docs/openapi.json
python scripts/run_live_demo.py    # live post attempt; writes docs/logs/*
```

All five platforms need credentials in `.env` for successful posts (see `.env.example`).

## Screenshots / logs for submission

Pre-generated logs (re-run `scripts/run_live_demo.py` to refresh):

- `docs/logs/demo-response.json`
- `docs/logs/demo-run.log`

Manual screenshots → `docs/screenshots/` (see `docs/screenshots/README.md`).

Full checklist and email template: [docs/SUBMISSION.md](docs/SUBMISSION.md).

## Security

- Do **not** commit `.env` or real tokens (`.gitignore` excludes `.env`).
- Use `.env.example` only for variable names.

## License

MIT — for practical test submission.# python_automated_posting

<!-- Last updated: Monday, Nov 16, 2026, 04:23 PM (UTC+5:30) -->
