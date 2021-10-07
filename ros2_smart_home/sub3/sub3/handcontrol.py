import rclpy
from rclpy.node import Node
import os, time
from ssafy_msgs.msg import TurtlebotStatus,HandControl
from geometry_msgs.msg import Twist
import threading
from time import sleep
from std_msgs.msg import Int16
from modules import *

# Hand Control 노드는 시뮬레이터로부터 데이터를 수신해서 확인(출력)하고, 메세지를 송신해서 Hand Control기능을 사용해 보는 노드입니다. 
# 메시지를 받아서 Hand Control 기능을 사용할 수 있는 상태인지 확인하고, 제어 메시지를 보내 제어가 잘 되는지 확인해보세요. 
# 수신 데이터 : 터틀봇 상태 (/turtlebot_status)
# 송신 데이터 : Hand Control 제어 (/hand_control)


# 노드 로직 순서
# 1. publisher, subscriber 만들기
# 2. 사용자 메뉴 구성
# 3. Hand Control Status 출력
# 4. Hand Control - Preview
# 5. Hand Control - Pick up
# 6. Hand Control - Put down


class Handcontrol(Node):



    def __init__(self):
        super().__init__('hand_control')
        print("handcontol ready")
        ## 로직 1. publisher, subscriber 만들기
        self.hand_control = self.create_publisher(HandControl, '/hand_control', 10)                
        self.turtlebot_status = self.create_subscription(TurtlebotStatus,'/turtlebot_status',self.turtlebot_status_cb,10)
        self.working_status_sub = self.create_subscription(Int16,'/working_status',self.working_status_callback,10) # woring status 값 받고 값을 다시 담아주기 위해 사용
        self.working_status_pub = self.create_publisher(Int16,'working_status',10) # woring status 값 받고 값을 다시 담아주기 위해 사용
        self.cmd_pub = self.create_publisher(Twist, 'cmd_vel', 10)
     
        # self.timer = self.create_timer(1, self.timer_callback)
        # print(threading.current_thread().getName())
        


        ## 제어 메시지 변수 생성 
        self.hand_control_msg=HandControl()        
        
        self.cmd_msg=Twist()
        self.turtlebot_status_msg = TurtlebotStatus()
        self.is_turtlebot_status = False

        self.working_status_msg = Int16()

        thread = threading.Thread(target = self.timer_callback)
        thread.daemon=True
        thread.start()
    def timer_callback(self):
        while True:
            time.sleep(1)
            print(checkCurrStage(self.working_status_msg.data))
            
            if checkCurrStage(self.working_status_msg.data) == 5: # 물건앞 도착해서 물건들기
                print("나 지금 들어올린다") 
                self.hand_control_pick_up()  
                self.working_status_msg.data = getCurrStage(6)
                self.working_status_pub.publish(self.working_status_msg)

            # 물건을 든 상태면 아래 조건만족
            if checkCurrStage(self.working_status_msg.data) == 6 and self.turtlebot_status_msg.can_put ==False and self.turtlebot_status_msg.can_use_hand == True:
                self.working_status_msg.data = getCurrStage(7)
                self.working_status_pub.publish(self.working_status_msg)
            
            if checkCurrStage(self.working_status_msg.data) == 9: # 들고 목적지 다온경우
                print("나 다왔어")
                self.hand_control_preview()
                time.sleep(1)
                self.hand_control_put_down()
                self.working_status_msg.data = getCurrStage(10)
                self.cmd_msg.linear.x=0.0
                self.cmd_msg.angular.z=0.0
                self.cmd_pub.publish(self.cmd_msg)
                self.working_status_pub.publish(self.working_status_msg)

    def hand_control_status(self):
        '''
        로직 3. Hand Control Status 출력 - 완료
        '''
        print('can_lift : ',self.turtlebot_status_msg.can_lift, ', can_put : ', self.turtlebot_status_msg.can_put, ', can_use_hand : ', self.turtlebot_status_msg.can_use_hand,']') 
        print("Control_mode : {0} , put_distance : {1} put_height : {2}".format(self.hand_control_msg.control_mode, self.hand_control_msg.put_distance, self.hand_control_msg.put_height))
        
        

    def hand_control_preview(self):
        '''
        로직 4. Hand Control - Preview - 완료
        '''
        self.hand_control_msg.control_mode = 1

        while self.turtlebot_status_msg.can_put ==False and self.turtlebot_status_msg.can_use_hand == True:
            self.hand_control.publish(self.hand_control_msg)

        
    def hand_control_pick_up(self):
        '''
        로직 5. Hand Control - Pick up - 완료   
        '''
        
        self.hand_control_msg.control_mode = 2
        self.hand_control_msg.put_distance = 0.7
        self.hand_control_msg.put_height = 0.2
        print("들기 함수실행")
        
        while self.turtlebot_status_msg.can_lift ==True:
            print("나여기 갖혀있어")
            self.hand_control.publish(self.hand_control_msg)    

    def hand_control_put_down(self):        
        '''
        로직 6. Hand Control - Put down -완료
        '''
        self.hand_control_msg.control_mode = 3
        while self.turtlebot_status_msg.can_put ==True:
            self.hand_control.publish(self.hand_control_msg)

    def turtlebot_status_cb(self,msg):
        self.is_turtlebot_status=True
        self.turtlebot_status_msg=msg
    
    def working_status_callback(self,msg):
        self.working_status_msg = msg

def main(args=None):
    rclpy.init(args=args)
    sub1_hand_control = Handcontrol()    
    rclpy.spin(sub1_hand_control)
    sub1_hand_control.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()