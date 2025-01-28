import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
from ultralytics import YOLO
import numpy as np
import os

class custom_yolo_model:
    def __init__(self):
        # Initialize ROS node
        rospy.init_node('custom_yolo_node', anonymous=True)

        # Parameters
        self.image_topic = rospy.get_param('~image_topic', '/iris_depth_camera_0/camera/rgb/image_raw')
        self.confidence_threshold = rospy.get_param('~confidence_threshold', 0.7)
        self.result_topic = rospy.get_param('~result_topic', '/yolo_det/detections')

        self.model = YOLO(os.path.expanduser('~/catkin_ws/src/custom_yolo/scripts/custom11.pt'))  # Load the custom model in this file, custom8.pt custom11.pt etc.

        # CV Bridge for converting ROS Image messages
        self.bridge = CvBridge()

        # ROS subscribers and publishers
        self.image_sub = rospy.Subscriber(self.image_topic, Image, self.image_callback)
        self.result_pub = rospy.Publisher(self.result_topic, Image, queue_size=1)

        rospy.loginfo("YOLO ROS node initialized. Subscribing to: {}".format(self.image_topic))

    def image_callback(self, msg):
        try:
            # Convert ROS Image to OpenCV format
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except CvBridgeError as e:
            rospy.logerr("CvBridge Error: {}".format(e))
            return

        # Perform object detection
        results = self.model(cv_image)[0]

        # Draw detections on the image
        detection_image = self.draw_detections(cv_image, results)

        try:
            # Convert OpenCV image back to ROS Image message
            ros_image = self.bridge.cv2_to_imgmsg(detection_image, encoding='bgr8')
            self.result_pub.publish(ros_image)
        except CvBridgeError as e:
            rospy.logerr("CvBridge Error: {}".format(e))

    def draw_detections(self, image, results):
        # Iterate through detections and draw bounding boxes and labels
        for box in results.boxes:
            conf = box.conf.item()
            if conf < self.confidence_threshold:
                continue

            # Extract bounding box coordinates and label
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            label = results.names[box.cls.item()]

            # Draw bounding box and label
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(
                image,
                f"{label} {conf:.2f}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )
        return image

if __name__ == '__main__':
    try:
        custom_yolo_inference = custom_yolo_model()
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.logerr("Custom YOLO ROS node interrupted.")

