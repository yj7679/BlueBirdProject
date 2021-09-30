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
<<<<<<< HEAD
=======
        self.sio.wait()
>>>>>>> parent of bb119f9 (Merge branch 'feature/astar' into 'develop')

        # time_period = 0.3
        # self.timer = self.create_timer(time_period, self.timer_callback)

        thread = threading.Thread(target = self.timer_callback)
        thread.daemon = True
        thread.start()

    def timer_callback(self):
<<<<<<< HEAD
        if self.env_msg != '':
            env_msg = dict()
            env_msg['weather'] = self.env_msg.weather
            env_msg['day'] = self.env_msg.day
            env_msg['hour'] = self.env_msg.hour
            env_msg['minute'] = self.env_msg.minute
            env_msg['month'] = self.env_msg.month
            env_msg['temperature'] = self.env_msg.temperature
            self.sio.emit('env_msg', env_msg)

    def env_callback(self, msg):
        self.env_msg = msg
=======
        print('timer callback')
        self.cmd_pub.publish(self.cmd_msg)
>>>>>>> parent of bb119f9 (Merge branch 'feature/astar' into 'develop')

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