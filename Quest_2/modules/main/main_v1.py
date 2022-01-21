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
        self.behaviour = modules.getModule("behaviour")

    def start(self):
        self.globals.setProxies()
        self.motion.init()
        self.tools.cSubscribe()

        self.globals.posProxy.goToPosture('Stand', 1.0)
        
        img, pos = self.tools.getSnapshot()

        self.tools.SaveImage('testimage2.jpg', img)



        blobsFound, blobList, circles = self.vision.getBlobsData(img)
        self.tools.SaveImage('blobimage9.jpg', sum(circles))

        while blobsFound < 3:
            img, pos = self.tools.getSnapshot()
            blobsFound, blobList, circles = self.vision.getBlobsData(img)
            self.tools.SaveImage('testimage2.jpg', img)
            self.tools.SaveImage('blobimage9.jpg', sum(circles))

        blobDist = self.vision.calcAvgBlobDistance(blobList)

        center = self.vision.calcMidLandmark(blobList)

        

        angle = self.vision.calcAngleLandmark(blobList)

        signature = self.vision.findSignature(blobList)

        # i=0
        # colors=['green', 'blue', 'red']
        # for circle in circles:
        #     print(colors[i])
        #     self.tools.SaveImage('blobimage'+colors[i]+'.jpg', circle)
        #     i+=1
        # print(blobsFound)


        #self.behaviour.calcDirection(blobsFound, blobDist, angle, signature)


        self.tools.SaveImage('blobimage9.jpg', sum(circles))
        self.globals.posProxy.goToPosture('SitRelax', 1.0)
        self.tools.cUnsubscribe()
