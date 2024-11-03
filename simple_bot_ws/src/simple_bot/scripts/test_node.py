#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import random

class RandomMotionNode(Node):
    def __init__(self):
        super().__init__('random_motion_node')
        # Publisher for /cmd_vel
        self.cmd_vel_publisher = self.create_publisher(Twist, '/bot2/cmd_vel', 10)
        # Subscriber for camera feed
        self.camera_subscriber = self.create_subscription(Image, '/bot2/camera/image_raw', self.camera_callback, 10)
        
        # Initialize CvBridge
        self.bridge = CvBridge()
        
        # Define a list of movement commands
        self.movements = [
            ("forward", 0.5, 0.0),
            ("backward", -0.5, 0.0),
            ("right", 0.0, -0.5),
            ("left", 0.0, 0.5),
            ("stop", 0.0, 0.0)
        ]
        
        # Timer to publish random movements every 2 seconds
        self.timer = self.create_timer(2.0, self.publish_random_movement)

    def publish_random_movement(self):
        # Choose a random movement from the list
        movement = random.choice(self.movements)
        movement_name, linear_x, angular_z = movement
        self.get_logger().info(f"Selected movement: {movement_name}")

        # Create and publish the Twist message
        twist = Twist()
        twist.linear.x = linear_x
        twist.angular.z = angular_z
        self.cmd_vel_publisher.publish(twist)

    def camera_callback(self, msg):
        try:
            # Convert ROS Image message to OpenCV image
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            # Display the image
            cv2.imshow("Camera Feed", cv_image)
            cv2.waitKey(1)
        except Exception as e:
            self.get_logger().error(f"Could not convert image: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = RandomMotionNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
