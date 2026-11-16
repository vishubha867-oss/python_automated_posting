from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.schemas import PlatformResult, PostingResponse

client = TestClient(app)

VALID_MESSAGE = (
    "Check out our latest business platform and grow your online visibility. "
    "https://example.com"
)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_root_lists_docs():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data.get("docs") == "/docs"
    assert "POST /posting" in data.get("posting", "")


def test_posting_rejects_message_over_200_chars():
    long_message = "x" * 190 + " https://example.com"
    response = client.post("/posting", json={"message": long_message})
    assert response.status_code == 422


def test_posting_rejects_no_url():
    response = client.post("/posting", json={"message": "Hello world only text"})
    assert response.status_code == 422
    detail = response.json()["detail"]
    body = detail if isinstance(detail, str) else str(detail)
    assert "exactly one" in body.lower() or "cta" in body.lower()


def test_posting_rejects_multiple_urls():
    response = client.post(
        "/posting",
        json={"message": "See https://a.com and https://b.com for more"},
    )
    assert response.status_code == 422


def test_posting_rejects_invalid_url():
    response = client.post(
        "/posting",
        json={"message": "No valid host https:///path-only"},
    )
    assert response.status_code == 422
    detail = response.json()["detail"]
    body = detail if isinstance(detail, str) else str(detail)
    assert "invalid" in body.lower()


def test_posting_rejects_empty_message():
    response = client.post("/posting", json={"message": "   "})
    assert response.status_code == 422


@patch("app.main.publish_message", new_callable=AsyncMock)
def test_posting_success_response_shape(mock_publish: AsyncMock):
    mock_publish.return_value = PostingResponse(
        success=True,
        results=[
            PlatformResult(
                platform="Bluesky",
                status="success",
                posted_url="https://bsky.app/profile/user.bsky.social/post/abc",
                public_access=True,
                date=None,
                time=None,
                error=None,
            )
        ],
    )
    response = client.post("/posting", json={"message": VALID_MESSAGE})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["results"]) >= 1
    assert "platform" in data["results"][0]
    mock_publish.assert_awaited_once_with(VALID_MESSAGE)


@pytest.mark.asyncio
async def test_publish_message_continues_on_platform_failure():
    from datetime import date, time

    from app.services import posting_service
    from app.services.posting_service import publish_message

    class _FailPoster:
        name = "PlatformA"

        async def post(self, message: str) -> PlatformResult:
            return PlatformResult(
                platform=self.name,
                status="failed",
                posted_url=None,
                public_access=False,
                date=None,
                time=None,
                error="Authentication failed",
            )

    class _OkPoster:
        name = "PlatformB"

        async def post(self, message: str) -> PlatformResult:
            return PlatformResult(
                platform=self.name,
                status="success",
                posted_url="https://example.com/post/123",
                public_access=True,
                date=date(2026, 11, 15),
                time=time(10, 30, 0),
                error=None,
            )

    with patch.object(
        posting_service,
        "_build_posters",
        return_value=[_FailPoster(), _OkPoster()],
    ):
        response = await publish_message(VALID_MESSAGE)

    assert len(response.results) == 2
    assert response.results[0].status == "failed"
    assert response.results[1].status == "success"
    assert response.success is True


@pytest.mark.asyncio
async def test_publish_message_returns_five_platforms():
    from app.services.posting_service import publish_message

    response = await publish_message(VALID_MESSAGE)
    names = [r.platform for r in response.results]
    assert names == ["Discord", "Telegram", "Slack", "Bluesky", "Ntfy"]


@pytest.mark.integration
@pytest.mark.asyncio
async def test_live_social_post_when_enabled():
    import os

    if os.environ.get("RUN_INTEGRATION") != "1":
        pytest.skip("Set RUN_INTEGRATION=1 to run live social API test")

    from app.config import get_settings
    from app.services.posting_service import publish_message

    settings = get_settings()
    if not settings.ntfy_topic and not settings.bluesky_app_password:
        pytest.skip("Set NTFY_TOPIC or Bluesky app password for live integration test")

    response = await publish_message(VALID_MESSAGE)
    assert len(response.results) == 5
    assert response.success or any(r.status == "failed" for r in response.results)
# Last updated: Monday, Nov 16, 2026, 04:23 PM (UTC+5:30)
