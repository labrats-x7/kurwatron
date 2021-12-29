# kurwatron
ROS 2 (Foxy) package for Raspberry Pi 4, a pca9685 PWM board and camera for teleoperation of a "Ripsaw" style tracked rover



Build:
cd ~/ros2_ws
colcon build --packages-select kurwatron --allow-overriding kurwatron

Source:
source ros2_ws/install/local_setup.bash

Run (Rover):

i2cdetect -y 1
ros2 topic echo cmd_vel

ros2 run v4l2_camera v4l2_camera_node -p reliability:=best_effort
ros2 param list /v4l2_camera
ros2 run image_transport republish compressed --ros-args --remap in/compressed:=/camera1/color/image_raw/compressed --ros-args --remap out:=image/decompressed

ros2 run kurwatron drive





Run (Base):

ros2 run rqt_image_view rqt_image_view --ros-args -p reliability:=best_effort
ros2 launch teleop_twist_joy teleop-launch.py joy_config:='ps3'


ros2 run rqt_reconfigure rqt_reconfigure
rqt_graph


PS4 Dualshock configuration (USB connected)
sudo gedit /opt/ros/foxy/share/teleop_twist_joy/config/ps3.config.yaml

teleop_twist_joy_node:
  ros__parameters:
    axis_linear:
      x: 5
    scale_linear:
      x: 0.4
    scale_linear_turbo:
      x: 1.0

    axis_linear:
      y: 2
    scale_linear:
      y: 0.4
    scale_linear_turbo:
      y: 1.0

    axis_angular:
      yaw: 3
    scale_angular:
      yaw: 0.2
    scale_angular_turbo:
      yaw: 0.1

    enable_button: 5  # L1 shoulder button
    enable_turbo_button: 4  # R1 shoulder button