# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#https://github.com/ros2/demos/blob/foxy/quality_of_service_demo/rclpy/quality_of_service_demo_py/common_nodes.py
#https://github.com/ros2/demos/blob/foxy/quality_of_service_demo/rclpy/quality_of_service_demo_py/liveliness.py

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSLivelinessPolicy
from rclpy.qos import QoSProfile
from rclpy.duration import Duration
from rclpy.logging import get_logger
from rclpy.qos_event import SubscriptionEventCallbacks
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
import time
import adafruit_pca9685
from adafruit_servokit import ServoKit
import serial
import board
import busio



global thrinit, strinit, maxr, minl, maxthr, minthr, throttle, reverse, steer, newthrvalue, newstrvalue, comm



maxr=180
minl=0
maxthr=180
minthr= 0
thrinit = 90
strinit = 90
throttle = 0
reverse = 0
steer = 0
thrvalue = 0
revvalue = 0
strvalue = 0
newthrvalue = 0
newstrvalue = 0




kit = ServoKit(channels=16, address=0x40)
print("Initializing IO System - kit")

i2c = busio.I2C(board.SCL, board.SDA)
print("Initializing IO System - board")

pca = adafruit_pca9685.PCA9685(i2c)
print("Initializing IO System - pca")

pca.frequency = 100
print("Initializing IO System - freq")

kit.servo[0].angle = thrinit
print("Initializing Propulsion System")
time.sleep(1)

kit.servo[1].angle = strinit
print("Initializing Steering System")
time.sleep(1)



class KurwatronDrive(Node):

    def __init__(self, qos_profile, event_callbacks):
        super().__init__('kurwatron_drive')
        #self.subscription = None
        self.qos_profile = qos_profile
        self.event_callbacks = event_callbacks
        self.subscription = self.create_subscription(
            Twist,
            'cmd_vel',
            self.listener_callback,
            10)
        self.subscription #prevent unused variable warning

    def listener_callback(self, msg):
        global comm, throttle, reverse, steer
        throttle=msg.linear.x
        reverse=msg.linear.y
        steer=msg.angular.z
        
        comm = True

        self.get_logger().info('Forward: "%s"' % throttle)
        self.get_logger().info('Reverse: "%s"' % reverse)
        self.get_logger().info('Steer: "%s"' % steer)
        self.get_logger().info('comm: "%s"' % comm)



def convertscales(thrvalue,revvalue,strvalue):
    global newthrvalue, newstrvalue
    # 0=1-1  max=-1-1=-2	min=1--1=2
    newthrvalue = int(90+((thrvalue)-(revvalue))*-45)
    
    #limit throttle
    if newthrvalue > maxthr:
        newthrvalue = maxthr
    if newthrvalue < minthr:
        newthrvalue = minthr
    
            
    if strvalue < 0:
        strvalue = -strvalue
        newstrvalue=int(strinit+(strvalue*((maxr-strinit)/3)))
    else:
        newstrvalue=int(strinit-(strvalue*((strinit-minl)/3)))
    
    #limit steering
    if newstrvalue > maxr:
        newstrvalue = maxr
    if newstrvalue < minl:
        newstrvalue = minl
        
    print("converstscales:  Throttle="+str(newthrvalue)+" ,  Steering="+str(newstrvalue))
    



def send_pwm(thrnum,strnum):
    print("send PWM:  Throttle="+str(thrnum)+" ,  Steering="+str(strnum))
    kit.servo[0].angle = thrnum
    kit.servo[1].angle = strnum



def main(args=None):
    global thrinit, strinit, maxr, minl, maxthr, minthr, throttle, reverse, steer, newthrvalue, newstrvalue, comm
    comm = False
    
    
    rclpy.init(args=args)
    
    liveliness_lease_duration = Duration(seconds= 3 /1000.0)
    
    qos_profile = QoSProfile(
        depth=10,
        liveliness=QoSLivelinessPolicy.RMW_QOS_POLICY_LIVELINESS_AUTOMATIC,
        liveliness_lease_duration=liveliness_lease_duration)
        
    subscription_callbacks = SubscriptionEventCallbacks(liveliness=lambda event: get_logger('KurwatronDrive').info(str(event)))
    kurwatron_drive = KurwatronDrive(qos_profile, event_callbacks=subscription_callbacks)

    while True:
        if not comm:
            send_pwm(90,90)
            rclpy.spin_once(kurwatron_drive,timeout_sec=1)
        while comm:
            print("while comm")
            comm = False
            rclpy.spin_once(kurwatron_drive,timeout_sec=1)
            if not comm:
                break
            else:
                convertscales(throttle,reverse,steer)
                send_pwm(newthrvalue,newstrvalue)
             
    
    # cmd_vel werte senden wenn kein timeout passiert ist
   

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    kurwatron_drive.destroy_node()
    rclpy.shutdown()



if __name__ == '__main__':
    main()