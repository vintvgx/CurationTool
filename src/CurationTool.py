# image_browser.py

import glob
import PySimpleGUI as sg
import shutil
import os
import csv

from PIL import Image, ImageTk

sg.theme('DarkGrey13')

good_destination = "Good_images"
bad_destination = "Bad_images"
good_directory = ""
bad_directory = ""

def check_good_bad_dir(path):
    global good_directory
    global bad_directory
    filtered_images = []

    for image in path:
        for img in good_directory or bad_directory:
            if image != img:
                filtered_images.append(image)
            else:
                pass
    return filtered_images

def parse_folder(path):
    global good_directory
    global bad_directory
    images = sorted(glob.glob(f'{path}/*.jpg') + glob.glob(f'{path}/*.png'))
    filtered_images = []
    good_directory = os.path.join(path, good_destination)
    bad_directory = os.path.join(path, bad_destination)

    if os.path.isdir(good_directory) == False and os.path.isdir(good_directory) == False:
        os.mkdir(good_directory)
        os.mkdir(bad_directory)
        sg.popup("Good & Bad Images Directory Made")
        return images
    else:
        for image in path:
            if os.path.exists(good_directory + image) or os.path.exists(bad_directory + image) == True:
                print(good_directory + image)
            else:
                print(good_directory + image)
                filtered_images.append(image)
            return images
    

def load_image(path, window):
    try:
        image = Image.open(path)
        image.thumbnail((900, 900))
        photo_img = ImageTk.PhotoImage(image)
        window["image"].update(data=photo_img)
    except:
        print(f"Unable to open {path}!")
        
def copy_image(img, dest):
    try:
        #take copy of image and put it in destination
        shutil.copy(img, dest)
    except:
        print(f"Unable to copy image!")
                
def save_to_csv(path, values):
    f = open({path}, 'w')
    with open({path} + '/curated.csv', 'w') as f:
        writer = csv.writer(f)
        writer = csv.writer(values)
         

def update_window(window, location, images):
    window['-START-'].update(location)
    window['-END-'].update(len(images))
    window['-TITLE-'].update(images[location])

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

    window = sg.Window("Curation Tool", layout, resizable=True)
    images = []
    location = 0

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        elif event == "file":
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
                copy_image(images[location], good_directory)
                location += 1
                load_image(images[location], window)
            else:
                copy_image(images[location], bad_directory)
                location += 1
                load_image(images[location], window)
            update_window(window, location, images)
            print(location, images[location])
        
            

    window.close()


if __name__ == "__main__":
    main()