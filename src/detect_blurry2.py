
import cv2
import glob
import os
import shutil

blur = '/home/ksaygbe/Pictures/blur'
non_blur = '/home/ksaygbe/Pictures/non-blur'

def variance_of_laplacian(image):
	# compute the Laplacian of the image and then return the focus
	# measure, which is simply the variance of the Laplacian
	return cv2.Laplacian(image, cv2.CV_64F).var()

def main():
    images = sorted(glob.glob('/home/ksaygbe/Pictures/*'))
    os.mkdir(blur)
    os.mkdir(non_blur)

    for img in images:
        if variance_of_laplacian(img) < 10:
            shutil.copy(img, blur)
        else:
            shutil.copy(img, non_blur)

if __name__ == "__main__":
    main()