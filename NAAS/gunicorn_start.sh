#!/bin/bash
NAME="NAAS"
DJANGODIR=/opt/NAAS
SOCKFILE=/opt/NAAS/run/gunicorn.sock
USER=root
GROUP=root
NUM_WORKERS=3
DJANGO_SETTINGS_MODULE=NAAS.settings
DJANGO_WSGI_MODULE=NAAS.wsgi
cd $DJANGODIR
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR
echo 'yes' | python3 manage.py collectstatic
python3 manage.py makemigrations
python3 manage.py migrate
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
--name $NAME \
--workers $NUM_WORKERS \
--user=$USER --group=$GROUP \
--bind=unix:$SOCKFILE \
--log-level=debug \
--log-file=-