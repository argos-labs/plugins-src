# from __future__ import print_function
import io
import os
# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "stt-test-db6074635845.json"

# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
# file_name = os.path.abspath('file-20180212-58335-1ihxyz8.jpg')
file_name = os.path.abspath('ROAD-SIGN-2-ALAMY_2699740b.jpg')

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

# noinspection PyUnresolvedReferences
image = types.Image(content=content)

# Performs label detection on the image file
response = client.label_detection(image=image)
labels = response.label_annotations

print('Labels:')
for label in labels:
    print(label.description)

