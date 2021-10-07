import rclpy
from rclpy.node import Node

import time
from geometry_msgs.msg import Twist,Point,Point32
from ssafy_msgs.msg import TurtlebotStatus
from squaternion import Quaternion
from nav_msgs.msg import Odometry,Path
from math import pi,cos,sin,sqrt,atan2
import numpy as np
from std_msgs.msg import Int16
from modules import *

# 센서 데이터를 받아 사용하기 위함.
from sensor_msgs.msg import LaserScan, PointCloud
# path_tracking 노드는 로봇의 위치(/odom), 로봇의 속도(/turtlebot_status), 주행 경로(/local_path)를 받아서, 주어진 경로를 따라가게 하는 제어 입력값(/cmd_vel)을 계산합니다.
# 제어입력값은 선속도와 각속도로 두가지를 구합니다. 
# sub2의 path_tracking은 sub1의 path_tracking를 사용해도 됩니다.


# 노드 로직 순서
# 1. 제어 주기 및 타이머 설정
# 2. 파라미터 설정
# 3. Quaternion 을 euler angle 로 변환
# 4. 터틀봇이 주어진 경로점과 떨어진 거리(lateral_error)와 터틀봇의 선속도를 이용해 전방주시거리 계산
# 5. 전방 주시 포인트 설정
# 6. 전방 주시 포인트와 로봇 헤딩과의 각도 계산
# 7. 선속도, 각속도 정하기


class followTheCarrot(Node):

    def __init__(self):
        super().__init__('path_tracking')
        self.cmd_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.subscription = self.create_subscription(Odometry,'/odom',self.odom_callback,10)
        self.status_sub = self.create_subscription(TurtlebotStatus,'/turtlebot_status',self.status_callback,10)
        self.path_sub = self.create_subscription(Path,'/local_path',self.path_callback,10)
        
        self.working_status_sub = self.create_subscription(Int16,'/working_status',self.working_status_callback,10) # woring status 값 받고 값을 다시 담아주기 위해 사용
        self.working_status_pub = self.create_publisher(Int16,'working_status',10) # woring status 값 받고 값을 다시 담아주기 위해 사용
    

        # 로직 1. 제어 주기 및 타이머 설정
        time_period=0.05 
        self.timer = self.create_timer(time_period, self.timer_callback)

        # 주행이 다끝나면 로직 처리 (최종 목적지 도착인 경우는 0으로만들고, 아닌 경우는 bit shift + 1)
        self.is_finish_driving = True
        self.is_odom=False
        self.is_path=False
        self.is_status=False
        self.collision = False
        self.working_status_msg = Int16()
        self.odom_msg=Odometry()            
        self.robot_yaw=0.0
        # 현재 일중인지 publish 할 것
        self.path_msg=Path()
        self.cmd_msg=Twist()
        # 로직 2. 파라미터 설정
        self.lfd=0.1
        self.min_lfd=0.1
        self.max_lfd=1.0
        

    def timer_callback(self):
        # 가야할 때만 가는 것

        # if self.is_status and self.is_odom ==True and self.is_path==True and (self.working_status_msg.data == 0b0011 or self.working_status_msg.data == 0b00111111 or self.working_status_msg.data == 0b11111111 or self.working_status_msg.data == ):
        if self.is_status and self.is_odom ==True and self.is_path==True:

            if len(self.path_msg.poses)> 1:
                self.is_look_forward_point= False
                self.is_finish_driving = False
                # 로봇의 절대위치를 받아옴
                robot_pose_x=self.status_msg.twist.angular.x
                robot_pose_y=self.status_msg.twist.angular.y

                # 로봇이 경로에서 떨어진 거리를 나타내는 변수
                lateral_error= sqrt(pow(self.path_msg.poses[0].pose.position.x-robot_pose_x,2)+pow(self.path_msg.poses[0].pose.position.y-robot_pose_y,2))
                #print(robot_pose_x,robot_pose_y,lateral_error)
                '''
                로직 4. 로봇이 주어진 경로점과 떨어진 거리(lateral_error)와 로봇의 선속도를 이용해 전방주시거리 설정 - 완료
                '''
                self.lfd= (self.status_msg.twist.linear.x +lateral_error) * 0.5 # ? 적절하게 전방주시거리를 설정한다
                
                if self.lfd < self.min_lfd :
                    self.lfd=self.min_lfd
                if self.lfd > self.max_lfd:
                    self.lfd=self.max_lfd

                

                min_dis=float('inf')
                '''
                로직 5. 전방 주시 포인트 설정 - 완료
                '''
                for num,waypoint in enumerate(self.path_msg.poses) :
                    self.current_point = waypoint.pose.position

                    dis = sqrt(pow(self.path_msg.poses[0].pose.position.x - self.current_point.x,2) + pow(self.path_msg.poses[0].pose.position.y - self.current_point.y,2))
                    if abs(dis - self.lfd) < min_dis:
                        min_dis = abs(dis - self.lfd)
                        self.forward_point = self.current_point
                        self.is_look_forward_point = True

                              
                
                if self.is_look_forward_point :
            
                    global_forward_point=[self.forward_point.x ,self.forward_point.y,1]

                    '''
                    로직 6. 전방 주시 포인트와 로봇 헤딩과의 각도 계산 - 완료

                    (테스트) 맵에서 로봇의 위치(robot_pose_x,robot_pose_y)가 (5,5)이고, 헤딩(self.robot_yaw) 1.57 rad 일 때, 선택한 전방포인트(global_forward_point)가 (3,7)일 때
                    변환행렬을 구해서 전방포인트를 로봇 기준좌표계로 변환을 하면 local_forward_point가 구해지고, atan2를 이용해 선택한 점과의 각도를 구하면
                    theta는 0.7853 rad 이 나옵니다.
                    trans_matrix는 로봇좌표계에서 기준좌표계(Map)로 좌표변환을 하기위한 변환 행렬입니다.
                    det_tran_matrix는 trans_matrix의 역행렬로, 기준좌표계(Map)에서 로봇좌표계로 좌표변환을 하기위한 변환 행렬입니다.  
                    local_forward_point 는 global_forward_point를 로봇좌표계로 옮겨온 결과를 저장하는 변수입니다.
                    theta는 로봇과 전방 주시 포인트와의 각도입니다. 
                    '''

                    trans_matrix = np.array([
                        [cos(self.robot_yaw), -sin(self.robot_yaw), robot_pose_x],
                        [sin(self.robot_yaw), cos(self.robot_yaw), robot_pose_y],
                        [0, 0, 1]

                    ])

                    det_trans_matrix = np.linalg.inv(trans_matrix)
                    local_forward_point = det_trans_matrix.dot(global_forward_point)
                    theta = -atan2(local_forward_point[1],local_forward_point[0])
                    

                    
                    '''
                    로직 7. 선속도, 각속도 정하기
                    '''

                    out_vel = 0.3
                    out_rad_vel= theta * 1.1

                                 
                    self.cmd_msg.linear.x=out_vel
                    self.cmd_msg.angular.z=out_rad_vel
                    
 
                    
           
            else :
                # 주행 중이다가 마지막 위치 도착하면 실행
                if self.is_finish_driving == False:
                    print("이거반복되면 안됨!!")
                    if self.working_status_msg.data == getUDPstage(2):
                        print('path_tracking.py : 2단계에서 목적지에 도착했습니다. 3단계를 퍼블리시합니다.')
                        self.is_finish_driving = True
                        self.working_status_msg.data = getUDPstage(3)
                        self.working_status_pub.publish(self.working_status_msg)
                    else :
                        print('working status = 2')
                        self.is_finish_driving = True
                        self.working_status_msg.data = getCurrStage(checkCurrStage(self.working_status_msg.data) + 1) # 비트 shift하고 + 1
                        self.working_status_pub.publish(self.working_status_msg)
                    

                print("no found forward point")
                self.cmd_msg.linear.x=0.0
                self.cmd_msg.angular.z=0.0

            
            self.cmd_pub.publish(self.cmd_msg)

 
    
          
    def working_status_callback(self,msg):
        self.working_status_msg = msg

    def odom_callback(self, msg):
        self.is_odom=True
        self.odom_msg=msg
        '''
        로직 3. Quaternion 을 euler angle 로 변환
        '''
        # 메시지로 날라온 쿼터니언을 다시 오일러로 바꿔서 알고리즘에 넣을 수 있도록 한다. 인자는 w,x,y,z순서
        q = Quaternion(msg.pose.pose.orientation.w,msg.pose.pose.orientation.x,msg.pose.pose.orientation.y,msg.pose.pose.orientation.z)
        
        _,_,self.robot_yaw= q.to_euler()

    def path_callback(self, msg):
        self.is_path=True
        self.path_msg=msg       


    def status_callback(self,msg):
        self.is_status=True
        self.status_msg=msg

 
        
def main(args=None):
    rclpy.init(args=args)

    path_tracker = followTheCarrot()

    rclpy.spin(path_tracker)


    path_tracker.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
