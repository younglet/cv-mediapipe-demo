import cv2
import mediapipe as mp
import numpy as np
import pyautogui

#判断手势是否为食指
def isIndexFinger():
    fingerDict = {}
    for idx in range(21):
        fingerDict[idx] = hand_landmarks.landmark[idx].y
    fingerOrder = sorted(fingerDict,key=fingerDict.__getitem__)
    if fingerOrder[:3] == [8,7,6]:
        return True
    return False

controlFlag = 0
hands  = mp.solutions.hands.Hands(min_detection_confidence=0.7, 
                                    min_tracking_confidence=0.7) 

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
height, width = frame.shape[0], frame.shape[1]

while ret:
    #图片色彩空间转换处理
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    #如果检测到有手的情况，则对手的信息进行分析
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            
            #根据食指指尖的索引值转换坐标
            x = int(hand_landmarks.landmark[8].x * width)
            y = int(hand_landmarks.landmark[8].y * height)
            
            if isIndexFinger():
                #如果不是第一次进入控制鼠标控制，更新当前坐标和之前坐标
                if controlFlag ==1:
                     x_p, y_p = x_n, y_n
                     x_n, y_n = x ,y 
                #如果是第一次进入鼠标控制，那么当前坐标（x_p, y_p）和之前坐标（x_n, y_n）均设为现在的手指位置
                if controlFlag==0:
                    controlFlag = 1 
                    x_p, y_p = x ,y 
                    x_n, y_n = x ,y 

                #根据坐标变化移动鼠标
                pyautogui.moveRel(x_p - x_n , y_n- y_p )
                #在食指指尖绘制红色的圆
                cv2.circle(img, (x, y), 10, (0, 0, 255), -1)
            else:
                controlFlag = 0  
                #在食指指尖绘制绿色的点
                cv2.circle(img, (x, y), 4, (0, 200, 0), -1)
 
    cv2.imshow('demo', cv2.flip(img, 1))

    ret, frame = cap.read()
    if cv2.waitKey(30) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

    