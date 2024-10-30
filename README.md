Telegram activity emulator
---

[![linters](https://github.com/esemi/telegram-activity-emulator/actions/workflows/linters.yml/badge.svg?branch=master)](https://github.com/esemi/telegram-activity-emulator/actions/workflows/linters.yml)

An automated system designed to simulate organic user activity around your Telegram channel, enhancing engagement metrics through realistic interactions like views, reactions, and message exchanges.


### Pre-requirements
- [redis server up and running](https://redis.io/docs/getting-started/installation/)
- [python 3.12+](https://www.python.org/downloads/)
- [telegram bot token](https://t.me/botfather)


### Local setup
```shell
git clone git@github.com:esemi/telegram-activity-emulator.git
cd telegram-activity-emulator
python3.12 -m venv venv
source venv/bin/activate
pip install -U --no-cache-dir poetry pip setuptools
poetry install
```

Create env file to override default config
```shell
cat > .env << EOF
OBSERVER_BOT_TOKEN="68123456324:AAG_k3xRJSDHSJDSJKkww53P5Jr-DdDdDd"
OBSERVED_CHANNEL_ID="-1002078951125"
OBSERVED_CHANNEL_INVITE_LINK="https://t.me/+1FKK6Yr_sDdSfdS"
EOF
```

### Run fake-users session authorization checking
```shell
poetry run python -m app.prepare_fake_users
```

### Run observer bot
```shell
poetry run python -m app.observer
```

### Run emulator bot
```shell
poetry run python -m app.emulator
```
