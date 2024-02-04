#!/usr/bin/env bash
set -e

# Setup

CYAN='\033[0;36m'
RED='\033[31m'
NC='\033[0m' # No Color

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.."
SCRIPTS_DIR="$DIR/scripts"

VENV_DIR="$DIR/venv"
if [ $# -gt 1 ]
then
    VENV_DIR=$2
fi

COREVERSION="latest"
if [ $# -gt 2 ]
then
    COREVERSION=$3
fi

# Take the user
USER=$(whoami)
echo "User Raspberry Pi: $USER"

USER_DIR="/home/$USER"

echo -e "${CYAN}DIR=$DIR - VENV_DIR=$VENV_DIR - USER=$USER - COREVERSION=$COREVERSION ${NC}"

$SCRIPTS_DIR/update_file.sh $USER


function gitPull() {
    echo -e "${RED}Git repository update...${NC}"
    git pull
}

function aptUpgrade() {
    # Update raspbian and install programm utils
    echo -e "${RED}Updating Raspberry Pi OS...${NC}"
    sudo apt install --fix-missing
    sudo apt update && sudo apt dist-upgrade -y
    echo -e "${RED}Installing needed programs...${NC}"
    sudo apt install -y python3-pip  python3-venv python3-dev tcl tmux supervisor nginx redis-server ntpdate
}

function aptInstall() {
    echo -e "${RED}Updating Raspberry Pi OS...${NC}"
    sudo apt install --fix-missing
    echo -e "${RED}Installing needed programs...${NC}"
    # sudo apt install -y libgtk2.0-dev libraspberrypi-dev
    # sudo apt install -y python3-kms++ libcap-dev libcamera-dev
    sudo apt install -y tesseract-ocr 
    sudo apt install -y python3-picamera2 --no-install-recommends
    # sudo apt install -y build-essential tesseract-ocr libgl1-mesa-glx
    # sudo apt install -y python3-numpy build-essential tesseract-ocr libjpeg-dev libpng-dev libavcodec-dev libavformat-dev \
    #     libswscale-dev libgtk2.0-dev libcanberra-gtk* libgtk-3-dev libgstreamer1.0-dev gstreamer1.0-gtk3 libgstreamer-plugins-base1.0-dev gstreamer1.0-gl \
    #     libx264-dev libtbb-dev libv4l-dev v4l-utils libopenblas-dev libatlas-base-dev libblas-dev liblapack-dev gfortran libhdf5-dev \
    #     libprotobuf-dev libgoogle-glog-dev libgflags-dev protobuf-compiler
}

function aptRemove() {
    echo -e "${RED}Remove apt packages...${NC}"
    sudo apt remove --purge -y python3-numpy build-essential tesseract-ocr libjpeg-dev libpng-dev libavcodec-dev libavformat-dev \
        libswscale-dev libgtk2.0-dev libcanberra-gtk* libgtk-3-dev libgstreamer1.0-dev gstreamer1.0-gtk3 libgstreamer-plugins-base1.0-dev gstreamer1.0-gl \
        libx264-dev libtbb-dev libv4l-dev v4l-utils libopenblas-dev libatlas-base-dev libblas-dev liblapack-dev gfortran libhdf5-dev \
        libprotobuf-dev libgoogle-glog-dev libgflags-dev protobuf-compiler
    sudo apt autoremove --purge -y
}

function supervisorUpdate() {
    # Supervisor update
    echo -e "${RED}Supervisor configuration update...${NC}"
    sudo mv -v /tmp/flask_webapp.conf /etc/supervisor/conf.d
    sudo supervisorctl reread
    sudo supervisorctl update
}

function nginxUpdate() {
    # Nginx update
    echo -e "${RED}Nginx configuration update...${NC}"
    sudo cp -v $DIR/FOLDER_FOR_INSTALL/default /etc/nginx/sites-available/
    sudo nginx -t
    sudo systemctl restart nginx
}

function serviceStop() {
    echo -e "${RED}Stop services...${NC}"
    sudo supervisorctl stop all
    wait
}

function serviceStart() {
    echo -e "${RED}Start services...${NC}"
    sudo supervisorctl start all
    wait
}

function pythonEnv() {
    # Environnement create
    if [ ! -d "$VENV_DIR" ]
    then
        echo -e "${RED}Installing needed Python additions...${NC}"
        pip3 config set global.trusted-host "pypi.org files.pythonhosted.org pypi.python.org"
        # wget https://bootstrap.pypa.io/get-pip.py -e https_proxy="$URL_PROXY"
        # sudo python3 get-pip.py
        # rm get-pip.py
        echo -e "${RED}Creating Python environment...${NC}"
        python3 -m venv $VENV_DIR --system-site-packages
        echo -e "${RED}Install Python package...${NC}"
        $VENV_DIR/bin/python -m pip install wheel setuptools pip --upgrade
        $VENV_DIR/bin/python -m pip install -r requirements.txt  --verbose
    else
        # Update Python environnement
        echo -e "${RED}Update Python environment...${NC}"
        $VENV_DIR/bin/python -m pip install wheel setuptools pip --upgrade
        $DIR/venv/bin/python -m pip install --upgrade -r requirements.txt --verbose
    fi
}

function pythonDevUpdate() {
    if [ -d "$VENV_DIR" ]
    then
        # Update Python environnement
        echo -e "${RED}Update Python Dev environment...${NC}"
        $DIR/venv/bin/python -m pip install --upgrade -r requirements_dev.txt
    fi
    echo -e "${RED}Update Python Dev environment completed...${NC}"
}

function install() {
    aptUpgrade
    aptInstall
    pythonEnv

    sudo mkdir -pv /mnt/CSD/
    sudo chown -R $USER:$USER /mnt/CSD/
    chmod -R 0777 /mnt/CSD

    # copy files config RasPi
    echo -e "${RED}Copy files config RasPi...${NC}"
    sudo cp -v $DIR/FOLDER_FOR_INSTALL/motd.tcl /etc/
    sudo chmod 755 /etc/motd.tcl
    
    supervisorUpdate
    nginxUpdate
    serviceStart

    echo -e "${RED}Install completed...${NC}"
}

function update() {
    echo -e "${RED}Update CanPi...${NC}"
    serviceStop
    aptUpgrade
    aptInstall
    pythonEnv

    supervisorUpdate
    nginxUpdate
    serviceStart

    echo -e "${RED}Update completed...${NC}"
}


# Commands

case $1 in
    "install")
        install
        ;;
    "pull")
        gitPull
        ;;
    "update")
        # gitPull
        update
        ;;
    "dev")
        pythonDevUpdate
        ;;
esac
