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
        img, pos = self.tools.getSnapshot()
        name1 = 'test.image1.jpg'
        name2 = 'test.image2.jpg'
        r_img = self.vision.filterImage(img, [102,0,0], [255,153,153])
        self.tools.SaveImage(name2, r_img)

        # self.tools.getSnapshot()
        self.tools.cUnsubscribe()
