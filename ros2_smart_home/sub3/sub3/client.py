import socketio
import threading
import rclpy
from rclpy.node import Node
from connection import *
from geometry_msgs.msg import Twist
from ssafy_msgs.msg import EnviromentStatus
from std_msgs.msg import Int16, Int8

def startConn(conn):
    rclpy.spin(conn)
    conn.destroy_node()
    rclpy.shutdown()


class client(Node):
    
    def __init__(self):
        rclpy.init(args=None)
        super().__init__('client')

        conn = connection()
        self.working_status_pub = self.create_publisher(Int16,'working_status',10)
        self.sio = socketio.Client()
        self.turtlebot_status_msg = TurtlebotStatus()

        self.working_status_msg =  Int16()
        self.working_status_msg.data = 0


        @self.sio.event
        def connect():
            conMod_thread = threading.Thread(target=startConn, args=[conn])
            conMod_thread.daemon = True
            conMod_thread.start()
            print('connection established')

        @self.sio.on('stuffBringToROS')
        def stuffBringStart(data):
            print('Vue로 부터온 명령어 : ', data)

            conn.operation = data
            # 찾기 원하는 물건을 publish
            if data['stuff']['name'] == '상자':
                conn.want_stuff = 1
            elif data['stuff']['name'] == '서류':
                conn.want_stuff = 2
            elif data['stuff']['name'] == '물':
                conn.want_stuff = 3
                print("물로 넣음")
            # original test
            # self.working_status_msg.data = 0b1
            
            # tf_test
            self.working_status_msg.data = 0b111
            self.working_status_pub.publish(self.working_status_msg)
        
        @self.sio.on('env_msg_request')
        def envRequest():
            print('server emit env_msg_request!')
            env_msg_response = dict()
            env_msg_response['weather'] = conn.env_data.weather
            env_msg_response['temperature'] = conn.env_data.temperature
            
            print('env response : ',env_msg_response)
            self.sio.emit('env_msg_response', env_msg_response)

        @self.sio.event
        def disconnect():
            print('disconnected from server')
        

        self.sio.connect('http://localhost:12001/')


def main(args=None):
    try:
        client_run = client()

    except KeyboardInterrupt:
        rclpy.spin(client_run)
        client_run.destroy_node()
        rclpy.shutdown()
        exit()

if __name__ == '__main__':
    main()
