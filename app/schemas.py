import re
from datetime import date as DateType, time as TimeType
from typing import Literal

from pydantic import BaseModel, Field, field_validator

_URL_PATTERN = re.compile(
    r"https?://[^\s<>\"]+",
    re.IGNORECASE,
)


class PostingRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        description="Short message with exactly one http(s) CTA link (max 200 characters).",
    )

    @field_validator("message")
    @classmethod
    def validate_message(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Message must not be empty.")
        if len(value) > 200:
            raise ValueError("Message must not exceed 200 characters.")

        urls = _URL_PATTERN.findall(value)
        if len(urls) == 0:
            raise ValueError("Message must include exactly one CTA link (http or https URL).")
        if len(urls) > 1:
            raise ValueError("Message must include exactly one CTA link, not multiple URLs.")

        cta = urls[0].rstrip(".,);]")
        if not _is_valid_url(cta):
            raise ValueError(f"Invalid CTA URL: {cta}")

        return value


def _is_valid_url(url: str) -> bool:
    try:
        from urllib.parse import urlparse

        parsed = urlparse(url)
        return parsed.scheme in ("http", "https") and bool(parsed.netloc)
    except Exception:
        return False


class PlatformResult(BaseModel):
    platform: str
    status: Literal["success", "failed"]
    posted_url: str | None = None
    public_access: bool
    date: DateType | None = None
    time: TimeType | None = None
    error: str | None = None


class PostingResponse(BaseModel):
    success: bool
    results: list[PlatformResult]
# Last updated: Monday, Nov 16, 2026, 04:23 PM (UTC+5:30)
