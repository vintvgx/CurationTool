
import cv2 as cv
from tqdm import tqdm
import glob
import os
import shutil

blur = 'Bad_images/blur_images'
good_images = 'Good_images'
bad_images = 'Bad_images'


# iterates through images and detects bluriness using Laplacian eqtn &
# puts blurred images in bad image folder / unblurred into images_to_be_curated
def detect_blur(path):
    #set paths for good/bad images
    global blur
    global good_images
    global bad_images
    images = sorted(glob.glob(path + '/*.png'))
    bad_images = os.path.join(path, bad_images)
    blur = os.path.join(path, blur)
    good_images = os.path.join(path, good_images)


    # makes the directories to send images to
    if os.path.isdir(blur) == False and os.path.isdir(good_images) == False:
        os.mkdir(bad_images)
        os.mkdir(blur)
        os.mkdir(good_images)
    else:
        pass

    # read image, convert to gray scale, compute the variance of Laplacian
    # the lower the number = more burry / set to < 50    
    print("PROCESSING ", len(images) ," IMAGES & DISCARDING OVERLY DETECTED BLURRINESS: ")
    for img in tqdm(images):
        try:
            image = cv.imread(img)
            gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
            variance_of_laplacian = cv.Laplacian(gray, cv.CV_64F).var()
            if variance_of_laplacian < 50:
                shutil.copy(img, blur)
            else:
                shutil.copy(img, good_images)
        except:
            pass