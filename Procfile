web: gunicorn clup.wsgi:application
python src/manage.py collectstatic --noinput
manage.py migrate