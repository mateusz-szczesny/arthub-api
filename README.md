# ArtHub (Server Application)

Platforma pośrednicząca w sprzedaży
(licencjonowaniu) własności artystycznych zamieszczanych przez jej użytkowników.

## Uruchomienie programu lokalnie

```bash
$ # clone repository
$ python -m pip install -r requirements.txt
$ (if needed) python manage.py migrate
$ python manage.py runserver
```

## Utworzenie superuser'a

```bash
$ python manage.py createsuperuser
$ #provide credentials
$ #access localhost:post/admin when server running
```

## Manualne wdrożenie serwisu na środowisko testowe

```bash
$ git remte add dokku dokku@mszczesny.com:arthub-test
& git push dokku develop:master # source_branch:target_branch
```
