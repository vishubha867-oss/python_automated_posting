import httpx

from app.config import get_settings
from app.platforms.base import BasePlatformPoster
from app.schemas import PlatformResult


class TelegramPoster(BasePlatformPoster):
    name = "Telegram"

    async def post(self, message: str) -> PlatformResult:
        settings = get_settings()
        token = settings.telegram_bot_token
        chat_id = settings.telegram_chat_id
        if not token or not chat_id:
            return self._not_configured()

        api_url = f"https://api.telegram.org/bot{token}/sendMessage"
        try:
            response = await self.client.post(
                api_url,
                json={
                    "chat_id": chat_id,
                    "text": message,
                    "disable_web_page_preview": False,
                },
                timeout=30.0,
            )
            if response.status_code >= 400:
                return self._failure_from_response(response)
            payload = response.json()
            if not payload.get("ok"):
                return self._failure_from_response(response)

            result = payload.get("result", {})
            chat = result.get("chat", {})
            message_id = result.get("message_id")
            username = chat.get("username")
            if username and message_id is not None:
                posted_url = f"https://t.me/{username}/{message_id}"
            else:
                posted_url = f"https://t.me/c/{str(chat.get('id', '')).lstrip('-100')}/{message_id}"

            return self._success(posted_url=posted_url, public_access=True)
        except httpx.HTTPStatusError as exc:
            return self._failure_from_response(exc.response)
        except Exception as exc:
            return self._failure(str(exc))
# Last updated: Monday, Nov 16, 2026, 04:23 PM (UTC+5:30)
