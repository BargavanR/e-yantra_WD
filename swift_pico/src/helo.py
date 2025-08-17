

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose
from waypoint_navigation.srv import GetWaypoints
import heapq
import random
import cv2  

class AStarPathfinder:
    def __init__(self, grid):
        self.grid = grid
        self.rows, self.cols = grid.shape
        self.directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, down, left, right

    def is_valid(self, row, col):
        # Check if within bounds and not an obstacle
        return 0 <= row < self.rows and 0 <= col < self.cols and self.grid[row, col] == 0

    def heuristic(self, start, end):
        # Manhattan distance heuristic
        return abs(start[0] - end[0]) + abs(start[1] - end[1])

    def find_path(self, start, end):
        # Priority queue to store the paths
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == end:
                return self.reconstruct_path(came_from, current)

            for d in self.directions:
                neighbor = (current[0] + d[0], current[1] + d[1])

                if self.is_valid(neighbor[0], neighbor[1]):
                    tentative_g_score = g_score[current] + 1

                    if tentative_g_score < g_score.get(neighbor, float('inf')):
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score = tentative_g_score + self.heuristic(neighbor, end)
                        heapq.heappush(open_set, (f_score, neighbor))

        return None  # Return None if no path is found
    
class DronePathPlanner(Node):
    def __init__(self):
        super().__init__('drone_path_planner')

    def reconstruct_path(self, came_from, current):
        # Backtrace the path
        path = []
        while current in came_from:
            path.append(current)
            current = came_from[current]
        path.append(current)
        return path[::-1]
        
        

    def pixel_to_whycon(imgx, imgy):
        goal_x= 0.02537*imgx - 12.66
        goal_y= 0.02534*imgy - 12.57
        goal_z= 27.0
        goal = [goal_x, goal_y, goal_z]
        return goal
    
    def whycon_to_pixel(x,y,z):
        imgx=(x+12.66)/0.02537
        imgy =(y+12.57)/0.02534
        image_goal = [imgx,imgy]
        return image_goal
    
    def path_planning(self):
        self.planned_path=[]
        self.image_path = cv2.imread('2D_bit_map.png', cv2.IMREAD_GRAYSCALE)
        self.planned_path = []
        self.whyconpath = []

        #Replace with your actual waypoints
        self.randomly_generate_waypoints = [[-6.3175,0.1,27],[-5.3175,0.1,27]]
        
        self.pathfinder = AStarPathfinder(self.image_path)
        #self.whycon_startend = self.randomly_generate_waypoints

        self.whyconpath=[]
        self.changedValues =[]
        self.pathfinder=AStarPathfinder(self.image_path) 
        for i in  range(len(self.randomly_generate_waypoints)):
            self.changedValues.append(self.whycon_to_pixel(self.randomly_generate_waypoints[i]))
            print(self.changedValues)
        for i in  range (len(self.changedValues)):
            
            path = self.pathfinder.find_path(self.changedValues[i],self.changedValues[i+1])
            
            if path:
                self.path_step=0
                for point in path:

                    self.image_path[point] = 127
                    self.image_path[point]=255
                    self.path_step+=1
                    if self.path_step==50:
                        self.image_path[point]=0
                        self.path_step=0
                        self.planned_path.append(point)
                        self.whyconpath.append(self.pixel_to_whycon(point))
                        print(self.whyconpath)
                        #print(point)
                else:
                    self.planned_path.append(point)
                    self.whyconpath.append(self.pixel_to_whycon(point))
                    print(self.whyconpath)
                    #print(point)