import cv2
from naoqi import ALProxy
import math
import time

class sonar_v2():    
    globals = None
    def setDependencies(self, modules):
        self.globals = modules.getModule("globals")

    #unsubscribe from sonars
    def sUnsubscribe(self):
        """ Try to unsubscribe from the camera """
        try:
            self.globals.sonarProxy.unsubscribe(self.subscription_name)
        except Exception as inst:
            print("Unsubscribing impossible:", inst)

    #subscribe to camera
    def sSubscribe(self):
        '''subscribe to the nsonar feed'''
        self.subscription_name = str(time.time())
        self.globals.sonarProxy.subscribe(self.subscription_name)


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

    def averageSonar(self):
        sum_left = 0
        sum_right = 0
        j = 30
        for i in range(j):
            left, right = self.getSonarData(value=0)
            sum_left += left
            sum_right += right
        mean_left = sum_left / j
        mean_right = sum_right / j
        return mean_left, mean_right
