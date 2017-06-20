# My django blog repo

create database

```
cp website/settings.py website/settings-local.py

touch website//keysettings.py
```


You need to fill the keysettings with your:

    SECRET_KEY
    DATABASES
    NORECAPTCHA_SITE_KEY
    NORECAPTCHA_SECRET_KEY
    ANYMAIL
    EMAIL_BACKEND
    DEFAULT_FROM_EMAIL





### Update server with fabric:

```
fab update_repo
```
