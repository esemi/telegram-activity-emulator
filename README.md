WIP: telegram-activity-emulator
---


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

### Host setup
```shell
apt-get update
apt-get install software-properties-common
add-apt-repository ppa:deadsnakes/ppa
apt install supervisor python3.12 python3.12-venv redis

curl -sS https://bootstrap.pypa.io/get-pip.py | python3.12

python3.12 -m pip install --upgrade setuptools

groupadd supervisor
usermod -a -G supervisor root
vi /etc/supervisor/supervisord.conf  # change chown and chmod params
service supervisor restart

adduser -q telegram-activity
usermod -a -G supervisor telegram-activity

cp etc/supervisor-example.conf /etc/supervisor/conf.d/telegram-activity.conf

# run deploy from github actions
poetry run python -m app.prepare_fake_users
service supervisor restart

# repeat deploy from github actions
```
