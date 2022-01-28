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
        self.globals.posProxy.goToPosture('Stand', 1.0)
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
                self.behaviour.lookAt()
                turn, walk, finished = self.behaviour.calcDirection(blobsFound, blobDist, angle, signature)
                #if we have reached a border turn according to calc direction
                if not walk:
                    self.behaviour.turn(turn)

            safe = self.behaviour.avoid()



        self.tools.cUnsubscribe()
