#!/usr/bin/env python

import socket
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from math import pi

TCP_IP = '192.168.74.5'
TCP_PORT = 8001
BUFFER_SIZE = 30

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.angular.z)
    rospy.loginfo(rospy.get_caller_id() + "I heard X %s", data.linear.x)
    r = 0

    if data.angular.z > 0:
        r = (data.linear.x/data.angular.z)
        #calculate linear velocities and get wheel rpm values
        vl = ((data.angular.z*(r-0.245))/(0.2*pi))*60
        vr = ((data.angular.z*(r+0.245))/(0.2*pi))*60
    else:
        vl=((data.linear.x)/(0.2*pi))*60
        vr=((data.linear.x)/(0.2*pi))*60
    
    vl = round(vl,0)            
    vr = round(vr,0)        
            
    message = str(vl) + ":" + str(vr) + ";" 
    k= len(message)
    for x in range (0,30-k)
        message += message + "a"         
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
