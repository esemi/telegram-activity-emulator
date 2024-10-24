from enum import Enum

from redis import asyncio as aioredis

from app.settings import app_settings

db_pool: aioredis.Redis = aioredis.from_url(
    str(app_settings.REDIS_DSN),
    encoding='utf-8',
    decode_responses=True,
)
queue_channel = db_pool.pubsub()


class Action(Enum):
    view = 'view'
    reaction = 'reaction'


async def push_event(username: str, message_id: int, action: Action) -> None:
    await db_pool.publish(
        app_settings.REDIS_CHANNEL_NAME,
        f'{username}:{message_id}:{action.value}',
    )
