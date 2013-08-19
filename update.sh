#!/bin/sh

git reset --hard
$HOME/.virtualenvs/herbalcell/bin/python manage.py update-$1
$HOME/.virtualenvs/herbalcell/bin/python manage.py clear-cache
$HOME/.virtualenvs/herbalcell/bin/python manage.py collectstatic -l
touch tmp/restart.txt
