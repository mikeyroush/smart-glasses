import RPi.GPIO as GPIO
import time
from picamera import PiCamera
import os
import io
from google.cloud import vision
from google.cloud import translate_v2 as translate
from gtts import gTTS
import pandas as pd
import json
import requests

# loading credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'serviceAccountToken.json'
with open('telegramToken.json') as f:
    data = json.load(f)

# variable declarations
FOLDER_PATH = '/tmp'
INPUT_FILE = 'picture.jpg'
TELEGRAM_TOKEN = data['token']
TELEGRAM_CHAT = data['chat']
OUTPUT = ""
OUTPUT_FILE = 'output.txt'

#establish camera and GPIO for button
GPIO.setmode(GPIO.BCM)
camera = PiCamera()

GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_UP)

vClient = vision.ImageAnnotatorClient()
try:
    while True:
        input_state = GPIO.input(14)
        if input_state == False:
            # Take the picture
            print('Button Pressed')
            camera.start_preview()
            time.sleep(1)
            camera.capture('/tmp/picture.jpg')
            camera.stop_preview()

            # call vision API to pull text from image
            with io.open(os.path.join(FOLDER_PATH, INPUT_FILE), 'rb') as image_file:
                content = image_file.read()
            image = vision.types.Image(content=content)
            response = vClient.text_detection(image=image)
            texts = response.text_annotations

            # if no text, find objects in image
            if not texts:
                objects = vClient.object_localization(
                    image=image).localized_object_annotations

                # store objects in a variable
                OUTPUT = ('Number of objects found: {}'.format(len(objects)))
                for object_ in objects:
                    OUTPUT = OUTPUT + \
                        ('\n{} (confidence: {})'.format(object_.name, object_.score))

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

                # store translation in a variable
                OUTPUT = (u'Translation: {}'.format(translation['translatedText']))

            # output response
            f = open(OUTPUT_FILE, "w")
            f.write(OUTPUT)
            print(OUTPUT)
            response1 = requests.get('https://api.telegram.org/bot{}/sendPhoto?chat_id={}&caption={}'.format(
                TELEGRAM_TOKEN, TELEGRAM_CHAT, OUTPUT), files=dict(photo=content))
            print(response1.status_code)
            # response2 = requests.get('https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'.format(TELEGRAM_TOKEN, TELEGRAM_CHAT, OUTPUT))
            f.close()

            # say the output
            tts = gTTS(text=OUTPUT, lang='en', slow=False)
            tts.save("output.mp3")
            os.system("mpg321 output.mp3")

except KeyboardInterrupt:
    GPIO.cleanup()