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
        """
        Input: None
        Output:
            objectLocation: The location where the closest object is located
            objectDistance: The distance that this object is located at, derived from sonars.
        """
        right, left = self.sonar.averageSonar()             # Get locationdata from robot's sonars
        ratio = left/right                                  # Calculate the ratio of the sonar's distance data
        sensitivity = 0.2                                   # Sensitivity setting for location calculation
        if ratio > 1+sensitivity:
            # An object is located on the left side
            print("object left")
            objectLocation = "left"
            objectDistance = left
        elif ratio < 1-sensitivity:
            # An object is located on the right side
            print("object right")
            objectLocation = "right"
            objectDistance = right
            # left turn
        elif 1-sensitivity < ratio < 1+sensitivity:
            # An object is located in front of the robot
            print("object front")
            objectLocation = "front"
            objectDistance = (left+right)/2                 # Average of both sonar's data for more accuracy
        return objectLocation, objectDistance

    def avoid(self):
        """
        Input: None
        Output: None
        """
        tooClose = 0.35# Value of when the robot is too close to an obstacle
        objectLocation, objectDistance = self.objectDetection()
        # When robot is close to object
        while objectDistance < tooClose:
            self.globals.speechProxy.say("I am way too close")
            if objectLocation == "front":
                self.globals.motProxy.moveTo(-0.1)
                self.globals.motProxy.stopMove()
            if objectLocation == "left":
                self.globals.motProxy.stopMove()
                self.globals.motProxy.moveTo(-0.1,0,0)
                self.turn(-0.77, 'right')
            if objectLocation == "right":
                self.globals.motProxy.stopMove()
                self.globals.motProxy.moveTo(-0.1,0,0)
                self.turn(0.77, 'left')
            objectLocation, objectDistance = self.objectDetection()

    def turn(self, turn, signature):
        """
        Input:
            turn: Radian value of the turn the robot should make
            signature: String value that holds the type of turn
        Output: None
        """
        print(turn)
        self.globals.motProxy.moveTo(0,0, round(turn, 2))
        self.globals.speechProxy.say('turning'+signature)
        self.globals.posProxy.goToPosture('StandInit', 1.0)

    #React to found observations
    def calcDirection(self, blobsFound, blobDist, angle, signature):
        '''
        Input:
            blobsFound: The amount of blobs that were found in an image
            blobDist:   The average distance between blobs
            angle:      The angle in radians that the center of the blobs is offset to the robot's head position
            signature:  The signature of the found clue
        Output:
            turn:       The amount the robot should turn
            walk:       Whether or not the robot should walk
            finished:   Whether or not the robot is finsihed
        '''
        side = 1.57     # 90 degrees in radians
        back = 3.14     # 180 degrees in radians
        turn = None
        walk = True
        finished = False
        # print(blobDist)
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

    def lookFor(self):
        """
        Input: None
        Output:
            blobsFound:
            blobList:
        """
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
        """
        Input:
            blobList:
        Output:
            blobDist:
            angle:
            signature:
        """
        #navigate based on landmarks
        blobDist = self.vision.calcAvgBlobDistance(blobList)
        angle = self.vision.calcAngleLandmark(blobList)
        signature  = self.vision.findSignature(blobList)
        print(signature)
        return blobDist, angle, signature

    def search(self):
        # print("behaviour: search")


        blobsFound = 0
        objectLocation = self.objectDetection()
        while blobsFound < 3:
            blobsFound, blobList = self.lookFor()
            blobDist, angle, signature = self.getVisualCues(blobList)
            if objectLocation == 'tooFar':
                self.globals.speechProxy("I am too far away, let's keep going")
                objectlocation = None
                break
            objectLocation = self.objectDetection()
        return blobsFound, blobDist, angle, signature

    def wander(self):
        # print("behaviour: wander")
        """ Iets doen dat de avoid aangeroepen wordt en zorgt dat deze functie stopt?"""

        self.globals.motProxy.setWalkTargetVelocity(0.5,0,0.3,0.3)
        while self.globals.motProxy.moveIsActive():
            self.avoid()


        # self.avoid()


        # print(obstacleClose)
        # while not obstacleClose:
        #     obstacleClose = self.avoid()
        #     # self.globals.speechProxy.say("Let's go")
        #     self.globals.motProxy.setWalkTargetVelocity(0.5,0,0,0.3)
        #     blobsFound, blobDist, angle, signature = self.search()


        # self.globals.posProxy.goToPosture('StandInit', 1.0)
        # return  blobsFound, blobDist, angle, signature
i
    def detectFreeRange(self):
        right, left = self.sonar.averageSonar()             # Get locationdata from robot's sonars
        sensitivity = 0.2                                   # Sensitivity setting for location calculation
        if left > 1+sensitivity:
            # An object is located on the left side
            freeLocation = "left"
            freeDistance = left
        elif right > 1+sensitivity:
            # An object is located on the right side
            freeLocation = "right"
            freeDistance = right
            # left turn
        elif left > 1+sensitivity and right > 1=sensitivity:
            # An object is located in front of the robot
            freeLocation = "right"
            freeDistance = (left+right)/2              # Average of both sonar's data for more accuracy
        return freeLocation, freeDistance
    def walkFree(freeLocation, freeDistance):
        if objectLocation == "front":
            self.turn(0, 'front')
            self.globals.motProxy.stopMove()
        if objectLocation == "left":
            self.turn(-0.77, 'right')
            self.globals.motProxy.stopMove()
        if objectLocation == "right":
            self.turn(0.77, 'left')
            self.globals.motProxy.stopMove()




        # self.avoid()


        # print(obstacleClose)
        # while not obstacleClose:
        #     obstacleClose = self.avoid()
        #     # self.globals.speechProxy.say("Let's go")
        #     self.globals.motProxy.setWalkTargetVelocity(0.5,0,0,0.3)
        #     blobsFound, blobDist, angle, signature = self.search()


        # self.globals.posProxy.goToPosture('StandInit', 1.0)
        # return  blobsFound, blobDist, angle, signature
