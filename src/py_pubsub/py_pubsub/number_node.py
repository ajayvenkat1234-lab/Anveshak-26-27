import rclpy
from rclpy.node import Node
from std_msgs.msg import Int8

class NumberNode(Node):

    def __init__(self):
        super().__init__('number_node')
        self.subscription = self.create_subscription(
            Int8,
            '/count',
            self.listener_callback,
            10)
        self.publisher_ = self.create_publisher(Int8, '/number',10)
        self.n = 0
        self.timer = self.create_timer(0.5,self.timer_callback)
    def timer_callback(self):
        self.timer.cancel()
        self.n += 1
        msg = Int8()
        msg.data = self.n
        self.get_logger().info(f'Initial publish: n={self.n}')
        self.publisher_.publish(msg)

    def listener_callback(self, msg):
        count = msg.data
        if count == self.n:
            self.n = self.n + 1
        elif count < self.n:
            self.n = self.n
        
        output = Int8()
        output.data = self.n
        self.get_logger().info(f'Count: {count}, n={self.n}')
        self.publisher_.publish(output)


def main(args=None):
    rclpy.init(args=args)
    number_node = NumberNode()
    rclpy.spin(number_node)
    number_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()