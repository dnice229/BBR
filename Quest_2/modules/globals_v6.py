# @file globals.py
# @func module which starts the session with Nao robot. 
# @auth Hessel van der Molen
# @date 4 May 2012
# @update 2022 by Arnoud Visser

from naoqi import qi
import sys

class globals_v6:
    ipadress = "146.50.60.48"
    port = "9559"

    def setDependencies(self, modules):


        # Initialize qi framework.
        connection_url = "tcp://" + self.ipadress + ":" + self.port
        app = qi.Application(["BehaviorBasedRobotics",
                          "--qi-url=" + connection_url])
        try:
             app.start()
        except RuntimeError:
             print ("Can't connect to Naoqi at ip \"" + self.ipadress + "\" on port " + self.port +".\n")
             sys.exit(1)

        self.session = app.session 

    def setProxies(self):
        self.motProxy = self.session.service("ALMotion")
        self.posProxy = self.session.service("ALRobotPosture")
        self.vidProxy = self.session.service("ALVideoDevice")
        self.lifeProxy = self.session.service("ALAutonomousLife")
        self.speechProxy = self.session.service("ALTextToSpeech")
        self.songProxy = self.session.service("ALAudioPlayer")
        self.sonarProxy = self.session.service("ALSonar")
        self.memoryProxy = self.session.service("ALMemory")

	
	
#        self.motProxy = ALProxy("ALMotion", self.ipadress, 9559)
#        self.posProxy = ALProxy("ALRobotPosture", self.ipadress, 9559)
#        self.vidProxy = ALProxy("ALVideoDevice", self.ipadress, 9559)
   

        # Subscribe to sonars, this will launch sonars (at hardware level) and start data acquisition.
        

        #Uncomment to access sonars
        #self.sonarProxy = ALProxy("ALSonar", self.ipadress, 9559)
        #self.memoryProxy = ALProxy("ALMemory", self.ipadress, 9559)
		
		