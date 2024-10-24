import logging

import uvloop
from pyrogram import Client
from pyrogram.errors import UserAlreadyParticipant
from pyrogram.raw.functions.account import UpdateNotifySettings
from pyrogram.raw.types import InputNotifyPeer, InputPeerNotifySettings

from app.settings import app_settings

MUTE_TTL: int = 2147483647  # 2 ^ 32 / 2 - 1

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
        await _process_fake_user_session(fake_user_app)
        await fake_user_app.disconnect()


async def _process_fake_user_session(fake_user_app: Client) -> None:
    is_authorized = await fake_user_app.connect()
    if not is_authorized:
        logger.info('auth is awaiting {0}'.format(fake_user_app.phone_number))
        await fake_user_app.authorize()

    try:
        await fake_user_app.join_chat(app_settings.OBSERVED_CHANNEL_INVITE_LINK)
    except UserAlreadyParticipant:
        pass

    channel = await fake_user_app.resolve_peer(app_settings.OBSERVED_CHANNEL_ID)
    mute_request = UpdateNotifySettings(
        peer=InputNotifyPeer(peer=channel),  # type: ignore
        settings=InputPeerNotifySettings(mute_until=MUTE_TTL),
    )
    await fake_user_app.invoke(mute_request)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)-8s %(message)s',  # noqa: WPS323
    )
    uvloop.run(main())  # type: ignore
