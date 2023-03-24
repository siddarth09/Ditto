#!/usr/bin/python3

import rospy
from ditto.msg import OTP
from std_msgs.msg import Int32
import pyqrcode
import random


def pub():
    otp=random.randint(1000,9999)
    rospy.init_node('otp_gen',anonymous=True)
    pub=rospy.Publisher("/otp",Int32,queue_size=10)
    qr=pyqrcode.create(otp,version=10)
    qr.png('otp.png',scale=6)

    while not rospy.is_shutdown():
        
        
        msg=1216
        #msg.location="BLR"
        pub.publish(msg)
        rospy.loginfo(msg)
        rospy.Rate(10).sleep()
if __name__=='__main__':
    pub()