web: gunicorn clup.wsgi:application --log-file - --log-level debug
python src/manage.py collectstatic --noinput
manage.py migrate