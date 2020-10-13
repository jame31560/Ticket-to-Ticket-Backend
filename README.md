# Ticket-to-Ticket-Backend

## Install package

Note: Recommend using virtual environment.

```
(ENV)$ pip3 install -r requirement.txt
```

## Create Config File

Add `config.py` and put the following content.
`[XXX]` means the variable which you need to replace it.

```python
class Config(object):
    DEBUG = True
    CSRF_ENABLED = True


class Configdb(Config):
    MONGOALCHEMY_DATABASE = "[DB_name]"
    MONGOALCHEMY_CONNECTION_STRING = "mongodb://[username]:[password]@[server]/[DB_name]"


class ConfigJWT(Config):
    JWT_SECRET_KEY = "[your_JWT_KEY]"

```

## Run app (Test)

Recommend useing wsgi to run app when publish.

```
(ENV)$ python run.py
```
