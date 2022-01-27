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
        ninety = 1.57
        turn = None
        walk = True
        if blobDist < 0.73:
            walk = False
            if blobsFound > 2:
                if signature == 'Right' or signature == 'Left':
                    turn = angle + ninety
                if signature == 'Finish' or signature == 'Back':
                    turn = -angle

        return turn, walk
    # avoid obstacles
    def avoid(self, left, right):
        self.sonar.sSubscribe()
        safe = True
        while safe:
            left, right = self.sonar.getSonarData()
            if left< 0.5 or right < 0.5:
                safe = False
        
        self.sonar.sUnsubscribe()
        return safe

    def lookAround(self):
        self.tools.cSubscribe()
        for yaw in range(0,10):
            print("yaw: "+str(yaw*0.1))
            self.motion.setHead(yaw*0.1,-4.5)
            time.sleep(0.5)
            img, pos = self.tools.getSnapshot()
            self.tools.SaveImage("pitch.jpg",img)
            time.sleep(0.1)

        self.tools.cUnsubscribe()