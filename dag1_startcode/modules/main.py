class main:
    def setDependencies(self, modules):
        self.globals = modules.getModule("globals")


    def start(self):
        self.globals.setProxies()
        self.globals.speechProxy.say("hello there! ")
        self.globals.posProxy.goToPosture('Stand', 1.0)
        # First forward steps
        self.globals.speechProxy.say("walking")
        self.globals.motProxy.moveTo(1, 0, 0)
        self.globals.posProxy.goToPosture('StandInit', 1.0)

        # Square
        for i in range(3):
            self.globals.speechProxy.say("turning now")
            self.globals.motProxy.moveTo(0, 0, 1.57)
            self.globals.posProxy.goToPosture('StandInit', 1.0)
            self.globals.speechProxy.say("walking")
            self.globals.motProxy.moveTo(1, 0, 0)
            self.globals.posProxy.goToPosture('StandInit', 1.0)

        # Circle
        self.globals.motProxy.moveTo(1, 0, 6.24)
        # End sequence
        self.globals.posProxy.goToPosture('SitRelax', 1.0)
        self.globals.speechProxy.say("Hasta la vista baby")

