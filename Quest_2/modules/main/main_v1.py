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
        self.sonar.sSubscribe()
        finished = False

        while not finished:
            self.behavior.wander()
            blobsFound, blobDist, angle, signature = self.behaviour.search()
            turn, finished = self.behaviour.calcDirection(blobsFound, blobDist, angle, signature)
            objectLocation, objectDistance = self.behaviour.objectLocation()
            #if we have reached a border turn according to calc direction
            if objectDistance<0.7:
                self.behaviour.turn(turn, signature)
            time.sleep(3)




        self.globals.speechProxy.say('Yay, I made it')
        fileID = self.globals.songProxy.loadFile("audio/IWon.mp3")
        self.globals.songProxy.play(fileID, _async=True)
        self.globals.posProxy('Sit', 1.0)



        self.sonar.sUnsubscribe()
        self.tools.cUnsubscribe()
        self.sonar.sUnsubscribe()
