import numpy as np
import math
import time

class behaviour_v1():
    globals = None

    def setDependencies(self, modules):
        self.globals = modules.getModule("globals")
        self.motion = modules.getModule("motion")
        self.sonar = modules.getModule("sonar")
        self.vision = modules.getModule("vision")
        self.tools = modules.getModule("tools")

    #React to found observations
    def calcDirection(self, blobsFound, blobDist, angle, signature):
        '''
        Input: Stuff
        Output: less to no stuff
        '''
        side = 1.57
        back = 3.14
        turn = None
        walk = True
        finished = False
        if blobDist < 0.73:
            walk = False
            if blobsFound > 2:
                if signature == 'Right' or signature == 'Left':
                    turn = angle + side
                if signature == 'Back':
                    turn = -angle + back
                if signature =='Finish':
                    finished = True
        return turn, walk, finished
    # avoid obstacles
    def avoid(self):
        self.sonar.sSubscribe()
        safe = True
        while safe:
            left, right = self.sonar.getSonarData()
            if left < 0.5 or right < 0.5:
                safe = False
        self.sonar.sUnsubscribe()
        return safe

    def lookAround(self):
        self.tools.cSubscribe()
        for yaw in [x * 0.1 for x in range(0, 10)]:
            print("yaw: "+str(yaw))
            self.motion.setHead(yaw,-4.5)
            time.sleep(0.5)
            img, pos = self.tools.getSnapshot()
            self.tools.SaveImage("pitch.jpg",img)
            time.sleep(0.1)

        self.tools.cUnsubscribe()
    
    def wander(self):
        self.globals.motProxy.setWalkTargetVelocity(1,0,0,0.6)
        time.sleep(10)
        self.globals.motProxy.stopMove()
    def turn(self, turn):
        self.globals.posProxy.goToPosture('StandInit')
        self.globals.motProxy.moveTo(0,0, turn)
        self.globals.posProxy.goToPosture('StandInit')
    # def remember(self):
    #     self.globals.memoryProxy
