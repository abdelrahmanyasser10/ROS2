import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from turtlesim.srv import Spawn




class ChasingNode(Node):
    def __init__(self):
        super().__init__("Spawn Turtle Catch")
        self.cmd_vel_publisher_ = self.create_publisher(msg_type=Twist, topic="/turtle1/cmd_vel", qos_profile=10)
        self.pose_subscriber_ = self.create_subscription(msg_type=Pose, topic="/turtle1/pose", callback= self.pose_subscribtion_callback, qos_profile=10)
        self.get_logger().info("THE GAME HAS STARTED..!!")

    def pose_subscribtion_callback(self, pose:Pose):
        pass

    def call_spawn_service(self, x, y, theta):
        client = self.create_client(srv_type=Spawn, srv_name="/spawn")
        while not client.wait_for_service(1.0):
            self.get_logger().warn("Waiting for service....")

        


def main(args=None):
    rclpy.init(args=args)
    rclpy.shutdown()