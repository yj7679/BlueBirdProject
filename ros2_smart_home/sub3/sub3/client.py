import socketio
import threading
import rclpy
from rclpy.node import Node
from connection import *
from geometry_msgs.msg import Twist
from ssafy_msgs.msg import EnviromentStatus

def startConn(conn):
    rclpy.spin(conn)
    conn.destroy_node()
    rclpy.shutdown()


class client(Node):
    
    def __init__(self):
        rclpy.init(args=None)
        super().__init__('client')


        conn = connection()

        self.sio = socketio.Client()

        @self.sio.event
        def connect():
            conMod_thread = threading.Thread(target=startConn, args=[conn])
            conMod_thread.daemon = True
            conMod_thread.start()
            print('connection established')



        @self.sio.on('goToGoal')
        def goToGoal_start(data):
            print('Vue로 부터온 명령어 : ', data)
            conn.destination.x = data.x
            conn.destination.y = data.y
            print(conn.destination.x, conn.destination.y)
            conn.is_goToGoal = True


        @self.sio.event
        def my_message(data):
            print('message received with ', data)
            sio.emit('my response', {'response': 'my response'})

 

        @self.sio.on('msg')
        def get_msg(data):
            print(data)

        @self.sio.event
        def disconnect():
            print('disconnected from server')

        self.sio.connect('http://localhost:12001/')

        # time_period = 0.3
        # self.timer = self.create_timer(time_period, self.timer_callback)

        # thread = threading.Thread(target = self.timer_callback)
        # thread.daemon = True
        # thread.start()

        # self.sio.wait()

    # def timer_callback(self):
    #     if self.env_msg != '':
    #         env_msg = dict()
    #         env_msg['weather'] = self.env_msg.weather
    #         env_msg['day'] = self.env_msg.day
    #         env_msg['hour'] = self.env_msg.hour
    #         env_msg['minute'] = self.env_msg.minute
    #         env_msg['month'] = self.env_msg.month
    #         env_msg['temperature'] = self.env_msg.temperature
    #         self.sio.emit('env_msg', env_msg)

    # def env_callback(self, msg):
    #     self.env_msg = msg

def main(args=None):
    try:
        client_run = client()

    except KeyboardInterrupt:
        
        client_run.destroy_node()
        rclpy.shutdown()
        exit()

if __name__ == '__main__':
    main()
