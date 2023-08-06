import cv2 as __cv
from matplotlib import pyplot as __plt
import picklepie as __pp

from . import __haarcascade

# to find cascade : C:\Users\ahadi\AppData\Local\Programs\Python\Python39\Lib\site-packages\cv2\data
# to find base dir of cv2
# import cv2,os
# cv2_base_dir = os.path.dirname(os.path.abspath(cv2.__file__))


# https://towardsdatascience.com/russian-car-plate-detection-with-opencv-and-tesseractocr-dce3d3f9ff5c

def car_plate (a_file='') :
    loc_img = __cv.imread(a_file)
    #convert my image to grayscale
    loc_gray = __cv.cvtColor(loc_img, __cv.COLOR_BGR2GRAY)
    #perform adaptive threshold so that I can extract proper contours from the image
    #need this to extract the name plate from the image. 
    loc_thresh = __cv.adaptiveThreshold(loc_gray,255,__cv.ADAPTIVE_THRESH_GAUSSIAN_C, __cv.THRESH_BINARY,11,2)
    loc_contours,loc_h = __cv.findContours(loc_thresh,1,2)

    #once I have the contours list, i need to find the contours which form rectangles.
    #the contours can be approximated to minimum polygons, polygons of size 4 are probably rectangles
    loc_largest_rectangle = [0,0]
    for loc_cnt in loc_contours:
        loc_approx = __cv.approxPolyDP(loc_cnt,0.01*__cv.arcLength(loc_cnt,True),True)
        if len(loc_approx)==4: #polygons with 4 points is what I need.
            loc_area = __cv.contourArea(loc_cnt)
            if loc_area > loc_largest_rectangle[0]:
                #find the polygon which has the largest size.
                loc_largest_rectangle = [__cv.contourArea(loc_cnt),loc_cnt,loc_approx]

    x,y,w,h = __cv.boundingRect(loc_largest_rectangle[1])
    #crop the rectangle to get the number plate.
    loc_roi = loc_img[y:y+h,x:x+w]
    #cv2.drawContours(img,[largest_rectangle[1]],0,(0,0,255),-1)
    loc_plot = __plt.figure()
    __plt.imshow(loc_roi,cmap = 'gray')
    # __plt.show()
    __plt.close()
    return loc_plot

def show_image (a_file,b_title='My Pickle Image',b_target='inline') :
    loc_img = __cv.imread(a_file)
    if (b_target == '') :
        # __cv.startWindowThread()
        __cv.namedWindow(b_title,__cv.WINDOW_NORMAL)
        # __cv.resizeWindow(b_title, 600,600)
        __cv.imshow(b_title,loc_img)
        __cv.waitKey()
        __cv.destroyAllWindows()
    elif (b_target == 'inline') :
        loc_color = __cv.cvtColor(loc_img,__cv.COLOR_BGR2RGB)
        __plt.imshow(loc_color)
        __plt.title(b_title)
        __plt.show()

# press Escape button to stop
def show_webcam (a_title='My Pickle Camera') :
    loc_video_capture = __cv.VideoCapture(0)
    while(1):
        loc_success, loc_frame = loc_video_capture.read()
        __cv.imshow(a_title,loc_frame)
        loc_quit = __cv.waitKey(5) & 0xFF
        if loc_quit == 27 :
            loc_video_capture.release()
            __cv.destroyAllWindows()
            break
            
# face detection
def face_detection (b_title='My Pickle Camera',b_source='camera',b_file='') :
    if (b_source == 'camera') :
        # Load the cascade
        loc_face_cascade = __cv.CascadeClassifier(__cv.data.haarcascades + 'haarcascade_frontalface_default.xml')
        # Select Input
        if (b_source == 'camera') : 
            loc_video_capture = __cv.VideoCapture(0)
        elif (b_source == 'video') : 
            loc_video_capture = __cv.VideoCapture(b_file)
        while True:
            # Read the frame
            loc_success,loc_frame = loc_video_capture.read()
            # Convert to grayscale
            loc_gray = __cv.cvtColor(loc_frame,__cv.COLOR_BGR2GRAY)
            # Detect the faces
            loc_faces = loc_face_cascade.detectMultiScale(loc_gray,1.1,4)
            # Draw the rectangle around each face
            for (x,y,w,h) in loc_faces:
                __cv.rectangle(loc_frame,(x,y),(x+w,y+h),(255,0,0),2)
            # Display
            __cv.imshow(b_title,loc_frame)
            loc_quit = __cv.waitKey(5) & 0xFF
            if loc_quit == 27 :
                loc_video_capture.release()
                __cv.destroyAllWindows()
                break
    elif (b_source == 'image') :
        # load the cascade
        loc_face_cascade = __cv.CascadeClassifier(__cv.data.haarcascades + 'haarcascade_frontalface_default.xml')
        # read the input image
        loc_img = __cv.imread(b_file)
        # convert into grayscale
        loc_gray = __cv.cvtColor(loc_img,__cv.COLOR_BGR2GRAY)
        __cv.startWindowThread()
        __cv.namedWindow(b_title,__cv.WINDOW_NORMAL)
        # detect the faces
        loc_faces = loc_face_cascade.detectMultiScale(loc_gray,1.1,4)
        # draw the rectangle around each face
        for (x,y,w,h) in loc_faces:
            __cv.rectangle(loc_img,(x,y),(x+w,y+h),(255,0,0),2)
        # __cv.resizeWindow(b_title, 600,600)
        __cv.imshow(b_title,loc_img)
        __cv.waitKey()
        __cv.destroyAllWindows()

# car detection
# https://dev.to/kalebu/how-to-perform-real-time-vehicle-detection-in-python-4i9h
def car_detection (b_title='My Pickle Camera',b_source='camera',b_file='') :
    if (b_source == 'camera' or b_source == 'video') :
        # Load the cascade
        # loc_car_cascade = __cv.CascadeClassifier(__cv.data.haarcascades + 'haarcascade_car.xml') # common
        loc_car_cascade = __cv.CascadeClassifier(__pp.ai.cv.__haarcascade.__dir + 'haarcascade_car.xml') # common
        # Select Input
        if (b_source == 'camera') : 
            loc_video_capture = __cv.VideoCapture(0)
        elif (b_source == 'video') : 
            loc_video_capture = __cv.VideoCapture(b_file)
        while True:
            # Read the frame
            loc_success,loc_frame = loc_video_capture.read()
            # Convert to grayscale
            loc_gray = __cv.cvtColor(loc_frame,__cv.COLOR_BGR2GRAY)
            # Detect the faces
            loc_cars = loc_car_cascade.detectMultiScale(loc_gray,scaleFactor=1.05,minNeighbors=3)
            # Draw the rectangle around each face
            for (x,y,w,h) in loc_cars:
                __cv.rectangle(loc_frame,(x,y),(x+w,y+h),(255,0,0),2)
            # Display
            __cv.imshow(b_title,loc_frame)
            loc_quit = __cv.waitKey(5) & 0xFF
            if loc_quit == 27 :
                loc_video_capture.release()
                __cv.destroyAllWindows()
                break
    elif (b_source == 'image') :
        # load the cascade
        loc_face_cascade = __cv.CascadeClassifier(__cv.data.haarcascades + 'haarcascade_frontalface_default.xml')
        # read the input image
        loc_img = __cv.imread(b_file)
        # convert into grayscale
        loc_gray = __cv.cvtColor(loc_img,__cv.COLOR_BGR2GRAY)
        __cv.startWindowThread()
        __cv.namedWindow(b_title,__cv.WINDOW_NORMAL)
        # detect the faces
        loc_faces = loc_face_cascade.detectMultiScale(loc_gray,1.1,4)
        # draw the rectangle around each face
        for (x,y,w,h) in loc_faces:
            __cv.rectangle(loc_img,(x,y),(x+w,y+h),(255,0,0),2)
        # __cv.resizeWindow(b_title, 600,600)
        __cv.imshow(b_title,loc_img)
        __cv.waitKey()
        __cv.destroyAllWindows()

