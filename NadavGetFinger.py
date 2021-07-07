import mediapipe as mp 
import cv2

mp_drwaing = mp.solutions.drawing_utils #drawing uility - Help to render the landmarks
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480) 

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
                    mp_drwaing.draw_landmarks(image, handLMS, mp_hands.HAND_CONNECTIONS)
                    h , w , c = image.shape
                    cx , cy = int(lm.x * w) , int (lm.y * h)
                    #print (id, cx , cy)
                    

                    # if id == 4 : # this is the thumb landmark
                    #     cv2.circle(image, (cx,cy) , 15 , (255,0,255), -1 )
                    #     #print (results.multi_handedness[0])

                    if id == 8 : # this is the thumb landmark
                        cv2.circle(image, (cx,cy) , 15 , (255,0,255), -1 )
      
        #if results.multi_hand_landmarks:
        #    for num, hand in enumerate(results.multi_hand_landmarks):
        #        mp_drwaing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS)

        image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
        cv2.imshow('image',image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break


cap.release()
cv2.destroyAllWindows()