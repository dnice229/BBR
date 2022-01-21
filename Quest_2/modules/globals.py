# @file globals.py
# @func module which starts the session with Nao robot.
# @auth Hessel van der Molen
# @date 4 May 2012
# @update 2020 by Arnoud Visser

from naoqi import qi
from naoqi import ALProxy
import sys

class globals:
    ipadress = "146.50.60.32"
    port = "9559"
    def setDependencies(self, modules):
        self.session = qi.Session()
        try:
             self.session.connect("tcp://" + self.ipadress + ":" + self.port)
        except RuntimeError:
             print ("Can't connect to Naoqi at ip \"" + self.ipadress + "\" on port " + self.port +".\n")
             sys.exit(1)

    def setProxies(self):
        self.motProxy = self.session.service("ALMotion")
        self.posProxy = self.session.service("ALRobotPosture")
        self.vidProxy = self.session.service("ALVideoDevice")


        self.motProxy = ALProxy("ALMotion", self.ipadress, 9559)
        self.posProxy = ALProxy("ALRobotPosture", self.ipadress, 9559)
        self.vidProxy = ALProxy("ALVideoDevice", self.ipadress, 9559)


        # Subscribe to sonars, this will launch sonars (at hardware level) and start data acquisition.


        #Uncomment to access sonars
        #self.sonarProxy = ALProxy("ALSonar", self.ipadress, 9559)
        #self.memoryProxy = ALProxy("ALMemory", self.ipadress, 9559)
