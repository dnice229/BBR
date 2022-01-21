# @file main.py
# @func module which starts the task to be done by the Nao robot. 
# @auth Hessel van der Molen
# @date 4 May 2012
# @update 2020 by Arnoud Visser

import cv2
#import numpy as np
#from naoqi import ALProxy
#import time
#import sys

			
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
        
        self.tools.SaveImage("image1.png",last_image)
        # You can find lower bound and upper bound of filtering with HSV ColorSpace by Googling
	  # Uncomment below to use it
        image_hsv = self.tools.convertColourSpace(last_image, cv2.COLOR_BGR2HSV)
        self.tools.SaveImage("hsv_image1.png",image_hsv)
		
           
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
        
        
        
