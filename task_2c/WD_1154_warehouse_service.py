#!/usr/bin/env python3
'''
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose
from waypoint_navigation.srv import GetWaypoints
import heapq
import numpy as np
from std_msgs.msg import Int32MultiArray

# A* Pathfinding class
class AStarPathfinder:
    def __init__(self, grid):
        self.grid = grid
        self.rows, self.cols = grid.shape
        self.directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, down, left, right

    def is_valid(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols and self.grid[row, col] == 0

    def heuristic(self, start, end):
        return abs(start[0] - end[0]) + abs(start[1] - end[1])

    def find_path(self, start, end):
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

    def reconstruct_path(self, came_from, current):
        path = []
        while current in came_from:
            path.append(current)
            current = came_from[current]
        path.append(current)
        return path[::-1]

class WayPoints(Node):
    def __init__(self):
        super().__init__('waypoints_service')
        
        # Service to get waypoints and paths
        self.srv = self.create_service(GetWaypoints, 'waypoints', self.waypoint_callback)
        
        # Subscription to random points topic
        self.create_subscription(Int32MultiArray, '/random_points', self.random_points_callback, 10)
        
        # Initialize variables
        self.grid = np.zeros((100, 100))  # Example grid for pathfinding
        self.pathfinder = AStarPathfinder(self.grid)
        self.waypoints = []  # Waypoints will be populated by random points

    def random_points_callback(self, msg):
        """Convert random points received in image coordinates to waypoints."""
        self.waypoints = []
        for i in range(0, len(msg.data), 2):
            imgx, imgy = msg.data[i], msg.data[i+1]
            whycon_coord = self.pixel_to_whycon(imgx, imgy)
            self.waypoints.append(whycon_coord)
        self.get_logger().info("Random points converted to waypoints")

    def pixel_to_whycon(self, imgx, imgy):
        """Convert image coordinates to WhyCon (real-world) coordinates."""
        goal_x = 0.02537 * imgx - 12.66
        goal_y = 0.02534 * imgy - 12.57
        return [goal_x, goal_y, 27.0]

    ''''''def waypoint_callback(self, request, response):
        """Handle waypoint or path planning requests."""
        
        # Provide waypoints directly
        if request.get_waypoints:
            response.waypoints.poses = [Pose() for _ in range(len(self.waypoints))]
            for i, wp in enumerate(self.waypoints):
                response.waypoints.poses[i].position.x = wp[0]
                response.waypoints.poses[i].position.y = wp[1]
                response.waypoints.poses[i].position.z = wp[2]
            self.get_logger().info("Sending waypoints directly")
            return response

        # Path planning from one waypoint to another
        elif request.get_path_plan:
            response.waypoints.poses = []
            for i in range(len(self.waypoints) - 1):
                start = tuple(map(int, self.waypoints[i][:2]))
                end = tuple(map(int, self.waypoints[i + 1][:2]))
                
                # Find path in pixel coordinates and convert to WhyCon
                pixel_path = self.pathfinder.find_path(start, end)
                
                if pixel_path:
                    for pixel in pixel_path:
                        pose = Pose()
                        whycon_pos = self.pixel_to_whycon(*pixel)
                        pose.position.x, pose.position.y, pose.position.z = whycon_pos
                        response.waypoints.poses.append(pose)
                else:
                    self.get_logger().info("No path found between waypoints")

            self.get_logger().info("Path planning response generated")
            return response
''''''
    def waypoint_callback(self, request, response):
        if request.get_waypoints:
            response.waypoints.poses = [Pose() for _ in range(len(self.waypoints))]
            for i, wp in enumerate(self.waypoints):
                response.waypoints.poses[i].position.x = wp[0]
                response.waypoints.poses[i].position.y = wp[1]
                response.waypoints.poses[i].position.z = wp[2]
            self.get_logger().info("Incoming request for waypoints")

        if request.get_path_plan:  # If path planning is requested
            self.get_logger().info("Path planning requested")
            response.waypoints.poses = []
            for i in range(len(self.waypoints) - 1):
                start = [self.waypoints[i][0], self.waypoints[i][1]]
                end = [self.waypoints[i + 1][0], self.waypoints[i + 1][1]]
                pixel_path = self.pathfinder.find_path(start, end)

                for pixel in pixel_path:
                    pose = Pose()
                    pose.position.x, pose.position.y = self.pixel_to_whycon(pixel[0], pixel[1])[:2]
                    pose.position.z = 27.0  # Assuming altitude remains constant
                    response.waypoints.poses.append(pose)

        return response

def main(args=None):
    rclpy.init(args=args)
    waypoints = WayPoints()
    rclpy.spin(waypoints)
    waypoints.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
'''
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose
from waypoint_navigation.srv import GetWaypoints
import heapq
import numpy as np
from std_msgs.msg import Int32MultiArray

# A* Pathfinding class
class AStarPathfinder:
    def __init__(self, grid):
        self.grid = grid
        self.rows, self.cols = grid.shape
        self.directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, down, left, right

    '''def is_valid(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols and self.grid[row, col] == 0'''
    def is_valid(self, row, col):
        return (
        0 <= int(row) < self.rows and
        0 <= int(col) < self.cols and
        self.grid[int(row), int(col)] == 0
    )


    def heuristic(self, start, end):
        return abs(start[0] - end[0]) + abs(start[1] - end[1])

    '''def find_path(self, start, end):
        open_set = []
        heapq.heappush(open_set, (0, tuple(start)))  # Convert start to tuple
        came_from = {}
        g_score = {tuple(start): 0}  # Ensure start is a tuple

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == tuple(end):  # Compare with tuple of end
                return self.reconstruct_path(came_from, current)

            for d in self.directions:
                neighbor = (current[0] + d[0], current[1] + d[1])

                if self.is_valid(neighbor[0], neighbor[1]):
                    tentative_g_score = g_score[current] + 1

                    if tentative_g_score < g_score.get(neighbor, float('inf')):
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score = tentative_g_score + self.heuristic(neighbor, tuple(end))
                        heapq.heappush(open_set, (f_score, neighbor))

        return None  # Return None if no path is found'''
    def find_path(self, start, end):
        open_set = []
        heapq.heappush(open_set, (0, tuple(map(int, start))))  # Ensure start is tuple of integers
        came_from = {}
        g_score = {tuple(map(int, start)): 0}

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == tuple(map(int, end)):  # Compare with tuple of integers
                return self.reconstruct_path(came_from, current)

            for d in self.directions:
                neighbor = (current[0] + d[0], current[1] + d[1])

                if self.is_valid(neighbor[0], neighbor[1]):
                    tentative_g_score = g_score[current] + 1

                    if tentative_g_score < g_score.get(neighbor, float('inf')):
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score = tentative_g_score + self.heuristic(neighbor, tuple(map(int, end)))
                        heapq.heappush(open_set, (f_score, neighbor))

        return None  # Return None if no path is found


    def reconstruct_path(self, came_from, current):
        path = []
        while current in came_from:
            path.append(current)
            current = came_from[current]
        path.append(current)
        return path[::-1]

class WayPoints(Node):
    def __init__(self):
        super().__init__('waypoints_service')
        
        # Service to get waypoints and paths
        self.srv = self.create_service(GetWaypoints, 'waypoints', self.waypoint_callback)
        
        # Subscription to random points topic
        self.create_subscription(Int32MultiArray, '/package_loc', self.random_points_callback, 10)
        
        # Initialize variables
        self.grid = np.zeros((100, 100))  # Example grid for pathfinding
        self.pathfinder = AStarPathfinder(self.grid)
        self.waypoints = []  # Waypoints will be populated by random points

    '''def random_points_callback(self, msg):
        """Convert random points received in image coordinates to waypoints."""
        self.waypoints = []
        for i in range(0, len(msg.data), 2):
            imgx, imgy = msg.data[i], msg.data[i + 1]
            whycon_coord = self.pixel_to_whycon(imgx, imgy)
            self.waypoints.append(whycon_coord)
        self.get_logger().info("Random points converted to waypoints")'''
    def random_points_callback(self, msg):
        """Convert random points received in image coordinates to waypoints."""
        self.waypoints = []
        for i in range(0, len(msg.data), 2):
            imgx, imgy = msg.data[i], msg.data[i + 1]
            whycon_coord = self.pixel_to_whycon(imgx, imgy)

            # Check path validity from the previous waypoint to the current one (if exists)
            if self.waypoints:  # Ensure there's a previous waypoint to compare
                start = self.waypoints[-1][:2]
                end = whycon_coord[:2]
                pixel_path = self.pathfinder.find_path(start, end)

                if not pixel_path:  # Skip to next random point if no path is found
                    self.get_logger().warning(f"No path found from {start} to {end}. Skipping point ({imgx}, {imgy}).")
                    continue

        # Add the valid point to the waypoints list
        self.waypoints.append(whycon_coord)
        self.get_logger().info("Random points converted to waypoints")


    def pixel_to_whycon(self, imgx, imgy):
        """Convert image coordinates to WhyCon (real-world) coordinates."""
        goal_x = 0.02537 * imgx - 12.66
        goal_y = 0.02534 * imgy - 12.57
        return [goal_x, goal_y, 27.0]

    def waypoint_callback(self, request, response):
        """Handle waypoint or path planning requests."""
        
        if request.get_waypoints:
            response.waypoints.poses = [Pose() for _ in range(len(self.waypoints))]
            for i, wp in enumerate(self.waypoints):
                response.waypoints.poses[i].position.x = wp[0]
                response.waypoints.poses[i].position.y = wp[1]
                response.waypoints.poses[i].position.z = wp[2]
            self.get_logger().info("Sending waypoints directly")

        if request.get_path_plan:  # If path planning is requested
            response.waypoints.poses = []
            for i in range(len(self.waypoints) - 1):
                start = self.waypoints[i][:2]
                end = self.waypoints[i + 1][:2]
                pixel_path = self.pathfinder.find_path(start, end)

                if pixel_path:
                    for pixel in pixel_path:
                        pose = Pose()
                        whycon_pos = self.pixel_to_whycon(*pixel)
                        pose.position.x = whycon_pos[0]
                        pose.position.y = whycon_pos[1]
                        pose.position.z = whycon_pos[2]
                        response.waypoints.poses.append(pose)
                else:
                    self.get_logger().warning(f"No path found between {start} and {end}")

        return response

def main(args=None):
    rclpy.init(args=args)
    waypoints = WayPoints()
    rclpy.spin(waypoints)
    waypoints.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
