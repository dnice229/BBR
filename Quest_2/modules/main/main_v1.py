import cv2
import numpy as np
from naoqi import ALProxy
import time
import sys
# red_low = [8, 50, 169]
# red_high= [58, 100, 219]
# green_low = [7, 86, 19]
# green_high= [57, 136,69]
class main_v1:
    def setDependencies(self, modules):
        self.globals = modules.getModule("globals")
        self.motion = modules.getModule("motion")
        self.tools = modules.getModule("tools")
        self.vision = modules.getModule("vision")
        self.sonar = modules.getModule("sonar")

    def start(self):
        self.globals.setProxies()
        self.motion.init()
        self.tools.cSubscribe()
        # self.globals.posProxy.goToPosture('Stand', 1.0)
        img, pos = self.tools.getSnapshot()

        # red = np.array([33,75, 194])
        # blue = np.array([159, 59, 25])
        # green = np.array([32, 111, 44])
        # colors = [blue, green, red]
        # circles = []
        # blobList = []
        # Make detect circles
        # for color in colors:
        #     filteredImage = self.vision.filterImage(img, color-35, color+35)
        #     circles.append(filteredImage)
        # self.tools.SaveImage('blobimage9.jpg', sum(circles))


        self.tools.SaveImage('test.image1.jpg', img)
        blobsFound, blobList, circles = self.vision.getBlobsData(img)
        self.tools.SaveImage('blobimage9.jpg', sum(circles))
        while blobsFound < 3:
            img, pos = self.tools.getSnapshot()
            blobsFound, blobList, circles = self.vision.getBlobsData(img)

        distance = self.vision.calcAvgBlobDistance(blobList)
        center = self.vision.calcMidLandmark(blobList)
        self.tools.SaveImage('blobimage9.jpg', sum(circles))
        angle=self.vision.calcAngleLandmark(center)
        sig = self.vision.findSignature(blobList)
        print(sig)
        # i=0
        # colors=['green', 'blue', 'red']
        # for circle in circles:
        #     print(colors[i])
        #     self.tools.SaveImage('blobimage'+colors[i]+'.jpg', circle)
        #     i+=1
        # print(blobsFound)
        self.tools.cUnsubscribe()
