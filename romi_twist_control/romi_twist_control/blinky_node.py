import rclpy
from rclpy.node import Node
from std_msgs.msg import Int16MultiArray

class BlinkyNode(Node):
    def __init__(self):
        super().__init__('blinky')
        
        # Publisher for the LEDs
        self.publisher_ = self.create_publisher(
            Int16MultiArray, 
            '/leds', 
            10
        )
        
        # Timer to trigger the callback every 1.0 seconds
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.state = 0
        
        self.get_logger().info("Blinky node started. Toggling LEDs...")

    def timer_callback(self):
        msg = Int16MultiArray()
        
        # Cycle through Red, Yellow, Green
        if self.state == 0:
            msg.data = [1, 0, 0]
            led_name = "YELLOW"
        elif self.state == 1:
            msg.data = [0, 1, 0]
            led_name = "GREEN"
        else:
            msg.data = [0, 0, 1]
            led_name = "RED"

        self.publisher_.publish(msg)
        self.get_logger().info(f"Toggled LED: {led_name}")
        
        # Increment state and wrap back to 0
        self.state = (self.state + 1) % 3

def main(args=None):
    rclpy.init(args=args)
    node = BlinkyNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        # Turn off all LEDs before shutting down
        msg = Int16MultiArray()
        msg.data = [0, 0, 0]
        node.publisher_.publish(msg)
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()