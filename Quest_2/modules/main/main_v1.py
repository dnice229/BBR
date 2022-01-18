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

    def start(self):
        self.globals.setProxies()
        self.motion.init()
        self.tools.cSubscribe()
        self.globals.posProxy.goToPosture('Stand', 1.0)
        img, pos = self.tools.getSnapshot()
        self.tools.SaveImage('test.image1.jpg', img)
        resultImage = self.vision.filterImage(img, [0,0,152],[135,135,255])

        self.tools.SaveImage('filtered_img.jpg', resultImage)

        self.tools.cUnsubscribe()
