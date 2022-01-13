import cv2
from naoqi import ALProxy
import math

class sonar_v1():    
    globals = None
    def setDependencies(self, modules):
        self.globals = modules.getModule("globals")

    #unsubscribe from sonars
    def sUnsubscribe(self):
        """ Try to unsubscribe from the camera """ 
        try:
            self.globals.sonarProxy.unsubscribe(self.sonar_sub)
            print "gotHERE----------------------------------------"
        except Exception as inst:
            print "Unsubscribing impossible:", inst

    #subscribe to camera        
    def sSubscribe(self):
        '''subscribe to the nsonar feed'''
        self.sonar_sub = self.globals.sonarProxy.subscribe("myApplication")
       
    # get snapshot from camera
    def getSonarData(self,value = 0):
        """
        GEt data from sonar echos
        """
        if value==0:
            left = self.globals.memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
            # Same thing for right.
            right = self.globals.memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")
        else:
            left = self.globals.memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value"+str(value))
            # Same thing for right.
            right = self.globals.memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value2"+str(value))
        # Get camPos
        # getPosition(name, space={0,1,2}, useSensorValues)
        return left,right
        