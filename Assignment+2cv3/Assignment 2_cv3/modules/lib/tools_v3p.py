import cv2
from naoqi import ALProxy
import math
import Image
import vision_definitions

import numpy as np
def cv2_wait():
    key = cv2.waitKey(-1) & 0xFF
    if key==27:    # Esc key to stop
        cv2.destroyAllWindows()
        exit()
    return key

class tools_v3():
    globals = None

    def setDependencies(self, modules):
        self.globals = modules.getModule("globals")

    #unsubscribe from camera
    def cUnsubscribe(self):
        """ Try to unsubscribe from the camera """
        try:
            self.globals.vidProxy.unsubscribe(self.video_client)
            print "Unsubscribing from video service-----------------------------------"
        except Exception as inst:
            print "Unsubscribing impossible:", inst

    #subscribe to camera
    def cSubscribe(self, resolution=1):
        """ Subscribe to the camera feed. """
        print "Subscribing to video service-----------------------------------"

        self.globals.vidProxy.setParam(18,1)
        # subscribe(gvmName, resolution={0,1,2}, colorSpace={0,9,10,rgb=11,hsy=12,bgr=13}, fps={5,10,15,30}
        #self.globals.vidProxy.subscribe("python_GVM", resolution, 13, 30)
        resolution =1
        #colorSpace = vision_definitions.kYUVColorSpace
        colorSpace = 13
        fps = 30
        self.video_client = self.globals.vidProxy.subscribe("python_r", resolution, colorSpace, fps)

    # get snapshot from camera
    def getSnapshot(self):
        """ snapShot() -> iplImg, (cameraPos6D, headAngles)

        Take a snapshot from the current subscribed video feed.

        """
        # Get camPos
        # getPosition(name, space={0,1,2}, useSensorValues)
        camPos = self.globals.motProxy.getPosition("CameraBottom", 2, True)
        headAngles = self.globals.motProxy.getAngles(["HeadPitch", "HeadYaw"], True)

        # Get image
        # shot[0]=width, shot[1]=height, shot[6]=image-data
        shot = self.globals.vidProxy.getImageRemote(self.video_client)
        assert shot is not None, "You need to do: \n\ (1) ssh nao@ipaddress  (password nao). \n\
                                                      (2) nao restart                      \n\
                                                      Wait for restarting, and run again."
# Get the image size and pixel array.
        w, h = shot[0], shot[1]
        array = shot[6]
        image_string = str(bytearray(array))
#        self.cUnsubscribe()
#        w, h = shot[0], shot[1]
#        data_bytes = shot[6]
        data_npyarr = np.fromstring(image_string, np.uint8)
        frame = data_npyarr.reshape((h,w,3))
	# You can find lower bound and upper bound of filtering with HSV ColorSpace by Googling
	# Uncomment below to use it
	# image_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 #       image_hsv = frame

 #       self.cUnsubscribe()
        return (frame, (camPos, headAngles))

    # conversion is an int: cv2.cv.CV_<scrColorSpace>2<dstColorSpace>
    def convertColourSpace(self, srcImage, conversion):
        dstImage = cv2.cvtColor(srcImage, conversion) # cv2.COLOR_RGB2RGBA)
        return dstImage

    def SaveImage(self, name, img):
        print "Saving image", name
        cv2.imwrite(name, img)
		
    def SavePilImage(self, name, image_string, imageWidth, imageHeight):
        print "Saving PIL image", name
        
		# Create a PIL Image from our pixel array.
        im = Image.fromstring("RGB", (imageWidth, imageHeight), image_string)

        # Save the image.
        im.save(name, "PNG")

    def minimizedAngle( angle ):
        """ maps an angle to the interval [pi, pi] """
        if angle > math.pi:
            angle -= 2*math.pi
        if angle <= -math.pi:
            angle += 2*math.pi
        return angle
