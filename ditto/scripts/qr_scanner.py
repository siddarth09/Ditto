#!/usr/bin/python3

import rospy
from std_msgs.msg import Int32

import cv2
import depthai as dai
import numpy as np
from time import sleep

class OAKD():
    def __init__(self):
        pass
    
    def getFrame(self,queue):
        # Get frame from queue
        self.frame = queue.get()
        # Convert frame to OpenCV format and return
        return self.frame.getCvFrame()
        
    def getMonoCamera(self,pipeline):
        # Configure mono camera
        mono = pipeline.createMonoCamera()

        # Set Camera Resolution
        mono.setResolution(dai.MonoCameraProperties.SensorResolution.THE_480_P)
        mono.setBoardSocket(dai.CameraBoardSocket.RGB)
        
        return mono

    def getColorCam(self,pipeline):
        rgb=pipeline.create(dai.node.ColorCamera)
        rgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)
        
        return rgb

class QR():
    def __init__(self):
        
        self.passcode=0
        self.qrdata=0
        rospy.Subscriber('/otp',Int32,callback=self.get_data)

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
            detector = cv2.QRCodeDetector()
            # Set display window name
            
            while True:
                # Get left frame
                Frame = camera.getFrame(Queue)
                data, bbox, _ = detector.detectAndDecode(Frame)
                # check if there is a QRCode in the image
                if data:
                    rospy.loginfo("QRCODE FOUND")
                    sleep(3)
                    self.qrdata=data
                    break
                else:
                    rospy.loginfo("NO QRCode found")
                self.qrdata=data
                cv2.imshow("QRCODEscanner", Frame)    
                if cv2.waitKey(1) == ord("q"):
                    break           

    def get_data(self,msg):
        
        self.passcode=msg.data

    def verify(self):
        self.get_camera()
        if (self.passcode == self.qrdata):
            rospy.loginfo(self.passcode)
            rospy.loginfo(self.qrdata)
            rospy.loginfo("SUCCESS")
        else:
            rospy.loginfo(self.passcode)
            rospy.loginfo(self.qrdata)
            rospy.loginfo("FAILURE")

if __name__=="__main__":
    rospy.init_node('qr_scan')
    scanner=QR()
    scanner.verify()
    
    