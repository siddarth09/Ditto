#!/usr/bin/python3

import rospy
from std_msgs.msg import Int32
import pyqrcode
import random

otp=random.randint(1000,9999)

pub=rospy.Publisher('/otp',Int32,queue_size=10)
qr=pyqrcode.create(otp,version=10)
qr.png('otp.png',scale=6)

while not rospy.is_shutdown():
    rospy.init_node('otp_gen',anonymous=True)
    msg=Int32
    msg.data=otp
    pub.publish(msg)
    rospy.loginfo(msg.data)
    rospy.Rate(1).sleep()