#!/usr/bin/env python3

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from waypoint_navigation.action import NavToWaypoint
from waypoint_navigation.srv import GetWaypoints
from geometry_msgs.msg import Pose

class WayPointClient(Node):
    def __init__(self):
        super().__init__('waypoint_client')
        self.goals = []
        self.goal_index = 0
        self.action_client = ActionClient(self, NavToWaypoint, 'waypoint_navigation')
        self.cli = self.create_client(GetWaypoints, 'waypoints')

        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...')

    def send_goal(self, waypoint):
        goal_msg = NavToWaypoint.Goal()
        goal_msg.waypoint.position.x = waypoint[0]
        goal_msg.waypoint.position.y = waypoint[1]
        goal_msg.waypoint.position.z = waypoint[2]

        self.action_client.wait_for_server()
        self.send_goal_future = self.action_client.send_goal_async(goal_msg, feedback_callback=self.feedback_callback)
        self.send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return
        self.get_logger().info('Goal accepted')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info('Result: {0}'.format(result.hov_time))
        self.goal_index += 1

        if self.goal_index < len(self.goals):
            self.send_goal(self.goals[self.goal_index])
        else:
            self.get_logger().info('All waypoints have been reached successfully')

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        x = feedback.current_waypoint.pose.position.x
        y = feedback.current_waypoint.pose.position.y
        z = feedback.current_waypoint.pose.position.z
        self.get_logger().info(f'Feedback - Current position: ({x}, {y}, {z})')

    '''def send_request(self, get_path=False):
        request = GetWaypoints.Request()
        request.get_waypoints = not get_path
        request.get_path_plan = get_path
        future = self.cli.call_async(request)
        return future'''
    def send_request(self, get_path=False):
        request = GetWaypoints.Request()
        request.get_waypoints = not get_path  # True if no path planning is requested
        request.get_path_plan = get_path     # Set this to True for path planning

        self.future = self.cli.call_async(request)
        return self.future


    '''def receive_goals(self, get_path=False):
        future = self.send_request(get_path)
        rclpy.spin_until_future_complete(self, future)
        response = future.result()

        if response:
            self.get_logger().info('Waypoints or Path received by the client')
            for pose in response.waypoints.poses:
                waypoint = [pose.position.x, pose.position.y, pose.position.z]
                self.goals.append(waypoint)
                self.get_logger().info(f'Waypoint: {waypoint}')
            self.send_goal(self.goals[0])
        else:
            self.get_logger().info('Failed to receive waypoints or path')'''
    def receive_goals(self, get_path=False):
        future =self.send_request()
        future = self.send_request(get_path)
        rclpy.spin_until_future_complete(self, future)
        response = future.result()
        self.get_logger().info('Waypoints received by the action client')


        if response and response.waypoints.poses:
            self.get_logger().info('Waypoints or Path received by the client')
            for pose in response.waypoints.poses:
                waypoint = [pose.position.x, pose.position.y, pose.position.z]
                self.goals.append(waypoint)
                self.get_logger().info(f'Waypoint: {waypoint}')
            
            if self.goals:  # Ensure goals are not empty
                self.send_goal(self.goals[0])
            else:
                self.get_logger().warning('No waypoints were added to the goals list')
        else:
            self.get_logger().error('Failed to receive waypoints or path')


def main(args=None):
    rclpy.init(args=args)
    waypoint_client = WayPointClient()
    waypoint_client.receive_goals(get_path=True)
    try:
        rclpy.spin(waypoint_client)
    except KeyboardInterrupt:
        waypoint_client.get_logger().info('KeyboardInterrupt, shutting down.\n')
    finally:
        waypoint_client.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
