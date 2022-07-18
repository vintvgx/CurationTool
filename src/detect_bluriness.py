
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
    blurry_images = 0


    # makes the directories to send images to
    os.makedirs(bad_images, exist_ok=True)
    os.makedirs(blur, exist_ok=True)
    os.makedirs(good_images, exist_ok=True)

    # read image, convert to gray scale, compute the variance of Laplacian
    # the lower the number = more burry / set to < 50    
    print("PROCESSING ", len(images) ," IMAGES & DISCARDING BLURRY IMAGES:")
    for img in tqdm(images):
        try:
            image = cv.imread(img)
            gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
            variance_of_laplacian = cv.Laplacian(gray, cv.CV_64F).var()
            if variance_of_laplacian < 25:
                shutil.copy(img, blur)
                blurry_images = blurry_images + 1
            else:
                shutil.copy(img, good_images)
        except:
            pass
    print("found ", blurry_images, "blurry images" )