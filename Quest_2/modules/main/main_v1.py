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
        self.tools.cSubscribe()
        # self.globals.posProxy.goToPosture('Stand', 1.0)

        blobsFound = 0

        while blobsFound < 3:
            raw_img, pos = self.tools.getSnapshot()
            self.tools.SaveImage('1_raw_img.jpg', raw_img)
            cut_img = self.vision.findSquare(raw_img)
            self.tools.SaveImage('2_cut_img.jpg', cut_img)
            blobsFound, blobList, circles = self.vision.getBlobsData(cut_img)                      
            self.tools.SaveImage('3_blob_img.jpg', sum(circles))


        blobDist = self.vision.calcAvgBlobDistance(blobList)
        # if blobDist is None:


        # while blobDist > 72:
        #     img, pos = self.tools.getSnapshot()
        #     blobsFound, blobList, circles = self.vision.getBlobsData(img)
        #     self.globals.motProxy.moveTo(0.20,0,0)
        #     blobDist = self.vision.calcAvgBlobDistance(blobList)
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
