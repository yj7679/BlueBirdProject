import rclpy
import numpy as np
from rclpy.node import Node
import os
from geometry_msgs.msg import Pose,PoseStamped
from squaternion import Quaternion
from nav_msgs.msg import Odometry,OccupancyGrid,MapMetaData,Path
from math import pi,cos,sin
from collections import deque
import heapq as hq
# a_star 노드는  OccupancyGrid map을 받아 grid map 기반 최단경로 탐색 알고리즘을 통해 로봇이 목적지까지 가는 경로를 생성하는 노드입니다.
# 로봇의 위치(/pose), 맵(/map), 목표 위치(/goal_pose)를 받아서 전역경로(/global_path)를 만들어 줍니다. 
# goal_pose는 rviz2에서 2D Goal Pose 버튼을 누르고 위치를 찍으면 메시지가 publish 됩니다. 
# 주의할 점 : odom을 받아서 사용하는데 기존 odom 노드는 시작했을 때 로봇의 초기 위치가 x,y,heading(0,0,0) 입니다. 로봇의 초기위치를 맵 상에서 로봇의 위치와 맞춰줘야 합니다. 
# 따라서 sub2의 odom 노드를 수정해줍니다. turtlebot_status 안에는 정답데이터(절대 위치)가 있는데 그 정보를 사용해서 맵과 로봇의 좌표를 맞춰 줍니다.

# 노드 로직 순서
# 1. publisher, subscriber 만들기
# 2. 파라미터 설정
# 3. 맵 데이터 행렬로 바꾸기
# 4. 위치(x,y)를 map의 grid cell로 변환
# 5. map의 grid cell을 위치(x,y)로 변환
# 6. goal_pose 메시지 수신하여 목표 위치 설정
# 7. grid 기반 최단경로 탐색

# 이 코드의 목표 : A* 알고리즘을 적용해서 글로벌 패스를 만든다.
class a_star(Node):

    def __init__(self):
        super().__init__('a_Star')
        print("a_star is ready")
        # 로직 1. publisher, subscriber 만들기
        self.map_sub = self.create_subscription(OccupancyGrid,'global_map',self.map_callback,1)
        self.odom_sub = self.create_subscription(Odometry,'odom',self.odom_callback,1) #로봇의 위치를 받아서 출발지로 하기 위하여 odom받음
        self.goal_sub = self.create_subscription(PoseStamped,'goal_pose',self.goal_callback,1)
        self.a_star_pub= self.create_publisher(Path, 'global_path', 1)
        
        self.map_msg=OccupancyGrid()
        self.odom_msg=Odometry()
        self.is_map=False
        self.is_odom=False
        self.is_found_path=False
        self.is_grid_update=False


        # 로직 2. 파라미터 설정
        self.goal = [184,224] #초기설정 : 에어컨 앞, 목적지를 찍지 않으면 이 곳이 목적지
        #맵에 대한 파라미터, 위치 x y를 맵 cell에 매칭할 때 혹인 그 반대로 맵 cell을 위치 x y로 바꿀 때 사용할 파라미터
        self.map_size_x=350
        self.map_size_y=430
        self.map_resolution=0.05
        self.map_offset_x=-14.75
        self.map_offset_y=1.25
    
        self.GRIDSIZE=350 
        
        # 주변의 인덱스를 탐색할 때 사용하기 위해 만든 변수
        self.dx = [-1,0,0,1,-1,-1,1,1]
        self.dy = [0,1,-1,0,-1,1,-1,1]
        self.dCost = [1,1,1,1,1.414,1.414,1.414,1.414]
        # 각 셀 1칸 = 1, 대각선 = 1.414


    def grid_update(self):
        self.is_grid_update=True
        
        '''
        로직 3. 맵 데이터 행렬로 바꾸기 - 완료
        메시지를 통해 받은 맵은 1차원 배열로 들어오기 때문에 좀 더 직관적으로 사용 위해 350*350인 2차원행렬로 바꿔준다.
        '''
        map_to_grid=list(map(int, self.map_msg.data)) # 리스트로 만들고 int형으로 바꾼다.
        
        self.grid=np.reshape(map_to_grid, (350,350),order='F') # 350*350 그리드로 만듬
        print(self.grid)

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


    def odom_callback(self,msg):
        self.is_odom=True
        self.odom_msg=msg
        


    def map_callback(self,msg):
        self.is_map=True
        self.map_msg=msg

    # goal_pose 메시지는 rviz2에서 2D Goal pose 클릭하고 맵에 목적지 누르면 publish되기 때문에 a_star.py에서 받아올 수있음
    def goal_callback(self,msg):
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

            goal_x = msg.pose.position.x
            goal_y = msg.pose.position.y
            goal_cell = self.pose_to_grid_cell(goal_x,goal_y)
            self.goal = list(map(int, goal_cell))


            print(self.is_map)
            print(self.is_odom)
            if self.is_map ==True and self.is_odom==True  :
                if self.is_grid_update==False :
                    self.grid_update()
        
                self.final_path=[]

                x=self.odom_msg.pose.pose.position.x
                y=self.odom_msg.pose.pose.position.y
                start_grid_cell=self.pose_to_grid_cell(x,y)

                self.path = [[0 for col in range(self.GRIDSIZE)] for row in range(self.GRIDSIZE)] # 방문 배열 -> 해당 그리드 위치에 갔을 때, 어디에서왔는지 좌표를 저장
                self.cost = np.array([[self.GRIDSIZE*self.GRIDSIZE for col in range(self.GRIDSIZE)] for row in range(self.GRIDSIZE)]) # 코스트 비교할 때, 필요할 때

                print(self.grid[self.goal[0]][self.goal[1]])
                # 다익스트라 알고리즘을 완성하고 주석을 해제 시켜주세요. 
                # 시작지, 목적지가 탐색가능한 영역이고, 시작지와 목적지가 같지 않으면 경로탐색을 합니다.
                if self.grid[start_grid_cell[0]][start_grid_cell[1]] == 0  and self.grid[self.goal[0]][self.goal[1]] == 0  and start_grid_cell != self.goal :
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
    
    
    def hEucl(self, node):
        dx = abs(node[0] - self.goal[0])
        dy = abs(node[1] - self.goal[1])
        D = 1 
        return D * np.sqrt(dx * dx + dy * dy)           
    
    def hMan(self, node):
        dx = abs(node[0] - self.goal[0])
        dy = abs(node[1] - self.goal[1])
        D = 1
        return D * (dx + dy) 


        
def main(args=None):
    rclpy.init(args=args)

    global_planner = a_star()

    rclpy.spin(global_planner)


    global_planner.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
