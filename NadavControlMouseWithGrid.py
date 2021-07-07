import mediapipe as mp 
import cv2
import win32api
import win32con
import time
import win32gui

duringClick=False

#win32gui.ShowWindow(hwnd,5)
#win32gui.SetForegroundWindow(hwnd)
#win32gui.BringWindowToTop(hwnd)
#win32gui.SetWindowPos(
#        hwnd, win32con.HWND_TOP,
#        -0, -0, 1000, 600,
#        0
#    )

def trackMouse(x,y):
    win32api.SetCursorPos((x,y))
        

def clickMouse(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
  

def focusNadav(hwndself):
    win32gui.ShowWindow(hwndself,5)
    win32gui.SetForegroundWindow(hwndself)
    win32gui.BringWindowToTop(hwndself) 
    win32gui.SetWindowPos(
        hwnd, win32con.HWND_TOP,
        -0, -0, 1000, 600,
        0
    )


time.sleep(2)
#hwnd = win32gui.FindWindow(None, "zoom.txt - notepad") 
hwnd = win32gui.FindWindow(None, "Grid 3 - Nadav - Home") 
focusNadav(hwnd)

print(hwnd) 



mp_drwaing = mp.solutions.drawing_utils #drawing uility - Help to render the landmarks
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480) 

finger5Y=0
finger8Y=0
finger8X=0
finger9X=0
finger9Y=0
finger0X=0
finger0Y=0



with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5, max_num_hands=1) as hands:

    while cap.isOpened():

        re, frame = cap.read()
        #time.sleep(0.1)
        
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
                mp_drwaing.draw_landmarks(image,handLMS, mp_hands.HAND_CONNECTIONS) # draw connection - handLMS is the hand index
                for id , lm in enumerate(handLMS.landmark):
                    h , w , c = image.shape
                    cx , cy = int(lm.x * w) , int (lm.y * h)
                    
                    #print (id, cx , cy)
                    
                    if id == 9 : # this is finger 9 landmark
                        #cv2.circle(image, (cx,cy) , 25 , (200,100,150), -1 )
                        finger9Y = cy
                        finger9X = cx

                    if id == 0 : # this is finger 9 landmark
                        cv2.circle(image, (cx,cy) , 15 , (200,100,150), -1 )
                        finger0Y = cy
                        finger0X = cx
                        trackMouse(cx,cy)

                    if id == 5 : # this is the index finger MCP landmark
                        #cv2.circle(image, (cx,cy) , 15 , (255,0,255), -1 )
                        finger5Y = cy
                        #print (results.multi_handedness[0])

                    if id == 8 : # this is index finger landmark
                        #cv2.circle(image, (cx,cy) , 25 , (255,0,255), -1 )
                        finger8Y = cy
                        finger8X = cx
                        
                        
      
        #if results.multi_hand_landmarks:
        #    for num, hand in enumerate(results.multi_hand_landmarks):
        #        mp_drwaing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS)


        #print('dif":', finger5Y-finger8Y)

        if finger5Y-finger8Y <10 :
            if not(duringClick):
                print('Inside click')
                #focusNadav(hwnd)
                clickMouse(finger0X,finger0Y)
                duringClick=True
            else:
                print('not allowed to')
        else:
            duringClick=False
            print('Turn back flase')



        image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
        cv2.imshow('image',image)
        cv2.moveWindow('image',900,0)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break


cap.release()
cv2.destroyAllWindows()