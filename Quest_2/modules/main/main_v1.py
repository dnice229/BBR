import cv2
import numpy as np
from naoqi import ALProxy
import time
import sys

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
        # self.globals.posProxy.goToPosture('Stand', 1.0)
        blobsFound = 0

        while blobsFound != 3 :
            img, pos = self.tools.getSnapshot()
            img = self.vision.findsquare(img)
            blobsFound, blobList, circles = self.vision.getBlobsData(img)

        blobDist = self.vision.calcAvgBlobDistance(blobList)
        center = self.vision.calcMidLandmark(blobList)
        angle = self.vision.calcAngleLandmark(blobList)
        signature  = self.vision.findSignature(blobList)
        turn, walk = self.behaviour.calcDirection(blobsFound, blobDist, angle, signature)

        self.behaviour.avoid()

        self.tools.cUnsubscribe()
