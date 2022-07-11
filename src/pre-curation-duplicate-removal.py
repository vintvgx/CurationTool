import os
import csv
from tqdm.notebook import tqdm
import numpy as np
import os
import shutil
import glob
from PIL import Image

from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.preprocessing.image import img_to_array

dupli_images = "duplicate"
unique_img = "unique"
blah = "/mnt/KiwiFTP/kiwi_transfer/rawImageData/KETR_Number/8606/BabyShark_2022-06-14-18-31-47/2DOD_2022-06-14-18-31-47/long_range/Curated/Good/blah"

model = ResNet50(
    weights='imagenet',
    include_top=False,
    pooling="avg",
    input_shape=(512, 512, 3),
)

def generate_embeddings(input_pil_image):
    resized_image = input_pil_image.resize((512, 512))
    x = img_to_array(resized_image)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    
    embeddings = model.predict(x).flatten().tolist()
    return embeddings

folder_path = input("enter path to directory: ")

images = sorted(glob.glob(f'{folder_path}/*.png'))
dupli_images = os.path.join(folder_path, dupli_images)
unique_img = os.path.join(folder_path, unique_img)
print(dupli_images)
print(unique_img)

if os.path.isdir(unique_img) == False and os.path.isdir(dupli_images) == False:
    os.mkdir(unique_img)
    os.mkdir(dupli_images)
else:
    pass

embeddings = []
unique_images = []
duplicates = []
ctr = 0
total_num_of_images = len(images)
print("processing: ", total_num_of_images)
for image in tqdm(images):
    image_path = os.path.join(folder_path, image)
    im = Image.open(image_path).convert('RGB')
    embedding = generate_embeddings(im)
    print(image)
    ctr = ctr + 1
    if embeddings == []:
        embeddings.append(embedding)
        unique_images.append(image_path)
        shutil.copy(image, unique_img)
    else:
        List1 = np.array(embeddings)
        similarity_scores = List1.dot(embedding)/ (np.linalg.norm(List1, axis=1) * np.linalg.norm(embedding))
        max_similarity_idx = np.argmax(similarity_scores)
        print (ctr, "out of", total_num_of_images, "=", similarity_scores[max_similarity_idx])
        if similarity_scores[max_similarity_idx] > 0.97:
            duplicates.append(image_path)
            shutil.copy(image_path, dupli_images)
        else:
            embeddings.append(embedding)
            unique_images.append(image_path)
            shutil.copy(image_path, unique_img)
        
        
            
print("found ", len(unique_images), " unique images")
print("found ", len(duplicates), " duplicate images")

with open(os.path.join(folder_path, 'unique_images.csv'), 'w+', newline ='') as file:    
    write = csv.writer(file)
    write.writerows(unique_images)

with open(os.path.join(folder_path,'duplicates.csv'), 'w+', newline ='') as file:    
    write = csv.writer(file)
    write.writerows(duplicates)