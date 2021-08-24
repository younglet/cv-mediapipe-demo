import pymunk
import random 
import cv2
import numpy as np

class Ball():   
    def __init__(self, space) -> None:
        """初始化球对象，设置半径、随机颜色、物理身体、物理形状和初始坐标
        参数:
            space (pymunk.Space): pymunk.Space类的实例，新创建的球会自动添加到该空间
        """        
        self.radius = 12
        self.color = [random.randint(123,234) for _ in range(3)]
        self.body = pymunk.Body(100.0,1666, body_type=pymunk.Body.DYNAMIC)
        self.shape = pymunk.Circle(self.body, self.radius)
        self.body.position = random.randint(100,600),  400
        space.add(self.body, self.shape)

    #更新坐标，并将自己绘制到指定的图像中
    def update(self, img):
        """更新位置，并根据传入图像大小换算小球坐标，并在传入的图像上将小球绘制出来
        参数:
            img (nd-array): [小球会被绘制在该图片对象上]
        """            
        xb = int(self.body.position[0])
        yb = int(img.shape[0]-self.body.position[1])
        cv2.circle(img, (xb, yb), self.radius, self.color, -1)

class Finger():
    def __init__(self ,space) -> None:
        """初始化手部识别点的小球对象，设置半径、颜色、物理身体和物理形状。区别于小球，不用设置初始坐标
        参数:
            space (pymunk.Space): pymunk.Space类的实例，新创建的球会自动添加到该空间
        """        
        self.radius = 20
        self.color = [0, 0, 255]
        self.body  = pymunk.Body( 10,1666,body_type=pymunk.Body.KINEMATIC)
        self.shape = pymunk.Circle(self.body, self.radius)
        space.add(self.body, self.shape)

    def update(self,hand_landmarks, idx, img):
        """通过索引idx更新识别点的x,y坐标值，并根据传入图像大小换算小球坐标，并将识别点小球对象绘制在传入的图像上
        参数:
            hand_landmarks (NormalizedLandmarkList): 一只手的所有识别点的坐标信息。注意：'NormalizedLandmarkList' object is not iterable
            for idx, fineger in enumerate(fingers) :
            idx (int): 遍历小球的使用的index值
            img (nd-array): 小球会被绘制在该图片对象上
        """        
        x = int(hand_landmarks.landmark[idx].x * img.shape[1])
        y = int(hand_landmarks.landmark[idx].y * img.shape[0])
        self.body.velocity = 14.0*(x - self.body.position[0]), 14.0*(y - self.body.position[1])
        cv2.circle(img, (x, y), self.radius, self.color, 1)
