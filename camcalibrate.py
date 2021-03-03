import cv2 
import numpy as np

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)  

objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.


# define a video capture object 
vid = cv2.VideoCapture(0) 
state = 0
calibrated = False

while(True): 
      
    # Capture the video frame by frame 
    ret, frame = vid.read() 

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    ret, corners = cv2.findChessboardCorners(gray, (7,6), None)

    if ret == True:
        corners2 = cv2.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        cv2.drawChessboardCorners(frame, (7,6), corners2, True)
        
        objpoints.append(objp)
        imgpoints.append(corners)

    cv2.imshow('frame', frame) 

    if(len(objpoints)>5 and state==1 and calibrated == False):
        print("Calibrando...")
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
        print(f"erro de projeção RMS: {ret}")
        
        print("matriz de intrínsecos (K):")
        print(mtx)

        print("Vetores de Rotação:")
        print(rvecs[:2])

        print("Vetores de translação:")
        print(tvecs[:2])

        print("Parâmetros de distorção: [k1, k2, p1, p2, k3]")
        print(dist)
        calibrated = True

    # 'q' button is set for interaction
    if cv2.waitKey(1) & 0xFF == ord('q'):
        if state==1:
            break

        if state==0:
            print("Tentando calibrar...")
            state+=1
        


# After the loop release the cap object 
vid.release() 
# Destroy all the windows 
cv2.destroyAllWindows() 