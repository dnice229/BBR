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
        # self.behaviour = modules.getModule("behaviour")

    def start(self):
        self.globals.setProxies()
        self.motion.init()
        self.tools.cSubscribe()
        # self.globals.posProxy.goToPosture('Stand', 1.0)
        img, pos = self.tools.getSnapshot()
        self.tools.SaveImage('testimage2.jpg', img)
        img = self.vision.findsquare(img)
        self.tools.SaveImage('testimage3.jpg', img)




        blobsFound, blobList, circles = self.vision.getBlobsData(img)
        self.tools.SaveImage('blobimage9.jpg', sum(circles))

        while blobsFound < 3:
            img, pos = self.tools.getSnapshot()
            blobsFound, blobList, circles = self.vision.getBlobsData(img)
            print(blobsFound)

        blobDist = self.vision.calcAvgBlobDistance(blobList)
        # if blobDist is None:


        # while blobDist > 72:
        #     img, pos = self.tools.getSnapshot()
        #     blobsFound, blobList, circles = self.vision.getBlobsData(img)
        #     self.globals.motProxy.moveTo(0.20,0,0)
        #     blobDist = self.vision.calcAvgBlobDistance(blobList)
        print(blobDist)
        center = self.vision.calcMidLandmark(blobList)
        angle = self.vision.calcAngleLandmark(blobList)
        signature  = self.vision.findSignature(blobList)
        # self.behaviour.calcDirection(blobsFound, blobDist, angle, signature)
        # self.tools.SaveImage('blobimage9.jpg', sum(circles))
        # i=0
        # colors=['green', 'blue', 'red']
        # for circle in circles:
        #     print(colors[i])
        #     self.tools.SaveImage('blobimage'+colors[i]+'.jpg', circle)
        #     i+=1
        # print(blobsFound)
        self.tools.cUnsubscribe()
