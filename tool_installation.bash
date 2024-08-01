sudo apt install python3-colcon-common-extensions
sudo apt install git-all
source /opt/ros/humble/setup.bash
sudo apt update
sudo rosdep init
rosdep update
sudo apt install python3-pip
pip install setuptools==58.2.0
python3 -m pip install -U pygame==2.6.0
sudo pip install adafruit-blinka
sudo pip install RPi.GPIO
pip install --user --no-cache-dir adafruit-circuitpython-neopixel
sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel

