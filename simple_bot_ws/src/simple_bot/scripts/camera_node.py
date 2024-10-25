#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class MobileCameraPublisher(Node):
    def __init__(self, camera_url):
        super().__init__('mobile_camera_publisher')
        self.publisher_ = self.create_publisher(Image, 'camera/image_raw', 10)
        self.bridge = CvBridge()
        self.camera_url = camera_url
        self.cap = cv2.VideoCapture(self.camera_url)

        self.timer = self.create_timer(0.1, self.publish_image)
        self.get_logger().info('Mobile camera publisher node has been started.')

    def publish_image(self):
        ret, frame = self.cap.read()
        if ret:
            # Convert the frame to a ROS Image message
            ros_image = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
            # Publish the image
            self.publisher_.publish(ros_image)
            self.get_logger().info('Published an image frame')
        else:
            self.get_logger().warning('Failed to capture frame from the camera')

    def destroy_node(self):
        self.cap.release()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    camera_url = 0
    node = MobileCameraPublisher(camera_url)
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
