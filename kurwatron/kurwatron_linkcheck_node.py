import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
from std_msgs.msg import Int64

global oldcount, failcount

oldcount = 0
failcount = 0

class KurwatronLinkcheckNode(Node):
    def __init__(self):
        super().__init__("kurwatron_linkcheck_node")
        self.get_logger().info("Starting linkcheck...")
        self.pub_ = self.create_publisher(Bool, "link_status", 0)
        self.subscription = self.create_subscription(
            Int64, 'nonce', self.listener_callback, 0)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        global oldcount, failcount
        newcount = Int64()
        newcount = msg.data
        self.get_logger().info('I heard: {}'.format(msg.data))
        if (oldcount - newcount) == 0:
            failcount = failcount + 1
        if (oldcount - newcount) > 0:
            failcount = failcount + 1
        if (oldcount - newcount) < 0:	
            failcount = 0

        oldcount = newcount
        
        if failcount > 20:
            print('Connection error. Failcount: {}'.format(failcount))
        else:
            print('Connection OK')
        
#        self.get_logger().info('Published: {}'.format(new_msg.data))
#        self.pub_.publish(new_msg)

def main(args=None):
    rclpy.init(args=args)
    linknode = KurwatronLinkcheckNode()
    rclpy.spin(linknode)
    linknode.destroy_node()
    rclpy.shutdown()
if __name__ == "__main__":
    main()