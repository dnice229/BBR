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
        self.tools.SaveImage('test.image1.jpg', img)
        # # red
        # resultImage = self.vision.filterImage(img, red_low,red_high)
        # circles = self.vision.findCircle(resultImage)
        # circleImage = self.vision.drawCircles(circles)
        # self.tools.SaveImage('redcircle.jpg', circleImage)
        # #green
        # resultImage = self.vision.filterImage(img, green_low,green_high)
        # circles = self.vision.findCircle(resultImage)
        # circleImage = self.vision.drawCircles(circles)
        # self.tools.SaveImage('greencircle.jpg', circleImage)
        blobsFound, blobList, circles = self.vision.getBlobsData(img)
        while blobsFound < 3:
            img, pos = self.tools.getSnapshot()
            blobsFound, blobList, circles = self.vision.getBlobsData(img)
        i=0
        colors=['green', 'blue', 'red']
        for circle in circles:
            print(colors[i])
            self.tools.SaveImage('blobimage'+colors[i]+'.jpg', circle)
            i+=1
        print(blobsFound)
        self.tools.cUnsubscribe()
