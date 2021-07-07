import mediapipe as mp 
import cv2
import win32api
import win32con

def trackMouse(x,y):
    win32api.SetCursorPos((x,y))
        

def clickMouse(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
    

mp_drwaing = mp.solutions.drawing_utils #drawing uility - Help to render the landmarks
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720) 

finger5Y=0
finger8Y=0
finger8X=0
finger9X=0
finger9Y=0



with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5, max_num_hands=1) as hands:

    while cap.isOpened():

        re, frame = cap.read()
        
        # Start the detecion 
         
        # change it to RGB
        image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        
        # flip the image
        image = cv2.flip(image, 1)
      
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True

        if results.multi_hand_landmarks:

            for handLMS in results.multi_hand_landmarks:
                #mpDraw.draw_landmarks(img,handLMS) # draw dots - handLMS is the hand index
                #mpDraw.draw_landmarks(img,handLMS, mpHands.HAND_CONNECTIONS) # draw connection - handLMS is the hand index
                for id , lm in enumerate(handLMS.landmark):
                    h , w , c = image.shape
                    cx , cy = int(lm.x * w) , int (lm.y * h)
                    
                    #print (id, cx , cy)
                    
                    if id == 9 : # this is finger 9 landmark
                        cv2.circle(image, (cx,cy) , 25 , (200,100,150), -1 )
                        finger9Y = cy
                        finger9X = cx

                    if id == 5 : # this is the index finger MCP landmark
                        cv2.circle(image, (cx,cy) , 15 , (255,0,255), -1 )
                        finger5Y = cy
                        #print (results.multi_handedness[0])

                    if id == 8 : # this is index finger landmark
                        cv2.circle(image, (cx,cy) , 25 , (255,0,255), -1 )
                        finger8Y = cy
                        finger8X = cx
                        
                        trackMouse(cx,cy)
      
        #if results.multi_hand_landmarks:
        #    for num, hand in enumerate(results.multi_hand_landmarks):
        #        mp_drwaing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS)


        #print('dif":', finger5Y-finger8Y)

        if finger5Y-finger8Y <20 :
            print('Inside click')
            clickMouse(finger9X,finger9Y) 

        image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
        cv2.imshow('image',image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break


cap.release()
cv2.destroyAllWindows()