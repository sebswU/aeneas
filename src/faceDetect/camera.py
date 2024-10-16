import picamera2
from picamera2 import Picamera2, Preview
import gpiozero
import time
import os, sys

def activate():
    count = 0
    for i in range(count):
        os.remove(f"images/test{i}.jpg")
    picam2 = Picamera2()
    picam2.start_preview(Preview.QTGL)
    picam2.start()
    time.sleep(2)
    picam2.capture_file(f"images/test{count}.jpg")
