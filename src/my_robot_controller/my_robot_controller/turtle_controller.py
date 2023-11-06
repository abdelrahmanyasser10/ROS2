#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from turtlesim.srv import SetPen
from functools import partial

class TurtleControllerNode(Node):
    def __init__(self):
        super().__init__("turtle_controller")
        self.previous_x_= 0 
        self.cmd_vel_publisher_ = self.create_publisher(msg_type=Twist, topic="/turtle1/cmd_vel", qos_profile=10)
        self.pose_subscriber_= self.create_subscription(msg_type=Pose, topic="/turtle1/pose", callback=self.pose_callback, qos_profile=10)
        self.get_logger().info("Turtle Controller has been started.")

    def pose_callback(self, pose: Pose):
        cmd = Twist()
        if pose.x > 9.5 or pose.x < 1.5 or pose.y < 1.5 or pose.y > 9.5 :
            cmd.linear.x = 1.0
            cmd.angular.z = 1.0
        else:
            cmd.linear.x = 5.0
            cmd.angular.z = 0.0  
        self.cmd_vel_publisher_.publish(cmd)

        if pose.x > 5.5 and self.previous_x_ <= 5.5:
            self.previous_x_ = pose.x
            self.call_set_pen_service(r=255, g=152, b=80, width=3, off=0)
        elif pose.x <= 5.5 and self.previous_x_ > 5.5:
            self.previous_x_= pose.x
            self.call_set_pen_service(r=30, g=50, b=100, width=3, off=0)

    def call_set_pen_service(self, r, g, b, width, off):
        client = self.create_client(srv_type=SetPen, srv_name="/turtle1/set_pen")
        while not client.wait_for_service(1.0):
            self.get_logger().warn("Waiting for service....")

        request = SetPen.Request()            
        request.r = r
        request.g = g
        request.b = b
        request.width = width
        request.off = off

        future = client.call_async(request)
        
        future.add_done_callback(callback=partial(self.callback_set_pen))
        
    def callback_set_pen(self, future):
        try:
            response = future.result()

        except Exception as e:
            self.get_logger().error("Service call failed: %r" %(e,))
                


def main(args=None):
    rclpy.init(args=args)
    node = TurtleControllerNode()
    rclpy.spin(node)
    rclpy.shutdown()