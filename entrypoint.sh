# PORT from environment variable
PORT=${PORT:-3000}
export PORT=$PORT

#!/bin/bash
set -e

# Set cronjob to apply interest every 24h
crontab scheduler.txt
crontab -l
service cron start

# Start supervisord
exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf
