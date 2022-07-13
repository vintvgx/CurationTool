
import cv2 as cv
import glob
import os
import shutil

blur = 'Bad_images/blur_images'
good_images = 'Good_images'
bad_images = 'Bad_images'


# iterates through images and detects bluriness using Laplacian eqtn &
# puts blurred images in bad image folder / unblurred into images to be curated
def detect_blur(path):
    global blur
    global good_images
    global bad_images
    images = sorted(glob.glob(path + '/*.png'))
    bad_images = os.path.join(path, bad_images)
    print(bad_images)
    blur = os.path.join(path, blur)
    print(blur)
    good_images = os.path.join(path, good_images)
    print(good_images)


    if os.path.isdir(blur) == False and os.path.isdir(good_images) == False:
        os.mkdir(bad_images)
        os.mkdir(blur)
        os.mkdir(good_images)
    else:
        pass

    # read image, convert to gray scale, compute the variance of Laplacian
    # the lower the number = more burry    
    for img in images:
        try:
            image = cv.imread(img)
            gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
            variance_of_laplacian = cv.Laplacian(gray, cv.CV_64F).var()
            print(img, variance_of_laplacian)
            if variance_of_laplacian < 50:
                shutil.copy(img, blur)
            else:
                shutil.copy(img, good_images)
        except:
            pass