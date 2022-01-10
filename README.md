# kurwatron
ROS 2 (Foxy) package for Raspberry Pi 4, a pca9685 PWM board and camera for teleoperation of a "Ripsaw" style tracked rover

![KurwaTron_1](/kurwatron_1.jpg) 
![KurwaTron_2](/kurwatron_2.jpg) 
![KurwaTron_3](/kurwatron_3.jpg) 



---
## Install Ubuntu and ROS2 Foxy:

### Ubuntu Server 20.04 for Raspberry Pi 4B +2Gb:
follow: https://roboticsbackend.com/install-ubuntu-on-raspberry-pi-without-monitor/

#### add WiFi:
```
nano /boot/firmware/network-config
```

### Install ROS2 Foxy on your Ubuntu Server 20.04 install:

(https://roboticsbackend.com/install-ros2-on-raspberry-pi/)

#### Setup locale:
```
sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8
```

#### Setup sources
```
sudo apt update && sudo apt install curl gnupg2 lsb-release
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key  -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(source /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
```

#### Install ROS2 core packages:
```
sudo apt update
sudo apt install ros-foxy-ros-base
```

#### Install colcon:
```
sudo apt install python3-colcon-common-extensions
```

#### Install auto completion:
```
sudo apt install python3-pip
pip3 install argcomplete
```

#### Setup environment:
```
sudo nano ~/.bashrc
```

and add the following 5 lines:

```
source /opt/ros/foxy/setup.bash
source /usr/share/colcon_cd/function/colcon_cd.sh
source ~/ros2_ws/install/local_setup.bash
export _colcon_cd_root=~/ros2_install
export ROS_DOMAIN_ID=13
```

#### install python packages:
```
sudo apt install python3-colcon-common-extensions
sudo pip3 install adafruit-pca9685
sudo pip3 install adafruit-circuitpython-servokit
sudo pip3 install serial
pip3 install adafruit-circuitpython-ssd1306
sudo apt-get install python3-pil


```

#### add user to i2c group
```
sudo groupadd i2c
sudo usermod -aG i2c ubuntu
```

#### Load kurwatron package from git
```
mkdir ~/ros2_ws/src
cd ~/ros2_ws/src git clone https://github.com/labrats-x7/kurwatron.git
```

---

### Setup VPN autoconnect for Fritzbox (if needed):
```
sudo apt install vpnc
```

#### configure VPN connection:

For Fritzbox VPN follow: http://www.kuemmel.wtf/?p=363
(Other VPN services are also possible but not covered here.)

```
sudo touch /etc/vpnc/fritzbox.conf
sudo nano /etc/vpnc/fritzbox.conf
```

#### Install AutoVPN-script:
```
cp ~ros2_ws/src/kurwatron/autovpnsript.sh /etc/init.d/autovpnsript.sh
sudo chmod +x /etc/init.d/autovpnsript.sh
sudo crontab -a
```
add the following line for a check every 2 minutes:
```
*/2 * * * * /etc/init.d/autovpnscript.sh
```

Adapt /etc/init.d/autovpnscript.sh file for your network configuration and VPN tool!

---

## Build kurwatron ROS2 package:


### Build package with colcon

Adapt the ~/ros2_ws/src/kurwatron/kurwatron/kurwatron_drive_node.py for your needs if you use another steering system like ackermann or differential drive :)

```
cd ~/ros2_ws
colcon build --packages-select kurwatron --allow-overriding kurwatron
```

### Source new build:
```
source ros2_ws/install/local_setup.bash
```

---

## Run (on ROS2 Rover instance):


### check i2c communication (ID 40 present?)
```
i2cdetect -y 1
```

### check if topics from Base (see below) are published and visible on rover?
```
ros2 topic echo cmd_vel
```

### start camera and set smaller picture size
```
gst-launch-1.0 -v v4l2src ! videoscale ! video/x-raw,width=800,height=600,framerate=20/1 ! avenc_mjpeg ! multipartmux ! tcpserversink port=8004 host=0.0.0.0
```

or on ROS2

```
ros2 run v4l2_camera v4l2_camera_node -p reliability:=best_effort
ros2 param set /v4l2_camera image_size [320,240]
```

### start drive node
```
ros2 run kurwatron drive
```

---


## Base Station (ROS2 installation on your computer)

### Setup environment:
```
sudo nano ~/.bashrc
```

and add the following 5 lines:

```
source /opt/ros/foxy/setup.bash
source /usr/share/colcon_cd/function/colcon_cd.sh
source ~/ros2_ws/install/local_setup.bash
export _colcon_cd_root=~/ros2_install
export ROS_DOMAIN_ID=13
```

### PS4 Dualshock configuration (USB connected)
```
sudo cp ~/ros2_ws/src/kurwatron/ps3.config.yaml /opt/ros/foxy/share/teleop_twist_joy/config/ps3.config.yaml
```

### uncompress and view image
```
ssh ubuntu@192.168.178.101 gst-launch-1.0 v4l2src ! videoconvert ! videoscale ! video/x-raw,width=800,height=600,framerate=15/1 ! avenc_mjpeg ! multipartmux ! fdsink | pv | ffplay -
```
or on ROS2 (high latency):

```
ros2 run image_transport republish compressed --ros-args --remap in/compressed:=/image_raw/compressed --ros-args --remap out:=image/decompressed --ros-args -p reliability:=best_effort
ros2 run rqt_image_view rqt_image_view --ros-args -p reliability:=best_effort
```

### start teloperation via ps4 controller

add autodrivestart.sh in crontab

```
crontab -e


```

```
ros2 launch teleop_twist_joy teleop-launch.py joy_config:='ps3'
```

control the rover :-)


---

### helpful tools
```
ros2 doctor
ros2 topic list
ros2 topic echo topic/to_echo
ros2 param list /v4l2_camera
ros2 run rqt_reconfigure rqt_reconfigure
rqt_graph
uhubctl -l 1-1 -a 2 -R
```

