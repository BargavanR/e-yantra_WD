#!/usr/bin/env python3
'''
# Team ID:          1154
# Theme:            Warehouse Drone (WD)
# Author List:      R Bargavan,P Sabarishh,Prasanth kanaga Sabai S,Dhasrad Raghav A B.
# Filename:         map.py
# Functions:        identification,text_file
'''
import cv2
import numpy as np
import cv2.aruco as aruco
import argparse

class Arena:

    def __init__(self, image_path):
        self.width = 1000
        self.height = 1000
        self.image_path = image_path
        self.detected_markers = []
        self.obstacles = 0
        self.total_area = 0

    def identification(self):
        # Read the image
        frame = cv2.imread(self.image_path)
        height, width, channels = frame.shape

        # ArUco dictionary and detection parameters
        aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_100)
        parameters = aruco.DetectorParameters()

        # Detect ArUco markers
        corners, ids, rejectedImgPoints = aruco.detectMarkers(frame, aruco_dict, parameters=parameters)

        if ids is not None:
            borders1, borders2, borders3, borders4 = [], [], [], []

            # Store the corners of detected markers
            for marker_corners in corners:
                points = marker_corners[0]
                borders1.append(points[0].astype(np.float32))
                borders2.append(points[1].astype(np.float32))
                borders3.append(points[2].astype(np.float32))
                borders4.append(points[3].astype(np.float32))

            # Perspective transform
            pointss = np.float32([borders1[3], borders4[1], borders2[2], borders3[0]])
            pointssss = np.float32([[0, 0], [0, height], [width, 0], [width, height]])
            matrix = cv2.getPerspectiveTransform(pointss, pointssss)
            transformed_image = cv2.warpPerspective(frame, matrix, (width, height))
            # Convert the image to grayscale
            gray = cv2.cvtColor(transformed_image, cv2.COLOR_BGR2GRAY)

            # Apply Gaussian and bilateral blur
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            blurred = cv2.bilateralFilter(blurred, 16, 51, 75)

            # Canny edge detection
            median_val = np.median(blurred)
            lower = int(max(0, 0.66 * median_val))
            upper = int(min(255, 1.33 * median_val))
            edges = cv2.Canny(blurred, lower, upper)

            # Refine edges using morphological operations
            kernel = np.ones((3, 3), np.uint8)
            edges_refined = cv2.dilate(edges, kernel, iterations=1)
            edges_refined = cv2.erode(edges_refined, kernel, iterations=1)

            # Find contours of obstacles
            contours, _ = cv2.findContours(edges_refined, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)
            contours = sorted(contours, key=cv2.contourArea, reverse=True)
            self.total_area = 0

            # Analyze contours and calculate the total area of obstacles
            for i, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                if area > 300:
                    self.total_area += area
                    self.obstacles += 1
                    transformed_image = cv2.drawContours(transformed_image, [contour], -1, (0, 255, 0), 9)

            self.detected_markers = ids.flatten().tolist()


        else:
            print("No ArUco markers detected.")
        #cv2.imshow("hello",transformed_image)


    def text_file(self):
        with open("obstacles.txt", "w") as file:
            file.write(f"Aruco ID: {self.detected_markers}\n")
            file.write(f"Obstacles: {self.obstacles}\n")
            file.write(f"Total Area: {self.total_area}\n")


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Process image to detect Aruco markers and obstacles.')
    parser.add_argument('--image', required=True, help='Path to the input image.')
    args = parser.parse_args()
    #image_path = 'task1c_image.jpg'
    arena = Arena(args.image)
    arena.identification()
    arena.text_file()
