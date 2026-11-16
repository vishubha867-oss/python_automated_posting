from abc import ABC, abstractmethod
from datetime import datetime, timezone

import httpx

from app.schemas import PlatformResult


class BasePlatformPoster(ABC):
    name: str

    def __init__(self, client: httpx.AsyncClient) -> None:
        self.client = client

    @abstractmethod
    async def post(self, message: str) -> PlatformResult:
        """Publish message to the platform."""

    def _success(
        self,
        posted_url: str | None,
        *,
        public_access: bool = True,
    ) -> PlatformResult:
        now = datetime.now(timezone.utc)
        return PlatformResult(
            platform=self.name,
            status="success",
            posted_url=posted_url,
            public_access=public_access,
            date=now.date(),
            time=now.time().replace(microsecond=0),
            error=None,
        )

    def _failure(self, error: str, *, public_access: bool = False) -> PlatformResult:
        return PlatformResult(
            platform=self.name,
            status="failed",
            posted_url=None,
            public_access=public_access,
            date=None,
            time=None,
            error=error,
        )

    def _not_configured(self) -> PlatformResult:
        return self._failure(
            f"{self.name} is not configured. Set the required environment variables (see .env.example)."
        )

    def _failure_from_response(self, response: httpx.Response) -> PlatformResult:
        """Return platform failure using the third-party API status and body."""
        return self._failure(_api_error_message(response, self.name))

    @staticmethod
    def _api_error_message(response: httpx.Response, platform: str) -> str:
        status = response.status_code
        raw = (response.text or "").strip()
        if not raw:
            phrase = response.reason_phrase or ""
            return f"{platform} API HTTP {status} {phrase}".strip()

        try:
            data = response.json()
        except Exception:
            return f"{platform} API HTTP {status}: {raw[:500]}"

        if isinstance(data, dict):
            parts: list[str] = []
            for key in ("error", "error_description", "message", "description", "error_user_msg"):
                value = data.get(key)
                if value is not None and str(value).strip():
                    parts.append(str(value).strip())
            if "error" in data and isinstance(data["error"], dict):
                nested = data["error"]
                for key in ("message", "type", "code"):
                    value = nested.get(key)
                    if value is not None:
                        parts.append(str(value))
            if parts:
                return f"{platform} API HTTP {status}: " + " | ".join(parts)

        return f"{platform} API HTTP {status}: {raw[:500]}"
# Last updated: Monday, Nov 16, 2026, 04:23 PM (UTC+5:30)
