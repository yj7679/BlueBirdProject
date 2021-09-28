import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist,Point,Point32
from ssafy_msgs.msg import TurtlebotStatus
from squaternion import Quaternion
from nav_msgs.msg import Odometry,OccupancyGrid,MapMetaData,Path
from geometry_msgs.msg import Pose,PoseStamped
from math import pi,cos,sin,sqrt,atan2
import numpy as np
from collections import deque
import heapq as hq
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
        self.subscription = self.create_subscription(Path,'/global_path',self.path_callback,10)
        self.local_map_sub = self.create_subscription(OccupancyGrid,'/local_map',self.local_map_callback,10)
        self.global_map_sub = self.create_subscription(OccupancyGrid,'/global_map',self.global_map_callback,10)
        self.a_star_pub= self.create_publisher(Path, 'global_path', 1)
        self.pcd_pub = self.create_publisher(PointCloud, 'pcd',1)
        self.goal_sub = self.create_subscription(PoseStamped,'goal_pose',self.goal_callback,1)      
        
        # 라이다 데이터 받기위한 subscriber
        self.lidar_sub = self.create_subscription(LaserScan, '/scan', self.lidar_callback, 10)

        # 로직 1. 제어 주기 및 타이머 설정
        time_period=0.05 
        self.timer = self.create_timer(time_period, self.timer_callback)
        
        self.is_global_map=False
        self.is_local_map=False
        self.is_odom=False
        self.is_path=False
        self.is_status=False
        self.collision = False
        self.is_local_grid_update=False
        self.is_global_grid_update=False

        self.odom_msg=Odometry()            
        self.robot_yaw=0.0
        self.path_msg=Path()
        self.cmd_msg=Twist()
        self.local_map_msg = OccupancyGrid()
        self.global_map_msg = OccupancyGrid()
        # 로직 2. 파라미터 설정
        self.goal = [184,224] #초기설정 : 에어컨 앞, 목적지를 찍지 않으면 이 곳이 목적지
        #맵에 대한 파라미터, 위치 x y를 맵 cell에 매칭할 때 혹인 그 반대로 맵 cell을 위치 x y로 바꿀 때 사용할 파라미터
        self.map_size_x=350
        self.map_size_y=350
        self.map_resolution=0.05
        self.map_offset_x=-14.75
        self.map_offset_y=1.25
    
        self.GRIDSIZE=350 
        
        # 주변의 인덱스를 탐색할 때 사용하기 위해 만든 변수
        self.dx = [-1,0,0,1,-1,-1,1,1]
        self.dy = [0,1,-1,0,-1,1,-1,1]
        self.dCost = [1,1,1,1,1.414,1.414,1.414,1.414]
        # 각 셀 1칸 = 1, 대각선 = 1.414
        # 로직 2. 파라미터 설정
        self.lfd=0.1
        self.min_lfd=0.1
        self.max_lfd=1.0


    def timer_callback(self):
  
        if self.is_status and self.is_odom ==True and self.is_path==True:

             
            if len(self.path_msg.poses)> 1:
                self.is_look_forward_point= False
                
                # 로봇의 현재 위치를 나타내는 변수
                robot_pose_x=self.odom_msg.pose.pose.position.x
                robot_pose_y=self.odom_msg.pose.pose.position.y

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
                    if self.collision==False:
                        out_vel = 0.7
                        out_rad_vel= theta * 1.3

                        self.cmd_msg.linear.x=out_vel
                        self.cmd_msg.angular.z=out_rad_vel
                    
                    # 충돌이 났다면 장애물을 인식 -> local_map + global_map을 통해 경로 재생성
                    

                              
            else :
                print("no found forward point")
                self.cmd_msg.linear.x=0.0
                self.cmd_msg.angular.z=0.0

            # 충돌 안난경우만 publish
            if self.collision==False:
                self.cmd_pub.publish(self.cmd_msg)
    
    # 처음 global path를 결정하는 부분
    def goal_callback(self,msg):
        print("goal")
        if msg.header.frame_id=='map':
            '''
            로직 6. goal_pose 메시지 수신하여 목표 위치 설정
            목적지를 받았을 때 호출되는 함수
            다른 frame에서 찍으면 좌표계가 다르기 때문에 rviz의 fixed_frame이 'map'인 상태에서 목적지를 입력했을 때만 사용 가능
            x y 좌표를 받아서 pose_to_grid_cell 함수로 목적지를 cell 단위로 바꿔준다.
            
            '''
            goal_x = msg.pose.position.x
            goal_y = msg.pose.position.y
            goal_cell = self.pose_to_grid_cell(goal_x,goal_y)
            self.goal = list(map(int, goal_cell))
            print("local ",self.is_local_map)
            print("global ",self.is_global_map)
            print("odom ", self.is_odom)
            if self.is_local_map ==True and self.is_global_map == True and self.is_odom==True  :
                if self.is_global_grid_update==False :
                    self.global_grid_update()
                if self.is_local_grid_update==False :
                    self.local_grid_update()

                print(self.global_grid[self.goal[0]][self.goal[1]])
        
                self.final_path=[]

                x=self.odom_msg.pose.pose.position.x
                y=self.odom_msg.pose.pose.position.y
                start_grid_cell=self.pose_to_grid_cell(x,y)

                self.path = [[0 for col in range(self.GRIDSIZE)] for row in range(self.GRIDSIZE)] # 방문 배열 -> 해당 그리드 위치에 갔을 때, 어디에서왔는지 좌표를 저장
                self.cost = np.array([[self.GRIDSIZE*self.GRIDSIZE for col in range(self.GRIDSIZE)] for row in range(self.GRIDSIZE)]) # 코스트 비교할 때, 필요할 때

                
                # 다익스트라 알고리즘을 완성하고 주석을 해제 시켜주세요. 
                # 시작지, 목적지가 탐색가능한 영역이고, 시작지와 목적지가 같지 않으면 경로탐색을 합니다.
                if self.global_grid[start_grid_cell[0]][start_grid_cell[1]] == 0  and self.global_grid[self.goal[0]][self.goal[1]] == 0  and start_grid_cell != self.goal :
                    self.dijkstra(start_grid_cell)


                self.global_path_msg=Path()
                self.global_path_msg.header.frame_id='map'
                for grid_cell in reversed(self.final_path) :
                    tmp_pose=PoseStamped()
                    waypoint_x,waypoint_y=self.grid_cell_to_pose(grid_cell)
                    tmp_pose.pose.position.x=waypoint_x
                    tmp_pose.pose.position.y=waypoint_y
                    tmp_pose.pose.orientation.w=1.0
                    self.global_path_msg.poses.append(tmp_pose)
            
                if len(self.final_path)!=0 :
                    self.a_star_pub.publish(self.global_path_msg)

    def dijkstra(self,start):

        Q = [(self.hEucl(start), start)]
        self.cost[start[0]][start[1]] = 1
        hq.heapify(Q)


        found = False
        print("다익스트라 실행")

        '''
        로직 7. grid 기반 최단경로 탐색
        deque를 이용해 탐색할 노드를 하나씩 append해서 사용하며 Q에 더 이상 탐색할 노드가 없으면 
        while문을 빠져나온다.
        그게 아니면 Q의 popleft()를 이용해 탐색할 노드를 선택하고 dx, dy를 이용해 next가 for문을 돌 때마다 바뀌게 설정한다.
        '''
        # self.grid는 local_grid와 global_grid를 통합해서 
        self.grid = [[0 for _ in range(self.GRIDSIZE)] for _ in range(self.GRIDSIZE)]

        for i in range(self.GRIDSIZE):
            for j in range(self.GRIDSIZE):
                # 새로 탐지된 장애물 일 때 반영해줌

                if self.local_grid[i][j] == 100 and self.global_grid[i][j] <50:
                    self.grid[i][j] = self.local_grid[i][j]
                    print("반영 ",i,j)
                else: # 나머지 부분은 global_map을 따라감
                    self.grid[i][j] = self.global_grid[i][j]
        print("local : ",self.local_grid[self.goal[0]][self.goal[1]])
        print("global : ",self.global_grid[self.goal[0]][self.goal[1]])
        print("grid : ",self.local_grid[self.goal[0]][self.goal[1]])

                
        while len(Q) !=0 : 
            if Q[0][1] == self.goal: 
                break

            current = hq.heappop(Q)[1]

            for i in range(8):
                #next는 current에 인접한 노드가 선택된다.
                next = (current[0] + self.dx[i], current[1] + self.dy[i]) 
                if next[0] >= 0 and next[1] >= 0 and next[0] < self.GRIDSIZE and next[1] < self.GRIDSIZE:
                    # next노드의 grid값이 50보다 작으면 로봇이 갈 수 있다는 의미이기 때문에 코스트 계산
                    # 코스트가 낮으면 path, cost변수를 갱신 후 Q에 next를 넣어준다.
                        if self.grid[next[0]][next[1]] < 50:
                            if self.cost[current[0]][current[1]] + self.dCost[i] < self.cost[next[0]][next[1]]:
                                
                                self.path[next[0]][next[1]] = current
                                self.cost[next[0]][next[1]] = self.cost[current[0]][current[1]] + self.dCost[i]
                                priority = self.cost[next[0]][next[1]] + self.hEucl(next)

                                hq.heappush(Q, (priority, next))

        # 모든 노드의 탐색이 끝났으면 저장했던 path를 역으로 추적해서 최종 경로를 얻는다.
        # 주석대로 처리하면 dijkstra방식이고 여기에 heuristic함수를 추가하면 a_star가 된다.
        node = self.goal



        while node != start:
            y = node[1]
            x = node[0]
            print(x, y)
            nextNode = self.path[x][y]
            self.final_path.append(nextNode)
            node = nextNode
        self.collision = False
        print("다익스트라 종료", self.collision)
    
    def hEucl(self, node):
        dx = abs(node[0] - self.goal[0])
        dy = abs(node[1] - self.goal[1])
        D = 1 
        return D * np.sqrt(dx * dx + dy * dy)            

    def odom_callback(self, msg):
        self.is_odom=True
        self.odom_msg=msg
        '''
        로직 3. Quaternion 을 euler angle 로 변환
        '''
        # 메시지로 날라온 쿼터니언을 다시 오일러로 바꿔서 알고리즘에 넣을 수 있도록 한다. 인자는 w,x,y,z순서
        q = Quaternion(msg.pose.pose.orientation.w,msg.pose.pose.orientation.x,msg.pose.pose.orientation.y,msg.pose.pose.orientation.z)
        
        _,_,self.robot_yaw= q.to_euler()

    # 맵 메시지를 grid 배열로
    def local_grid_update(self):
        self.is_local_grid_update=True
        map_to_grid=list(map(int, self.local_map_msg.data)) # 리스트로 만들고 int형으로 바꾼다.      
        self.local_grid=np.reshape(map_to_grid, (350,350),order='F') # 350*350 그리드로 만듬
        

    def global_grid_update(self):
        self.is_global_grid_update=True

        map_to_grid=list(map(int, self.global_map_msg.data)) # 리스트로 만들고 int형으로 바꾼다.        
        self.global_grid=np.reshape(map_to_grid, (350,350),order='F') # 350*350 그리드로 만듬

    # 연속 좌표 x,y를 넣었을 때, 우리가 탐색할 수 있도록 그리드 위치로 만들어 주는 함수
    def pose_to_grid_cell(self,x,y):
        map_point_x = 0
        map_point_y = 0
        '''
        로직 4. 위치(x,y)를 map의 grid cell로 변환 - 완료 하긴했는데 이상함..
        (테스트) pose가 (-8,-4)라면 맵의 중앙에 위치하게 된다. 따라서 map_point_x,y 는 map size의 절반인 (175,175)가 된다.
        pose가 (-16.75, -12.75) 라면 맵의 시작점에 위치하게 된다. 따라서 map_point_x,y는 (0,0)이 된다.???시작위치 -12.75인듯.. rviz2에서 확실하게 확인했음.
        '''
        # 사전학습 5강 11분 30초 
        map_point_x= int((x-self.map_offset_x)/ self.map_resolution)
        map_point_y= int((y-self.map_offset_y)/ self.map_resolution)

        
        return map_point_x,map_point_y

    # 그리드 위치를 연속좌표 x,y로 만들어 주는 것
    def grid_cell_to_pose(self,grid_cell):

        x = 0
        y = 0
        '''
        로직 5. map의 grid cell을 위치(x,y)로 변환 - 완료햇긴한데 이상함..
        최단경로 탐색결과는 맵의 cell로 얻어지기 때문에 전역경로로 만들 때는 위치 x y로 변환해서 사용해야한다.
        변환에는 map_offset, map_size, map_resolution이용
        (테스트) grid cell이 (175,175)라면 맵의 중앙에 위치하게 된다. 따라서 pose로 변환하게 되면 맵의 중앙인 (-8,-4)가 된다.
        grid cell이 (350,350)라면 맵의 제일 끝 좌측 상단에 위치하게 된다. 따라서 pose로 변환하게 되면 맵의 좌측 상단인 (0.75,6.25)가 된다. ??? (0.75, 4.75)인데..?
        '''

        grid_x, grid_y = grid_cell

        # 사전학습 5강 11분 30초 
        x = grid_x * self.map_resolution + self.map_offset_x
        y = grid_y * self.map_resolution + self.map_offset_y
        
        return [x,y]

    def local_map_callback(self, msg):
        self.is_local_map=True
        self.local_map_msg=msg
    
    def global_map_callback(self, msg):
        self.is_global_map=True
        self.global_map_msg=msg
        
    def path_callback(self, msg):
        self.is_path=True
        self.path_msg=msg


    def status_callback(self,msg):
        self.is_status=True
        self.status_msg=msg

    # 충돌 체크부분
    def lidar_callback(self, msg):
        self.lidar_msg=msg
        # 경로, 위치를 알아야 충돌 체크 가능
        if self.is_path==True and self.is_odom == True:
            
            # 1. 극좌표계-> 직교좌표계로 바꾸기
            pcd_msg = PointCloud()
            pcd_msg.header.frame_id='map'

            # local -> global
            pose_x = self.odom_msg.pose.pose.position.x
            pose_y = self.odom_msg.pose.pose.position.y
            theta = self.robot_yaw
            t=np.array([[cos(theta), -sin(theta), pose_x],
                        [sin(theta), cos(theta), pose_y],
                        [0,0,1]])
            for angle, r in enumerate(msg.ranges):
                global_point = Point32()

                if 0.0< r < 12:
                    #극좌표계 -> 직교좌표계
                    local_x = r*cos(angle*pi/180)
                    local_y = r*sin(angle*pi/180)
                    local_point=np.array(([local_x],[local_y],[1]))
                    # 로봇기준 local -> 맵기준 global
                    global_result = t.dot(local_point)
                    global_point.x = global_result[0][0]
                    global_point.y = global_result[1][0]
                    pcd_msg.points.append(global_point)
            
            self.collision=False
            for waypoint in self.path_msg.poses :
                for lidar_point in pcd_msg.points :
                    distance = sqrt(pow(waypoint.pose.position.x - lidar_point.x, 2)+pow(waypoint.pose.position.y - lidar_point.y, 2))
                    if distance < 0.01:
                        self.collision = True
                        print('collision')
                        # 0.02을 뒤로감
                        back_distance = 0.0
                        self.prev_time=rclpy.clock.Clock().now()
                        while back_distance < 0.02:
                            print("뒤로 가는중")
                            print(back_distance)
                            # 이전 스텝과 현재 스텝간의 시간 차이 계산
                            self.current_time=rclpy.clock.Clock().now()
                            self.period=(self.current_time-self.prev_time).nanoseconds/(1e+9)

                            back_distance += self.period
                            self.cmd_msg.linear.x=-1.0
                            self.cmd_msg.angular.z=0.0
                            self.cmd_pub.publish(self.cmd_msg)
                            self.prev_time=self.current_time
                        # 뒤로 간 뒤 멈춤
                        self.cmd_msg.linear.x=0.0
                        self.cmd_msg.angular.z=0.0
                        self.cmd_pub.publish(self.cmd_msg)
                        break
                if self.collision == True:
                    print("충돌 발생해서 맵 새로그리기")
                    self.cmd_msg.linear.x=0.0
                    self.cmd_msg.angular.z=0.0
                    self.cmd_pub.publish(self.cmd_msg)
                    # path가 있고 local map도 들어오고 odom도 들어올 때
                    print("------")
                    print(self.is_path)
                    print(self.is_local_map)
                    print(self.is_global_map)
                    print(self.is_odom)
                    print("====")
                    if self.is_path == True and self.is_local_map ==True and self.is_global_map ==True and self.is_odom==True  :
                        print("그리기 진행")
                        if self.is_local_grid_update==False :
                            self.local_grid_update()
                        if self.is_global_grid_update==False :
                            self.global_grid_update()
                        
                        self.final_path=[]

                        x=self.odom_msg.pose.pose.position.x
                        y=self.odom_msg.pose.pose.position.y
                        start_grid_cell=self.pose_to_grid_cell(x,y)

                        self.path = [[0 for col in range(self.GRIDSIZE)] for row in range(self.GRIDSIZE)] # 방문 배열 -> 해당 그리드 위치에 갔을 때, 어디에서왔는지 좌표를 저장
                        self.cost = np.array([[self.GRIDSIZE*self.GRIDSIZE for col in range(self.GRIDSIZE)] for row in range(self.GRIDSIZE)]) # 코스트 비교할 때, 필요할 때

                        #print(self.grid[self.goal[0]][self.goal[1]])
                        
                        if self.global_grid[start_grid_cell[0]][start_grid_cell[1]] == 0  and self.global_grid[self.goal[0]][self.goal[1]] == 0  and start_grid_cell != self.goal :
                            self.dijkstra(start_grid_cell)


                        self.global_path_msg=Path()
                        self.global_path_msg.header.frame_id='map'
                        for grid_cell in reversed(self.final_path) :
                            tmp_pose=PoseStamped()
                            waypoint_x,waypoint_y=self.grid_cell_to_pose(grid_cell)
                            tmp_pose.pose.position.x=waypoint_x
                            tmp_pose.pose.position.y=waypoint_y
                            tmp_pose.pose.orientation.w=1.0
                            self.global_path_msg.poses.append(tmp_pose)
                    
                        if len(self.final_path)!=0 :
                            self.a_star_pub.publish(self.global_path_msg)
                        self.collision = False                   
                    break # 들여쓰기 이게 맞다       

            self.is_lidar=True    
            self.pcd_pub.publish(pcd_msg)    

        
def main(args=None):
    rclpy.init(args=args)

    path_tracker = followTheCarrot()

    rclpy.spin(path_tracker)


    path_tracker.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
