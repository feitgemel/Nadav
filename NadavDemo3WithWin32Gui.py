import mediapipe as mp 
import cv2
import time
from pywinauto.application import Application
from pywinauto import Desktop

import sys
import win32gui
import win32con


from activateKeyboard import Akey
from activateKeyboard import PressKey, ReleaseKey  


mp_drwaing = mp.solutions.drawing_utils #drawing uility - Help to render the landmarks
mp_hands = mp.solutions.hands

tipIds=[4,8,12,16,20] # the tip of the five fingers

waitTimePressKey=0.3
startTime=0

cap = cv2.VideoCapture(0)
#cap.set(3,1920)
#cap.set(4,1080)
IsADetected = False


#app = Application(backend='win32').connect(title = 'Grid 3 - Nadav - Home',timeout=5)
#app.top_window().set_focus()

time.sleep(2)
hwnd = win32gui.FindWindow(None, "Grid 3 - Nadav - Home") 
#hwnd = win32gui.FindWindow(None, "zoom.txt - notepad") 
win32gui.ShowWindow(hwnd,5)
win32gui.SetForegroundWindow(hwnd)
win32gui.BringWindowToTop(hwnd)
win32gui.SetWindowPos(
        hwnd, win32con.HWND_TOP,
        -0, -0, 1200, 800,
        0
    )


with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5,max_num_hands=1) as hands:

    while cap.isOpened():
        
        re, frame = cap.read()

        # Start the detecion  i 
         
        # change it to RGB
        image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        
        # flip the image
        image = cv2.flip(image, 1)
        lmList=[]
      
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True

        if results.multi_hand_landmarks:
           
            for handLMS in results.multi_hand_landmarks:
                #mpDraw.draw_landmarks(img,handLMS) # draw dots - handLMS is the hand index
               # mp_drwaing.draw_landmarks(image,handLMS, mp_hands.HAND_CONNECTIONS) # draw connection - handLMS is the hand index
                for id , lm in enumerate(handLMS.landmark):
                    h , w , c = image.shape
                    cx , cy = int(lm.x * w) , int (lm.y * h)
                    lmList.append([id,cx,cy])

                                        

                    if id == 8 : # this is the indexFingerTip landmark
                        #cv2.circle(image, (cx,cy) , 15 , (255,0,255), -1 )
                        indexFingerTipX = cx
                        indexFingerTipY = cy
                        
                    if id == 5 : # this is the indexFingerMcp landmark
                        #cv2.circle(image, (cx,cy) , 15 , (255,0,255), -1 )
                        indexFingerMcpX = cx
                        indexFingerMcpY = cy

                    if id == 9 : # this is the middleFingerMcp landmark 
                        #cv2.circle(image, (cx,cy) , 15 , (255,0,255), -1 )
                        middleFingerMcpX = cx
                        middleFingerMcpY = cy
                    
                    if id == 12 : # this is the middleFingerTip landmark
                        #cv2.circle(image, (cx,cy) , 15 , (255,0,255), -1 )
                        middleFingerTipX = cx
                        middleFingerTipY = cy

            # check the fingers
            fingers=[]

            if len(lmList) !=0 : # check it is not empty
                for id in range(1,5): #check 4 fingers in the hand - not the thumb
                    if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]: # check the Y postion [2] for each finger 
                        #print('figner no. ',id,' is Opened')
                        fingers.append(1)  
                    else:
                        #print('figner no. ',id, ' is Closed')
                        fingers.append(0) 

                total = fingers.count(1) # print how many fingers are open (count the 1 valuesq)
                print('Open fingers:', total)

                if total==0 :
                    print('Close')

                    cv2.rectangle(image, (20, 100), (450, 225), (0, 255, 0), cv2.FILLED)
                    cv2.putText(image, "hand close", (45, 175), cv2.FONT_HERSHEY_SIMPLEX,
                        2, (255, 0, 255), 4)
                   

                elif total==4 :
                    print('Open')

                    cv2.rectangle(image, (20, 100), (450, 225), (0, 255, 0), cv2.FILLED)
                    cv2.putText(image, "Hand open", (45, 175), cv2.FONT_HERSHEY_SIMPLEX,
                        2, (255, 0, 255), 4)

                    if not(IsADetected):
                        IsADetected = True
                        PressKey(Akey) # press the A key
                        time.sleep(waitTimePressKey) 
                        ReleaseKey(Akey) # press the A key
                        startTime = time.time()

                    if time.time() - startTime > 2:
                        #print('Turn flag to False')
                        IsADetected=False


        image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
        cv2.imshow('image',image)

       
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break


cap.release()
cv2.destroyAllWindows()