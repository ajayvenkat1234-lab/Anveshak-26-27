import rclpy
from rclpy.node import Node
from std_msgs.msg import Int8

class CountNode(Node):
    def __init__(self):
        super().__init__('count_node')
        self.subscription = self.create_subscription(
            Int8,
            '/number',
            self.listener_callback,
            10)
        self.publisher_ = self.create_publisher(Int8, '/count', 10)
        self.count = 0
        self.current_number = None

    def listener_callback(self, msg):
        if msg.data == self.current_number:
            self.count += 1
        else:
            self.current_number = msg.data
            self.count = 1
        
        self.get_logger().info(f'Number: {msg.data},Count: {self.count}')
        output = Int8()
        output.data = self.count
        self.publisher_.publish(output)

def main(args=None):
    rclpy.init(args=args)
    count_node = CountNode()
    rclpy.spin(count_node)
    count_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()