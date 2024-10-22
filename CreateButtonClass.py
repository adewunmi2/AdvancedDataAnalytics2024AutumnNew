#!/usr/bin/env python3
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from rclpy.qos import QoSProfile, ReliabilityPolicy
import tkinter as tk  # Import Tkinter for the button functionality

class Esp32ControllerNode2(Node):

    def __init__(self):
        super().__init__('esp32_controller_node')
        topic = "/atv/debug"
        self.get_logger().info('Esp32ControllerNode is listening to Topic -> ' + topic)
        qos_profile = QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT)
        self.sub = self.create_subscription(String, topic, self.chatter_callback, qos_profile)
        
        # Create a publisher for the Twist message
        self.twist_pub = self.create_publisher(Twist, '/atv/ctrl_cmd', 10)
        
        # Create a timer to publish the Twist message
        timer_period = 4.0  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        
        self.iteration = 0
        
        # Set up the GUI with Tkinter
        self.create_gui()

    def create_gui(self):
        # Create a simple GUI with Tkinter
        self.root = tk.Tk()
        self.root.title("ATV Control")
        
        # Add a button to publish a twist message
        self.button = tk.Button(self.root, text="Publish Twist", command=self.button_callback)
        self.button.pack(pady=10)
        
        # Start the Tkinter loop in a non-blocking way
        self.root.after(100, self.update_tk)  # Updates Tkinter loop within the ROS loop

    def button_callback(self):
        # Action when button is clicked
        self.get_logger().info("Button clicked!")
        self.publish_twist(0.5, 0.0)  # Publish a specific twist message on button click

    def update_tk(self):
        self.root.update()

    def chatter_callback(self, msg: String):
        self.get_logger().info(str(msg))

    def publish_twist(self, speed, angle):
        twist_msg = Twist()
        twist_msg.linear.x = speed
        twist_msg.linear.y = 0.0
        twist_msg.linear.z = 0.0
        twist_msg.angular.x = 0.0
        twist_msg.angular.y = 0.0
        twist_msg.angular.z = angle
        self.twist_pub.publish(twist_msg)
        self.get_logger().info(f'Publishing Twist message with speed {speed} and angle {angle}')

    # demo program to move the steering
    def timer_callback(self):
        if self.iteration % 4 == 0:
            self.publish_twist(0.2, +0.1)
        if self.iteration % 4 == 1:
            self.publish_twist(0.2, -0.2)
        if self.iteration % 4 == 2:
            self.publish_twist(-0.2, +0.1)
        if self.iteration % 4 == 3:
            self.publish_twist(-0.2, -0.2)

        self.iteration += 1

def main(args=None):
    rclpy.init(args=args)
    node = Esp32ControllerNode()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()

if __name__ == '__main__':
    main()
