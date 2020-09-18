"""
Use IP camera application in your mobile device and get the IP address, enter that into the main function. 
GUIDE : 
Start running the program.
* Enter SPACEBAR to capture images. 
* Enter ESC to stop capturing
* Program will now display the images captured one by one.
* Press SPACEBAR to mark the edges of the page for cropping
* Press ESC after marking. Repeat the same for all the images captured.
* Once finished the images captured, their scanned verstions and a PDF file will be visible on the same folder where the code is saved, 
"""

import cv2
import numpy 
import imutils
from PIL import Image


refPt = []
widthImg = 800
heightImg = 1080

#function that stores the coordinates of the points clicked for marking the edges
def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(org,(x,y), 5 , (255,0,0), -1)        
        refPt.append([x,y])
        cv2.imshow('image',org)


#function that adds effects to the cropped image
def addEffects(img):
    dilated_img = cv2.dilate(img, numpy.ones((7, 7), numpy.uint8))
    bg_img = cv2.medianBlur(dilated_img, 15)
    diff_img = 255 - cv2.absdiff(img, bg_img)
    norm_img = diff_img.copy() 
    cv2.normalize(diff_img, norm_img, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
    _, thr_img = cv2.threshold(norm_img, 230, 0, cv2.THRESH_TRUNC)
    cv2.normalize(thr_img, thr_img, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
    
    return thr_img

#function that takes the image and outputs the scanned image
def Scanner(im):
    cv2.imshow('image',im)
    q = cv2.waitKey(0)
    #spacebar
    if(q==32):
        print("mark the edges")
        cv2.setMouseCallback("image", click_event)  
        x = cv2.waitKey(0)
	#escape key
        if(x==27):
            cv2.destroyAllWindows()
            print(refPt)

        imgContour = org.copy() 
        
        contour = [numpy.array(refPt).astype(int)]
        cv2.drawContours(imgContour, contour, -1, (0, 255, 0), 6) 
        
        pts1 = numpy.float32(contour)
        pts2 = numpy.float32([[0, 0],[widthImg, 0], [widthImg, heightImg], [0, heightImg],])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)

        imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg))
        return imgWarpColored

#function that converts all the scanned images to a single pdf file
def convertPDF(scanList):
    imageList = []
    for i in scanList:
        image = Image.open(i)
        im = image.convert('RGB')
        imageList.append(im)

    image.save(r'Scan.pdf',save_all=True, append_images=imageList)
    print('PDF file saved !')

#function that saves the scanned image to the folder
def saveScanned(img,count):
    img_name = "Scanned_Image_{}.png".format(count)
    cv2.imwrite(img_name, img)
    print("{} written!".format(img_name))
    count += 1
    return img_name, count

#function that saves the image from the webcam to the folder
def Capture(frame, img_counter):
    img_name = "opencv_frame_{}.png".format(img_counter)
    cv2.imwrite(img_name, frame)
    print("{} written!".format(img_name))
    img_counter += 1
    return img_name, img_counter


#main function
if __name__ == "__main__":
    #enter ip here
    url = 'http://yourip/video'
    
    cap = cv2.VideoCapture(url)
    ImageList =[]
    scanList =[]
    img_counter = 0
    while(True):
        ret, frame = cap.read()
        
        video = cv2.resize(frame, (480,640))
        cv2.imshow("video mode", video)

        q = cv2.waitKey(1)

        #Press SPACE to capture
        if(q==32):
            image, img_counter = Capture(frame, img_counter)

            ImageList.append(image) 
        
        #Press ESC to Scan the captured images
        if(q==27):
            cv2.destroyAllWindows()
            count=0
            
            for i in ImageList:
                refPt = []
                img = cv2.imread(i)
                img = cv2.resize(img, (widthImg,heightImg))
  
                org = img
                img = Scanner(img)
                img = addEffects(img) 
                scanName, count = saveScanned(img,count)
                scanList.append(scanName)
            convertPDF(scanList)
            break
    
   


