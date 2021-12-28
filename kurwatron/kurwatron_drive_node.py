import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class KurwatronDriveNode(Node):
    def __init__(self):
        super().__init__("kurwatron_drive_node")
        self.get_logger().info("Starting subscriber...")
        self.subscription = self.create_subscription(
            String, 'nonce', self.listener_callback, 2)
        self.subscription  # prevent unused variable warning
        
    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)

def main(args=None):
    rclpy.init(args=args)
    drivenode = KurwatronDriveNode()
    rclpy.spin(drivenode)
    drivenode.destroy_node()
    rclpy.shutdown()
if __name__ == "__main__":
    main()