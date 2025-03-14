#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
import RPi.GPIO as GPIO

class RelayController(Node):
    def __init__(self):
        super().__init__('relay_controller')

        # Define GPIO pins for the relays (BCM numbering)
        self.relay_pins = {
            0: 17,  # Relay 0 connected to GPIO17
            1: 27,  # Relay 1 connected to GPIO27
            2: 22,  # Relay 2 connected to GPIO22
            3: 24   # Relay 3 connected to GPIO24
        }

        # Setup GPIO
        GPIO.setmode(GPIO.BCM)
        for pin in self.relay_pins.values():
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.HIGH)  # Initialize all relays to inactive (HIGH)

        self.get_logger().info('RelayController node has been started.')
        self.get_logger().info(f'Using GPIO pins: {self.relay_pins}')

        # Subscribe to 'bio_relay_command' topic
        self.subscription = self.create_subscription(Int32,'bio_relay',self.command_callback,10)
        self.subscription  # Prevent unused variable warning

    def command_callback(self, msg: Int32):
        command = msg.data
        self.get_logger().info(f'Received command: {command}')

        if command == 1:
            GPIO.output(self.relay_pins[0], GPIO.LOW)  # Heater 1 on
        elif command == 2:
            GPIO.output(self.relay_pins[1], GPIO.LOW)  # Heater 2 on
        elif command == 3:
            GPIO.output(self.relay_pins[2], GPIO.LOW)  # Heater 2 on
        elif command == 4:
            GPIO.output(self.relay_pins[0], GPIO.HIGH)  # Heater 1 off
        elif command == 5:
            GPIO.output(self.relay_pins[1], GPIO.HIGH)  # Heater 2 off
        elif command == 6:
            GPIO.output(self.relay_pins[2], GPIO.HIGH)  # Heater 3 off
        elif command == 7:
            GPIO.output(self.relay_pins[3], GPIO.LOW)  # LED on
        elif command == 8:
            GPIO.output(self.relay_pins[3], GPIO.HIGH)  # LED off
            pass
        else:
            self.get_logger().warn('Invalid command received.')

    def destroy_node(self):
        GPIO.cleanup()
        self.get_logger().info('Cleaned up GPIO settings.')
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    relay_controller = RelayController()

    try:
        rclpy.spin(relay_controller)
    except KeyboardInterrupt:
        relay_controller.get_logger().info('Keyboard Interrupt (SIGINT) received. Shutting down node.')
    finally:
        relay_controller.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
