import httpx

from app.config import get_settings
from app.platforms.base import BasePlatformPoster
from app.schemas import PlatformResult


class SlackPoster(BasePlatformPoster):
    name = "Slack"

    async def post(self, message: str) -> PlatformResult:
        webhook_url = get_settings().slack_webhook_url
        if not webhook_url:
            return self._not_configured()

        try:
            response = await self.client.post(
                webhook_url,
                json={"text": message},
                timeout=30.0,
            )
            if response.status_code >= 400:
                return self._failure_from_response(response)
            return self._success(posted_url=None, public_access=False)
        except httpx.HTTPStatusError as exc:
            return self._failure_from_response(exc.response)
        except Exception as exc:
            return self._failure(str(exc))
# Last updated: Monday, Nov 16, 2026, 04:23 PM (UTC+5:30)
