WIP: telegram-activity-emulator
---

### Local setup
```shell
git clone git@github.com:esemi/telegram-activity-emulator.git
cd telegram-activity-emulator
python3.12 -m venv venv
source venv/bin/activate
pip install -U --no-cache-dir poetry pip setuptools
poetry install
```

### Run fake-users session authorization checking
```shell
poetry run python -m app.fake_session_refresh
```

### Run observer bot
```shell
poetry run python -m app.observer
```

### Run emulator bot
```shell
poetry run python -m app.emulator
```