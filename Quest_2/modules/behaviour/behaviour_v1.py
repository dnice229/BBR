import numpy as np
import math
import time
import cv2

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
        sensitivity = 0.5
        if 1-sensitivity < ratio < 1+sensitivity:
            # An object is located in front of the robot
            # print("object front")
            objectLocation = "front"
            objectDistance = (left+right)/2                                  # Sensitivity setting for location calculation
        elif ratio > 1+sensitivity:
            # An object is located on the left side
            objectLocation = "right"
            objectDistance = right
        elif ratio > 1-sensitivity:
            # An object is located on the right side
            objectLocation = "left"
            objectDistance = left
            # left turn
            # Average of both sonar's data for more accuracy
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
            #self.globals.motProxy.stopMove()
            if objectLocation == "front":
                time.sleep(1)
                self.globals.motProxy.setWalkTargetVelocity(-1.0,0,0,0.3)
                # self.globals.speechProxy.say("Obstacle in front of me!")
                time.sleep(3)
                break
            elif objectLocation == "left":
                # self.globals.motProxy.stopMove()
                self.globals.motProxy.setWalkTargetVelocity(-0.5,0,0,0.3)
                time.sleep(4)
                self.turn(0.77, 'right')
            elif objectLocation == "right":
                #self.globals.motProxy.stopMove()
                self.globals.motProxy.setWalkTargetVelocity(-0.5,0,0,0.3)
                time.sleep(4)
                self.turn(-0.77, 'left')
            objectLocation, objectDistance = self.objectDetection()



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
        finished = False
        # print(blobDist)
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
        return turn, finished

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
            # self.tools.SaveImage("image"+str(x)+".jpg", img)
            img = self.vision.imageCorrection(img, 2, -127, 2)
            img = self.vision.maskSquare(img)
            blobsFound, blobList, circles = self.vision.getBlobsData(img)
            if blobsFound > 2:
                break
            yaw = round(0.77*np.sin((np.pi/10)*x),2)
            self.motion.setHead(yaw,-0.3)
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
        return blobDist, angle, signature

    def search(self):
        # print("behaviour: search")


        blobsFound = 0
        objectLocation, objectDistance = self.objectDetection()
        while blobsFound < 3:
            blobsFound, blobList = self.lookFor()
            blobDist, angle, signature = self.getVisualCues(blobList)
            objectLocation = self.objectDetection()
        return blobsFound, blobDist, angle, signature


    def wander(self):
        # print("behaviour: wander")
        """ Iets doen dat de avoid aangeroepen wordt en zorgt dat deze functie stopt?"""

        self.globals.motProxy.setWalkTargetVelocity(0.5,0,-0.045,0.3)
        self.avoid()
        self.globals.motProxy.setWalkTargetVelocity(0.5,0,-0.045,0.3)
        while self.globals.motProxy.moveIsActive():
            self.avoid()
            objectLocation,objectDistance= self.objectDetection()
            if objectDistance < 0.7 and objectLocation == 'front':
                return 1
    def turn(self, turn, signature):
        """
        Input:
            turn: Radian value of the turn the robot should make
            signature: String value that holds the type of turn
        Output: None
        """

        time.sleep(2)
        self.globals.motProxy.moveTo(0,0, round(turn, 2))
        self.globals.speechProxy.say('turning'+signature)
        time.sleep(2)
