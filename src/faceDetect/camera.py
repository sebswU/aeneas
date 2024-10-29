import picamera2
from picamera2 import Picamera2, Preview
import gpiozero
import time
from camsetup import settingup
from time import sleep
import os, sys

def activate():
    count = 0
    for i in range(count):
        os.remove(f"images/test{i}.jpg")
    try:
        picam2 = Picamera2()
    except:
        try:
            print("Camera not instantiated. Detecting camera ...")
            settingup()
        except Exception as error:
            print("an error has occurred: ")
            print(error)
    picam2.start_preview(Preview.QTGL)
    picam2.start()
    sleep(2)
    picam2.capture_file(f"images/test{count}.jpg")
    picam2.stop_preview()

