#!/bin/bash

source /opt/ros/foxy/setup.bash
source /usr/share/colcon_cd/function/colcon_cd.sh
export _colcon_cd_root=~/ros2_install
export ROS_DOMAIN_ID=13
source ~/ros2_ws/install/local_setup.bash

while true; do
    /opt/ros/foxy/bin/ros2 run kurwatron drive
    sleep 1
done
