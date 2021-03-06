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
        time.sleep(10)
        self.globals.posProxy.goToPosture('Stand', 1.0)
        self.tools.cSubscribe()
        self.sonar.sSubscribe()
        finished = False

        while not finished:

            self.behaviour.wander()
            blobsFound, blobDist, angle, signature = self.behaviour.search()
            turn, finished = self.behaviour.calcDirection(blobsFound, blobDist, angle, signature)
            if turn is not None:
                self.behaviour.turn(turn, signature)



        self.globals.speechProxy.say('Yay, I made it')
        self.globals.posProxy('Sit', 1.0)


        self.sonar.sUnsubscribe()
        self.tools.cUnsubscribe()
