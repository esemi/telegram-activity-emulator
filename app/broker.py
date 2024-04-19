from redis import asyncio as aioredis

from app.settings import app_settings

db_pool: aioredis.Redis = aioredis.from_url(
    str(app_settings.REDIS_DSN),
    encoding='utf-8',
    decode_responses=True,
)
queue_channel = db_pool.pubsub()
