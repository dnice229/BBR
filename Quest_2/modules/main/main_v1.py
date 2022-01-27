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
        self.tools.cSubscribe()
        safe =True
        finished = False
        # if not reached end of maze
        while not finished:
            # check safe to move forward
            if safe:
                # move forward
                self.behaviour.wander()
                # check for landmarks
                blobsFound=0
                while blobsFound != 3 :
                    img, pos = self.tools.getSnapshot()
                    img = self.vision.findsquare(img)
                    blobsFound, blobList, circles = self.vision.getBlobsData(img)
                #navigate based on landmarks
                blobDist = self.vision.calcAvgBlobDistance(blobList)
                center = self.vision.calcMidLandmark(blobList)
                angle = self.vision.calcAngleLandmark(blobList)
                signature  = self.vision.findSignature(blobList)
                turn, walk, finished = self.behaviour.calcDirection(blobsFound, blobDist, angle, signature)
                #if we have reached a border turn according to calc direction
                if not walk:
                    self.behaviour.turn(turn)

            safe = self.behaviour.avoid()



        self.tools.cUnsubscribe()
