import uvloop

from app.settings import app_settings

uvloop.install()


async def main() -> None:
    for user in app_settings.FAKE_USERS:
        # todo
        pass


if __name__ == '__main__':
    uvloop.run(main())  # type: ignore
