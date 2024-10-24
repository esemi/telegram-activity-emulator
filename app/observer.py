import logging
import random

import uvloop
from aiogram import Bot, Dispatcher, F, types

from app.broker import Action, push_event
from app.settings import app_settings

logger = logging.getLogger(__file__)

bot = Bot(token=app_settings.OBSERVER_BOT_TOKEN)
dp = Dispatcher()


@dp.channel_post(F.chat.id == app_settings.OBSERVED_CHANNEL_ID)
async def welcome(message: types.Message) -> None:
    logger.info('new post activity! {0} {1}'.format(message.message_id, message.chat.id))
    views_percent: int = random.randint(app_settings.MIN_VIEWS_PERCENT, app_settings.MAX_VIEWS_PERCENT)
    reaction_percent: int = random.randint(app_settings.MIN_REACTIONS_PERCENT, app_settings.MAX_REACTIONS_PERCENT)

    logger.info('population {0}, views {1}%, reactions {2}%'.format(
        len(app_settings.FAKE_USERS),
        views_percent,
        reaction_percent,
    ))

    for user in app_settings.FAKE_USERS:
        is_view = bool(random.randint(0, 100) <= views_percent)
        is_reaction = bool(random.randint(0, 100) <= reaction_percent) and is_view

        if is_reaction:
            await push_event(user.name, message.message_id, action=Action.reaction)
            logger.info('create reaction task')

        elif is_view:
            await push_event(user.name, message.message_id, action=Action.view)
            logger.info('create view task')


async def main() -> None:
    logger.info('observer started')
    await dp.start_polling(bot)
    logger.info('observer stopped')


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)-8s %(message)s',  # noqa: WPS323
    )
    uvloop.run(main())  # type: ignore
