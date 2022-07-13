# image_browser.py

import glob
import PySimpleGUI as sg
import shutil
import os
import csv
import detect_duplicates 
import numpy as np

from PIL import Image, ImageTk

sg.theme('DarkGrey13')

good_destination = "Good_images"
bad_destination = "Bad_images"
curated_destination = "Good_images/Curated_Images"
good_directory = ""
bad_directory = ""
pre_curate_done = False


#FIX : check good & bad folders and if images are present then do not return them
# to images that need to be curated
# def check_good_bad_dir(path):
#     global good_directory
#     global bad_directory
#     filtered_images = []

#     for image in path:
#         for img in good_directory or bad_directory:
#             if image != img:
#                 filtered_images.append(image)
#             else:
#                 pass
#     return filtered_images
 
def pre_curation(path):
    global pre_curate_done
    try:
        while(pre_curate_done == False):
            sg.PopupAnimated(sg.DEFAULT_BASE64_LOADING_GIF, background_color='white', time_between_frames=100, location=(600,400)) 
            detect_duplicates.detect_bluriness.detect_blur(path)
            detect_duplicates.duplicate_image_removal(path)
            pre_curate_done = True
    except:
        print("Pre-Curation failed")

def parse_folder(path):
    global good_directory
    global bad_directory
    global curated_destination
    # images = sorted(glob.glob(f'{path}/*.jpg') + glob.glob(f'{path}/*.png'))
    # filtered_images = []
    good_directory = os.path.join(path, good_destination)
    bad_directory = os.path.join(path, bad_destination)
    curated_destination = os.path.join(path, curated_destination)
    images_to_be_curated = sorted(glob.glob(f'{good_directory}/*.jpg') + glob.glob(f'{good_directory}/*.png'))

    os.makedirs(curated_destination, exist_ok=True)
    os.makedirs(good_directory, exist_ok=True)
    os.makedirs(bad_directory, exist_ok=True)
    previously_curated_images = sorted(glob.glob(f'{curated_destination}/*.png'))

    # checks the curated folder and returns only the images that have not
    # yet been curated 
    for img in images_to_be_curated[:]:
        for element in previously_curated_images:
            try:
                if img[-10:] == element[-10:]:
                    images_to_be_curated.remove(img)
                else:
                    pass
            except:
                pass

    if images_to_be_curated == 0:
        sg.popup("This Folder Has Already Been Curated!")
    else:
        return images_to_be_curated
    

    # if os.path.isdir(curated_destination) == False :
    #     os.mkdir(curated_destination)
    #     sg.popup("Directories Made In Folder")
    #     return images_to_be_curated
    # else:
    #     return images_to_be_curated

    
    

def load_image(path, window):
    try:
        #loads image into window, opens up pop up if image can not be open
        image = Image.open(path)
        image.thumbnail((900, 900))
        photo_img = ImageTk.PhotoImage(image)
        window["image"].update(data=photo_img)
    except:
        print(f"Unable to open {path}!")
        sg.popup("Unable to open image!")
        
def copy_image(img, dest):
    try:
        #take copy of image and put it in destination
        shutil.copy(img, dest)
    except:
        print(f"Unable to copy image!")
                
def save_to_good_csv(path, values):
    with open(os.path.join(path, 'curated_Good_Images.csv'), 'w+', newline='') as file:
        write = csv.writer(file)
        write.writerows(values)

def save_to_bad_csv(path, values):
    with open(os.path.join(path, 'curated_Bad_Images.csv'), 'w+', newline='') as file:
        write = csv.writer(file)
        write.writerows(values)         

def update_window(window, location, images):
    #updates elements in window
    try:
        window['-START-'].update(location)
        window['-END-'].update(len(images))
        window['-TITLE-'].update(images[location])
    except:
        sg.popup("Folder has been curated!")

def main():
    option = ''
    
    options_selection_column = [

        [sg.Text("Choose option")],
        [    
            sg.Radio('Good', "-OPTION-", key="-GOOD-"),
        ],
        [
            sg.Radio('Bad - Excessive Motion Blur', "-OPTION-", key="-BAD-")
        ],
        [
            sg.Radio('Bad - Unpopulated', "-OPTION-", key="-BAD-")
        ],
        [
            sg.Radio('Bad - Occulation', "-OPTION-", key="-BAD-")
        ],
        [
            sg.Radio('Bad - Duplicate', "-OPTION-", key="-BAD-")
        ],
        [
            sg.Radio('Bad - Other', "-OPTION-", key="-BAD-")
        ],
        [
            sg.Button('Submit')
        ]
    ]

    elements = [
        [sg.Image(key="image")],
        [
            sg.Text("Image Folder"),
            sg.Input(size=(25, 1), enable_events=True, key="file"),
            sg.FolderBrowse(),
        ],
        [
            sg.Button("Prev"),
            sg.Button("Next")
        ],
        [
            sg.Text("0", key="-START-"), sg.Text("out of"),
            sg.Text("0", key="-END-"),
        ],
        [
            sg.Text("", key="-TITLE-" )
        ]
        
    ]

    layout = [
        [
            sg.Column(elements, expand_x=True, expand_y=True),
            sg.VSeparator(),
            sg.Column(options_selection_column, expand_x=True, expand_y=True)
        ]
    ]

    window = sg.Window("Curation Tool", layout, resizable=True, location=(600,400))
    images = []
    location = 0

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        elif event == "file":
            pre_curation(values["file"])
            images = parse_folder(values["file"])
            if images:
                load_image(images[0], window)
            update_window(window, location, images)
        elif event == "Next" and images:
            if location == len(images) - 1:
                location = 0
            else:
                location += 1
            load_image(images[location], window)
            update_window(window, location, images)
        elif event == "Prev" and images:
            if location == 0:
                location = len(images) - 1
            else:
                location -= 1
            load_image(images[location], window)
            update_window(window, location, images)
        # copies current image into bad or good dest folder & increments to next photo
        elif event == "Submit":
            current_image = images[location]
            if values["-GOOD-"] == True:
                copy_image(images[location], curated_destination)
                save_to_good_csv(curated_destination, images[location])
                location += 1
                load_image(images[location], window)
            elif values["-BAD-"] == True:
                copy_image(images[location], bad_directory)
                save_to_bad_csv(bad_destination, images[location])
                location += 1
                load_image(images[location], window)
            else:
                sg.popup("Choose Selection Before Submitting!")
            update_window(window, location, images)
            print(location, images[location])
        
            

    window.close()


if __name__ == "__main__":
    main()