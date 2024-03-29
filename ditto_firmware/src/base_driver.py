#!/usr/bin/python3
import rospy
from geometry_msgs.msg import Twist
import RPi.GPIO as GPIO
import time
from math import pi

leftPWM = 12
rightPWM = 13

leftDir = 16
rightDir = 6


wheel_separation = 0.40
wheel_diameter = 0.065
wheel_radius = wheel_diameter/2
circumference_of_wheel = 2 * pi * wheel_radius

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(leftPWM,GPIO.OUT)
GPIO.setup(leftDir,GPIO.OUT)
GPIO.setup(rightPWM,GPIO.OUT)
GPIO.setup(rightDir,GPIO.OUT)

pwmL = GPIO.PWM(leftPWM, 100)
pwmL.start(0)
pwmR = GPIO.PWM(rightPWM, 100)
pwmR.start(0)

def stop():
    #print('stopping')
    pwmL.ChangeDutyCycle(0)
    GPIO.output(leftPWM, GPIO.HIGH)
    GPIO.output(leftDir, GPIO.HIGH)
    pwmR.ChangeDutyCycle(0)
    GPIO.output(rightPWM, GPIO.HIGH)
    GPIO.output(rightDir, GPIO.HIGH)


def forward(left_speed,right_speed):
    lspeed = min(((left_speed/0.2)*100),100)
    rspeed = min(((right_speed/0.2)*100),100)
    #print(str(left_speed)+" "+str(right_speed))
    pwmL.ChangeDutyCycle(lspeed)
    pwmR.ChangeDutyCycle(rspeed)
    GPIO.output(leftPWM, GPIO.HIGH)
    GPIO.output(leftDir, GPIO.LOW)
    GPIO.output(rightPWM, GPIO.HIGH)
    GPIO.output(rightDir, GPIO.HIGH)
    
def backward(left_speed,right_speed):
    lspeed = min(((left_speed/0.2)*100),100)
    rspeed = min(((right_speed/0.2)*100),100)
    #print(str(left_speed)+" "+str(right_speed))
    pwmL.ChangeDutyCycle(lspeed)
    pwmR.ChangeDutyCycle(rspeed)
    GPIO.output(leftPWM, GPIO.HIGH)
    GPIO.output(leftDir, GPIO.HIGH)
    GPIO.output(rightPWM, GPIO.LOW)
    GPIO.output(rightDir, GPIO.LOW)

def left(left_speed,right_speed):
    lspeed = min(((left_speed/0.2)*100),100)
    rspeed = min(((right_speed/0.2)*100),100)
    #print(str(left_speed)+" "+str(right_speed))
    pwmL.ChangeDutyCycle(lspeed)
    pwmR.ChangeDutyCycle(rspeed)
    GPIO.output(leftPWM, GPIO.HIGH)
    GPIO.output(leftDir, GPIO.LOW)
    GPIO.output(rightPWM, GPIO.LOW)
    GPIO.output(rightDir, GPIO.LOW)
    
def right(left_speed,right_speed):
    lspeed = min(((left_speed/0.2)*100),100)
    rspeed = min(((right_speed/0.2)*100),100)
    #print(str(left_speed)+" "+str(right_speed))
    pwmL.ChangeDutyCycle(lspeed)
    pwmR.ChangeDutyCycle(rspeed)
    GPIO.output(leftPWM, GPIO.HIGH)
    GPIO.output(leftDir, GPIO.HIGH)
    GPIO.output(rightPWM, GPIO.HIGH)
    GPIO.output(rightDir, GPIO.HIGH)
    
def callback(data):
    
    global wheel_radius
    global wheel_separation
    
    linear_vel = data.linear.x
    angular_vel = data.angular.z
    #print(str(linear)+"\t"+str(angular))
    
    rplusl  = ( 2 * linear_vel ) / wheel_radius
    rminusl = ( angular_vel * wheel_separation ) / wheel_radius
    
    right_omega = ( rplusl + rminusl ) / 2
    left_omega  = rplusl - right_omega 
    
    right_vel = right_omega * wheel_radius
    left_vel  = left_omega  * wheel_radius
    
    #print (str(left_vel)+"\t"+str(right_vel))
    '''
    left_speed  = abs ( linear - ( (wheel_separation/2) * (angular) ) )
    right_speed = abs ( linear - ( (wheel_separation/2) * (angular) ) )
    '''
    
    if (left_vel == 0.0 and right_vel == 0.0):
        stop()
    elif (left_vel >= 0.0 and right_vel >= 0.0):
        forward(abs(left_vel), abs(right_vel))
    elif (left_vel <= 0.0 and right_vel <= 0.0):
        backward(abs(left_vel), abs(right_vel))
    elif (left_vel < 0.0 and right_vel > 0.0):
        left(abs(left_vel), abs(right_vel))
    elif (left_vel > 0.0 and right_vel < 0.0):
        right(abs(left_vel), abs(right_vel))
    else:
        stop()
def listener():
    rospy.init_node('motorcontrol', anonymous=False)
    rospy.Subscriber("/cmd_vel", Twist, callback)
    rospy.spin()

if __name__== '__main__':
    print('DITTO STARTED')
    listener()