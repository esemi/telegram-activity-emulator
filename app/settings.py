"""Application settings."""
import hashlib
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
    two_fa: str
    name: str


def parse_fake_users_settings(filepath: str) -> list[FakeUser]:
    if not os.path.exists(filepath):
        raise RuntimeError('Create {0} file first'.format(filepath))

    with open(filepath, mode='r') as fd:
        users = []
        for row in fd.readlines():
            user_props = row.split('\t')
            unique_name = hashlib.md5(
                string='{0}_{1}'.format(
                    user_props[1].strip()[:6],
                    user_props[2].strip()[:30],
                ).encode(),
                usedforsecurity=False,
            ).hexdigest()

            users.append(FakeUser(
                phone=user_props[0].strip(),
                api_id=int(user_props[1].strip()),
                api_hash=user_props[2].strip(),
                two_fa=user_props[3].strip(),
                name=unique_name,
            ))
        return users


class AppSettings(BaseSettings):
    """Application settings class."""

    REDIS_DSN: RedisDsn = Field(default='redis://localhost/1')
    REDIS_TIMEOUT: float = Field(default=10)
    REDIS_CHANNEL_NAME: str = 'channel:activity-emulator'

    EMULATOR_ACTION_THROTTLING_MIN: int = 5
    EMULATOR_ACTION_THROTTLING_MAX: int = 36

    OBSERVER_BOT_TOKEN: str
    OBSERVED_CHANNEL_ID: int
    OBSERVED_CHANNEL_INVITE_LINK: str

    MIN_VIEWS_PERCENT: int = Field(
        default=73,
        description='Минимальный процент просмотров относительно всей популяции',
    )
    MAX_VIEWS_PERCENT: int = Field(
        default=95,
        description='Максимальный процент просмотров относительно всей популяции',
    )
    MIN_REACTIONS_PERCENT: int = Field(
        default=30,
        description='Минимальный процент реакций относительно просмотров',
    )
    MAX_REACTIONS_PERCENT: int = Field(
        default=60,
        description='Максимальный процент реакций относительно просмотров',
    )

    AVAILABLE_REACTIONS: list[str] = [
        '❤',
        '❤',
        '❤',
        '❤',
        '🔥',
        '🔥',
        '🔥',
        '️👍',
        '️👍',
        '🎉',
        '🤩',
        '😁',
        '🤔',
        '👏',
        '🫡',
        '🌚',
        '🍾',
    ]
    FAKE_USERS: list[FakeUser] = parse_fake_users_settings(
        filepath=os.path.join(APP_PATH, 'fake-users.tsv'),
    )
    SESSIONS_PATH: str = os.path.join(APP_PATH, 'sessions')


app_settings = AppSettings(
    _env_file=os.path.join(APP_PATH, '.env'),  # type:ignore
)
uvloop.install()
