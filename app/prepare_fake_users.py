import logging

import uvloop
from pyrogram import Client
from pyrogram.errors import UserAlreadyParticipant

from app.settings import app_settings

logger = logging.getLogger(__file__)


async def main() -> None:
    for user in app_settings.FAKE_USERS:
        logger.info('preparing of {0} faker started {1}'.format(user.phone, user.name))
        fake_user_app = Client(
            workdir=app_settings.SESSIONS_PATH,
            name=user.name,
            api_id=user.api_id,
            api_hash=user.api_hash,
            phone_number=user.phone,
            password=user.two_fa,
        )

        is_authorized = await fake_user_app.connect()
        if not is_authorized:
            logger.info('auth is awaiting'.format(user.phone))
            await fake_user_app.authorize()

        try:
            await fake_user_app.join_chat(app_settings.OBSERVED_CHANNEL_INVITE_LINK)
        except UserAlreadyParticipant:
            pass

        await fake_user_app.disconnect()
        del fake_user_app

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)-8s %(message)s',  # noqa: WPS323
    )
    uvloop.run(main())  # type: ignore
