web: python slang/manage.py collectstatic --noinput; gunicorn_django --workers=1 --bind=0.0.0.0:$PORT slang/settings.py 