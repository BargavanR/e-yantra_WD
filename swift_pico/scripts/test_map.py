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

        frame = cv2.imread(self.image_path)
        
        aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_100)
        parameters = aruco.DetectorParameters()

        corners, ids, _ = aruco.detectMarkers(frame, aruco_dict, parameters=parameters)
        self.detected_markers = [] 

        if ids is not None:
            self.detected_markers = ids.flatten().tolist()
            print("Detected Markers:", self.detected_markers)
            for marker_id, corner in zip(self.detected_markers, corners):
                print(f"Detected Aruco marker ID: {marker_id} at corners: {corner[0]}")
# Ensure exactly 4 markers are detected for perspective transform
        if len(corners) == 4:
            src_points = np.array([corner[0] for corner in corners], dtype="float32")
            src_points = self.sort_points(src_points)  # Sort for correct transformation

            dst_points = np.array([
                [0, 0],
                [self.width - 1, 0],
                [self.width - 1, self.height - 1],
                [0, self.height - 1]
            ], dtype="float32")

            M = cv2.getPerspectiveTransform(src_points, dst_points)
            transformed_image = cv2.warpPerspective(frame, M, (self.width, self.height))

            cv2.imshow("Transformed Image", transformed_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            gray = cv2.cvtColor(transformed_image, cv2.COLOR_BGR2GRAY)
            _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV) 

            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            self.obstacles = len(contours)
            self.total_area = sum(cv2.contourArea(contour) for contour in contours)
        else:
            print("Error: Exactly 4 Aruco markers are required for perspective transformation.")
            

    def sort_points(self, points):
        # Sort points for top-left, top-right, bottom-right, bottom-left order
        sorted_points = np.zeros_like(points)
        sum_coords = points.sum(axis=1)
        diff_coords = np.diff(points, axis=1)
        sorted_points[0] = points[np.argmin(sum_coords)]  # Top-left
        sorted_points[2] = points[np.argmax(sum_coords)]  # Bottom-right
        sorted_points[1] = points[np.argmin(diff_coords)]  # Top-right
        sorted_points[3] = points[np.argmax(diff_coords)]  # Bottom-left
        return sorted_points
    def text_file(self):
        with open("obstacles.txt", "w") as file:
            file.write(f"Aruco ID: {self.detected_markers}\n")
            file.write(f"Obstacles: {self.obstacles}\n")
            file.write(f"Area: {self.total_area}\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process image to detect Aruco markers and obstacles.')
    parser.add_argument('--image', required=True, help='Path to the input image.')
    args = parser.parse_args()
    
    arena = Arena(args.image)
    arena.identification()
    arena.text_file()'''



'''import cv2
import numpy as np
import cv2.aruco as aruco

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
        frame = cv2.imread()
        



        ###################################
        # Identify the Aruco ID's in the given image

        

        self.detected_markers = []
        ###################################
        # Apply Perspeactive Transform



        transformed_image = ()
        ###################################
        # Use the transformed image to find obstacles and their area



        self.total_area = 0
        ###################################


    def text_file(self):
        with open("obstacles.txt", "w") as file:
            file.write(f"Aruco ID: {self.detected_markers}\n")
            file.write(f"Obstacles: {self.obstacles}\n")
            file.write(f"Area: {self.total_area}\n")


if __name__ == '__main__':
    image_path = 'task1c_image.jpg'
    arena = Arena(image_path)
    arena.identification()
    arena.text_file()
    '''