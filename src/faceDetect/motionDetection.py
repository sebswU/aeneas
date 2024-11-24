import gpiozero
from gpiozero import MotionSensor, LED
from time import sleep
from camera import activate, settingup
import picamera2
from picamera2 import Picamera2
"""
GPIO: 
8 -> red LED
25 -> white LED
17 -> MotionSensor
"""

pir = MotionSensor(17)
red = LED(8)
white = LED(25)

try:
    picam2 = Picamera2()
except:
    try:
        print("Camera not instantiated. Detecting camera ...")
        settingup()
    except Exception as error:
        print("an error has occurred: ")
        print(error)

print("waiting for no motion")
pir.wait_for_no_motion()

while True:
    white.off()
    red.on()
    print("waiting for motion")
    pir.wait_for_motion()
    print("motion detected")

    testActivate()
    red.off()
    white.on()
    sleep(2)
    
    
if __name__=="__main__":
    pass