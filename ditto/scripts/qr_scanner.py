#!/usr/bin/python3

import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import Int32
from cv_bridge import CvBridge
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image,CompressedImage
import cv2
import numpy as np
from time import sleep
import pyrebase

from std_srvs.srv import SetBool, SetBoolResponse

class QR():
    def __init__(self):
        # Initialize member variables
        self.passcode = 0
        self.qrdata = 0
        self.last_image = None
        
        # Set up Firebase connection
        self.firebaseConfig = {
                                "apiKey": "AIzaSyBpi-oM5Yxpp-9d0PmBUkGDUz1Q_tQpHLM",
                                "authDomain": "ditto-2b57b.firebaseapp.com",
                                "databaseURL": "https://ditto-2b57b-default-rtdb.firebaseio.com",
                                "projectId": "ditto-2b57b",
                                "storageBucket": "ditto-2b57b.appspot.com",
                                "messagingSenderId": "623176561332",
                                "appId": "1:623176561332:web:365da031201202ffc69de1",
                                "measurementId": "G-TTT6H08PF8"
                                }
        self.firebase = pyrebase.initialize_app(self.firebaseConfig)
        
        # Set up ROS subscribers
        self.bridge = CvBridge()
        rospy.Subscriber('/rgb_stereo_publisher/color/image/compressed', CompressedImage, self.image_callback)
        rospy.loginfo("SCANNER SERVICE STARTED and IS RUNNING....")
        
    def image_callback(self, msg):
        try:
            # Convert image message to OpenCV format
            rospy.loginfo_once("CAMERA STARTED")
            self.last_image = self.bridge.compressed_imgmsg_to_cv2(msg, "bgr8")
        except CvBridgeError as e:
            rospy.logerr(e)
            
   
        
    def verify(self, req):
        # Get passcode from Firebase
        db = self.firebase.database()
        self.passcode = db.child('OTP').get().val()
        
        # Initialize QR detector
        detector = cv2.QRCodeDetector()
        
        # Set up service server to turn on/off QR scanning
        self.scanning_enabled = req.data
        
        
        while not rospy.is_shutdown():
            # Check if QR scanning is enabled
            if not self.scanning_enabled:
                rospy.logwarn("QR scanning disabled.")
                break
            else:
                rospy.loginfo("QR Scanning Started")
                # Check if there is a QR code in the last received image
                if self.last_image is not None:
                    data, bbox, _ = detector.detectAndDecode(self.last_image)
                    
                    if data:
                        rospy.loginfo("QRCODE FOUND")
                        sleep(3)
                        self.qrdata = data
                        
                    else:
                        rospy.loginfo("NO QRCode found")
                        self.qrdata = None
                
                # Sleep for a short time before checking again
                sleep(0.1)
            
            if self.qrdata is not None:
                if self.passcode == int(self.qrdata):
                    rospy.loginfo(self.passcode)
                    rospy.loginfo(self.qrdata)
                    rospy.loginfo("SUCCESS")
                    return SetBoolResponse(success=True)
                else:
                    rospy.loginfo(self.passcode)
                    rospy.loginfo(self.qrdata)
                    rospy.loginfo("FAILURE")
                    return SetBoolResponse(success=False)
            else:
                rospy.loginfo("No QR code detected.")
                return SetBoolResponse(success=False)
        rospy.loginfo("QR scanning stopped.")
        return SetBoolResponse(success=False)

    def handle_toggle_qr_scanning(self, req):
        self.qr_scanning_enabled = req.data
        rospy.loginfo("QR scanning is now " + ("enabled" if self.qr_scanning_enabled else "disabled"))
        return SetBoolResponse(success=True)


if __name__=="__main__":
    rospy.init_node('qr_scan')
    scanner=QR()
    #scanner.verify()
    rospy.Service('start_qr_scan', SetBool, scanner.verify)
    rospy.spin()
