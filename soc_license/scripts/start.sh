#!/usr/bin/env bash

if ! [[ -f $PWD/data/db.sqlite3 ]] ;
then
  python manage.py migrate
  python manage.py loaddata $PWD/../tools/initial-data.json
fi

python manage.py runserver 0.0.0.0:8000