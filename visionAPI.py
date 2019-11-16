#!/usr/bin/env python
# imports
import os
import io
from google.cloud import vision
from google.cloud import translate_v2 as translate
import pandas as pd

# setting google application credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'serviceAccountToken.json'

# variable declarations
FOLDER_PATH = r'./images'
INPUT_FILE = 'test6.jpg'
OUTPUT_FILE = 'output.txt'

# open output file
f = open(OUTPUT_FILE, "w")

# call vision API to pull text from image
vClient = vision.ImageAnnotatorClient()
with io.open(os.path.join(FOLDER_PATH, INPUT_FILE), 'rb') as image_file:
    content = image_file.read()
image = vision.types.Image(content=content)
response = vClient.text_detection(image=image)
texts = response.text_annotations

# if no text, find objects in image
if not texts:
    objects = vClient.object_localization(
        image=image).localized_object_annotations

    # write objects to a file
    f.write('Number of objects found: {}'.format(len(objects)))
    for object_ in objects:
        f.write('\n{} (confidence: {})'.format(object_.name, object_.score))

# else parse text and translate
else:
    # parse response from vision API
    df = pd.DataFrame(columns=['locale', 'description'])
    for text in texts:
        df = df.append(
            dict(
                locale=text.locale,
                description=text.description
            ),
            ignore_index=True
        )
    output = df['description'][0]

    # call translation API to translate response
    tClient = translate.Client()
    translation = tClient.translate(
        output,
        target_language="en"
    )

    # write translation to a file
    f.write(u'Translation: {}'.format(translation['translatedText']))
f.close()
