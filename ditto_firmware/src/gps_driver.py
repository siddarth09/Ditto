#!/usr/bin/python

import rospy
from sensor_msgs.msg import NavSatFix
import serial

def main():
    rospy.init_node('gps_publisher')
    rate = rospy.Rate(10)  # 10 Hz

    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    gps_pub = rospy.Publisher('/fix', NavSatFix, queue_size=10)

    while not rospy.is_shutdown():
        line = ser.readline().decode('ascii')
        if line.startswith('$GPGGA'):
            data = line.split(',')
            if data[2] and data[4] and data[9]:
                lat = float(data[2][:2]) + float(data[2][2:]) / 60.0
                if data[3] == 'S':
                    lat = -lat
                lon = float(data[4][:3]) + float(data[4][3:]) / 60.0
                if data[5] == 'W':
                    lon = -lon
                alt = float(data[9])

                fix_msg = NavSatFix()
                fix_msg.header.stamp = rospy.Time.now()
                fix_msg.header.frame_id = 'gps'
                fix_msg.latitude = lat
                fix_msg.longitude = lon
                fix_msg.altitude = alt

                gps_pub.publish(fix_msg)

        rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
