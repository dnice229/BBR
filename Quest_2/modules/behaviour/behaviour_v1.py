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
                # Use ladmark to know the turn to make
                if signature == 'Right':
                    turn = angle + side
                if signature == 'Left':
                    turn = side - angle
                if signature == 'Back':
                    turn = -angle + back
                if signature =='Finish':
                    finished = True
        return turn, walk, finished


    # avoid obstacles
    def avoid(self):
        obstacleClose = True
        objectLocation = self.objectDetection()
        blobsFound = 0
        blobDist =  angle =  signature = None
        # When robot is close to object
        while objectLocation is not None:
            self.globals.motProxy.stopMove()
            self.globals.speechProxy("I am way too close")
            if objectLocation == "front":
                while  blobsFound < 3:
                    # Walk backwards
                    self.globals.motProxy.setWalkTargetVelocity(-0.5,0,0.3)
                    time.sleep(2)
                    self.globals.posProxy.goToPosture('StandInit', 1.0)
                    # Look for landmarks and retrieve visual cues
                    blobsFound, blobDist, angle, signature = self.lookFor()
                    objectLocation = self.objectDetection()
                    # If  walked too far away from  maze wall stop and got back
                    # to wonder
                    if objectLocation == 'tooFar':
                        self.globals.speechProxy("I am too far away, let's keep going")
                        objectlocation = None
                        break
            if objectLocation == "left":
                # one step left
                self.turn(-1, 'left')
                self.globals.posProxy.goToPosture('StandInit', 1.0)
            if objectLocation == "right":
                # one step right
                self.turn(1, 'right')
                self.globals.posProxy.goToPosture('StandInit', 1.0)
            objectLocation = self.objectDetection()
        # Robot is not close to anything
        if objectLocation == None:
            obstacleClose = False

        return obstacleClose, blobsFound, blobDist, angle, signature

    def objectDetection(self):
        left, right = self.sonar.averageSonar()
        tooClose = 0.45
        tooFar = 1.2
        if left < tooClose and right < tooClose:
            objectLocation = "front"
        if left < tooClose and right > tooClose:
            objectLocation = "left"
        if left > tooClose and right < tooClose:
            objectLocation = "right"
        if left > tooFar or  right > tooFar:
            objectLocation = 'tooFar'
        if left > tooClose and right > tooClose:
            objectLocation = None

        print("objectLocation: "+str(objectLocation))
        return objectLocation

    def lookFor(self):
        blobsFound = 0
        pitch = -4.5
        yaw = 0.
        print('f')
        for x in range(0,21):
            img, pos = self.tools.getSnapshot()
            img = self.vision.findsquare(img)
            blobsFound, blobList, circles = self.vision.getBlobsData(img)
            yaw = round(3*np.sin(5*x),2)
            self.motion.setHead(yaw,pitch)
        #navigate based on landmarks
        blobDist = self.vision.calcAvgBlobDistance(blobList)
        center = self.vision.calcMidLandmark(blobList)
        angle = self.vision.calcAngleLandmark(blobList)
        signature  = self.vision.findSignature(blobList)
        print(signature)
        return blobsFound, blobDist, angle, signature




    def wander(self):
        obstacleClose, blobsFound, blobDist, angle, signature = self.avoid()
        print(obstacleClose)
        while not obstacleClose:
            self.globals.speechProxy("Let's go")
            self.globals.motProxy.setWalkTargetVelocity(0.5,0,0,0.3)

            obstacleClose, blobsFound, blobDist, angle, signature = self.avoid()

        self.globals.posProxy.goToPosture('StandInit', 1.0)
        return  blobsFound, blobDist, angle, signature
        # self.globals.motProxy.stopMove()

    def turn(self, turn, signature):
        print(turn)
        self.globals.motProxy.moveTo(0,0, round(turn, 2))
        self.globals.speechProxy.say('turning'+signature)
        self.globals.posProxy.goToPosture('StandInit', 1.0)
    # def remember(self):
    #     self.globals.memoryProxy
