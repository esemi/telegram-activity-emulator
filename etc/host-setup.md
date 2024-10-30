
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
