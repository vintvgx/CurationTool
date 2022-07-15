import time
import sys
import detect_duplicates 

done = 'false'
path = '/home/ksaygbe/Pictures/example1_36'
#here is the animation
def cond_change():
    global done
    done = 'True'

def pre_curation(path):
    global done
    try:
        while(done == 'false'):
            animate().__init_subclass__
            detect_duplicates.detect_bluriness.detect_blur(path)
            detect_duplicates.duplicate_image_removal(path)
            cond_change()
    except:
        print("Pre-Curation failed")

def animate():
    global done
    while done == 'false':
        sys.stdout.write('\rloading |')
        time.sleep(0.1)
        sys.stdout.write('\rloading /')
        time.sleep(0.1)
        sys.stdout.write('\rloading -')
        time.sleep(0.1)
        sys.stdout.write('\rloading \\')
        time.sleep(0.1)
    sys.stdout.write('\rDone!     ')

pre_curation(path)
#long process here
done = 'false'