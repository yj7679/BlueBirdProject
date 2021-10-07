import socketio
import threading
import rclpy
import time
from rclpy.node import Node
from connection import *
from modules import *
from geometry_msgs.msg import Twist
from ssafy_msgs.msg import EnviromentStatus
from std_msgs.msg import Int16, Int8

# 심부름 상태에 대해 컨트롤할 것 #
work_status = {
    0 : "사용 가능",
    getCurrStage(1) : "물건을 가지러 가는 중입니다",
    getCurrStage(2) : "물건을 가지러 가는 중입니다",
    getCurrStage(3) : "물건을 찾는 중입니다",
    getCurrStage(4) : "물건으로 이동 중입니다",
    getCurrStage(5) : "물건을 들고 이동 중입니다",
    getCurrStage(6) : "물건을 들고 이동 중입니다",
    getCurrStage(7) : "물건을 들고 이동 중입니다",
    getCurrStage(8) : "물건을 들고 이동 중입니다",
    getCurrStage(9) : "물건을 들고 이동 중입니다",
    getUDPstage(1) : "가전기기로의 경로를 생성 중 입니다",
    getUDPstage(2) : "가전기기로 이동 중 입니다.",
    getUDPstage(3) : "가전기기를 제어 중 입니다.",
    getUDPstage(4) : "가전기기 제어를 종료 중입니다",
}
 
def startConn(conn):
    rclpy.spin(conn)
    conn.destroy_node()
    rclpy.shutdown()

class client(Node):
    
    def __init__(self):
        rclpy.init(args=None)
        super().__init__('client')

        conn = connection()
        self.working_status_msg =  Int16()
        self.working_status_pub = self.create_publisher(Int16,'working_status',10)
        self.sio = socketio.Client()
        self.turtlebot_status_msg = TurtlebotStatus()

        thread = threading.Thread(target=self.checkDone_callback, args=[conn])
        thread.daemon = True 
        thread.start()

        @self.sio.event
        def connect():
            conMod_thread = threading.Thread(target=startConn, args=[conn])
            conMod_thread.daemon = True
            conMod_thread.start()
            # print('connection established')

        @self.sio.on('deviceControlToROS')
        def deviceOn(data):
            print('clinet.py : device Control 명령이 들어왔습니다.')

            conn.operation = data
            
            if data['arrival']['on_off'] == 'on':
                conn.want_stuff = -1
            else: # off
                conn.want_stuff = -2

            self.working_status_msg.data = getUDPstage(1)
            print('client.py : 1단계 working_status_msg를 publish 합니다.')
            self.working_status_pub.publish(self.working_status_msg)

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
            self.working_status_msg.data = getCurrStage(1)
            
            # tf_test
            # self.working_status_msg.data = 0b111
     
            self.working_status_pub.publish(self.working_status_msg)
        
        @self.sio.on('env_msg_request_ros')
        def envRequest():
            # print('server emit env_msg_request!')
            env_msg_response = dict()
            env_msg_response['weather'] = conn.env_data.weather
            env_msg_response['temperature'] = conn.env_data.temperature
            
            # print('env response : ',env_msg_response)
            self.sio.emit('env_msg_response_ros', env_msg_response)

        @self.sio.on('bot_status_request_ros')
        def botRequest():
            bot_status_response = dict()
            
            bot_status_response['available'] = '사용가능' if conn.working_status_msg.data == 0 else '사용불가'
            bot_status_response['job'] = work_status[conn.working_status_msg.data]
            
            self.sio.emit('bot_status_response_ros', bot_status_response)

        @self.sio.event
        def disconnect():
            print('disconnected from server')
        

        self.sio.connect('http://localhost:12001/')

    def checkDone_callback(self, conn):
        prev = 0
        curr = 0
        while True:
            if conn != None:
                curr = conn.doneCount

                if prev != curr:
                    print('작업 하나 완료')
                    jd = dict()
                    jd['data']='done'
                    self.sio.emit('jobDone',jd)
                prev = conn.doneCount
            time.sleep(1)


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
