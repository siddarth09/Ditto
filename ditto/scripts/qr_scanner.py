#!/usr/bin/python3

import rospy
from ditto.msg import OTP
from camera_node import OAKD
import cv2
import depthai as dai
import numpy as np

class QR():
    def __init__(self):
        self.otp= rospy.Subscriber('/otp',OTP,self.get_data)

    def get_camera(self):
        camera=OAKD()
        pipeline = dai.Pipeline()
        # Set up left and right cameras
        cam = camera.getColorCam(pipeline)
        # Set output Xlink for left camera
        xoutLeft = pipeline.create(dai.node.XLinkOut)
        xoutLeft.setStreamName("rgb")
        # Attach cameras to output Xlink
        cam.preview.link(xoutLeft.input)
        
        # Pipeline is defined, now we can connect to the device
        with dai.Device(pipeline) as device:

            # Get output queues. 
            Queue = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)
            
            # Set display window name
            
            while True:
                # Get left frame
                Frame = camera.getFrame(Queue)
                #rospy.loginfo("USB SPEED= {}".format(device.getUsbSpeed().name))
                # Display output image
                cv2.imshow("QR SCANNER",Frame)
                
                # Check for keyboard input
                key = cv2.waitKey(1)
                if key == ord('q'):
                    # Quit when q is pressed
                    break
                
    def get_data(self,msg):
        self.passcode=msg.password
        
        



if __name__=="__main__":

    scanner=QR()
    scanner.get_camera()