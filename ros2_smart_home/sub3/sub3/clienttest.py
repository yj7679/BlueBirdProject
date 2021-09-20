import socketio
import threading
import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist

class goFront(Node):
    
    def __init__(self):
        super().__init__('clienttest')
        self.cmd_pub = self.create_publisher(Twist,'cmd_vel', 10)

        self.cmd_msg=Twist()
        self.cmd_msg.linear.x=0.0
        self.cmd_msg.angular.z=0.0

        self.sio = socketio.Client()

        @self.sio.event
        def connect():
            print('connection established')

        @self.sio.event
        def my_message(data):
            print('message received with ', data)
            sio.emit('my response', {'response': 'my response'})

        @self.sio.on('get_linear_x')
        def get_linear_x(data):
            # print('get linear x ', data)
            self.cmd_msg.linear.x=data

        @self.sio.event
        def disconnect():
            print('disconnected from server')

        self.sio.connect('http://localhost:3000/')
        self.sio.wait()

        # time_period = 0.3
        # self.timer = self.create_timer(time_period, self.timer_callback)

        thread = threading.Thread(target = self.timer_callback)
        thread.daemon = True
        thread.start()

    def timer_callback(self):
        print('timer callback')
        self.cmd_pub.publish(self.cmd_msg)

def main(args=None):
    rclpy.init(args=args)

    clientTest = goFront()

    rclpy.spin(clientTest)

    clientTest.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

# sio = socketio.Client()

# @sio.event
# def connect():
#     print('connection established')

# @sio.event
# def my_message(data):
#     print('message received with ', data)
#     sio.emit('my response', {'response': 'my response'})

# @sio.event
# def disconnect():
#     print('disconnected from server')

# sio.connect('http://localhost:3000/')
# sio.wait()