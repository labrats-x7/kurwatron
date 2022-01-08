# kurwatron
ROS 2 (Foxy) package for Raspberry Pi 4, a pca9685 PWM board and camera for teleoperation of a "Ripsaw" style tracked rover

Install:

Set up ROS2 Foxy on Ubuntu Server 20.04 for Raspberry Pi 4B +2Gb:
https://roboticsbackend.com/install-ubuntu-on-raspberry-pi-without-monitor/

Install ROS2 Foxy on your fresh Ubuntu Server 20.04 install:

Setup locale:
sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

Setup sources
sudo apt update && sudo apt install curl gnupg2 lsb-release
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key  -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(source /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

Install ROS2 core packages:
sudo apt update
sudo apt install ros-foxy-ros-base

Install colcon:
sudo apt install python3-colcon-common-extensions

Install auto completion:
sudo apt install python3-pip
pip3 install argcomplete


install python pca9685, ... packages

Setup environment:

sudo nano ~/.bashrc
and add the following 5 lines:

source /opt/ros/foxy/setup.bash
source /usr/share/colcon_cd/function/colcon_cd.sh
source ~/ros2_ws/install/local_setup.bash
export _colcon_cd_root=~/ros2_install
export ROS_DOMAIN_ID=13



Setup VPN for Fritzbox:
sudo apt install vpnc
configure VPN connection:
sudo touch /etc/vpnc/fritzbox.conf
sudo nano /etc/vpnc/fritzbox.conf
Install AutoVPN-script:
cp autovpnsript.sh /etc/init.d/autovpnsript.sh
sudo chmod +x /etc/init.d/autovpnsript.sh
sudo crontab -a
*/2 * * * * /etc/init.d/autovpnscript.sh


Build kurwatron ROS2 package:
cd ~/ros2_ws
colcon build --packages-select kurwatron --allow-overriding kurwatron

Source:
source ros2_ws/install/local_setup.bash

Run (Rover):

uhubctl -l 1-1 -a 2 -R

i2cdetect -y 1
ros2 topic echo cmd_vel

ros2 run v4l2_camera v4l2_camera_node -p reliability:=best_effort
ros2 param list /v4l2_camera
ros2 param set /v4l2_camera image_size [320,240]

ros2 run kurwatron drive





Run (Base):

ros2 run rqt_image_view rqt_image_view --ros-args -p reliability:=best_effort
ros2 launch teleop_twist_joy teleop-launch.py joy_config:='ps3'

ros2 run image_transport republish compressed --ros-args --remap in/compressed:=/image_raw/compressed --ros-args --remap out:=image/decompressed

ros2 run rqt_reconfigure rqt_reconfigure
rqt_graph


PS4 Dualshock configuration (USB connected)
sudo gedit /opt/ros/foxy/share/teleop_twist_joy/config/ps3.config.yaml

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
