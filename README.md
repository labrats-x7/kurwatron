# kurwatron
ROS 2 (Foxy) package for Raspberry Pi 4, a pca9685 PWM board and camera for teleoperation of a "Ripsaw" style tracked rover

## Install Ubuntu and ROS2 Foxy:

### Ubuntu Server 20.04 for Raspberry Pi 4B +2Gb:
follow: https://roboticsbackend.com/install-ubuntu-on-raspberry-pi-without-monitor/

#### add WiFi:
nano /boot/firmware/network-config

### Install ROS2 Foxy on your Ubuntu Server 20.04 install:

(https://roboticsbackend.com/install-ros2-on-raspberry-pi/)

#### Setup locale:
sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8


#### Setup sources
sudo apt update && sudo apt install curl gnupg2 lsb-release
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key  -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(source /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null


#### Install ROS2 core packages:
sudo apt update
sudo apt install ros-foxy-ros-base

#### Install colcon:
sudo apt install python3-colcon-common-extensions

#### Install auto completion:
sudo apt install python3-pip
pip3 install argcomplete

#### Setup environment:

sudo nano ~/.bashrc
and add the following 5 lines:

source /opt/ros/foxy/setup.bash
source /usr/share/colcon_cd/function/colcon_cd.sh
source ~/ros2_ws/install/local_setup.bash
export _colcon_cd_root=~/ros2_install
export ROS_DOMAIN_ID=13

#### install python packages:
sudo apt install python3-colcon-common-extensions
sudo pip3 install adafruit-pca9685
sudo pip3 install adafruit-circuitpython-servokit
sudo pip3 install serial

#### add user to i2c group
sudo groupadd i2c
sudo usermod -aG i2c ubuntu

#### Setup VPN autoconnect for Fritzbox:
sudo apt install vpnc
configure VPN connection:
sudo touch /etc/vpnc/fritzbox.conf
sudo nano /etc/vpnc/fritzbox.conf
Install AutoVPN-script:
cp autovpnsript.sh /etc/init.d/autovpnsript.sh
sudo chmod +x /etc/init.d/autovpnsript.sh
sudo crontab -a
*/2 * * * * /etc/init.d/autovpnscript.sh


## Load and build kurwatron ROS2 package:

### Load kurwatron package from git
mkdir ~/ros2_ws
cd ~/ros2_ws git clone https://github.com/labrats-x7/kurwatron.git
cd ~/ros2_ws

### build package with colcon
colcon build --packages-select kurwatron --allow-overriding kurwatron

### Source new build:
source ros2_ws/install/local_setup.bash



## Run (on ROS2 Rover instance):

### reset USB interface
uhubctl -l 1-1 -a 2 -R

### check i2c communication (ID 40 present?)
i2cdetect -y 1

### check if topics from Base (see below) are published and visible on rover?
ros2 topic echo cmd_vel

### start camera
ros2 run v4l2_camera v4l2_camera_node -p reliability:=best_effort
ros2 param list /v4l2_camera
ros2 param set /v4l2_camera image_size [320,240]

### start drive node
ros2 run kurwatron drive





## Base Station (ROS2 also on ROS_DOMAIN_ID 13)

### image
ros2 run rqt_image_view rqt_image_view --ros-args -p reliability:=best_effort
ros2 launch teleop_twist_joy teleop-launch.py joy_config:='ps3'

ros2 run image_transport republish compressed --ros-args --remap in/compressed:=/image_raw/compressed --ros-args --remap out:=image/decompressed


ros2 run rqt_reconfigure rqt_reconfigure
rqt_graph


### PS4 Dualshock configuration (USB connected)
sudo gedit /opt/ros/foxy/share/teleop_twist_joy/config/ps3.config.yaml

''''Json
teleop_twist_joy_node:
  ros__parameters:
    axis_linear:
      x: 5
    scale_linear:
      x: 0.2
    scale_linear_turbo:
      x: 0.4

    axis_linear:
      y: 2
    scale_linear:
      y: 0.2
    scale_linear_turbo:
      y: 0.4

    axis_angular:
      yaw: 3
    scale_angular:
      yaw: 0.6
    scale_angular_turbo:
      yaw: 0.7

    enable_button: 5  # L1 shoulder button
    enable_turbo_button: 4  # R1 shoulder button
''''
