from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    discord_webhook_url: str | None = None
    telegram_bot_token: str | None = None
    telegram_chat_id: str | None = None
    slack_webhook_url: str | None = None
    bluesky_service_url: str = "https://bsky.social"
    bluesky_handle: str | None = None
    bluesky_app_password: str | None = None
    ntfy_server_url: str = "https://ntfy.sh"
    ntfy_topic: str | None = None
    ntfy_access_token: str | None = None
    ntfy_public_topic: bool = True


def get_settings() -> Settings:
    return Settings()
# Last updated: Monday, Nov 16, 2026, 04:23 PM (UTC+5:30)
