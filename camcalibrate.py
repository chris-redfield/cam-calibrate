# import the opencv library 
import cv2 
  
  
# define a video capture object 
vid = cv2.VideoCapture(0) 
state = 0

while(True): 
      
    # Capture the video frame 
    # by frame 
    ret, frame = vid.read() 
  
    #frame = frame*0.99998

    # Display the resulting frame 
    cv2.imshow('frame', frame) 
      
    # the 'q' button is set as the 
    # quitting button you may use any 
    # desired button of your choice 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        if state==1:
            break
            
        if state==0:
            print(frame)
            state+=1
        

# After the loop release the cap object 
vid.release() 
# Destroy all the windows 
cv2.destroyAllWindows() 