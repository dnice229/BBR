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
        

        blobsFound, blobList, circles = self.vision.getBlobsData(img)
        while blobsFound < 3:
            img, pos = self.tools.getSnapshot()
            self.tools.SaveImage('test.image1.jpg', img)
            blobsFound, blobList, circles = self.vision.getBlobsData(img)
            self.tools.SaveImage('imagecircles.jpg', sum(circles))
        distance = self.vision.calcAvgBlobDistance(blobList)

        
        
        
        center = self.vision.calcMidLandmark(blobList)

        print(self.vision.findSignature(blobList))

        self.tools.cUnsubscribe()
