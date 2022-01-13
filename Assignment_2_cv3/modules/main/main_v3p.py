import cv2
import numpy as np
from naoqi import ALProxy
import time
import sys

class main_v3:
    def setDependencies(self, modules):
        self.globals = modules.getModule("globals")
        self.motion = modules.getModule("motion")
        self.tools = modules.getModule("tools")
        self.vision = modules.getModule("vision")
        self.sonar = modules.getModule("sonar")

    def start(self):
        self.globals.setProxies()
        self.motion.init()
        self.globals.posProxy.goToPosture("Sit", 0.5)
        self.tools.cSubscribe()
        last_image, (camPos, headAngles) = self.tools.getSnapshot()
#        print last_image.shape[0], last_image.shape[1] 
        self.tools.SaveImage("image1.png",last_image)
        self.tools.SavePilImage("image_1.png",last_image, last_image.shape[1],last_image.shape[0])

        last_image, (camPos, headAngles) = self.tools.getSnapshot()
        self.tools.SaveImage("image2.png",last_image)
		
        last_image, (camPos, headAngles) = self.tools.getSnapshot()
        self.tools.SaveImage("image3.png",last_image)
		
        last_image, (camPos, headAngles) = self.tools.getSnapshot()
        self.tools.SaveImage("image4.png",last_image)
		
        last_image, (camPos, headAngles) = self.tools.getSnapshot()
        self.tools.SaveImage("image5.png",last_image)
		
        last_image, (camPos, headAngles) = self.tools.getSnapshot()
        self.tools.SaveImage("image6.png",last_image)
		
        last_image, (camPos, headAngles) = self.tools.getSnapshot()
        self.tools.SaveImage("image7.png",last_image)
		
        last_image, (camPos, headAngles) = self.tools.getSnapshot()
        self.tools.SaveImage("image8.png",last_image)
		
        last_image, (camPos, headAngles) = self.tools.getSnapshot()
        self.tools.SaveImage("image9.png",last_image)
		
        self.tools.cUnsubscribe()
        self.globals.motProxy.rest()
        
