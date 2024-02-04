#!/usr/bin/env bash
set -e

# Setup
CYAN='\033[0;36m'
RED='\033[31m'
NC='\033[0m' # No Color

FILE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/../FOLDER_FOR_INSTALL"

USER="pi"
if [ $# -gt 0 ]
then
    USER=$1
fi
PROG_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.."


cat << EOF > /tmp/flask_webapp.conf
[program:flask-webapp]
directory = $PROG_DIR
command = $PROG_DIR/venv/bin/python -m gunicorn -w 2 -b 127.0.0.1:8000 wsgi:app
user = $USER
autostart = true
autorestart = true

stdout_logfile = /dev/null
stderr_logfile = /dev/null
EOF
