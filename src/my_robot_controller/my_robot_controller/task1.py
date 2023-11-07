import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from turtlesim.srv import Spawn
from turtlesim.srv import Kill
from functools import partial
import random
import math


class ChasingNode(Node):
    def __init__(self):
        super().__init__("spawn_turtle_catch")  
        self.flag = True
        self.SX, self.SY, self.SName = self.spawn_turtle(x=random.uniform(0.0,11.0), y= random.uniform(0.0, 11.0), theta=random.uniform(0.0, 2 * 3.14159), name=random.randint(0,100000000))
        self.dy = None
        self.dx = None
        self.cmd_vel_publisher_ = self.create_publisher(msg_type=Twist, topic="/turtle1/cmd_vel", qos_profile=10)
        self.pose_subscriber_ = self.create_subscription(msg_type=Pose, topic="/turtle1/pose", callback= self.main_turtle_motion, qos_profile=10)
        self.get_logger().info("THE GAME HAS STARTED..!!")

    def main_turtle_motion(self, pose:Pose):
        cmd = Twist()
                    

        # get the slope of the line between the turtles
        self.dy = self.SY - pose.y
        self.dx = self.SX - pose.x
        self.angle_req = math.atan2(self.dy, self.dx)

        # if pose.x > self.SX:
        #     self.angle_req = self.angle_req - math.pi


        # change the position theta of the main turtle
        if round(pose.theta, 1) != round(self.angle_req, 1):
            cmd.linear.x = 0.0
            cmd.angular.z = 2.0
        else:
            cmd.linear.x = 45.0
            cmd.angular.z = 0.0
        self.cmd_vel_publisher_.publish(cmd)

        
        if self.SX - 0.3 <= pose.   x <= self.SX + 0.3 :
            self.kill_turtle(self.SName)
            self.SX, self.SY, self.SName = self.spawn_turtle(x=random.uniform(0.0,11.0), y= random.uniform(0.0, 11.0), theta=random.uniform(0.0, 2 * 3.14159), name=random.randint(0,100000000))

    def spawn_turtle(self, x, y, theta, name):
        client = self.create_client(srv_type=Spawn, srv_name="/spawn")
        while not client.wait_for_service(1.0):
            self.get_logger().warn("Waiting for service....")

        request = Spawn.Request()
        request.x = x
        request.y = y
        request.theta = theta
        request.name = 'a' + str(name)        
        future = client.call_async(request)

        future.add_done_callback(callback=partial(self.spawn_callback))
        
        return(request.x, request.y, 'a'+str(name))

    def spawn_callback(self, future):
        try: 
            response = future.result()
        except Exception as e:
            self.get_logger().error("Service call failed: %r" %(e,))

    def kill_turtle(self, name):
        client = self.create_client(srv_type=Kill, srv_name="/kill")
        while not client.wait_for_service(1.0):
            self.get_logger().warn("Waiting for service....")
    
        request = Kill.Request()
        request.name = name

        future = client.call_async(request)
        
        future.add_done_callback(callback=partial(self.kill_callback))

    def kill_callback(self, future):
        try: 
            response = future.result()
        except Exception as e:
            self.get_logger().error("Service call failed: %r" %(e,))


def main(args=None):
    rclpy.init(args=args)
    node = ChasingNode()
    rclpy.spin(node)
    rclpy.shutdown()