# import cv2.cv as cv
import cv2
import numpy, math
import numpy as np

def cv2_wait():
    key = cv2.waitKey(-1) & 0xFF
    if key==27:    # Esc key to stop
        cv2.destroyAllWindows()
        exit()
    return key

class vision_v2():
    globals = None

    def setDependencies(self, modules):
        self.globals = modules.getModule("globals")

    #Filter HSV Image with given values
    def filterImage(self, img, min_bgr, max_bgr):
        '''
        Input: HSV Image, 2 List of min and max HSV values
        Output:np.asarray(cv2.GetMat(img)) Black White Matrix/Image
        '''
        img = img
        min_scal = np.array(min_bgr)
        max_scal = np.array(max_bgr)
        filtered_img = cv2.inRange(img, min_scal,max_scal)
        return filtered_img
    #Find Circle in a filtered image
    def findCircle(self,imgMat):
        '''
        Input: Black Whit Image
        Return: List of center position of found Circle
        '''
        if len(circles[0]) == 0: # circles == None
            return None
        else:
            return np.reshape(circles,(circles.shape[1],circles.shape[2]))

    def in_range_bgr(self,img,bgr_low,bgr_high):
        return cv2.inRange(img, np.array(bgr_low), np.array(bgr_high))


    # Proces image to detect color blobs
    def getBlobsData(self, image):
        '''
        Input: Image
        Return: numberOfBlobsFound , [List [center-pixels] of blobs]
        '''
        return blobsFound, blobList, imagearray

    def drawCircles(self,circle_data):
        if not circle_data is None:
            img = np.zeros((320,400,3), np.uint8)
            for i in circle_data:
                if not i is None:
                    cv2.circle(img,(i[0],i[1]),i[2],(255,255,255),-1)
            # return cv.fromarray(img)
            return img
        else:
            print "NO CIRCLES"


    # Get Average Distance between multiple blobs
    def calcAvgBlobDistance(self, blobList):
        '''
        Input: [Pink, Blue, Orange]
        Output: Avarege Distance in pixels
        '''
        return Distance

    # Find centre of a Landmark
    def calcMidLandmark(self, blobList):
        '''
        Input: [Pink, Blue, Orange]
        Output: center pixel as (x,y)
        '''
        return center

    # Find the angle between a found Landmark and the Nao
    def calcAngleLandmark(self, center):
        '''
        Input: center pixel, (x,y)
        Output: Angle in radians
        '''
        return angle

    # Find the Signature
    def findSignature(self,blobList):
        '''
        Input: [Pink, Blue, Orange]
        Output: Signature
        '''
        return signature
