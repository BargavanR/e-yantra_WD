import cv2
import numpy as np
import imutils
import heapq
borders1=[]
borders2=[]
borders3=[]
borders4=[]
planned_path=[]
image_path = '2.jpg' 
img = cv2.imread(image_path)
height, width, channels = img.shape
cv2.imwrite('heheheh.jpg',img)
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)  
parameters = cv2.aruco.DetectorParameters()



corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(img, aruco_dict, parameters=parameters)


if ids is not None:
   
    

    
    for marker_corners in corners:
        
        points = marker_corners[0]
        
        
        
        borders1.append(points[0].astype(np.float32))

        borders2.append(points[1].astype(np.float32))
        borders3.append(points[2].astype(np.float32))
        borders4.append(points[3].astype(np.float32))
print(borders1[3])
pointss=np.float32([borders1[3],borders2[2],borders3[0]+(57,0),borders4[1]-(57,0)])
'''tl tr br bl'''
'''youtube tl bl tr br'''
'''here tl tr bl br'''
cv2.putText(img,f'tl',(106,107),cv2.FONT_HERSHEY_COMPLEX,3,(255,255,255),3)
cv2.putText(img,f'tr',(897,107),cv2.FONT_HERSHEY_COMPLEX,3,(255,255,255),3)
cv2.putText(img,f'bl',(47+57,899),cv2.FONT_HERSHEY_COMPLEX,3,(255,255,255),3)
cv2.putText(img,f'br',(956-57,897),cv2.FONT_HERSHEY_COMPLEX,3,(255,255,255),3)
cv2.circle(img, (106,107), radius=2,color=(0,0,255),thickness=10)
cv2.circle(img, (897,107), radius=2,color=(0,0,255),thickness=10)
cv2.circle(img, (47+57,899), radius=2,color=(0,0,255),thickness=10)
cv2.circle(img, (956-57,897), radius=2,color=(0,0,255),thickness=10)
cv2.imwrite('image.jpg',img)

print(pointss)
pointssss=np.float32([[0,0],[0,height],[width,0],[width,height]])
print(type(pointss[0]))
matrix=cv2.getPerspectiveTransform(pointss,pointssss)
transformed=cv2.warpPerspective(img,matrix,(width,height))
heheheh=transformed.copy()
image=transformed.copy()
cv2.line(image, (0, 0), (width, 0), (255, 255, 255), thickness=10)
cv2.line(image, (0, 0), (0, height), (255, 255, 255), thickness=10)
cv2.line(image, (width - 1, 0), (width - 1, height), (255, 255, 255), thickness=10)
cv2.line(image, (0, height - 1), (width, height - 1), (255, 255, 255), thickness=10)
transformed=image.copy()
cv2.imshow("lovaaaa",transformed)
height,width,_=transformed.shape
gray = cv2.cvtColor(transformed, cv2.COLOR_BGR2GRAY)


cv2.imshow("lovaaaa",gray)
_, bitmap = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
cv2.imshow('Detected Contour', bitmap)
cv2.imwrite('contour.jpg',bitmap)

contours, _ = cv2.findContours(bitmap, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)
contours = sorted(contours, key=cv2.contourArea, reverse=True,)
print(f"Number of contours found: {len(contours)}")
a=0
numberofobstacles=0
for i, contour in enumerate(contours):
    area = cv2.contourArea(contour)
    if ((area>300 )and (cv2.contourArea(contour)<700000)):
        a=a+area
        numberofobstacles=numberofobstacles+1
        print(f"Contour {i + 1}: Area = {area}")
        image_with_contour = cv2.drawContours(transformed, [contour], -1, (0, 0, 0), 25)
image_with_contour = cv2.cvtColor(image_with_contour, cv2.COLOR_BGR2GRAY)
_, bitmap = cv2.threshold(image_with_contour, 128, 255, cv2.THRESH_BINARY)
cv2.imshow("second tansformed",bitmap)
_, binary_grid = cv2.threshold(image_with_contour, 127, 1, cv2.THRESH_BINARY_INV)
cv2.imwrite('afnvfs.jpg',bitmap)
cv2.imshow('Detected Contour', bitmap)
cv2.waitKey(0)
cv2.destroyAllWindows()