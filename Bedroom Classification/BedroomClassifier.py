# -------
#This program iterates through a hotel room database and classifies the images as 'Bedroom' or 'NotBedroom'
# -------

import tensorflow as tf
import pandas as pd
from PIL import Image
import numpy as np
import os

# Assign folder path variable with the path to the image database
folder_path = ''

# Load the Teachable Machine model
model = tf.keras.models.load_model('converted_kerasImproved/keras_model.h5')


class_names = open("converted_kerasImproved/labels.txt", "r").readlines()

# Prepare a list to store the results
results = []

# Function to preprocess the image
def preprocess_image(image_path):
    img = Image.open(image_path)
    img = img.resize((224, 224))  # Resize to the input size expected by the model
    img = np.array(img) / 255.0  # Normalize to [0, 1] range
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    return img
def class_rename(class_idx):
  class_name = "null"
  if class_idx == 0:
    class_name = "Bedroom"
  else:
    class_name = "NotBedroom"
  return class_name


# Loop through each image in the directory
for image_name in os.listdir(folder_path):
    if image_name.endswith(('.png', '.jpg', '.jpeg')):  # Check for valid image files
        image_path = os.path.join(folder_path, image_name)
        try:
            img = preprocess_image(image_path)
            prediction = model.predict(img)
            class_idx = np.argmax(prediction, axis=1)[0]
            index = np.argmax(prediction)
            class_name = class_rename(class_idx)
            confidence_score = prediction[0][index]
            results.append((image_name, class_name, confidence_score))
        except Exception as e:
            print(f"Error processing image {image_name}: {e}")

# Create a DataFrame from the results
df = pd.DataFrame(results, columns=['Image Name', 'Class', "Confidence Score"])
df.to_csv('allHotelsClassified.csv', index=False)