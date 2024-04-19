import logging
import math
import random

import uvloop
from aiogram import Bot, Dispatcher, types, F

from app.broker import db_pool
from app.settings import app_settings, FakeUser

uvloop.install()
logger = logging.getLogger(__file__)

bot = Bot(token=app_settings.OBSERVER_BOT_TOKEN)
dp = Dispatcher()


@dp.channel_post(F.chat.id == app_settings.OBSERVED_CHANNEL_ID)
async def welcome(message: types.Message) -> None:
    logger.info('new post activity! {0}'.format(message.message_id))
    users_sample_size: int = min(1, math.floor(len(app_settings.FAKE_USERS) / 100 * app_settings.FAKE_USERS_PER_POST))
    selected_users: list[FakeUser] = random.sample(app_settings.FAKE_USERS, users_sample_size)

    for user in selected_users:
        await db_pool.publish(app_settings.REDIS_CHANNEL_NAME, f'{user.phone}:{message.id}')
    logger.info('pushed {0} random users from pool'.format(len(selected_users)))


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
