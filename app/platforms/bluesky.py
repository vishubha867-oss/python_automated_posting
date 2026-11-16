from datetime import datetime, timezone

import httpx

from app.config import get_settings
from app.platforms.base import BasePlatformPoster
from app.schemas import PlatformResult


class BlueskyPoster(BasePlatformPoster):
    """Publish a text post via Bluesky AT Protocol (app password)."""

    name = "Bluesky"

    async def _create_session(self) -> tuple[str, str]:
        """Return (access_jwt, did)."""
        settings = get_settings()
        handle = (settings.bluesky_handle or "").strip()
        app_password = (settings.bluesky_app_password or "").strip()
        if not handle or not app_password:
            raise ValueError("missing credentials")

        base = settings.bluesky_service_url.rstrip("/")
        response = await self.client.post(
            f"{base}/xrpc/com.atproto.server.createSession",
            json={"identifier": handle, "password": app_password},
            timeout=30.0,
        )
        if response.status_code >= 400:
            raise httpx.HTTPStatusError(
                "Bluesky session failed",
                request=response.request,
                response=response,
            )
        data = response.json()
        token = data.get("accessJwt")
        did = data.get("did")
        if not token or not did:
            raise ValueError("Bluesky session response missing accessJwt or did")
        return token, did

    async def post(self, message: str) -> PlatformResult:
        settings = get_settings()
        if not settings.bluesky_handle or not settings.bluesky_app_password:
            return self._not_configured()

        base = settings.bluesky_service_url.rstrip("/")
        try:
            access_jwt, did = await self._create_session()
        except httpx.HTTPStatusError as exc:
            return self._failure_from_response(exc.response)
        except Exception as exc:
            return self._failure(str(exc))

        created_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        record = {
            "$type": "app.bsky.feed.post",
            "text": message,
            "createdAt": created_at,
        }
        try:
            response = await self.client.post(
                f"{base}/xrpc/com.atproto.repo.createRecord",
                headers={"Authorization": f"Bearer {access_jwt}"},
                json={
                    "repo": did,
                    "collection": "app.bsky.feed.post",
                    "record": record,
                },
                timeout=30.0,
            )
            if response.status_code >= 400:
                return self._failure_from_response(response)

            data = response.json()
            uri = data.get("uri", "")
            rkey = uri.rsplit("/", 1)[-1] if uri else None
            handle = settings.bluesky_handle.strip().lstrip("@")
            posted_url = None
            if rkey and handle:
                posted_url = f"https://bsky.app/profile/{handle}/post/{rkey}"

            return self._success(posted_url=posted_url, public_access=True)
        except httpx.HTTPStatusError as exc:
            return self._failure_from_response(exc.response)
        except Exception as exc:
            return self._failure(str(exc))
# Last updated: Monday, Nov 16, 2026, 04:23 PM (UTC+5:30)
