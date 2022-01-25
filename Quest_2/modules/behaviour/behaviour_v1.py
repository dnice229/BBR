import numpy as np

class behaviour_v1():
    globals = None

    def setDependencies(self, modules):
        self.globals = modules.getModule("globals")
        self.motion = modules.getModule("motion")
        self.sonar = modules.getModule("sonar")
        self.vision = modules.getModule("vision")

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
