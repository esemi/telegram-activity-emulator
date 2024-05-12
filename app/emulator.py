import asyncio
import logging
import random
import signal

import uvloop
from pyrogram import Client
from pyrogram.errors import ChannelInvalid
from pyrogram.raw.functions.messages import GetMessagesViews

from app.broker import queue_channel
from app.settings import app_settings

logger = logging.getLogger(__file__)

__stop_request: bool = False


def sigint(*args, **kwargs) -> None:  # type: ignore
    global __stop_request  # noqa: WPS420, WPS442
    logger.info('stop request received')
    __stop_request = True  # noqa: WPS122, WPS442


async def main() -> None:
    logger.info('emulator started')
    await queue_channel.subscribe(app_settings.REDIS_CHANNEL_NAME)

    while True:
        if __stop_request:
            logger.warning('stop by request')
            break

        message = await queue_channel.get_message(ignore_subscribe_messages=True, timeout=app_settings.REDIS_TIMEOUT)
        if message is None:
            continue

        logger.info('catch message {0}'.format(message))
        chat_id, user_name, message_id = message['data'].split(':')

        async with Client(workdir=app_settings.SESSIONS_PATH, name=user_name) as fake_user_app:
            await asyncio.sleep(random.randint(2, 8))
            await _increment_views(int(chat_id), int(message_id), fake_user_app)

            await asyncio.sleep(random.randint(5, 15))
            await _increment_reactions(int(chat_id), int(message_id), fake_user_app)

    logger.info('emulator stopped')


async def _increment_views(chat_id: int, message_id: int, user_app: Client) -> None:
    try:
        channel = await user_app.resolve_peer(int(chat_id))
    except ChannelInvalid:
        logger.warning('invalid channel exception')
        return None

    request = GetMessagesViews(peer=channel, id=[message_id], increment=True)
    await user_app.invoke(request)
    await user_app.read_chat_history(chat_id=chat_id, max_id=message_id)
    logger.info('marked as read')


async def _increment_reactions(chat_id: int, message_id: int, user_app: Client) -> None:
    reaction = random.choice(app_settings.FAKE_USERS_REACTIONS)
    logger.info('reaction {0} sent'.format(reaction))
    await user_app.send_reaction(chat_id, message_id, reaction)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)-8s %(message)s',  # noqa: WPS323
    )
    signal.signal(signal.SIGINT, sigint)
    uvloop.run(main())  # type: ignore
