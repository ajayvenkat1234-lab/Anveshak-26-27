import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import math
from turtlesim.msg import Pose

class DShapeNode(Node):
    def __init__(self):
        super().__init__('d_shape_node')
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.pose_sub = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        self.timer = self.create_timer(0.1, self.timer_callback)
        
        self.v = 1.0
        self.r = 1.0
        
        self.straight_time = 2 * self.r / self.v
        self.arc_time = math.pi * self.r / self.v
        self.turn_time = (math.pi/2) * self.r / self.v
        
        self.state = 0
        self.elapsed = 0.0
        self.dt = 0.1
        self.current_heading = 0.0

    def pose_callback(self, msg):
        self.current_heading = msg.theta 

    def timer_callback(self):
        msg = Twist()
        if self.state == 0:
            msg.linear.x = 0.0
            msg.angular.z = 1.0
            self.elapsed += self.dt
            if self.elapsed >= (math.pi/2) / msg.angular.z:
                self.elapsed = 0.0
                self.state = 1
            
        elif self.state == 1:
            msg.linear.x = self.v
            msg.angular.z = 0.0
            self.elapsed += self.dt
            if self.elapsed >= self.straight_time:
                self.elapsed = 0.0
                self.state = 2
        elif self.state == 2:
            msg.linear.x = 0.0
            msg.angular.z = -(self.v/self.r)
            self.elapsed += self.dt
            if self.elapsed >= self.turn_time:
                self.elapsed = 0.0
                self.state = 3
        elif self.state == 3:
            msg.linear.x = self.v
            msg.angular.z = -self.v / self.r
            self.elapsed += self.dt
            if self.elapsed >= self.arc_time:
                msg.linear.x = 0.0
                msg.angular.z = 0.0
                self.publisher_.publish(msg)
                self.timer.cancel()
                return

        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    d_shape_node = DShapeNode()
    rclpy.spin(d_shape_node)
    d_shape_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()