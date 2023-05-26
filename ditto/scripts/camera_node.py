#!/usr/bin/python3

import cv2
import depthai as dai

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
