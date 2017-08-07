[![Build Status](https://travis-ci.org/eduzen/eduzen.svg?branch=master)](https://travis-ci.org/eduzen/eduzen)

# My django blog Repo: http://eduzen.com.ar

## Configuration:

1. create your database

2. create you local setting for develop. I used another file `keysettings.py` where I put all private keys

```bash

cp website/settings.py website/settings-local.py

touch website/keysettings.py
```

In that file you need to fill it with your:

```python
    SECRET_KEY
    DATABASES
    NORECAPTCHA_SITE_KEY
    NORECAPTCHA_SECRET_KEY
    ANYMAIL
    EMAIL_BACKEND
    DEFAULT_FROM_EMAIL
```

3. Then you need to create migration, migrate, create superuser and run the app.

```bash
python manage.py makemigration --settings=website.settings-local
python manage.py migrate --settings=website.settings-local
python manage.py createsuperuser --settings=website.settings-local

python manage.py runserver --settings=website.settings-local
```


### Update server with fabric:

```bash

fab update_repo
```
