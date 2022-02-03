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
        time.sleep(5)
        self.globals.posProxy.goToPosture('Stand', 1.0)
        self.tools.cSubscribe()
        self.sonar.sSubscribe()
        finished = False

        while not finished:



            self.behaviour.wander()
            blobsFound, blobDist, angle, signature = self.behaviour.search()
            print("signature: "+str(signature))
            turn, finished = self.behaviour.calcDirection(blobsFound, blobDist, angle, signature)
            if turn is not None:
                self.globals.speechProxy.say('turning'+signature)
                self.behaviour.turn(turn, signature)



        self.globals.speechProxy.say('Yay, I made it')
        self.globals.posProxy('Sit', 1.0)
        # img = cv2.imread('image7.jpg')
        # img = self.vision.imageCorrection(img, 2, -127, 2)
        # img = self.vision.findSquare(img)
        # print(self.vision.findSignature(self.vision.getBlobsData(img)[1]))


        self.sonar.sUnsubscribe()
        self.tools.cUnsubscribe()
