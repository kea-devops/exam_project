# PORT from environment variable
PORT=${PORT:-3000}
export PORT=$PORT

#!/bin/bash
set -e

# Start supervisord
exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf
