# PORT from environment variable
PORT=${PORT:-3000}
export PORT=$PORT

#!/bin/bash
set -e

# Start supervisord
exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf


# DOCKERFILE
FROM jenkins/jenkins:lts-alpine-jdk21

USER root

RUN apk update && apk add docker && apk add nodejs npm

USER jenkins

RUN jenkins-plugin-cli --plugins "blueocean docker-workflow"

# ENTRYPOINT
#!/bin/bash

if [[ "$1" == "--build" ]]; then
  docker build -t dind-jenkins:latest .
fi

docker stop jenkins
docker rm jenkins
docker stop dind
docker network disconnect jenkins nginx-proxy
docker network remove jenkins
docker network create jenkins
docker network connect jenkins nginx-proxy
