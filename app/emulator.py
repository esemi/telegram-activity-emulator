import asyncio
import logging
import random
import signal

import uvloop
from pyrogram import Client
from pyrogram.errors import ChannelInvalid
from pyrogram.raw.functions.messages import GetMessagesViews

from app.broker import Action, pop_event, queue_channel
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

        try:
            if event := await pop_event():
                logger.info('catch message {0}'.format(event))
                await _process_event(*event)
                logger.info('event processed')
        except Exception as exc:
            logger.warning('processing error {0}'.format(exc))

    logger.info('emulator stopped')


async def _process_event(user_name: str, message_id: int, action: Action) -> None:
    async with Client(workdir=app_settings.SESSIONS_PATH, name=user_name) as fake_user_session:
        await _random_wait()

        if action is Action.view or action is Action.reaction:
            await _increment_views(
                app_settings.OBSERVED_CHANNEL_ID,
                message_id,
                fake_user_session,
            )

        if action is Action.reaction:
            await _increment_reactions(
                app_settings.OBSERVED_CHANNEL_ID,
                message_id,
                fake_user_session,
            )


async def _increment_views(chat_id: int, message_id: int, user_app: Client) -> None:
    try:
        channel = await user_app.resolve_peer(int(chat_id))
    except ChannelInvalid:
        logger.warning('invalid channel exception')
        return

    request = GetMessagesViews(peer=channel, id=[message_id], increment=True)  # type: ignore
    await user_app.invoke(request)
    await user_app.read_chat_history(chat_id=chat_id, max_id=message_id)
    logger.info('marked as read')


async def _increment_reactions(chat_id: int, message_id: int, user_app: Client) -> None:
    reaction = random.choice(app_settings.AVAILABLE_REACTIONS)
    logger.info('reaction {0} sent'.format(reaction))
    await user_app.send_reaction(chat_id, message_id, reaction)


async def _random_wait() -> None:
    timeout = random.randint(
        app_settings.EMULATOR_ACTION_THROTTLING_MIN,
        app_settings.EMULATOR_ACTION_THROTTLING_MAX,
    )
    logger.info('wait for {0} seconds'.format(timeout))
    await asyncio.sleep(timeout)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)-8s %(message)s',  # noqa: WPS323
    )
    logging.getLogger('pyrogram').setLevel(logging.WARNING)
    signal.signal(signal.SIGINT, sigint)
    uvloop.run(main())  # type: ignore
