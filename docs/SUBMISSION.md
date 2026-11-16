# Submission checklist (no secrets in repo)

Use this before the **22 November 2026** deadline. Git steps are optional until you are ready to publish.

## Platform credentials

Configure every integration using [SETUP.md](SETUP.md) before demoing live posts.

## Local verification

```bash
source .venv/bin/activate
pip install -r requirements.txt
pytest -v
python scripts/export_openapi.py
python scripts/run_live_demo.py    # needs network + .env for successful posts
uvicorn app.main:app --host 0.0.0.0 --port 4000
```

Artifacts for reviewers (generated locally):

| File | Purpose |
|------|---------|
| `docs/logs/demo-response.json` | Sample API result after live run |
| `docs/logs/demo-run.log` | Human-readable posting log |
| `docs/openapi.json` | Exported OpenAPI schema |

## Screenshots (capture manually)

Save PNG files under `docs/screenshots/`:

1. Browser: `http://localhost:4000/docs` with **POST /posting** visible.
2. Terminal: `uvicorn` listening on port `4000`.
3. `curl` or Swagger **Execute** showing JSON with at least one `"status": "success"`.
4. Optional: open a Bluesky post or ntfy topic from `posted_url`.

## Email template

**To:** hr@chivoxai.com  
**Subject:** Your Name - Python Practical test review

```text
1. Your Full Name:
2. GitHub Repository Link:
3. Contact Number:
4. Current Location:
5. Best Time to Discuss:
```

Replace placeholders and attach or mention the public repo link once uploaded.

<!-- Last updated: Monday, Nov 16, 2026, 04:23 PM (UTC+5:30) -->
