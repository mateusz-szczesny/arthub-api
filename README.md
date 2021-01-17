[![Buddy](https://app.buddy.works/mzpp/mzpp---p--bitbucket-instance/pipelines/pipeline/300110/badge.svg?token=623647084d320a82f313767f0bfed3e698adc43b4cd84d0f3560ef2bbbabae12 "Buddy")](https://app.buddy.works/mzpp/mzpp---p--bitbucket-instance/pipelines/pipeline/300110)
[![Travis CI](https://travis-ci.org/mateusz-szczesny/arthub-api.svg)](https://travis-ci.com/github/mateusz-szczesny/arthub-api)
[![Circle CI](https://circleci.com/gh/mateusz-szczesny/arthub-api.svg?style=svg "CircleCI")](https://app.circleci.com/pipelines/github/mateusz-szczesny/arthub-api)

# ArtHub (Aplikacja Serwerowa)

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


test
