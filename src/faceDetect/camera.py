import picamera2
from picamera2 import Picamera2, Preview
import gpiozero
import time
from camsetup import settingup
from time import sleep
import os, sys


def testActivate(picam2):
    """activate to test camera"""
    try:
        picam2.start_preview(Preview.QTGL)
    except:
        picam2.start_preview(True)
    picam2.start()
    print("camera has activated")
    sleep(2)
    picam2.capture_file(f"images/test.jpg")
    picam2.stop_preview()

def activate(picam2):
    """capture with camera"""
    try:
        picam2.start_preview(Preview.QTGL)
    except:
        picam2.start_preview(True)
    picam2.start()
    print("camera has activated")
    sleep(2)
    picam2.capture_file(f"images/test.jpg")
    picam2.stop_preview() 


def addFace(name):
    """add a user's face to the database"""
    picam2 = Picamera2()
    picam2.start_preview(Preview.QTGL)
    picam2.start()
    print("align your head with the middle of the screen")
    sleep(3)
    picam2.capture_file("images/{name}.jpg")
    picam2.stop_preview()
    picam2.stop()
    print(f"{name} is now saved locally on file")

def detectFace(picam2):
    """detect a camera-input """
    activate

if __name__ == "__main__":
    inp = input("exit(any) or add(a)")
    if inp == "a":
        addFace("buster")