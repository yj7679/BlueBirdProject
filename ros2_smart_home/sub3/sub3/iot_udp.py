import sys
import rclpy
from rclpy.node import Node  
import time
import os
import socket
import threading
import struct
import binascii
import datetime
from std_msgs.msg import Int16, Int8
from modules import *

# iot_udp 노드는 udp 통신을 이용해 iot로 부터 uid를 얻어 접속, 제어를 하는 노드입니다.
# sub1,2 에서는 ros 메시지를 이용해 쉽게 제어했지만, advanced iot 제어에서는 정의된 통신프로토콜을 보고 iot와 직접 데이터를 주고 받는 형식으로 제어하게 됩니다.
# 통신 프로토콜은 명세서를 참조해주세요.


# 노드 로직 순서
# 1. 통신 소켓 생성
# 2. 멀티스레드를 이용한 데이터 수신
# 3. 수신 데이터 파싱
# 4. 데이터 송신 함수
# 5. 사용자 메뉴 생성 
# 6. iot scan 
# 7. iot connect
# 8. iot control

# 통신프로토콜에 필요한 데이터입니다. 명세서에 제어, 상태 프로토콜을 참조하세요. 
params_status = {
    (0xa,0x25 ) : "IDLE" ,
    (0xb,0x31 ) : "CONNECTION",
    (0xc,0x51) : "CONNECTION_LOST" ,
    (0xb,0x37) : "ON",
    (0xa,0x70) : "OFF",
    (0xc,0x44) : "ERROR"
}


params_control_cmd= {
    "TRY_TO_CONNECT" : (0xb,0x31 )  ,
    "SWITCH_ON" : (0xb,0x37 ) ,
    "SWITCH_OFF" : (0xa,0x70),
    "RESET" : (0xb,0x25) ,
    "DISCONNECT" : (0x00,0x25) 
}


class iot_udp(Node):

    def __init__(self):
        super().__init__('iot_udp')

        self.ip='127.0.0.1'
        self.port=7502
        self.send_port=7401

        # 로직 1. 통신 소켓 생성
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        recv_address = (self.ip,self.port)
        self.sock.bind(recv_address)
        self.data_size=65535 
        self.parsed_data=[]
        
        self.lock = threading.Lock()

        self.working_status_msg =  Int16()
        self.working_status_msg.data = 0
        self.working_status_sub = self.create_subscription(Int16,'/working_status',self.working_status_callback,10) # woring status 값 받고 값을 다시 담아주기 위해 사용
        self.working_status_pub = self.create_publisher(Int16,'working_status',10)

        self.want_stuff_msg =Int8()
        self.want_stuff_sub = self.create_subscription(Int8,'/want_stuff', self.want_stuff_callback, 10) # 찾으려는 물건 값을 받기 위해 사용

        # 로직 2. 멀티스레드를 이용한 데이터 수신
        thread = threading.Thread(target=self.recv_udp_data)
        thread.daemon = True 
        thread.start() 

        # 기기를 끄거나 키라는 명령이 들어오는지 확인한다.
        self.timer = self.create_timer(0.05, self.timer_callback)

        self.is_recv_data=False
        self.recv_data_time=datetime.datetime(1995,11,29,0,0,0)

        # os.system('cls')
        # while True:
        #     # 로직 5. 사용자 메뉴 생성
        #     print('Select Menu [0: scan, 1: connect, 2:control, 3:disconnect, 4:all_procedures ] ')
        #     menu=int(input())

        #     if menu == 0 :
        #         self.scan()
        #     elif menu == 1:
        #         self.connect()
        #     elif menu == 2:
        #         print('Control Menu [0: ON, 1: OFF]')
        #         ctrl = int(input())
        #         if ctrl==0:
        #             self.control("SWITCH_ON")
        #         elif ctrl==1:
        #             self.control("SWITCH_OFF")
        #         else :
        #             print('wrong input')
        #     elif menu == 3:
        #         print(self.recv_data)
        #     else:
        #         pass

    def timer_callback(self):
        # print(getUDPstage(self.working_status_msg.data))
        if self.working_status_msg.data == getUDPstage(3):
            print('iot_udp.py : 3단계를 인식했습니다. 가전기기를 제어합니다.')
            self.scan()
            self.connect()
            if self.want_stuff_msg.data == -1: # on
                self.control('SWITCH_ON')
            else: # off
                self.control('SWITCH_OFF')
            self.working_status_msg.data = getUDPstage(4)
            print('iot_upd.py : 가전기기제어를 완료했습니다. 4단계를 퍼블리시합니다.')
            self.working_status_pub.publish(self.working_status_msg)

    def working_status_callback(self, msg):
        self.working_status_msg = msg
            
    def want_stuff_callback(self, msg):
        self.want_stuff_msg = msg

    def data_parsing(self,raw_data) :
        
        '''
        로직 3. 수신 데이터 파싱
        '''
        header=raw_data[:19].decode('utf-8')
        data_length=int.from_bytes(raw_data[19:23], "little")
        aux_data=raw_data[23:35]

        if header == '#Appliances-Status$' and data_length == 20:
            uid_pack=raw_data[35:51]
            uid=self.packet_to_uid(uid_pack)
        
            network_status=raw_data[51:53]
            network_status=params_status[(network_status[0], network_status[1])]

            device_status=raw_data[53:55]
            device_status=params_status[(device_status[0], device_status[1])]

            self.is_recv_data=True
            self.recv_data=[uid,network_status,device_status]
        
 
    def send_data(self,uid,cmd):
        '''
        로직 4. 데이터 송신 함수 생성
        '''

        header=b'#Ctrl-command$'
        data_length=(18).to_bytes(4, byteorder='little')
        aux_data=(0).to_bytes(12, byteorder='little')

        self.upper= header + data_length + aux_data
        self.tail=bytes([0x0D, 0x0A])

        uid_pack=self.uid_to_packet(uid)
        cmd = params_control_cmd[cmd]
        cmd_pack=bytes([cmd[0],cmd[1]])

        send_data=self.upper+uid_pack+cmd_pack+self.tail
        self.sock.sendto(send_data,(self.ip,self.send_port))
        time.sleep(0.2)


    def recv_udp_data(self):
        while True :
            raw_data, sender = self.sock.recvfrom(self.data_size)
            self.recv_data_time = datetime.datetime.now()
            self.data_parsing(raw_data)

            
    def uid_to_packet(self,uid):
        uid_pack=binascii.unhexlify(uid)
        return uid_pack

        
    def packet_to_uid(self,packet):
        uid=""
        for data in packet:
            if len(hex(data)[2:4])==1:
                uid+="0"
            
            uid+=hex(data)[2:4]
            
            
        return uid


    def scan(self):
        
        print('SCANNING NOW.....')
        print('BACK TO MENU : Ctrl+ C')
        '''
        로직 6. iot scan

        주변에 들어오는 iot 데이터(uid,network status, device status)를 출력하세요.

        '''
        # 주변에 데이터가 들어오고 있는지 체크한다.
        # self.is_recv_data 를 이용해서 체크가능하다.
        time_diff = datetime.datetime.now() - self.recv_data_time
        if abs(time_diff.seconds >= 1):
            self.is_recv_data = False
            self.recv_data = [None, None, None] # recv data reset
        
        if self.is_recv_data is True:
            print(self.recv_data[0], self.recv_data[1], self.recv_data[2])
        else :
            print('no iot data')
        
                   

    def connect(self):
        
        '''
        로직 7. iot connect

        iot 네트워크 상태를 확인하고, CONNECTION_LOST 상태이면, RESET 명령을 보내고,
        나머지 상태일 때는 TRY_TO_CONNECT 명령을 보내서 iot에 접속하세요.

        '''
        while self.recv_data[1] != 'CONNECTION':
            con_cmd = ''
            if self.recv_data[1]=='IDLE':
                con_cmd = 'TRY_TO_CONNECT'
            elif self.recv_data[1]=='CONNECTION_LOST':
                con_cmd = 'RESET'
            self.send_data(self.recv_data[0], con_cmd)
        print('connect success')
        

    
    def control(self, cmd):
        '''
        로직 8. iot control
        
        iot 디바이스 상태를 확인하고, ON 상태이면 OFF 명령을 보내고, OFF 상태면 ON 명령을 보내서,
        현재 상태를 토글시켜주세요.
        '''
        if self.is_recv_data is True:
            uid, network_status, device_status = self.recv_data
            if cmd=='SWITCH_ON':
                while self.recv_data[2] != 'ON':
                    print('가전기기를 키는중..')
                    self.send_data(uid, cmd)
            elif cmd=='SWITCH_OFF':
                while self.recv_data[2] != 'OFF':
                    print('가전기기를 끄는중..')
                    self.send_data(uid, cmd)
            

    def disconnect(self):
        if self.is_recv_data==True :
            self.send_data(self.recv_data[0],params_control_cmd["DISCONNECT"])
        

    def all_procedures(self):
        self.connect()
        time.sleep(0.5)
        self.control()
        time.sleep(0.5)
        self.disconnect()


           
    def __del__(self):
        self.sock.close()
        print('del')



def main(args=None):
    rclpy.init(args=args)
    iot = iot_udp()
    rclpy.spin(iot)
    iot.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()