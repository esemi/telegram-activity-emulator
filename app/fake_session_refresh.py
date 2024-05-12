import logging

import uvloop
from pyrogram import Client

from app.settings import app_settings

logger = logging.getLogger(__file__)


async def main() -> None:
    for user in app_settings.FAKE_USERS:
        fake_user_app = Client(
            workdir=app_settings.SESSIONS_PATH,
            name=user.phone,
            api_id=user.api_id,
            api_hash=user.api_hash,
            phone_number=user.phone,
        )

        is_authorized = await fake_user_app.connect()
        if not is_authorized:
            logger.info('refresh {0} session'.format(user))
            await fake_user_app.authorize()
        del fake_user_app

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)-8s %(message)s',  # noqa: WPS323
    )
    uvloop.run(main())  # type: ignore
