[![Build Status](https://travis-ci.org/eduzen/eduzen.svg?branch=master)](https://travis-ci.org/eduzen/eduzen)
[![codecov](https://codecov.io/gh/eduzen/eduzen/branch/master/graph/badge.svg)](https://codecov.io/gh/eduzen/eduzen)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/2e1abe2b9cdf49748eddfffb0453f59e)](https://www.codacy.com/manual/eduzen/eduzen?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=eduzen/eduzen&amp;utm_campaign=Badge_Grade)


# My django blog Repo: http://eduzen.com.ar

## Configuration:

1. Copy and fill with your credentials

```bash

cp .env.sample .env

```


2. Then you need to create migration, migrate, create superuser and run the app.

```bash
python manage.py makemigration --settings=website.settings-local
python manage.py migrate --settings=website.settings-local
python manage.py createsuperuser --settings=website.settings-local

python manage.py runserver --settings=website.settings-local
```

