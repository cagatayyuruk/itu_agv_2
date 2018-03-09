#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from math import pi

TCP_IP = '192.168.74.5'
TCP_PORT = 8001
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard Z %s", data.angular.z)
    rospy.loginfo(rospy.get_caller_id() + "I heard X %s", data.linear.x)
    x = data.linear.x
    w = data.angular.z
       
    #calculate linear velocities and get wheel rpm values  (v - e w) / R
    L = 0.245
    R = 0.1

    vr = (2*x+w*L)/2*R
    vl = (2*x-w*L)/2*R
    
    vl = format(vl, '.2f')           
    vr = format(vr, '.2f')      
            
    message = str(vl) + ":" + str(vr) + ";"            
    print message            
    s.send(message)
    
def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('agvSend', anonymous=True)

    rospy.Subscriber("turtle1/cmd_vel", Twist, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
