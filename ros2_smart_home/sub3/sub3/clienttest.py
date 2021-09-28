import socketio
import threading
import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from ssafy_msgs.msg import EnviromentStatus

class goFront(Node):
    
    def __init__(self):
        super().__init__('clienttest')
        self.env_sub = self.create_subscription(EnviromentStatus,'/envir_status',self.env_callback,1)
        self.cmd_pub = self.create_publisher(Twist,'cmd_vel', 10)

        self.cmd_msg=Twist()
        self.cmd_msg.linear.x=0.0
        self.cmd_msg.angular.z=0.0

        self.env_msg = ''

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

        @self.sio.on('msg')
        def get_msg(data):
            print(data)

        @self.sio.event
        def disconnect():
            print('disconnected from server')

        self.sio.connect('http://localhost:3000/')

        time_period = 0.3
        self.timer = self.create_timer(time_period, self.timer_callback)

        # thread = threading.Thread(target = self.timer_callback)
        # thread.daemon = True
        # thread.start()

        # self.sio.wait()

    def timer_callback(self):
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