import cv2
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
        frame = cv2.imread(self.image_path)
        height, width, channels = frame.shape

        ###################################
        # Identify the Aruco IDs in the given image

        # Define ArUco dictionary and detection parameters
        aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_100)
        parameters = aruco.DetectorParameters()
        
        # Detect ArUco markers
        corners, ids, _ = aruco.detectMarkers(frame, aruco_dict, parameters=parameters)
        
        if ids is not None:
            borders1, borders2, borders3, borders4 = [], [], [], []
            self.detected_markers = ids.flatten().tolist()

            # Store the corners of detected markers
            for marker_corners in corners:
                points = marker_corners[0]
                borders1.append(points[0].astype(np.float32))
                borders2.append(points[1].astype(np.float32))
                borders3.append(points[2].astype(np.float32))
                borders4.append(points[3].astype(np.float32))
        else:
            print("No ArUco markers detected.")

        ###################################
        # Apply Perspective Transform

        if ids is not None:
            # Define points for perspective transform with adjustments
            pointss = np.float32([borders1[3], borders2[2], borders3[0] + (50, 0), borders4[1] - (50, 0)])
            pointssss = np.float32([[0, 0], [0, height], [width, 0], [width, height]])
            matrix = cv2.getPerspectiveTransform(pointss, pointssss)
            transformed_image = cv2.warpPerspective(frame, matrix, (width, height))
        else:
            transformed_image = frame

        ###################################
        # Draw boundary lines around the transformed arena
        cv2.line(transformed_image, (0, 0), (width, 0), (255, 255, 255), thickness=10)  # Top border
        cv2.line(transformed_image, (0, 0), (0, height), (255, 255, 255), thickness=10)  # Left border
        cv2.line(transformed_image, (width - 1, 0), (width - 1, height), (255, 255, 255), thickness=10)  # Right border
        cv2.line(transformed_image, (0, height - 1), (width, height - 1), (255, 255, 255), thickness=10)  # Bottom border

        ###################################
        # Use the transformed image to find obstacles and their area

        gray = cv2.cvtColor(transformed_image, cv2.COLOR_BGR2GRAY)
        _, bitmap = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(bitmap, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_L1)
        
        # Sort and calculate obstacle areas
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        self.total_area = 0
        self.obstacles = 0

        for contour in contours:
            area = cv2.contourArea(contour)
            if 300 < area < 700000:
                self.total_area += area
                self.obstacles += 1
                transformed_image = cv2.drawContours(transformed_image, [contour], -1, (0, 0, 0), 20)

        transformed_image = cv2.cvtColor(transformed_image, cv2.COLOR_BGR2GRAY)
        _, bitmap = cv2.threshold(transformed_image, 128, 255, cv2.THRESH_BINARY)


        ###################################
        # Display and save the processed image with contours and borders
        cv2.imshow("Processed Arena", bitmap)
        cv2.imwrite("processed_arena.jpg", bitmap)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def text_file(self):
        with open("obstacles.txt", "w") as file:
            file.write(f"Aruco ID: {self.detected_markers}\n")
            file.write(f"Obstacles: {self.obstacles}\n")
            file.write(f"Area: {self.total_area}\n")


if __name__ == '__main__':
    image_path = 'frame0000.jpg'
    arena = Arena(image_path)
    arena.identification()
    arena.text_file()