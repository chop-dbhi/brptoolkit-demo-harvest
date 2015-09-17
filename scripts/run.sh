#!/bin/sh

cd /opt/app

# Flush memcached
python -c "import memcache; mc = memcache.Client(['mc:11211'], debug=0); mc.flush_all()"

./bin/manage.py syncdb --noinput
./bin/manage.py migrate --noinput
./bin/manage.py collectstatic --noinput
./bin/manage.py rebuild_index --noinput




if [ "$(ls -A /opt/app)" ]; then
    if [ "$FORCE_SCRIPT_NAME" = "" ]; then
	exec /usr/local/bin/uwsgi --chdir /opt/app/ --die-on-term --http-socket 0.0.0.0:8000 -p 2 -b 32768 -T --master --max-requests 5000 --static-map $FORCE_SCRIPT_NAME/static=/opt/app/_site/static --static-map /static=/usr/local/lib/python2.7/site-packages/django/contrib/admin/static --module wsgi:application
    else
        exec /usr/local/bin/uwsgi --chdir /opt/app/ --die-on-term --uwsgi-socket 0.0.0.0:8000 -p 2 -b 32768 -T --master --max-requests 5000 --static-map $FORCE_SCRIPT_NAME/static=/opt/app/_site/static --static-map /static=/usr/local/lib/python2.7/site-packages/django/contrib/admin/static --module wsgi:application
    fi
fi
