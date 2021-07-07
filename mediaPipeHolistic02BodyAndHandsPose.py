import mediapipe as mp 
import cv2

mp_drwaing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

cap = cv2.VideoCapture(0)
cap.set(3,1920)
cap.set(4,1080)

with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:

    while cap.isOpened():

        re, frame = cap.read()
        

        # change it to RGB
        image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results = holistic.process(image)
        #print (results.face_landmarks) # for the face
        #print (results.pose_landmarks) # body pose

        #print(mp_holistic.FACE_CONNECTIONS)
        #print(mp_holistic.POSE_CONNECTIONS)
        #print(mp_holistic.HAND_CONNECTIONS)

        # face_landmarks , pose_landmarks, left_hand_landmarks, right_hand_landmarks

        # recolor image back to BGR
        image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)

        # draw the face landmarks connections
        mp_drwaing.draw_landmarks(image,results.face_landmarks, mp_holistic.FACE_CONNECTIONS)

        # draw the right hand landmarks connections
        mp_drwaing.draw_landmarks(image,results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

        # draw the left hand landmarks connections
        mp_drwaing.draw_landmarks(image,results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

        # draw the body pose landmarks connections
        mp_drwaing.draw_landmarks(image,results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)

        cv2.imshow('image',image)

        #show original frame  
        #cv2.imshow('frame',frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break


cap.release()
cv2.destroyAllWindows()