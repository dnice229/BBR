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

    def objectDetection(self):
        right, left = self.sonar.averageSonar()
        ratio = left/right
        sensitivity = 0.1
        if ratio > 1+sensitivity:
            # right trun
            print("object left")
            objectLocation = "left"
            objectDistance = left
        elif ratio < 1-sensitivity:
            print("object right")
            objectLocation = "right"
            objectDistance = right
            # left turn
        elif 1-sensitivity < ratio < 1+sensitivity:
            print("object front")
            objectLocation = "front"
            objectDistance = (left+right)/2
            # front
        return objectLocation, objectDistance

    def avoid(self):
        obstacleClose = True
        objectLocation = self.objectDetection()

        # When robot is close to object
        while objectLocation is not None:
            self.globals.speechProxy.say("I am way too close")
            if objectLocation == "front":
                # Walk backwards
                self.globals.motProxy.setWalkTargetVelocity(-1,0,0,0.3)
                # time.sleep(2)
            if objectLocation == "left":
                self.globals.motProxy.stopMove()
                # one step left
                self.globals.motProxy.moveTo(-0.1,0,0)
                self.turn(-0.77, 'right')
                self.globals.posProxy.goToPosture('StandInit', 1.0)
            if objectLocation == "right":
                self.globals.motProxy.stopMove()
                # one step right
                self.globals.motProxy.moveTo(-0.1,0,0)
                self.turn(0.77, 'left')
                self.globals.posProxy.goToPosture('StandInit', 1.0)
            objectLocation = self.objectDetection()
        # Robot is not close to anything
        if objectLocation == None:
            obstacleClose = False
        return obstacleClose

    def turn(self, turn, signature):
        print("behaviour: turn")
        print(turn)
        self.globals.motProxy.moveTo(0,0, round(turn, 2))
        self.globals.speechProxy.say('turning'+signature)
        self.globals.posProxy.goToPosture('StandInit', 1.0)


    #React to found observations
    def calcDirection(self, blobsFound, blobDist, angle, signature):
        '''
        Input: Stuff
        Output: less to no stuff
        '''
        print("behaviour: calcDirection")
        # 90 degrees
        side = 1.57
        # 180 degrees
        back = 3.14
        turn = None
        walk = True
        finished = False
        print(blobDist)
        # Too close to landmark picture
        if blobDist> 60:
            # Stop walking
            walk = False
            if blobsFound > 2:
                # Use landmark to know the turn to make
                if signature == 'Right':
                    turn = side - angle
                if signature == 'Left':
                    turn = -side - angle
        
                if signature == 'Back':
                    turn = -angle + back
                if signature =='Finish':
                    finished = True
        return turn, walk, finished

    # avoid obstacles

    

    def lookFor(self):
        print("lookfor")
        blobsFound = 0
        for x in range(21):
            img, pos = self.tools.getSnapshot()
            img = self.vision.findSquare(img)
            blobsFound, blobList, circles = self.vision.getBlobsData(img)
            if blobsFound > 2:
                break
            yaw = round(1.57*np.sin((np.pi/10)*x),2)
            self.motion.setHead(yaw,-4.5)
        return blobsFound, blobList

    def getVisualCues(self, blobList):
        print("behaviour: getVisualCues")
        #navigate based on landmarks
        blobDist = self.vision.calcAvgBlobDistance(blobList)
        angle = self.vision.calcAngleLandmark(blobList)
        signature  = self.vision.findSignature(blobList)
        print(signature)
        return blobDist, angle, signature

    def search(self):
        print("behaviour: search")


        # blobsFound = 0
        # objectLocation = self.objectDetection()
        # while blobsFound < 3:
        #     blobsFound, blobList = self.lookFor()
        #     blobDist, angle, signature = self.getVisualCues(blobList)
        #     if objectLocation == 'tooFar':
        #         self.globals.speechProxy("I am too far away, let's keep going")
        #         objectlocation = None
        #         break
        #     objectLocation = self.objectDetection()
        return blobsFound, blobDist, angle, signature

    def wander(self):
        print("behaviour: wander")
        obstacleClose = self.avoid()
        

        print(obstacleClose)
        while not obstacleClose:
            obstacleClose = self.avoid()
            # self.globals.speechProxy.say("Let's go")
            self.globals.motProxy.setWalkTargetVelocity(0.5,0,0,0.3)
            blobsFound, blobDist, angle, signature = self.search()
            

        self.globals.posProxy.goToPosture('StandInit', 1.0)
        return  blobsFound, blobDist, angle, signature



