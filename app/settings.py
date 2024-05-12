"""Application settings."""
import os
from dataclasses import dataclass

import uvloop
from pydantic import Field, RedisDsn
from pydantic_settings import BaseSettings

APP_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        '..',
    ),
)


@dataclass
class FakeUser:
    phone: str
    api_id: int
    api_hash: str


def parse_fake_users_settings(filepath: str) -> list[FakeUser]:
    if not os.path.exists(filepath):
        raise RuntimeError('Create {0} file first'.format(filepath))

    with open(filepath, mode='r') as fd:
        results = []
        for row in fd.readlines():
            values = row.split('\t')
            results.append(FakeUser(
                phone=values[0].strip(),
                api_id=int(values[1].strip()),
                api_hash=values[2].strip(),
            ))
        return results


class AppSettings(BaseSettings):
    """Application settings class."""

    REDIS_DSN: RedisDsn = Field(default='redis://localhost/1')
    REDIS_TIMEOUT: float = 10.
    REDIS_CHANNEL_NAME: str = 'channel:activity-emulator'
    OBSERVER_BOT_TOKEN: str
    OBSERVED_CHANNEL_ID: int
    FAKE_USERS_PER_POST: int = Field(
        default=90,
        description='Процент фейк-пользователей, реагирующих на пост, относительно всей популяции',
    )
    FAKE_USERS_REACTIONS: list[str] = [
        '❤',
        '️👍',
        '🔥',
    ]
    FAKE_USERS: list[FakeUser] = parse_fake_users_settings(
        filepath=os.path.join(APP_PATH, 'fake-users.tsv'),
    )
    SESSIONS_PATH: str = os.path.join(APP_PATH, 'sessions')


app_settings = AppSettings(
    _env_file=os.path.join(APP_PATH, '.env'),  # type:ignore
)
uvloop.install()
