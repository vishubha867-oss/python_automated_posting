import httpx

from app.platforms import (
    BlueskyPoster,
    DiscordPoster,
    NtfyPoster,
    SlackPoster,
    TelegramPoster,
)
from app.platforms.base import BasePlatformPoster
from app.schemas import PlatformResult, PostingResponse


def _build_posters(client: httpx.AsyncClient) -> list[BasePlatformPoster]:
    return [
        DiscordPoster(client),
        TelegramPoster(client),
        SlackPoster(client),
        BlueskyPoster(client),
        NtfyPoster(client),
    ]


async def publish_message(message: str) -> PostingResponse:
    async with httpx.AsyncClient() as client:
        posters = _build_posters(client)
        results: list[PlatformResult] = []

        for poster in posters:
            try:
                result = await poster.post(message)
            except Exception as exc:
                result = PlatformResult(
                    platform=poster.name,
                    status="failed",
                    posted_url=None,
                    public_access=False,
                    date=None,
                    time=None,
                    error=f"Unexpected error: {exc}",
                )
            results.append(result)

    any_success = any(r.status == "success" for r in results)
    return PostingResponse(success=any_success, results=results)
# Last updated: Monday, Nov 16, 2026, 04:23 PM (UTC+5:30)
