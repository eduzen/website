[![Build Status](https://travis-ci.org/eduzen/eduzen.svg?branch=master)](https://travis-ci.org/eduzen/eduzen)

# My django blog repo

create database

```bash

cp website/settings.py website/settings-local.py

touch website/keysettings.py
```


You need to fill the keysettings with your:

    SECRET_KEY
    DATABASES
    NORECAPTCHA_SITE_KEY
    NORECAPTCHA_SECRET_KEY
    ANYMAIL
    EMAIL_BACKEND
    DEFAULT_FROM_EMAIL


```bash

python manage.py runserver --settings=website.settings-local
```


### Update server with fabric:

```bash

fab update_repo
```
