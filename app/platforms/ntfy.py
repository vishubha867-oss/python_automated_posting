import httpx

from app.config import get_settings
from app.platforms.base import BasePlatformPoster
from app.schemas import PlatformResult


class NtfyPoster(BasePlatformPoster):
    """
    Publish via ntfy.sh — simple HTTP POST (text notification).

    Docs: https://docs.ntfy.sh/publish/
    """

    name = "Ntfy"

    async def post(self, message: str) -> PlatformResult:
        settings = get_settings()
        topic = (settings.ntfy_topic or "").strip()
        if not topic:
            return self._not_configured()

        base = settings.ntfy_server_url.rstrip("/")
        url = f"{base}/{topic}"
        headers: dict[str, str] = {"Content-Type": "text/plain; charset=utf-8"}
        if settings.ntfy_access_token:
            headers["Authorization"] = f"Bearer {settings.ntfy_access_token.strip()}"

        try:
            response = await self.client.post(
                url,
                content=message.encode("utf-8"),
                headers=headers,
                timeout=30.0,
            )
            if response.status_code >= 400:
                return self._failure_from_response(response)

            posted_url = f"{base}/{topic}"
            return self._success(
                posted_url=posted_url,
                public_access=settings.ntfy_public_topic,
            )
        except httpx.HTTPStatusError as exc:
            return self._failure_from_response(exc.response)
        except Exception as exc:
            return self._failure(str(exc))
# Last updated: Monday, Nov 16, 2026, 04:23 PM (UTC+5:30)
