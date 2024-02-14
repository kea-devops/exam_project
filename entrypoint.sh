# PORT from environment variable
PORT=${PORT:-3000}
export PORT=$PORT

#!/bin/bash
set -e

# Start supervisord
python manage.py check --deploy
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py provision
exec gunicorn project.asgi:application -b 0.0.0.0:$PORT -k uvicorn.workers.UvicornWorker
# exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf
