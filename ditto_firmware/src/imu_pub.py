#!/usr/bin/python3

import rospy
from sensor_msgs.msg import Imu
import smbus
import tf

# MPU6050 Registers
PWR_MGMT_1 = 0x6B
SMPLRT_DIV = 0x19
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
INT_ENABLE = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H = 0x47

bus = smbus.SMBus(1)  # or 0 for older Raspberry Pi boards
address = 0x68  # MPU6050 address
tf_broadcaster = tf.TransformBroadcaster()

# Initialize MPU6050
def init_mpu():
    bus.write_byte_data(address, SMPLRT_DIV, 0)
    bus.write_byte_data(address, PWR_MGMT_1, 1)
    bus.write_byte_data(address, CONFIG, 0)
    bus.write_byte_data(address, GYRO_CONFIG, 24)
    bus.write_byte_data(address, INT_ENABLE, 1)

def publish_transform():
    # Publish transform from "imu_link" to "base_link"
    tf_broadcaster.sendTransform(
        (0.1, 0.2, 0.3),  # translation
        (0.0, 0.0, 0.0, 1.0),  # rotation
        rospy.Time.now(),
        "base_link",
        "imu_link"
    )

# Read raw data from MPU6050
def read_raw_data(addr):
    high = bus.read_byte_data(address, addr)
    low = bus.read_byte_data(address, addr + 1)
    value = ((high << 8) | low)
    if (value > 32768):
        value = value - 65536
    return value

def imu_publisher():
    # Initialize ROS node
    rospy.init_node('imu_publisher', anonymous=True)
    rate = rospy.Rate(10)  # 10 Hz
    rospy.loginfo("IMU STARTED")
    # Initialize IMU message
    imu_msg = Imu()
    imu_msg.header.frame_id = "imu_link"

    # Initialize MPU6050
    init_mpu()

    # Publish IMU message
    imu_pub = rospy.Publisher('/imu', Imu, queue_size=10)

    while not rospy.is_shutdown():
        # Read raw data from MPU6050
        accel_x = read_raw_data(ACCEL_XOUT_H)
        accel_y = read_raw_data(ACCEL_YOUT_H)
        accel_z = read_raw_data(ACCEL_ZOUT_H)
        gyro_x = read_raw_data(GYRO_XOUT_H)
        gyro_y = read_raw_data(GYRO_YOUT_H)
        gyro_z = read_raw_data(GYRO_ZOUT_H)

        # Convert raw data to SI units
        accel_scale = 16384.0  # LSB/g
        gyro_scale = 131.0  # LSB/deg/s
        imu_msg.linear_acceleration.x = accel_x / accel_scale
        imu_msg.linear_acceleration.y = accel_y / accel_scale
        imu_msg.linear_acceleration.z = accel_z / accel_scale
        imu_msg.angular_velocity.x = gyro_x / gyro_scale
        imu_msg.angular_velocity.y = gyro_y / gyro_scale
        imu_msg.angular_velocity.z = gyro_z / gyro_scale

        # Set orientation covariance to -1 to indicate that orientation is not provided
        imu_msg.orientation_covariance[0] = -1
        imu_msg.orientation_covariance[4] = -1
        imu_msg.orientation_covariance[8] = -1
        

        # Publish IMU message
        imu_msg.header.stamp = rospy.Time.now()
        imu_pub.publish(imu_msg)
        rate.sleep()
        publish_transform()

if __name__ == '__main__':
    try:
        imu_publisher()
    except rospy.ROSInterruptException:
        rospy.warn("IMU STOPPED")
