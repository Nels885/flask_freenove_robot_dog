#!/usr/bin/env bash
#
# CanPi (Raspberry Pi 2 or 3)
# setup script
#       Author: Lionel VOIRIN (Nels885)

set -e

cat << "EOF"
   .~ .~~~..~.     ____                     ____           
  : .~.'~'.~. :   /\  _`\                  /\  _`\   __    
 ~ (   ) (   ) ~  \ \ \/\_\     __      ___\ \ \L\ \/\_\   
( : '~'.~.'~' : )  \ \ \/_/_  /'__`\  /' _ `\ \ ,__/\/\ \  
 ~ .~ (   ) ~. ~    \ \ \L\ \/\ \L\.\_/\ \/\ \ \ \/  \ \ \ 
  (  : '~' :  )      \ \____/\ \__/.\_\ \_\ \_\ \_\   \ \_\
   '~ .~~~. ~'        \/___/  \/__/\/_/\/_/\/_/\/_/    \/_/
       '~'

EOF

cat << EOF
Open source Flask Freenove Robot Dog solution
Copyright 2023-$(date +'%Y'), Raspberry Pi solutions
https://github.com/Nels885, https://bitbucket.org/Nels885

===================================================

EOF

# Setup

CYAN='\033[0;36m'
RED='\033[31m'
NC='\033[0m' # No Color

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SCRIPTS_DIR="$DIR/scripts"
VENV_DIR="$DIR/venv"
if [ $# -eq 2 ]
then
    VENV_DIR=$2
fi

COREVERSION="1.0.0"

echo "raspi.sh version $COREVERSION"

# Functions

function checkPythonVersion() {
    ret=`python -c 'import sys; print("%i" % (sys.hexversion<0x03000000))'`
    if [ ! $ret -eq 0 ]
    then
        echo -e "${RED}we require python version > 3${NC}"
        sudo rm /usr/bin/python
        sudo ln -s /usr/bin/python3 /usr/bin/python
    fi
    python --version
}

function checkOutputDirExists() {
    if [ ! -d "$VENV_DIR" ]
    then
        echo "Cannot find a RasPi installation at $VENV_DIR."
        exit 1
    fi
}

function checkOutputDirNotExists() {
    if [ -d "$VENV_DIR" ]
    then
        echo "Looks like RasPi is already installed at $VENV_DIR."
        exit 1
    fi
}

function listCommands() {
cat << EOT
Available commands:

install
update
dev-env
help

See more at https://github.com/Nels885/canpi/wiki

EOT
}

# Commands

checkPythonVersion

case $1 in
    "install")
        checkOutputDirNotExists
        $SCRIPTS_DIR/run.sh install $VENV_DIR $COREVERSION
        ;;
    "update")
        checkOutputDirExists
        $SCRIPTS_DIR/run.sh update $VENV_DIR $COREVERSION
        ;;
    "dev-env")
        checkOutputDirExists
        $SCRIPTS_DIR/run.sh dev $VENV_DIR $COREVERSION
        ;;
    "help")
        listCommands
        ;;
    *)
        echo -e "${RED}No command found.${NC}"
        echo
        listCommands
esac
