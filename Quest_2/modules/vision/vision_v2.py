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
        Output: Black White Matrix/Image
        '''
        ## implement your filtering here.
        img = img

        min_scal = np.array(min_bgr)
        max_scal = np.array(max_bgr)

        resultImg = cv2.inRange(img, min_scal, max_scal)
        resultImg = cv2.blur(resultImg, (3, 3))

        return resultImg


    #Find Circle in a filtered image
    def findCircle(self,imgMat):
        '''
        Input: Black Whit Image
        Return: List of center position of found Circle
        '''
        img = imgMat
        dp   = 2 # search precision
        minD = 120 # Minimal distance between blobs; was 120
        p1 = 255 # 
        p2 = 27
        minS = 8 # minimal size blob px
        maxS = 300 # maximal size blob px
        circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, dp, minD, None, p1,
        p2, minS, maxS)
        if circles is None: # circles == None
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
        red = np.array([33,75, 194])
        blue = np.array([159, 59, 25])
        green = np.array([32, 111, 44])
        colors = [blue, green, red]
        circles = []
        blobList = []
        # Make detect circles
        for color in colors:
            filteredImage = self.filterImage(image, color-25, color+25)
            circleImage = self.findCircle(filteredImage)
            if circleImage is not None:
                blobList.append((circleImage[0][0], circleImage[0][1]))
                circleImg = self.drawCircles(circleImage)
                circles.append(circleImg)

        # retrieve blobs found in list
        blobsFound = len(blobList)
        return blobsFound, blobList, circles

    def drawCircles(self,circle_data):
        if not circle_data is None:
            img = np.zeros((240,300,3), np.uint8)
            for i in circle_data:
                if not i is None:
                    cv2.circle(img,(i[0],i[1]),i[2],(255,255,255),-1)
            # return cv.fromarray(img)
            return img
        else:
            print("NO CIRCLES")


    # Get Average Distance between multiple blobs
    def calcAvgBlobDistance(self, blobList):
        '''
        Input: [Green, Blue, Orange]
        Output: Avarege Distance in pixels
        '''
        if len(blobList) < 2:
            return None
        Distance = 0
        for i in range(len(blobList)):
            for j in range(i+1, len(blobList)):
                Distance +=np.sqrt((blobList[i][0] - blobList[j][0])**2 + (blobList[i][1] - blobList[j][1])**2)
        Distance/=len(blobList) if len(blobList) > 2 else 1
        return Distance

    # Find centre of a Landmark
    def calcMidLandmark(self, blobList):
        '''
        Input: [Blue, green,  Orange]
        Output: center pixel as (x,y)
        '''
        if len(blobList) == 0:
            return None
        x = 0
        y = 0

        for i in range(len(blobList)):                                                                          # IMPORTANT CHANGE: calc center from averages
            x += blobList[i][0]
            y += blobList[i][1]
        x /= len(blobList)
        y /= len(blobList)
        center = (x,y)
        return center

    # Find the angle between a found Landmark and the Nao
    def calcAngleLandmark(self, blobList):
        '''
        Input: blobList
        Output: Angle in radians
        '''
        if len(blobList) == 0:
            return None
        center = self.calcMidLandmark(blobList)
        pixel = 0.00038
        center_pix = (160, 120)
        ctr_shift = (center[0]-center_pix[0]) + (center[1]-center_pix[1])
        angle =  ctr_shift * pixel
        return angle

    # Find the Signature
    def findSignature(self,blobList):
        '''
        Input: [Blue, Green, Orange]
        Output: Signature
        '''
        if blobList is None:
            return -1
        xy_Blue = blobList[0]
        xy_Green = blobList[1]
        xy_Red = blobList[2]
        if xy_Blue[1] > xy_Green[1] and xy_Blue[1] > xy_Red[1]:
            signature = 'Finish'
        if xy_Blue[0] > xy_Green[0] and xy_Blue[0] > xy_Red[0]:
            signature = 'Right'
        if xy_Blue[0] < xy_Green[0] and xy_Blue[0] < xy_Red[0]:
            signature = 'Left'
        if xy_Blue[1] < xy_Green[1] and xy_Blue[1] < xy_Red[1]:
            signature = 'Back'
        return signature
