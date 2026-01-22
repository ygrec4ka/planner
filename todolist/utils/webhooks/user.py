import aiohttp
import logging
from core.models import User
from core.schemas.user import UserRead

log = logging.getLogger(__name__)

WEBHOOK_URL = "https://httpbin.org/post"


async def send_new_user_notification(user: User) -> None:
    wh_data = {
        "user": UserRead.model_validate(user).model_dump(),
    }
    log.info("Notify user created with data: %s", wh_data)
    async with aiohttp.ClientSession() as session:
        async with session.post(WEBHOOK_URL, json=wh_data) as response:
            data = await response.json()
            log.info("Sent webhook got response: %s", data)
