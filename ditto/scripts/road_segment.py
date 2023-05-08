#!/usr/bin/env python3

import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import depthai

class RoadSegmentationNode:
    def __init__(self):
        # Initialize ROS node
        rospy.init_node('road_segmentation_node', anonymous=True)

        # Initialize Oak-D Lite device
        self.device = depthai.Device('')

        # Set up Oak-D Lite pipeline
        self.pipeline = depthai.Pipeline()

        cam_rgb = self.pipeline.createColorCamera()
        cam_rgb.setPreviewSize(300, 300)
        cam_rgb.setInterleaved(False)
        cam_rgb.setBoardSocket(depthai.CameraBoardSocket.RGB)

        detection_nn = self.pipeline.createNeuralNetwork()
        detection_nn.setBlobPath("/home/pi/catkin_ws/src/Ditto/ditto/resource/road-segmentation-adas-0001/road-segmentation-adas-0001.json")
        detection_nn.setNumPoolFrames(1)
        detection_nn.input.setBlocking(False)

        xout_rgb = self.pipeline.createXLinkOut()
        xout_rgb.setStreamName("rgb")
        xout_rgb.setMetadata({'frame': 'rgb'})
        xout_rgb.input.setQueueSize(1)
        xout_rgb.input.setBlocking(False)

        xout_nn = self.pipeline.createXLinkOut()
        xout_nn.setStreamName("nn")
        xout_nn.setMetadata({'frame': 'nn'})
        xout_nn.input.setQueueSize(1)
        xout_nn.input.setBlocking(False)

        cam_rgb.preview.link(detection_nn.input)
        detection_nn.passthrough.link(xout_rgb.input)
        detection_nn.out.link(xout_nn.input)

        # Create ROS publisher for road segmentation output
        self.bridge = CvBridge()
        self.image_pub = rospy.Publisher('/roadsegmentation/image_raw', Image, queue_size=10)

    def run(self):
        # Start Oak-D Lite pipeline
        self.device.startPipeline(self.pipeline)

        while not rospy.is_shutdown():
            # Read RGB frame from Oak-D Lite camera
            in_rgb = self.device.getInputQueue('rgb').tryGet()
            if in_rgb is not None:
                rgb_frame = in_rgb.getCvFrame()

            # Read road segmentation output from Oak-D Lite device
            in_nn = self.device.getOutputQueue('nn').tryGet()
            if in_nn is not None:
                detection_results = in_nn.getFirstLayerFp16()
                road_segmentation = detection_results.reshape((3, 300, 300))[0] > 0.5  # Threshold at 0.5 for binary output
                road_segmentation = road_segmentation.astype("uint8") * 255  # Scale to 0-255 for display

                # Convert road segmentation output to ROS message and publish
                ros_image = self.bridge.cv2_to_imgmsg(road_segmentation, encoding="mono8")
                ros_image.header.stamp = rospy.Time.now()
                self.image_pub.publish(ros_image)

if __name__ == '__main__':
    try:
        node = RoadSegmentationNode()
        node.run()
    except rospy.ROSInterruptException:
        pass
