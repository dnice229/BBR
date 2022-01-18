from naoqi import ALProxy
class globals:
    ipaddress = "146.50.60.32"

    def setDependencies(self, module):
        pass

    def setProxies(self):
        self.speechProxy = ALProxy("ALTextToSpeech", self.ipaddress, 9559)
        self.motProxy = ALProxy("ALMotion", self.ipaddress, 9559)
        self.posProxy = ALProxy("ALRobotPosture", self.ipaddress, 9559)

