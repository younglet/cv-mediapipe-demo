
import Bodies
import pymunk
import cv2
import mediapipe as mp

#程序初始化，创建pymunk的Spcae空间，并为其设置重力，识别摄像头，并调整摄像头的长宽
space = pymunk.Space()
space.gravity = 0, -100
cap = cv2.VideoCapture(0) 
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360) 
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)

#实例3个Ball对象，它们将作为自由落体并能和手部分发生碰撞的小球
balls = [Bodies.Ball(space) for _ in range(3)]
#实例21个代表1只手的物理空间的Finger球，每个小球对应一个手部的识别点
fingers = [Bodies.Finger(space) for _ in range(21)] 
#实例一个手部对象，设置参数
hands  = mp.solutions.hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) 

ret, img = cap.read()
while ret:
    #Hands对象需要对RGB格式的图片处理才能正确工作，这里对图片色彩空间进行转换
    img = cv2.cvtColor(cv2.flip(img, 1), cv2.COLOR_BGR2RGB)
    results = hands.process(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    #如果检测到图像中出现了手，则对每只手进行遍历，通过下标将每个识别点绑定一个Finger球对象，并绘制在屏幕上
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for idx, ball in enumerate(fingers):            
                fingers[idx].update(hand_landmarks, idx, img)   
    #遍历小球更新小球的位置
    for ball in balls:
        ball.update(img)
    #显示画面并更新图像和物理空间数据
    cv2.imshow('demo',img)
    ret, img = cap.read()
    space.step(0.02)
    k = cv2.waitKey(10)
    #如果按下了【B】键，则重新生成3个小球。
    if k == ord('b'):
        balls = [Bodies.Ball(space) for _ in range(3)]